import datetime
import json
import os
import subprocess
from typing import NamedTuple

from googletrans import Translator

from cms_hunter.exceptions import NormalizeTextException
from cms_hunter.exceptions import CheckWpSiteException
from cms_hunter.exceptions import WhatWebScanException
from config.logger import logger
from config.settings import MEDIA_ROOT
from config.settings import WPSCAN_API_TOKEN

translator = Translator()

LOG_FILE = "log.json"
cms_list = ["WordPress", "Joomla", "Drupal"]


class WhatWebResult(NamedTuple):
    """WhatWeb result info"""
    ip: str
    cms: str
    server: str
    country: str


class ProxyInfo(NamedTuple):
    proxy: str
    proxy_user: str


def run_what_web(host: str, proxy: str = "", intensity: str = "1") -> WhatWebResult:
    """Run whatweb in the OS

    Args:
        host(str): Scanned host.
        proxy(str): Proxy server.
        intensity(str): Scan intensity.

    Returns:
        WhatWebResult: Info about host.
    """

    try:
        proxy, proxy_user = proxy

    except ValueError:
        proxy = ""
        proxy_user = ""

    if proxy and proxy_user:
        print(f"PROXY_USER: {proxy_user}")
        try:
            subprocess.run(
                [
                    "whatweb",
                    f"-a {intensity}",
                    f"--log-json={LOG_FILE}",
                    f"--proxy={proxy}",
                    f"--proxy-user={proxy_user}",
                    host,
                ]
            )

        except Exception:
            logger.error("Error during run whatweb with proxy and proxy user!")
            raise WhatWebScanException("Error during run whatweb with proxy and proxy user!")

    elif proxy:
        try:
            subprocess.run(
                [
                    "whatweb",
                    f"-a {intensity}",
                    f"--log-json={LOG_FILE}",
                    f"--proxy={proxy} ",
                    host,
                ]
            )

        except Exception:
            logger.error("Error during run whatweb with proxy!")
            raise WhatWebScanException("Error during run whatweb with proxy!")

    else:
        try:
            subprocess.run(
                ["whatweb", f"-a {intensity}", f"--log-json={LOG_FILE}", host]
            )

        except Exception:
            logger.error("Error during run pure whatweb")
            raise WhatWebScanException("Error during run pure whatweb")

    ip = ""
    server = ""
    cms = ""
    country = ""

    try:
        with open(f"{LOG_FILE}", "r") as f:
            json_data = json.load(f)

    except Exception:
        logger.error("Can not read whatweb result file!")
        raise WhatWebScanException("Error during reading whatweb result file.")

    finally:
        os.remove(f"{LOG_FILE}")

    for i in range(len(json_data)):
        try:
            ip = json_data[i]["plugins"]["IP"]["string"][0]
        except KeyError:
            continue

        try:
            server = json_data[i]["plugins"]["HTTPServer"]["string"][0]
        except KeyError:
            continue

        try:
            country = json_data[i]["plugins"]["Country"]["string"][0]
        except KeyError:
            continue

        try:
            cms = json_data[i]["plugins"]["MetaGenerator"]["string"][0]
        except KeyError:
            for _cms in cms_list:
                if _cms in json_data[i]["plugins"]:
                    cms = _cms
            continue

    return WhatWebResult(
        ip=ip,
        cms=cms,
        server=server,
        country=country
    )


def create_proxy_for_whatweb(data: dict) -> tuple:
    """Creates proxy for whatweb.

    Args:
        data(dict): IP and port of proxy server.

    Returns:
        Ip/port and user credentials.
    """

    ip = data["ip"]
    port = data["port"]

    if data["username"]:
        username = data["username"]
        password = data["password"]
        proxy_user = f"{username}:{password}"

    else:
        proxy_user = ""
        logger.info("Proxy without socks")

    proxy = f"{ip}:{port}"

    return ProxyInfo(
        proxy=proxy,
        proxy_user=proxy_user
    )


def check_wp_site(url: str) -> str:
    """Check site based on WP for vulnerabilities.

    Args:
        url: hostname

    Returns:
        Path to report file.
    """

    date, time = str(datetime.datetime.now()).split()

    path_to_file = f"{url}_{date}_{time}_report.txt"
    path = os.path.join(MEDIA_ROOT, path_to_file)

    url = "https://www." + url

    try:
        subprocess.run(
            ["wpscan", "--api-token", WPSCAN_API_TOKEN, "--url", url, "-o", path],
            encoding="utf-8",
        )

    except Exception:
        logger.error("Error during executing wpscan!")
        raise CheckWpSiteException("Error during executing wpscan")

    try:
        normalize_text(path)

    except NormalizeTextException:
        logger.error("Error during normalizing wpscan results")
        raise CheckWpSiteException("Error with normalizing text")

    return path_to_file


def normalize_text(file_name: str) -> None:
    """Remove not ascii symbols.

    Args:
        file_name: Report file name.

    Returns:
        None
    """
    try:
        with open(file_name, "r") as fd:
            info = fd.read()

    except Exception:
        logger.error("Error during normalizing text!")
        raise NormalizeTextException

    info = info.replace("[32m[+][0m", "")
    info = info.replace("[34m[i][0m", "")
    info = info.replace("[31m[i][0m", "")
    info = info.replace("[31m[!][0m", "")
    info = info.replace("[33m[!][0m", "")

    try:
        with open(file_name, "w") as fd:
            fd.write(info)

    except Exception:
        logger.error("Error during normalizing text!")
        raise NormalizeTextException


def check_site_for_vulnerabilities(url: str, cms: str) -> str:
    """Check site for vulnerabilities for WP(now) and Drupal and Joomla soon.

    Args:
        url: hostname.
        cms: Website CMS.

    Returns:
        path_to_file: Path to report file.
    """
    path_to_file = ""

    if "wordpress" in cms.lower():
        path_to_file = check_wp_site(url)

    return str(path_to_file)
