import click
from .common import RequestFailed
from . import start


@click.group()
def cli():
    """Interact with KeePass using the KeePassHTTP plugin"""
    pass

@cli.command()
@click.argument('appname')
@click.argument('url')
@click.option('--list', is_flag=True, help='List all matches instead of only the first.')
@click.option('--output', multiple=True, type=click.Choice(['Name', 'Login', 'Password']), help='Specify which data should be printed.')
@click.option('--plaintext', is_flag=True, help='Print out the password - BE CAREFUL')
def get(appname, url, output, plaintext, list):
    """Search for an entry."""
    warning = False
    try:
        session = start(appname)
    except RequestFailed:
        exit('Creating new key aborted by user!')
    result = session.get_logins(url)
    if not result:
        exit("No match for '{}'".format(url))
    if list:
        print('{} result(s) found'.format(len(result)))
        for r in result:
            print('Name: {}'.format(r['Name']))
            print('User: {}'.format(r['Login']))
            if plaintext:
                print('Password: {}'.format(r['Password'].value))
            else:
                print('Password: {}'.format(r['Password']))
                warning = True
    else:
        if output:
            data_out = []
            for item in output:
                if item == 'Password':
                    if plaintext:
                        data_out.append(result[0][item].value)
                    else:
                        data_out.append(str(result[0][item]))
                        warning = True
                else:
                    data_out.append(result[0][item])
            print(' '.join(data_out))
        else:
            if plaintext:
                print('{} {}'.format(result[0]['Login'], result[0]['Password'].value))
            else:
                print('{} {}'.format(result[0]['Login'], result[0]['Password']))
                warning = True
    if warning:
        print("Out of security reasons, you need to append "
              "'-p/--plaintext' to really print the password")
