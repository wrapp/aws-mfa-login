"""
CLI tool to generate environment variables from AWS STS get-session-token when MFA is needed for AWS CLI actions.
"""
import json
import subprocess
import configparser
import argparse
from os.path import expanduser
import os
import sys


def parse_args() -> argparse.Namespace:
    """Parse arguments and generate help. Tries to guess if this is a fish shell."""
    parser = argparse.ArgumentParser()
    parser.add_argument('--token', type=str, default=None, help='MFA token to use for login')

    serial_group = parser.add_mutually_exclusive_group()
    serial_group.add_argument('--profile', type=str, default='default',
                              help='AWS Profile to read MFA Serial from')
    serial_group.add_argument('--serial', type=int, default=None,
                              help='MFA device serial (e.g. arn:aws:iam::00000000000:mfa/myiamuser)')

    shell_group = parser.add_mutually_exclusive_group()
    shell_group.add_argument('--fish', action='store_true',
                             help='Override shell guessing, set to fish (use "set -e")')
    shell_group.add_argument('--bash', action='store_true',
                             help='Override shell guessing, set to bash (use "unset")')

    args = parser.parse_args()

    # Guess shell for unset
    if not args.bash and (any([k for k in os.environ if k.startswith('__fish')])):
        args.fish = True

    return args


def get_credentials(args: argparse.Namespace) -> dict:
    """Get the credentials from AWS STS.
    If no serial number is given in the args, will try to read from `.aws/config` profile.
    If no token is given, asks for it using `input()`"""
    if args.serial is None:
        config = configparser.ConfigParser()
        config.read(expanduser("~/.aws/config"))
        try:
            profile = config["profile " + args.profile]
        except KeyError:
            print("# Profile '%s' not found!" % args.profile, file=sys.stderr)
            sys.exit(-1)
        try:
            mfa_serial = profile["mfa_serial"]
        except KeyError:
            print("# Profile '%s' does not have mfa_serial set!" % args.profile, file=sys.stderr)
            sys.exit(-1)
    else:
        mfa_serial = str(args.serial)

    mfa_token = input("MFA token: ") if args.token is None else str(args.token)

    # AWS Session token already set but expired will make it break
    clean_env = os.environ.copy()
    if 'AWS_SESSION_TOKEN' in clean_env:
        print("# Deleting session token", file=sys.stderr)
        del clean_env['AWS_SESSION_TOKEN']

    # Get the session token
    proc = subprocess.Popen([
        "aws",  "--profile", args.profile, "sts", "get-session-token",
        "--serial-number", mfa_serial,
        "--token-code", mfa_token, '--output', 'json'
    ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=clean_env)
    data, _ = proc.communicate()
    if proc.returncode != 0:
        print("# get-session-token failed: ", data.decode('utf-8'), file=sys.stderr)
        sys.exit(-1)

    credentials = json.loads(data.decode('utf-8'))["Credentials"]
    return credentials


def print_credentials(credentials: dict, fish=False):
    """Print export commands for the credentials dict given.
    If AWS_PROFILE is set, also print unset command for it."""
    export = 'export %s=%s;' if not fish else 'set -x %s %s;'
    print(export % ("AWS_ACCESS_KEY_ID", credentials["AccessKeyId"]))
    print(export % ("AWS_SECRET_ACCESS_KEY", credentials["SecretAccessKey"]))
    print(export % ("AWS_SESSION_TOKEN", credentials["SessionToken"]))

    # Profile messes with the setup
    if 'AWS_PROFILE' in os.environ:
        print('unset AWS_PROFILE;' if not fish else 'set -e AWS_PROFILE;')


def main():
    """Parse arguments, get credentials, print credentials."""
    args = parse_args()
    credentials = get_credentials(args)
    print_credentials(credentials, fish=args.fish)


if __name__ == '__main__':
    main()
