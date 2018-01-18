"""

"""
import json
import subprocess
import configparser
import argparse
from os.path import expanduser
import os
import sys


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--token', type=int, default=None, help='MFA token to use for login')

    serial_group = parser.add_mutually_exclusive_group()
    serial_group.add_argument('--profile', type=str, default='default', help='AWS Profile to read MFA Serial from')
    serial_group.add_argument('--serial', type=int, default=None, help='MFA device serial (e.g. arn:aws:iam::00000000000:mfa/myiamuser)')

    shell_group = parser.add_mutually_exclusive_group()
    shell_group.add_argument('--fish', action='store_true')
    shell_group.add_argument('--bash', action='store_true')

    args = parser.parse_args()

    if args.serial is None:
        config = configparser.ConfigParser()
        config.read(expanduser("~/.aws/config"))
        try:
            profile = config["profile " + args.profile]
        except KeyError:
            print("# Profile '%s' not found!" % args.profile)
            sys.exit(-1)
        try:
            mfa_serial = profile["mfa_serial"]
        except KeyError:
            print("# Profile '%s' does not have mfa_serial set!" % args.profile)
            sys.exit(-1)
    else:
        mfa_serial = str(args.serial)

    mfa_token = input("MFA token: ") if args.token is None else str(args.token)

    # AWS Session token already set but expired will make it break
    clean_env = os.environ.copy()
    if 'AWS_SESSION_TOKEN' in clean_env:
        del clean_env['AWS_SESSION_TOKEN']

    proc = subprocess.Popen([
        "aws",  "sts", "get-session-token",
        "--serial-number", mfa_serial,
        "--token-code", mfa_token, '--output', 'json'
     ],stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=clean_env)
    data, _ = proc.communicate()
    if proc.returncode != 0:
        print("# get-session-token failed: ", data.decode('utf-8'))
        sys.exit(-1)

    credentials = json.loads(data.decode('utf-8'))["Credentials"]
    if args.bash or (not any([k for k in os.environ if k.startswith('__fish')]) and not args.fish):
        export = 'export %s=%s'
        unset = 'unset %s'
    else:
        export = 'set -x %s %s'
        unset = 'set -e %s'

    print(export % ("AWS_ACCESS_KEY_ID", credentials["AccessKeyId"]))
    print(export % ("AWS_SECRET_ACCESS_KEY", credentials["SecretAccessKey"]))
    print(export % ("AWS_SESSION_TOKEN", credentials["SessionToken"]))

    if 'AWS_PROFILE' in os.environ:
        print(unset % 'AWS_PROFILE')

if __name__ == '__main__':
    main()
