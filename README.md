>[!IMPORTANT]
I know it's meant to be a simple project but it's still a work in progress. This is just a fun little, yet useful project for me personally.
PR's welcome!

# UniFi Firewall DDNS Sync

A command-line tool + docker container to automatically synchronize dynamic DNS (DDNS) records with UniFi Firewall configurations.
It ensures that firewall rules remain up-to-date with the latest IP addresses of dynamic hosts by querying DNS and updating the UniFi Controller via its API.

This tool utilises the undocumented API that the UDM Pro/SE uses. I am unable to test on other devices but assume it maybe the same.

---

## Main Features:  

- **Dynamic White/Black-listing📃**  
  You can dynamically whitelist and/or blacklist IP addresses into your UniFi Network Controller's firewall rules! 😱🙀🤯 The main purpose of this thing...
- **Bulk Host Update 💻**  
  Supports reading a list of hosts from a JSON file and syncing them all in one go.
  You can specify if it's an ALLOW or DENY rule.
  Though For simplicity I won't really be focussing on doing too much at once.
- **CLI Support via Python 🐍**  
  You can just run in the CLI, extend/reuse/configure it the way you want, I don't care - go ham! But be careful...
- **Containerized Docker Approach 🐳**  
  The idea of the container is to segregate access to the UniFi controller + run as a background job.
  A comprehensive set of features and examples are available.
  

#### Other Notable Features:

- **CLI Argument Handling + Validation ✅⛔**  
  Ensures correctness of user input (gateway, credentials, file paths, service name, etc.).
- **Dynamic DNS Resolution 🛜**  
  Resolves DNS hosts to IPv4 addresses using Python’s built-in `socket` or custom logic.
- **Secure UniFi Authentication 🔐**  
  Stores and manages UniFi API tokens securely using OS keyring (Windows Credential Manager, macOS Keychain, etc.).
- **SSL Verification Control 🛂**  
  Allows users to disable SSL certificate validation for self-signed setups.

---

## Current Compatibility

- **UniFi Network Controllers 9.0.x+**  
- **Docker Multi-Architechture - linux/amd64, linux/arm64, linux/arm/v7**  

> [!NOTE]
It should work fine on older versions of UniFi Network Controllers, but I'm not certain.


## Prerequisites

1. **UniFi Controller / Gateway**  
   Ensure you have network connectivity to your UniFi device and know the login credentials.
   It is recommended you create a specific local user for this purpose.

#### For Docker 🐳

1. **Docker engine installed with compose**  
2. Either build it yourself via the `Dockerfile` or pull my image from [DockerHub](https://hub.docker.com/repository/docker/uguler/unifi-firewall-ddns-sync).
3. Take one of the `docker-compose.yml` and `.env` templates and substitute it for your environment!

> [!TIP]
I do recommend the MacVLAN one as you can assign as specific IP address and/or utilise your firewall to create specific rules. This is a better more controlled approach.

> [!CAUTION]
I generally recommend against just taking any image from anyone that gains access into your firewall, but hey people use homeassistant too. It's there for mainly my own convenience and only if you wish to use it! TBC for docker image.

#### .env File

```sh
# Healthcheck Overrides
HEALTHCHECK_INTERVAL=10s
HEALTHCHECK_TIMEOUT=5s
HEALTHCHECK_RETRIES=6

# Volume Mounts
CONFIG_VOLUME="./config"

#### Unifi Firewall DDNS Sync ####
# Minute, Hourly and Day Intervals.
# * = NULL. Use integers
CRON_MINS=*
CRON_HOURS=1
CRON_DAYS=*

# This WILL execute instantly upon starting container
# Recommended to leave as fasle for first run until you get a .json file correct.
RUN_ONCE=false

# If your Gateway runs via HTTPS
UNIFI_GATEWAY_HTTPS=true

# DNS or IP address of your gateway
UNIFI_GATEWAY="gateway.example.com"

# Username and Password. Recommended to create API Specific local-user credentials
UNIFI_USERNAME="USERNAME"
UNIFI_PASSWORD="PASSWORD"

# This is usually left 'default'
UNIFI_SITE="default"

# This can be revealed various way susch as querying the API or via the browser dev tools
UNIFI_SITE_ID="a1b2c3d4e5f6a7b8c9d0e1f2"

# If its a self signed cert on HTTPS, ignore the warning otherwise it will fail
UNIFI_NO_VERIFY_SSL=true

# Name of your rule file
UNIFI_RULE_FILENAME="unifi_ddns_sync.json"
```

#### Rule JSON File Template

```json
[
    // You can have various in array that are assigned to different kinds of firewall rules
    // This will NOT create the rule or group for you. It's just a PUT/update
    {
        "title": "IP ALLOW List", // This will update the name of the Profile/Network Object
        "firewallgroup": "a1b2c3d4e5f6g7h8j9a1b2c3", // This can be found on the URL in the address bar

        // List of hostnames to update
        "hosts": [
            "example.com",
            "vpn.example.com",
            "family-1.example.com",
            "family-2.example.com",
            "family-3.example.com",
            "friend-1.example.com",
            "friend-2.example.com",
            "friend-3.example.com"
        ]
    }
]
```

---

#### For a RAW Doggin' CLI Python approach 🐍

1. **Python 3.8+**  
   Some features (e.g., certain arg behaviors) may depend on newer Python versions.
2. **[Pipenv or venv (recommended)]**  
   For clean dependency management. Create it at the root folder.

---

## Caveats

**Project Structure**  
> [!NOTE]
Folders begining with the `py_` prefix are git submodules I've created. It was a decision I've made as a trade-off instead of utilizing PyPi.
It has tradeoffs, annoyingly the way it can be imported into other projects, the way the import looks 🤮, and having to commit each one... 🥱
But at the same time I feel like it's simpler and cleaner for me personally, don't hate me!
