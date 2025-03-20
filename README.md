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

> [!NOTE]
It should work fine on older versions but I'm not certain.


## Prerequisites
1. **UniFi Controller / Gateway**  
   Ensure you have network connectivity to your UniFi device and know the login credentials.
   It is recommended you create a specific local user for this purpose.

#### For Docker 🐳
1. **Docker engine installed with compose**  
2. Either build it yourself via the `Dockerfile` or pull my image.
3. Take one of the `docker-compose.yml` and `.env` templates and substitute it for your environment!

> [!CAUTION]
I generally recommend against just taking any image from anyone that gains access into your firewall, but hey people use homeassistant too. It's there for mainly my own convenience and only if you wish to use it! TBC for docker image.

#### For a RAW Doggin' CLI Python approach 🐍
1. **Python 3.8+**  
   Some features (e.g., certain arg behaviors) may depend on newer Python versions.
2. **[Pipenv or venv (recommended)]**  
   For clean dependency management. Create it at the root folder.

---

## Caveats
- **Project Structure**  
> [!NOTE]
Folders begining with the `py_` prefix are git submodules I've created. It was a decision I've made as a trade-off instead of utilizing PyPi.
It has tradeoffs, annoyingly the way it can be imported into other projects, the way the import looks 🤮, and having to commit each one... 🥱
But at the same time I feel like it's simpler and cleaner for me personally, don't hate me! 