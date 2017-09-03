"""Python3 module to interact with KeePass via the KeePassHTTP plugin."""
from .session import Session


def start(appname):
    """Start a new communication session."""
    return Session.start(appname)
