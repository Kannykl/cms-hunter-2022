class ServiceUnavailable(Exception):
    pass


class ProxyDoesntWork(Exception):
    pass


class BadInternetConnection(Exception):
    pass


class AuthenticationRequired(Exception):
    pass


class PageDoesntExists(Exception):
    pass


class UnknownException(Exception):
    pass


class NormalizeTextException(Exception):
    """Error throws if error occurs during reading a file or writing in a wpscan results file."""
    pass


class CheckWpSiteException(Exception):
    """Error throws if error occurs during check wordpress site."""
    pass


class WhatWebScanException(Exception):
    """Error throws if error occurs during check wordpress site."""
    pass
