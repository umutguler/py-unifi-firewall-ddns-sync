"""Main driver for the UniFi Firewall DDNS Sync application."""
# from py_dns.src.ddns import DDNS
from src.helpers.arguments import ArgumentHandler
from src.helpers.unifi_file_handler import FileHandler
from src.py_unifi.api import UnifiApi

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

    json_file = FileHandler(args.file)

    unifi_api = UnifiApi(args.gateway, args.username,
                         args.password, args.site, args.verify_ssl)

    for rule in json_file.read_json():
        unifi_api.update_firewall_group(rule)

    unifi_api.logout()
