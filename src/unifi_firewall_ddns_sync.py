"""Main driver for the UniFi Firewall DDNS Sync application."""
# from py_dns.src.ddns import DDNS
import logging
import warnings

from helpers.arguments import ArgumentHandler
from helpers.unifi_file_handler import FileHandler
from py_unifi.api import UnifiApi
from urllib3.exceptions import InsecureRequestWarning

warnings.simplefilter("ignore", InsecureRequestWarning)


DESCRIPTION = """
UniFi Firewall DDNS Sync

A command-line tool to automatically synchronize dynamic DNS (specifically DDNS) records
with UniFi Firewall configurations. It ensures that firewall rules remain
up-to-date with the latest IP addresses of dynamic hosts by querying DNS
and updating the UniFi Controller via its API.

Key features:
  - Ability to whitelist and/or blacklist IP addresses dynamically.
  - Gets and validates input arguments including; gateway, credentials, and JSON configuration files.
  - Secure token management using the OS keyring for UniFi API authentication.
    This is to ensure it's not mishandled.
  - Can handle self-signed gateway certificates through a configurable SSL verification flag.
  - Supports bulk host updates through a JSON file.
  - Simple, robust, and easily configurable via CLI arguments.
  - Dockerfile with the addition of docker compose and .env templates for your environment.
  - Use docker to containerize and run in the background periodically and/or assign to specific VLANs.

Ideal for environments with dynamic IP addresses where firewall rules must
automatically reflect DNS changes. For more details, refer to the project's documentation.
"""

if __name__ == "__main__":
    handler = ArgumentHandler(DESCRIPTION)
    args = handler.parse()
    logging.basicConfig(level=logging.INFO)
    logging.info("Starting UniFi Firewall DDNS Sync")

    json_file = FileHandler(args.file)
    unifi_api = UnifiApi(args.gateway, args.username,
                         args.password, args.site, args.verify_ssl)

    logging.info("Updating firewall rules...")
    for rule in json_file.read_json():
        logging.info("Updating rule: %s", rule['title'])
        unifi_api.update_firewall_group(rule)

    logging.info("Firewall rules updated successfully")
    unifi_api.logout()
