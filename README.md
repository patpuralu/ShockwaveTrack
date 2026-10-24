# ShockwaveTR

ShockwaveTR is a **terminal-based OSINT tool** written in Python

<img width="647" height="331" alt="image" src="https://github.com/user-attachments/assets/c23829c4-42ba-4790-b43d-f03fcc49be06" />

---

## Modules

### 1. IP Tracker
Geolocates any public IP and extracts all available information:

- Country, city, region and postal code
- Coordinates + direct Google Maps link
- ISP, ASN and organization
- Timezone, real-time local time and UTC offset
- Calling code, capital, flag emoji and bordering countries

---

### 2. Show Your IP
Displays your public IP and full local network details:

- Public IP via `ipify.org`
- Local IP, subnet mask, CIDR and broadcast address
- Usable host range and total available hosts
- Default gateway
- `/24` subnets if the network is larger

---

### 3. Phone Number Tracker
Analyzes a phone number in international format:

- Location and region code
- Carrier
- Number timezone
- Formats: international, E.164, mobile dialing
- Real number validity (not just format check)
- Type: Mobile, Landline, VoIP, Toll-free, Premium rate

---

### 4. Username Tracker
Searches a username across **22 platforms in parallel**:

| Platform | Platform | Platform |
|---|---|---|
| GitHub | Instagram | TikTok |
| YouTube | Twitch | SoundCloud |
| Pinterest | Tumblr | Reddit |
| Twitter / X | LinkedIn | Behance |
| Medium | Flickr | Dribbble |
| DeviantArt | Steam | Spotify |
| Product Hunt | Quora | Telegram |
| Snapchat | | |

Supports searching **1 user or multiple at once** (comma-separated).
Saves history with the results of each search.

---

### 5. Domain Lookup
Gets full information about a domain:

- DNS resolution → IP
- Country, city and ISP of the server
- Registrar and creation date (via whoisxmlapi)
- DNS records via `nslookup`

---

## Extra features

- **Automatic history** → every search is saved to `results/history_<type>_<date>.json`
- **Color-blindness support** → 4 color modes: normal, protanopia, deuteranopia, tritanopia
- **Parallel execution** → username tracker uses `ThreadPoolExecutor` to scan all 22 platforms simultaneously
- **ASCII banner** of Shockwave in the main menu

---

## Installation

**Requirements:**
- Python 3.9+ (Python 3.8 may work with `pytz` installed)
- Git

### Ubuntu / Debian

Install Python, `pip`, and virtual-environment support using the system package manager:

```bash
sudo apt update
sudo apt install -y git python3 python3-pip python3-venv
```

Clone the repository and enter its directory:

```bash
git clone https://github.com/patpuralu/ShockwaveTrack.git
cd ShockwaveTrack
```

Create and activate a virtual environment. This is recommended on modern Ubuntu and Debian systems because it avoids the `externally-managed-environment` error:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the dependencies. If the repository contains `requirements.txt`, use:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

If there is no `requirements.txt`, install the main dependencies directly:

```bash
python -m pip install --upgrade pip
python -m pip install requests phonenumbers
```

Then run the tool:

```bash
python ShockwaveTR.py
```

**Optional** (for better network interface detection):

```bash
python -m pip install netifaces pytz
```

Run these `python -m pip` commands after activating `.venv`. Avoid using `sudo pip` or forcing installation into the system Python.

### Termux

Install Python and Git:

```bash
pkg update
pkg install -y git python
```

Clone the repository and enter its directory:

```bash
git clone https://github.com/patpuralu/ShockwaveTrack.git
cd ShockwaveTrack
```

Install dependencies from `requirements.txt` if it exists:

```bash
python -m pip install -r requirements.txt
```

Otherwise, install the main dependencies directly:

```bash
python -m pip install requests phonenumbers
```

---

## Usage

```bash
python ShockwaveTR.py
```

**Main menu:**

<img width="655" height="306" alt="image" src="https://github.com/user-attachments/assets/546e1396-4c6e-4d3f-8db9-c8381d76dd84" />

**Example — IP Tracker:**

<img width="646" height="545" alt="image" src="https://github.com/user-attachments/assets/0b107c17-e022-4274-9905-31142dcdf179" />

**Example — Username Tracker:**

<img width="612" height="255" alt="image" src="https://github.com/user-attachments/assets/5dfd8793-574c-4816-9651-a7ec134941fb" />

---

<details>
  <summary>Credits</summary>

  <p><strong>Original concept by:</strong> <a href="https://github.com/HunxByts">HUNX04</a></p>
  <p><strong>Fork, rewrite & extended version by:</strong> patpuralu</p>
  <p><strong>Maintainer:</strong> patpuralu</p>

</details>

