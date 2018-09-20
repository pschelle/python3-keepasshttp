[![Build Status](https://travis-ci.org/MarkusFreitag/python3-keepasshttp.svg?branch=master)](https://travis-ci.org/MarkusFreitag/python3-keepasshttp)
[![Coverage Status](https://coveralls.io/repos/github/MarkusFreitag/python3-keepasshttp/badge.svg?branch=master)](https://coveralls.io/github/MarkusFreitag/python3-keepasshttp?branch=master)


# python3-keepasshttp
Access passwords stored in keepass using the http plugin 

## Installation

`pip3 install git+https://github.com/pschelle/python3-keepasshttp.git`

## Usage

### Python module
```python
import keepasshttp

session = keepasshttp.start('my_app_name')
logins = session.get_logins('http://www.amazon.com')
print(logins)
```

Which will output something like:

```
[{u'Login': 'bezos@amzn.com',
  u'Name': 'Amazon',
  u'Password': Password(*****),
  u'Uuid': '0da19f691e4ab51c11433f809695c84e'}]
```

The password field is protected with a thin wrapper so that it
isn't accidently printed.  The actual value of the password can
be accessed like

```python
logins[0]['Password'].value
```

### CLI tool
The CLI tools provides the possibility to search for an entry.
```
$ kphttp-cli --help
Usage: kphttp-cli [OPTIONS] COMMAND [ARGS]...

  Interact with KeePass using the KeePassHTTP plugin

Options:
  --help  Show this message and exit.

Commands:
  get  Search for an entry.
```
```
$ kphttp-cli get --help
Usage: kphttp-cli get [OPTIONS] APPNAME URL

  Search for an entry.

Options:
  --list                          List all matches instead of only the first.
  --output [Name|Login|Password]  Specify which data should be printed.
  --plaintext                     Print out the password - BE CAREFUL
  --help                          Show this message and exit.
```


## Notes

This library is based based off of the keepasshttp author's
[Protocol Summary](https://github.com/pfn/keepasshttp#protocol)
and the
[Javascript Client Implementation](https://github.com/pfn/passifox/blob/master/chromeipass/background/keepass.js)

I kept a copy of the notebook I used while playing around with the
protocol
[Keepass Protocol](https://github.com/jobevers/python-keepasshttp/blob/master/Keepass%20Protocol.ipynb)
for reference.

## Installing http server for keepassx

Versions of keepassx have been written that port the functionality of
the keepasshttp plugin. Check out
https://github.com/keepassx/keepassx/pull/111 for the latest info.

## Related projects

https://github.com/ccryx/python-keephasshttpc
