# EasyRSAPy

A Python SDK for [Easy-RSA](https://github.com/OpenVPN/easy-rsa). Development is in progress.

[Easy-RSA Documentation](https://easy-rsa.readthedocs.io/en/latest/)

## Run tests

Requires `easyrsa` on the PATH.

Install Easy-RSA:

macOS:

```bash
brew install easy-rsa
```

Ubuntu:

```bash
sudo apt-get update
sudo apt-get install -y easy-rsa
export PATH=$PATH:/usr/share/easy-rsa
```

Run tests:

```bash
make install-dev
make test
```
