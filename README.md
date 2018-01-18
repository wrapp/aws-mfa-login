# aws-mfa-auth
Command-line tool for MFA authentication against the AWS CLI. Only generates environment variables, no state or configuration (MFA serial can optionally be added to AWS config).

Will by default ask for MFA token, and grab MFA device serial from the default profile in `~/.aws/config`.

Profile, serial and token can also be passed on the command line.

You must have a valid authentication for AWS CLI already set up for the STS call to succeed.

Examples:

```
> aws-mfa-login --help
usage: aws-mfa-login [-h] [--token TOKEN] [--profile PROFILE | --serial SERIAL]
                    [--fish | --bash]

optional arguments:
  -h, --help         show this help message and exit
  --token TOKEN      MFA token to use for login
  --profile PROFILE  AWS Profile to read MFA Serial from
  --serial SERIAL    MFA device serial (e.g.
                     arn:aws:iam::00000000000:mfa/myiamuser)
  --fish             Override shell guessing, set to fish (use "set -e")
  --bash             Override shell guessing, set to bash (use "unset")

> aws-mfa-login
MFA token: 123456
export AWS_ACCESS_KEY_ID=ASIAJ5YFB3RUUOXGYOZQ
export AWS_SECRET_ACCESS_KEY=abWbgMq5432lLIn6x34tj+Wlpykq1WR/KvbG2SXg
export AWS_SESSION_TOKEN=FQodyXlDvLv//////////wEaDCDCm3ZyUN0wDhSDKd3klfssZo4zNgTqnmUiVH0Hp8EUwtdKwvbiAa7JsyXVfzP2vaM0MTZmur/SDFDSf33/77WSdNtpUnaMyEnNP//XA7OVzmzlMLAXKYAbzrq3tBVuXxspEccz+qrxMZkfXD+DfLfkgbKF384kSDksKDF+85kZZTTr6t4t7v1tZ9DNV3xEehNJk8BS5yrD6vKusGRir+ZVm3SDFddfdsDFFD
```
