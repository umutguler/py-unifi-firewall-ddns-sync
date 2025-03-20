"""
Handles all CLI arguments for program entrypoint.
"""
import argparse
from argparse import RawTextHelpFormatter

from .validations import ArgumentValidations


class ArgumentHandler:
    """Class to handle and validate command-line arguments."""

    def __init__(self, description):
        self.parser = argparse.ArgumentParser(
            description=description,
            formatter_class=RawTextHelpFormatter
        )
        self._build_arguments()

    def _build_arguments(self):
        self.parser.add_argument("-g", "--gateway", type=str, required=True,
                                 help="IP or hostname of UniFi Network Gateway " +
                                 "(e.g. example.com or 192.168.1.1)")

        self.parser.add_argument("-u", "--username", type=str, required=True,
                                 help="Username to login to the UniFi Gateway")

        self.parser.add_argument("-p", "--password", type=str, required=True,
                                 help="Password to login to the UniFi Gateway")

        self.parser.add_argument("--site", type=str, required=False, default="default",
                                 help="Site for the UniFi Gateway")

        self.parser.add_argument("--siteid", type=str, required=True,
                                 help="Site ID for the UniFi Gateway (e.g. default)")

        self.parser.add_argument("-s", "--servicename", type=str, required=False,
                                 default="UnifiApiClientToken",
                                 help=("[Optional] Service name for keyring storage of tokens. " +
                                       "Must contain only letters, hyphens, and underscores."))

        self.parser.add_argument("-f", "--file", type=str, required=False,
                                 default="unifi_ddns_sync.json",
                                 help=("[Optional] JSON file to handle multiple hosts (bulk). " +
                                       "File must: exist, has .json extension, is valid JSON."))

        self.parser.add_argument("--no-verify-ssl", dest="verify_ssl", action="store_false",
                                 help="Disable SSL certificate verification. " +
                                 "By default, SSL verification is enabled.")

        self.parser.set_defaults(verify_ssl=True)

    def _validate_arguments(self, args):
        ArgumentValidations.validate(args)
        return args

    def parse(self):
        """Parses and validates the command-line arguments before proceeding.
        Returns arguments if valid. Python argparse handles the rest.
        """
        args = self.parser.parse_args()
        return self._validate_arguments(args)
