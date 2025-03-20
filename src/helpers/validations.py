"""
Validation logic for all CLI arguments.
"""
import os
import json
import ipaddress
import re
import requests


class ArgumentValidations:
    """Validates all CLI arguments that is to be used in the application."""

    @staticmethod
    def validate(args):
        """
        Validate command-line arguments.

        Validations:
          - Gateway: Must be non-empty and either a valid IPv4 address or a hostname 
            that is contactable via an HTTP GET request.
          - Username: Must not be empty.
          - Password: Must not be empty.
          - Service name: Must not be empty.
            May only contain letters, hyphens, and underscores.
          - File: If provided, the file must exist, be a file,
            have a .json extension, and contain valid JSON.
          - Verify SSL: Must be a boolean value.

        Raises:
          ValueError: if any validation fails.
        """
        ArgumentValidations._validate_gateway(args.gateway, args.verify_ssl)
        ArgumentValidations._validate_username(args.username)
        ArgumentValidations._validate_password(args.password)
        ArgumentValidations._validate_service_name(args.servicename)
        ArgumentValidations._validate_site(args.site)
        ArgumentValidations._validate_siteid(args.siteid)
        ArgumentValidations._validate_file(args.file)
        ArgumentValidations._validate_verify_ssl(args.verify_ssl)
        return args

    @staticmethod
    def _validate_non_empty(value: str, field_name: str):
        if not value or not value.strip():
            raise ValueError(f"{field_name} cannot be empty.")
        return True

    @staticmethod
    def _validate_gateway(gateway: str, verify_ssl: bool):
        """
        Validate that gateway is either a valid IPv4 address or a hostname,
        and that it is contactable via an HTTP GET request.

        The verify_ssl parameter controls whether SSL certificates are verified.
        """
        ArgumentValidations._validate_non_empty(gateway, "Gateway")

        # Try IPv4 validation (even if it is valid, we'll still check connectivity).
        try:
            ipaddress.IPv4Address(gateway)
        except ipaddress.AddressValueError:
            # Not a valid IPv4 literal; treat as hostname.
            pass

        try:
            url = gateway if gateway.startswith(
                "http") else f"http://{gateway}/"
            # Pass the verify_ssl flag into the request
            response = requests.get(url, timeout=3, verify=verify_ssl)
            if not response.ok:
                raise ValueError(
                    f"Gateway '{gateway}' is not contactable.") from None
        except Exception as exc:
            raise ValueError(
                f"Gateway '{gateway}' is not contactable.") from exc

        return True

    @staticmethod
    def _validate_username(username: str):
        return ArgumentValidations._validate_non_empty(username, "Username")

    @staticmethod
    def _validate_password(password: str):
        return ArgumentValidations._validate_non_empty(password, "Password")

    @staticmethod
    def _validate_service_name(service_name: str):
        ArgumentValidations._validate_non_empty(service_name, "Service name")
        if not re.fullmatch(r"[A-Za-z_-]+", service_name):
            raise ValueError(
                "Service name must contain only letters, hyphens, and underscores.")
        return True

    @staticmethod
    def _validate_site(site: str):
        return ArgumentValidations._validate_non_empty(site, "Site")

    @staticmethod
    def _validate_siteid(siteid: str):
        return ArgumentValidations._validate_non_empty(siteid, "Site ID")

    @staticmethod
    def _validate_file(filepath: str):
        # pwd
        print(os.getcwd())
        if filepath:
            if not os.path.exists(filepath):
                raise ValueError(f"File '{filepath}' does not exist.")
            if not os.path.isfile(filepath):
                raise ValueError(f"Path '{filepath}' is not a file.")
            _, extension = os.path.splitext(filepath)
            if extension.lower() != ".json":
                raise ValueError(
                    f"File '{filepath}' does not have a .json extension.")
            try:
                with open(filepath, "r", encoding="utf8") as f:
                    json.load(f)
            except Exception as e:
                raise ValueError(
                    f"File '{filepath}' is not valid JSON: {e}") from e
        return True

    @staticmethod
    def _validate_verify_ssl(verify_ssl):
        if not isinstance(verify_ssl, bool):
            raise ValueError("Verify SSL must be a boolean value.")
        return True
