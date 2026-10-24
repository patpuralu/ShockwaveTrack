#!/usr/bin/env python3
# << CODE BY patpuralu
# Original base by HUNX04
# Full rewrite, improvements & new modules by patpuralu

import json
import requests
import time
import os
import ipaddress
import phonenumbers
from phonenumbers import carrier, geocoder, timezone
from concurrent.futures import ThreadPoolExecutor, as_completed
from sys import stderr
from datetime import datetime
import socket
import struct
import subprocess
import re

Bl = '\033[30m'
Re = '\033[1;31m'
Gr = '\033[1;32m'
Ye = '\033[1;33m'
Blu = '\033[1;34m'
Mage = '\033[1;35m'
Cy = '\033[1;36m'
Wh = '\033[1;37m'

HEADERS = {"User-Agent": "Mozilla/5.0"}
TIMEOUT = 10


color_schemes = {
    "normal": {
        "black":   '\033[30m',
        "white":   '\033[1;37m',
        "green":   '\033[1;32m',
        "red":     '\033[1;31m',
        "yellow":  '\033[1;33m',
        "blue":    '\033[1;34m',
        "cyan":    '\033[1;36m',
        "magenta": '\033[1;35m',
    },
    "protanopia": {  # No red - uses yellow/cyan instead
        "black":   '\033[30m',
        "white":   '\033[1;37m',
        "green":   '\033[1;36m',
        "red":     '\033[1;33m',
        "yellow":  '\033[1;33m',
        "blue":    '\033[1;34m',
        "cyan":    '\033[1;36m',
        "magenta": '\033[1;37m',  # bright white for contrast
    },
    "deuteranopia": {  # No green - uses yellow/magenta instead
        "black":   '\033[30m',
        "white":   '\033[1;37m',
        "green":   '\033[1;33m',
        "red":     '\033[1;31m',
        "yellow":  '\033[1;37m',  # bright white for contrast
        "blue":    '\033[1;34m',
        "cyan":    '\033[1;35m',
        "magenta": '\033[1;35m',
    },
    "tritanopia": {  # No blue - uses magenta/yellow instead
        "black":   '\033[30m',
        "white":   '\033[1;37m',
        "green":   '\033[1;32m',
        "red":     '\033[1;31m',
        "yellow":  '\033[1;32m',  # green for contrast
        "blue":    '\033[1;35m',
        "cyan":    '\033[1;33m',  # yellow for contrast
        "magenta": '\033[1;35m',
    }
}

current_scheme = "normal"


def create_results_folder():
    """Create the results/ folder if it doesn't exist"""
    if not os.path.exists("results"):
        os.makedirs("results")

def save_search_history(search_type, query, result):
    """Save search entry to history"""
    create_results_folder()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    filename = f"results/history_{search_type}_{datetime.now().strftime('%Y-%m-%d')}.json"
    
    data = {
        "timestamp": timestamp,
        "query": query,
        "result": result
    }
    
    try:
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                history = json.load(f)
        else:
            history = []
        
        history.append(data)
        with open(filename, 'w') as f:
            json.dump(history, f, indent=2)
    except Exception as e:
        print(f"{Re}Error saving history: {e}{Wh}")

def get_search_history(search_type):
    """Get search history entries"""
    create_results_folder()
    history_files = []
    
    for file in os.listdir("results"):
        if file.startswith(f"history_{search_type}"):
            history_files.append(os.path.join("results", file))
    
    all_history = []
    for filepath in sorted(history_files, reverse=True):
        try:
            with open(filepath, 'r') as f:
                all_history.extend(json.load(f))
        except:
            pass
    
    return all_history

def is_option(func):
    def wrapper(*args, **kwargs):
        run_banner()
        return func(*args, **kwargs)
    return wrapper

def _get_current_time(tz_id):
    """Return the current local time for a given IANA timezone ID."""
    if not tz_id:
        return "N/A"
    try:
        from zoneinfo import ZoneInfo          # Python 3.9+
        from datetime import datetime as dt
        return dt.now(ZoneInfo(tz_id)).strftime("%Y-%m-%d %H:%M:%S %Z")
    except Exception:
        try:
            import pytz                        # fallback if pytz is installed
            from datetime import datetime as dt
            return dt.now(pytz.timezone(tz_id)).strftime("%Y-%m-%d %H:%M:%S %Z")
        except Exception:
            return "N/A"


@is_option
def IP_Track():
    ip = input(f"{Wh}\n Enter IP target : {Gr}").strip()

    # Validate IP format before making the request
    try:
        ipaddress.ip_address(ip)
    except ValueError:
        print(f"{Re}\n [!] Invalid IP. Please enter a valid IP address.")
        return

    print(f"\n {Wh}============= {Gr}SHOW INFORMATION IP ADDRESS {Wh}=============")

    try:
        req_api = requests.get(f"http://ipwho.is/{ip}", headers=HEADERS, timeout=TIMEOUT)
        req_api.raise_for_status()
        ip_data = req_api.json()
    except requests.RequestException as e:
        print(f"{Re}\n [!] Error connecting to the API: {e}")
        return

    # Check if the API returned success
    if not ip_data.get("success"):
        print(f"{Re}\n [!] Error: {ip_data.get('message', 'IP not found or invalid')}")
        return

    time.sleep(1)

    # Use float to preserve coordinate precision
    lat = float(ip_data['latitude'])
    lon = float(ip_data['longitude'])

    fields = [
        ("IP target",       ip),
        ("Type IP",         ip_data.get("type", "N/A")),
        ("Country",         ip_data.get("country", "N/A")),
        ("Country Code",    ip_data.get("country_code", "N/A")),
        ("City",            ip_data.get("city", "N/A")),
        ("Continent",       ip_data.get("continent", "N/A")),
        ("Continent Code",  ip_data.get("continent_code", "N/A")),
        ("Region",          ip_data.get("region", "N/A")),
        ("Region Code",     ip_data.get("region_code", "N/A")),
        ("Latitude",        ip_data.get("latitude", "N/A")),
        ("Longitude",       ip_data.get("longitude", "N/A")),
        ("Maps",            f"https://www.google.com/maps/@{lat},{lon},8z"),
        ("EU",              ip_data.get("is_eu", "N/A")),
        ("Postal",          ip_data.get("postal", "N/A")),
        ("Calling Code",    ip_data.get("calling_code", "N/A")),
        ("Capital",         ip_data.get("capital", "N/A")),
        ("Borders",         ip_data.get("borders", "N/A")),
        ("Country Flag",    ip_data.get("flag", {}).get("emoji", "N/A")),
        ("ASN",             ip_data.get("connection", {}).get("asn", "N/A")),
        ("ORG",             ip_data.get("connection", {}).get("org", "N/A")),
        ("ISP",             ip_data.get("connection", {}).get("isp", "N/A")),
        ("Domain",          ip_data.get("connection", {}).get("domain", "N/A")),
        ("Timezone ID",     ip_data.get("timezone", {}).get("id", "N/A")),
        ("ABBR",            ip_data.get("timezone", {}).get("abbr", "N/A")),
        ("DST",             ip_data.get("timezone", {}).get("is_dst", "N/A")),
        ("Offset",          ip_data.get("timezone", {}).get("offset", "N/A")),
        ("UTC",             ip_data.get("timezone", {}).get("utc", "N/A")),
        ("Current Time",    _get_current_time(ip_data.get("timezone", {}).get("id", ""))),
    ]

    for label, value in fields:
        print(f"{Wh} {label:<16} :{Gr} {value}")


def _windows_ipconfig_blocks():
    """Return (interface name, block text) pairs from Windows ipconfig output."""
    try:
        result = subprocess.run(
            ["ipconfig", "/all"], capture_output=True, text=True,
            errors="replace", timeout=8, check=False
        )
        output = result.stdout or ""
        if not output:
            return []
    except (OSError, subprocess.SubprocessError):
        return []

    blocks = []
    current_name = "Windows network adapter"
    current_lines = []
    for line in output.splitlines():
        stripped = line.strip()
        # English and Spanish Windows adapter headings.
        if stripped.endswith(":") and (
            "adapter" in stripped.lower() or "adaptador" in stripped.lower()
        ):
            if current_lines:
                blocks.append((current_name, "\n".join(current_lines)))
            current_name = stripped[:-1].strip()
            current_lines = []
        else:
            current_lines.append(line)
    if current_lines:
        blocks.append((current_name, "\n".join(current_lines)))
    return blocks


def get_local_ifaces():
    """Return (interface, local IPv4, netmask) tuples on Windows, Linux and macOS."""
    ifaces = []

    # Preferred method: netifaces works across common operating systems when installed.
    try:
        import netifaces
        for iface in netifaces.interfaces():
            addrs = netifaces.ifaddresses(iface)
            for addr in addrs.get(netifaces.AF_INET, []):
                ip = addr.get("addr", "")
                netmask = addr.get("netmask", "")
                if ip and not ip.startswith("127."):
                    ifaces.append((iface, ip, netmask or "255.255.255.0"))
        if ifaces:
            return ifaces
    except (ImportError, OSError, ValueError):
        pass

    # Windows fallback: parse ipconfig /all, including English and Spanish labels.
    if os.name == "nt":
        for iface, block in _windows_ipconfig_blocks():
            ip_match = re.search(
                r"(?:IPv4 Address|Direcci[oó]n IPv4)\s*[^:]*:\s*([0-9]{1,3}(?:\.[0-9]{1,3}){3})",
                block, re.IGNORECASE
            )
            mask_match = re.search(
                r"(?:Subnet Mask|M[aá]scara de subred)\s*:\s*([0-9]{1,3}(?:\.[0-9]{1,3}){3})",
                block, re.IGNORECASE
            )
            if ip_match and not ip_match.group(1).startswith("127."):
                ip = ip_match.group(1)
                mask = mask_match.group(1) if mask_match else "255.255.255.0"
                try:
                    ipaddress.IPv4Address(ip)
                    ipaddress.IPv4Network(f"0.0.0.0/{mask}")
                    if not any(existing[1] == ip for existing in ifaces):
                        ifaces.append((iface, ip, mask))
                except ipaddress.AddressValueError:
                    continue
                except (ipaddress.NetmaskValueError, ValueError):
                    continue
        if ifaces:
            return ifaces

    # Portable fallback: determine the address used for outbound IPv4 traffic.
    sock = None
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect(("192.0.2.1", 80))  # TEST-NET address; no packet is sent by UDP connect.
        ip = sock.getsockname()[0]
        if ip and not ip.startswith("127."):
            ifaces.append(("default", ip, "255.255.255.0"))
    except OSError:
        pass
    finally:
        if sock is not None:
            sock.close()
    return ifaces


def get_gateway():
    """Return the default IPv4 gateway on Windows, Linux or macOS."""
    if os.name == "nt":
        # PowerShell is more reliable than parsing localized ipconfig output.
        commands = [
            ["powershell", "-NoProfile", "-Command",
             "(Get-NetRoute -DestinationPrefix '0.0.0.0/0' -ErrorAction SilentlyContinue | "
             "Sort-Object RouteMetric | Select-Object -First 1 -ExpandProperty NextHop)"],
            ["pwsh", "-NoProfile", "-Command",
             "(Get-NetRoute -DestinationPrefix '0.0.0.0/0' -ErrorAction SilentlyContinue | "
             "Sort-Object RouteMetric | Select-Object -First 1 -ExpandProperty NextHop)"],
        ]
        for command in commands:
            try:
                result = subprocess.run(
                    command, capture_output=True, text=True, errors="replace",
                    timeout=8, check=False
                )
                candidate = (result.stdout or "").strip().splitlines()
                if candidate:
                    gateway = candidate[0].strip()
                    ipaddress.IPv4Address(gateway)
                    return gateway
            except (OSError, subprocess.SubprocessError, ipaddress.AddressValueError):
                continue

        # Fallback for Windows editions where PowerShell route lookup failed.
        try:
            result = subprocess.run(
                ["ipconfig"], capture_output=True, text=True, errors="replace",
                timeout=8, check=False
            )
            match = re.search(
                r"(?:Default Gateway|Puerta de enlace predeterminada)\s*:\s*([0-9]{1,3}(?:\.[0-9]{1,3}){3})",
                result.stdout or "", re.IGNORECASE
            )
            if match:
                return match.group(1)
        except (OSError, subprocess.SubprocessError):
            pass
        return "N/A"

    # Linux route table. macOS generally falls back to the route command below.
    try:
        with open("/proc/net/route", encoding="ascii") as route_file:
            for line in route_file.readlines()[1:]:
                parts = line.strip().split()
                if len(parts) > 2 and parts[1] == "00000000":
                    gateway_hex = parts[2]
                    if int(parts[3], 16) & 0x2:
                        return socket.inet_ntoa(struct.pack("<L", int(gateway_hex, 16)))
    except (OSError, ValueError, IndexError):
        pass

    # macOS / other Unix fallback.
    try:
        result = subprocess.run(
            ["route", "-n", "get", "default"], capture_output=True,
            text=True, errors="replace", timeout=5, check=False
        )
        match = re.search(r"\bgateway:\s*([0-9.]+)", result.stdout or "", re.IGNORECASE)
        if match:
            ipaddress.IPv4Address(match.group(1))
            return match.group(1)
    except (OSError, subprocess.SubprocessError, ipaddress.AddressValueError):
        pass
    return "N/A"


def calc_network_info(ip_str, netmask_str):
    """Calculates network, broadcast, usable range, total hosts and /24 subnets."""
    try:
        net = ipaddress.IPv4Network(f"{ip_str}/{netmask_str}", strict=False)
        hosts = list(net.hosts())
        subnets = [str(s) for s in net.subnets(new_prefix=24)] if net.prefixlen < 24 else []
        return {
            "network":     str(net.network_address),
            "broadcast":   str(net.broadcast_address),
            "prefix":      net.prefixlen,
            "netmask":     str(net.netmask),
            "first_host":  str(hosts[0])  if hosts else "N/A",
            "last_host":   str(hosts[-1]) if hosts else "N/A",
            "total_hosts": net.num_addresses - 2 if net.num_addresses > 2 else 0,
            "subnets":     subnets,
        }
    except Exception:
        return None


@is_option
def showIP():
    # ── Public IP ──
    try:
        response = requests.get('https://api.ipify.org/', timeout=TIMEOUT)
        response.raise_for_status()
        public_ip = response.text.strip()
    except requests.RequestException as e:
        public_ip = f"Error: {e}"

    print(f"\n {Wh}========== {Gr}SHOW INFORMATION YOUR IP {Wh}==========\n")
    print(f" {Wh}[{Gr} + {Wh}] Public IP Address  : {Gr}{public_ip}\n")

    # ── Local Network ──
    ifaces  = get_local_ifaces()
    gateway = get_gateway()

    if not ifaces:
        print(f" {Ye}[!] Could not retrieve local network information.")
        return


    for iface, local_ip, netmask in ifaces:
        info = calc_network_info(local_ip, netmask)
        print(f" {Wh}{'─'*46}")
        print(f" {Wh}Interface           : {Gr}{iface}")
        print(f" {Wh}Local IP            : {Gr}{local_ip}")
        print(f" {Wh}Subnet Mask         : {Gr}{netmask}")
        if info:
            print(f" {Wh}CIDR                : {Gr}{info['network']}/{info['prefix']}")
            print(f" {Wh}Network Address     : {Gr}{info['network']}")
            print(f" {Wh}Broadcast           : {Gr}{info['broadcast']}")
            print(f" {Wh}Usable Range        : {Gr}{info['first_host']}  →  {info['last_host']}")
            print(f" {Wh}Total Usable Hosts  : {Gr}{info['total_hosts']}")
            print(f" {Wh}Gateway             : {Gr}{gateway}")
            if info['subnets']:
                print(f" {Wh}Subnets (/24)       : {Gr}{info['subnets'][0]}")
                for s in info['subnets'][1:]:
                    print(f" {Wh}{'':<20}    {Gr}{s}")


    print(f"\n {Wh}{'─'*46}")



@is_option
def phoneGW():
    User_phone = input(
        f"\n {Wh}Enter phone number target {Gr}Ex [+34XXXXXXXXX] {Wh}: {Gr}").strip()
    default_region = "ES"

    # Catch parse exception
    try:
        parsed_number = phonenumbers.parse(User_phone, default_region)
    except phonenumbers.NumberParseException as e:
        print(f"{Re}\n [!] Invalid number: {e}")
        return

    # Validate before continuing
    if not phonenumbers.is_valid_number(parsed_number):
        print(f"{Re}\n [!] The number is not valid for any known region.")
        return

    region_code    = phonenumbers.region_code_for_number(parsed_number)
    jenis_provider = carrier.name_for_number(parsed_number, "en")
    location       = geocoder.description_for_number(parsed_number, "id")
    is_valid       = phonenumbers.is_valid_number(parsed_number)
    is_possible    = phonenumbers.is_possible_number(parsed_number)
    fmt_intl       = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
    fmt_mobile     = phonenumbers.format_number_for_mobile_dialing(parsed_number, default_region, with_formatting=True)
    fmt_e164       = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)
    number_type    = phonenumbers.number_type(parsed_number)
    tz_list        = timezone.time_zones_for_number(parsed_number)
    timezoneF      = ', '.join(tz_list) if tz_list else "N/A"

    # More number types covered
    type_map = {
        phonenumbers.PhoneNumberType.MOBILE:        "Mobile",
        phonenumbers.PhoneNumberType.FIXED_LINE:    "Fixed-line",
        phonenumbers.PhoneNumberType.VOIP:          "VoIP",
        phonenumbers.PhoneNumberType.TOLL_FREE:     "Toll-free",
        phonenumbers.PhoneNumberType.PREMIUM_RATE:  "Premium rate",
    }
    type_str = type_map.get(number_type, "Unknown type")

    print(f"\n {Wh}========== {Gr}SHOW INFORMATION PHONE NUMBERS {Wh}==========\n")
    fields = [
        ("Location",             location or "N/A"),
        ("Region Code",          region_code or "N/A"),
        ("Timezone",             timezoneF),
        ("Operator",             jenis_provider or "N/A"),
        ("Valid number",         is_valid),
        ("Possible number",      is_possible),
        ("International format", fmt_intl),
        ("Mobile format",        fmt_mobile),
        ("E.164 format",         fmt_e164),
        ("Country code",         parsed_number.country_code),
        ("Local number",         parsed_number.national_number),
        ("Type",                 type_str),
    ]
    for label, value in fields:
        print(f" {Wh}{label:<22} :{Gr} {value}")


SOCIAL_MEDIA = [
    {
        "url": "https://www.github.com/{}",
        "name": "GitHub",
        "not_found": "Not Found",
    },
    {
        "url": "https://www.instagram.com/{}",
        "name": "Instagram",
        "not_found": "Page Not Found",
    },
    {
        "url": "https://www.tiktok.com/@{}",
        "name": "TikTok",
        "not_found": "Couldn\'t find this account",
    },
    {
        "url": "https://www.youtube.com/@{}",
        "name": "YouTube",
        "not_found": "404",
        "found": "channel",
    },
    {
        "url": "https://www.twitch.tv/{}",
        "name": "Twitch",
        "not_found": "Sorry. Unless you\'ve got a time machine",
    },
    {
        "url": "https://soundcloud.com/{}",
        "name": "SoundCloud",
        "not_found": "We can\'t find that user",
    },
    {
        "url": "https://www.pinterest.com/{}",
        "name": "Pinterest",
        "not_found": "User not found",
    },
    {
        "url": "https://www.tumblr.com/{}",
        "name": "Tumblr",
        "not_found": "There\'s nothing here",
    },
    {
        "url": "https://www.reddit.com/user/{}",
        "name": "Reddit",
        "not_found": "page not found",
    },
    {
        "url": "https://www.twitter.com/{}",
        "name": "Twitter / X",
        "not_found": "This account doesn\'t exist",
    },
    {
        "url": "https://www.linkedin.com/in/{}",
        "name": "LinkedIn",
        "not_found": "Page not found",
    },
    {
        "url": "https://www.behance.net/{}",
        "name": "Behance",
        "not_found": "Page Not Found",
    },
    {
        "url": "https://www.medium.com/@{}",
        "name": "Medium",
        "not_found": "Page not found",
    },
    {
        "url": "https://www.flickr.com/people/{}",
        "name": "Flickr",
        "not_found": "Page Not Found",
    },
    {
        "url": "https://www.dribbble.com/{}",
        "name": "Dribbble",
        "not_found": "Whoops, that page is gone",
    },
    {
        "url": "https://www.deviantart.com/{}",
        "name": "DeviantArt",
        "not_found": "Not Found",
    },
    {
        "url": "https://steamcommunity.com/id/{}",
        "name": "Steam",
        "not_found": "The specified profile could not be found",
    },
    {
        "url": "https://open.spotify.com/user/{}",
        "name": "Spotify",
        "not_found": "Page not found",
    },
    {
        "url": "https://www.producthunt.com/@{}",
        "name": "Product Hunt",
        "not_found": "page not found",
    },
    {
        "url": "https://www.quora.com/profile/{}",
        "name": "Quora",
        "not_found": "Page Not Found",
    },
    {
        "url": "https://t.me/{}",
        "name": "Telegram",
        "not_found": "If you have Telegram",
        "found": "View in Telegram",
    },
    {
        "url": "https://www.snapchat.com/add/{}",
        "name": "Snapchat",
        "not_found": "Page Not Found",
    },
]


def check_site(site, username):
    """
    Checks if the username exists using per-platform logic:
    - First looks for 'not_found' text in the HTML → user definitely doesn't exist
    - Then looks for 'found' text if defined       → user definitely exists
    - Fallback: status 200
    Returns (name, url) if found, (name, None) if not.
    """
    url = site["url"].format(username)
    try:
        resp = requests.get(url, headers=HEADERS, timeout=TIMEOUT, allow_redirects=True)
        html = resp.text.lower()

        not_found_str = site.get("not_found", "")
        found_str     = site.get("found", "")

        if not_found_str and not_found_str.lower() in html:
            return site["name"], None

        if found_str:
            return site["name"], url if found_str.lower() in html else None

        # Fallback to status 200
        return site["name"], url if resp.status_code == 200 else None

    except requests.RequestException:
        return site["name"], None


@is_option
def TrackLu():
    tracklu_options = [
        {'num': 1, 'text': 'Search 1 user'},
        {'num': 2, 'text': 'Search multiple users'},
        {'num': 3, 'text': 'View history'},
        {'num': 0, 'text': 'Back'},
    ]
    
    print()
    show_submenu("USERNAME TRACKER", tracklu_options)
    
    opcion = input(f" {Wh}[ + ] {Gr}Select {Wh}: {Gr}").strip()
    
    if opcion == "3":
        # View history
        history = get_search_history("tracklu")
        if history:
            print(f"\n {Cy}HISTORY:\n")
            for entry in history[-20:]:
                print(f" {Wh}[{entry['timestamp']}] {Gr}{entry['query']:<15} {Wh}→ {Gr}{len(entry['result']['found'])} found")
            print(f"\n")
        else:
            print(f"\n {Ye}[!] No history found\n")
        return
    
    elif opcion == "0":
        return
    
    elif opcion not in ["1", "2"]:
        print(f"{Re}\n [!] Invalid option")
        time.sleep(1)
        return
    
    # CLEAR AND BANNER BEFORE INPUT
    run_banner()
    
    # Get usernames
    if opcion == "1":
        print(f"\n {Wh}Username {Gr}: {Wh}", end="")
        usernames = [input().strip()]
    else:
        print(f"\n {Wh}Usernames (comma separated) {Gr}: {Wh}", end="")
        usernames_input = input().strip()
        usernames = [u.strip() for u in usernames_input.split(",") if u.strip()]
    
    if not usernames or (len(usernames) == 1 and not usernames[0]):
        print(f"{Re}\n [!] Username cannot be empty.")
        return
    
    # SINGLE BANNER AT THE START
    run_banner()
    
    # Search all users
    all_results = []
    
    for username in usernames:
        run_banner()
        
        print(f"\n {Cy}SEARCHING: {username.upper()}\n")
        print(f" {Wh}Scanning {len(SOCIAL_MEDIA)} platforms...\n")
        
        found_list = []
        not_found_list = []
        
        # Parallel requests
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = {executor.submit(check_site, site, username): site for site in SOCIAL_MEDIA}
            completed = 0
            for future in as_completed(futures):
                completed += 1
                name, url = future.result()
                if url:
                    found_list.append((name, url))
                    print(f" {Gr}[✓] {name:<20} {Wh}({completed}/{len(SOCIAL_MEDIA)})")
                else:
                    not_found_list.append(name)
                    print(f" {Ye}[✗] {name:<20} {Wh}({completed}/{len(SOCIAL_MEDIA)})")
        
        all_results.append({
            "username": username,
            "found": found_list,
            "not_found": not_found_list
        })
        
        # Save to history
        save_search_history("tracklu", username, {
            "found": found_list,
            "not_found": not_found_list
        })
    
    # SINGLE BANNER AT THE END
    run_banner()
    
    print(f"\n {Cy}FINAL RESULTS\n")
    
    for result in all_results:
        username = result["username"]
        found_list = result["found"]
        not_found_list = result["not_found"]
        
        print(f" {Wh}{'═' * 50}")
        print(f" {Gr}{username.upper()}\n")
        
        if found_list:
            print(f" {Gr}[+] Found on {len(found_list)} platform(s)\n")
            for name, url in sorted(found_list):
                print(f"  {Wh}[{Gr}✓{Wh}] {name:<20} {Gr}{url}")
        else:
            print(f"  {Ye}[!] Not found on any platform.")
        
        if not_found_list:
            print(f"\n {Ye}[-] Not found on: {', '.join(sorted(not_found_list)[:5])}")
        
        print(f"\n")


@is_option
def domainLookup():
    """Domain information lookup"""
    print(f"\n {Wh}Domain {Gr}: {Wh}", end="")
    domain = input().strip()
    
    if not domain:
        print(f"{Re}\n [!] Domain cannot be empty.")
        return
    
    # Clean domain
    domain = domain.replace("http://", "").replace("https://", "").replace("www.", "")
    
    print(f"\n {Cy}SEARCHING: {domain.upper()}\n")
    print(f" {Wh}Fetching information...\n")
    
    try:
        # Get domain IP
        try:
            ip_address = socket.gethostbyname(domain)
        except:
            ip_address = "N/A"
        
        # Get more info using the ipwho.is API
        domain_info = {}
        if ip_address != "N/A":
            try:
                req_api = requests.get(f"http://ipwho.is/{ip_address}", headers=HEADERS, timeout=TIMEOUT)
                domain_info = req_api.json()
            except:
                pass
        
        # Get registrar info using whois
        registrar = "N/A"
        creation_date = "N/A"
        try:
            req_whois = requests.get(f"https://www.whoisxmlapi.com/api/v1?apiKey=at_2eU2qS3LF7aaQ1aQnqNhEqNgVqA6z&domain={domain}", timeout=TIMEOUT)
            if req_whois.status_code == 200:
                whois_data = req_whois.json()
                if 'result' in whois_data and whois_data['result']:
                    registrar = whois_data['result'].get('registrar', {}).get('name', 'N/A')
                    creation_date = whois_data['result'].get('createdDate', 'N/A')
        except:
            pass
        
        # Single banner at the end
        run_banner()
        
        print(f"\n {Cy}RESULTS: {domain.upper()}\n")
        
        fields = [
            ("Domain",        domain),
            ("IP Address",    ip_address),
            ("Registrar",     registrar),
            ("Creation Date", creation_date),
            ("Country",       domain_info.get("country", "N/A")),
            ("City",          domain_info.get("city", "N/A")),
            ("ISP",           domain_info.get("connection", {}).get("isp", "N/A")),
            ("Organization",  domain_info.get("connection", {}).get("org", "N/A")),
            ("Timezone",      domain_info.get("timezone", {}).get("id", "N/A")),
        ]
        
        for label, value in fields:
            print(f" {Wh}{label:<20} {Cy}→ {Gr}{value}")
        
        # Try to get DNS records
        print(f"\n {Cy}DNS Records:\n")
        try:
            import subprocess
            result = subprocess.run(['nslookup', domain], capture_output=True, text=True, timeout=5)
            lines = result.stdout.split('\n')
            found_dns = False
            for line in lines:
                if 'Address' in line:
                    print(f" {Gr}{line}")
                    found_dns = True
            if not found_dns:
                print(f" {Ye}[!] Not found")
        except:
            print(f" {Ye}[!] Not found")
        
        print(f"\n")
        
        # Save to history
        save_search_history("domain", domain, {
            "ip": ip_address,
            "registrar": registrar,
            "creation_date": creation_date
        })
        
    except Exception as e:
        print(f" {Re}[!] Error: {e}\n")


@is_option
def colorBlindnessConfig():
    """Color configuration menu for color blindness modes"""
    global current_scheme, Bl, Wh, Gr, Re, Ye, Blu, Cy, Mage
    
    print(f"\n {Wh}╔═══════════════════════════════════════════╗")
    print(f" {Wh}║ {Gr}    COLOR CONFIG - VISION MODES      {Wh}║")
    print(f" {Wh}╚═══════════════════════════════════════════╝\n")
    
    print(f" {Wh}[{Gr}1{Wh}] {Gr}Normal Vision (no color blindness)")
    print(f" {Wh}[{Gr}2{Wh}] {Ye}Protanopia (red blindness)")
    print(f" {Wh}[{Gr}3{Wh}] {Ye}Deuteranopia (green blindness)")
    print(f" {Wh}[{Gr}4{Wh}] {Mage}Tritanopia (blue blindness)")
    print(f" {Wh}[{Gr}0{Wh}] {Wh}Back\n")
    
    choice = input(f" {Wh}Select your vision mode {Gr}: {Wh}").strip()
    
    schemes = {"1": "normal", "2": "protanopia", "3": "deuteranopia", "4": "tritanopia"}
    
    if choice in schemes:
        current_scheme = schemes[choice]
        scheme = color_schemes[current_scheme]
        Bl   = scheme["black"]
        Wh   = scheme["white"]
        Gr   = scheme["green"]
        Re   = scheme["red"]
        Ye   = scheme["yellow"]
        Blu  = scheme["blue"]
        Cy   = scheme["cyan"]
        Mage = scheme["magenta"]
        
        print(f"\n {Gr}[✓] Colors updated successfully!")
        print(f" {Wh}Scheme: {Gr}{current_scheme.upper()}\n")
        time.sleep(2)


options = [
    {'num': 1, 'text': 'IP Tracker',           'func': IP_Track},
    {'num': 2, 'text': 'Show Your IP',          'func': showIP},
    {'num': 3, 'text': 'Phone Number Tracker',  'func': phoneGW},
    {'num': 4, 'text': 'Username Tracker',      'func': TrackLu},
    {'num': 5, 'text': 'Domain Lookup',         'func': domainLookup},
    {'num': 6, 'text': 'Color Config',          'func': colorBlindnessConfig},
    {'num': 0, 'text': 'Exit',                  'func': exit},
]


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def show_submenu(title, options_list):
    """Display a secondary menu styled like the main menu"""
    # Show options without decorative boxes
    for opt in options_list:
        print(f'{Wh}[ {opt["num"]} ] {Gr}{opt["text"]}')
    print()


def option_text():
    text = ''
    for opt in options:
        text += f'{Wh}[ {opt["num"]} ] {Gr}{opt["text"]}\n'
    return text


def is_in_options(num):
    return any(opt['num'] == num for opt in options)


def call_option(opt):
    if not is_in_options(opt):
        raise ValueError('Option not found')
    for option in options:
        if option['num'] == opt:
            option.get('func', lambda: print('No function detected'))()


def option():
    clear()
    stderr.writelines(fr"""{Mage}
   ______ ______  _______ ___      _____ _   ______   _________  ___  _______ __
  / __/ // / __ \/ ___/ //_/ | /| / / _ | | / / __/__/_  __/ _ \/ _ |/ ___/ //_/
 _\ \/ _  / /_/ / /__/ ,<  | |/ |/ / __ | |/ / _//___// / / , _/ __ / /__/ ,<   
/___/_//_/\____/\___/_/|_| |__/|__/_/ |_|___/___/    /_/ /_/|_/_/ |_\___/_/|_|  {Wh}
                                                                                
                      {Wh}[ + ]  C O D E   B Y  PATPURALU  [ + ]
    """)
    stderr.writelines(f"\n\n\n{option_text()}")


def run_banner():
    """Show banner only"""
    clear()
    time.sleep(0.5)
    
    L = [
        Mage + """
                 %#.                     /&,                                  #/                     .#*                
                 ,@@#                    .&@%,                              (&%.                    #&#                 
                  (@&&#.                  (@&&#.                          /&&@/                  .#&&&*                
                  /@&&&@%                 .%&&&&&.                      #&&&&%.                 %&&&&%.                
                   %&&&@&@#                (@&&&&@#.                  *&&@&&&*               .#&&&&&@*                 
                   ,&&&&@&&&&               @&&&&&&@#               /&&&&&&&%               @&@&&&&@%                  
                    &&&@&&&@&&&&&@@%/.      ,@&&&&&&&&&&&&&&&&&&&&&&@&&&@&&@,      .(&@@&&&@&&&&&&&@,                  
                     @&&&&&&&&&&&&&&&&&&@*   #&&&&&&&&&&&&&&@&&&&&&&&&&&&&@#   %&&&&&&&&&&&&&&&&&&@#                 
                     (&&&&&&&&&&@&&&&&&&&%.  ,@&&&&&@&&&@%%%%%%&&&&&&&&&@&&,  *%&&&&&&&&&&&&&&&&&&&,                 
                     ,@&&&&@&.,*(%&@@@&&&&/   (&&&&&&&&&&#     (&&&&&&&&&@#   /&&&@@@&%#*,./@&&&&@#.                 
                      (&&&&&@%(/.      .,//   *&&&&&&&&&&&/   /&&&&&&&&@&&,  ./*.       .*/&&&&&&&*                   
                      ,%&&&@&&&&&@&&@&%#/,     %&&&&&&&&&&&, ,&&&&&&&&&&@#    .*((#&&@&&&&&&@&@&&%                    
                       #&&&&&@&&&&&&&&&&&&&&.  .@&&&&&&&&&&@#&&&&&&&&&&&@,  *@&&&&&&&&@&&&&&&&&&@,                    
                       .@&&&&&(  .,*(&@@@&&@(   %@&&&&&&&&&&&&&&&&&&&&&@#   @&&&@@&#/,.  .%&&&&@#                     
                        .@&&&&&&@%,        .**   (@&&&@&@&&&&&&&&@&@@&@/   *.         .%&&&&&&@(                      
                          #&&&&@&&&&@&&&@@&*.      (&&@&@&&&&&&&&&@&@*       *%@&&&&&&&&&&&&&&*                        
                           /@&&@@&&&&&&&&&&&&&@&&&,  /&&&&&&&&&&&&&.  *&&@&&@&&&&&&&&&&&&&&@#                          
                             #&&&&/,(%&&&@&&@&&&&&@&,  /&&&&&&&&%, .#&&&@&&@&&&&@&%#**%&&&%.                          
                          (/  ,&@@&@#.      ,/(#&&&&&&(  *&@@&%. ,%@&@&@%#(*.       /&&@@(   /*                        
                          /&&.  (@&&&@&/         *@@%&&@#. ,#. *@&&&&&%,         ,%&&&&%   ,&%.                        
                           %&&(  .%&&&&&&&%/      .&&&&@&&%, *%&&&&&@#       ,#&&&&&&&/  .#&@*                         
                           /&&&&.  (&@&&&&@@&&&#,   %@&@&&&@&@&&&&@&/    #%&&&@&&&&@%.  .@&&@.                         
                            @&&&@#   %&&@&@&@&&&&&@&(%&&&&&&&&&&&&&#%%&&&&&&&&&&@&&*   (@&&@(                          
                            *@&&&&&,  /@%@&@&&&&&&&&@&&&&&&&&&&&&&&&&&&&&&&&&&&&&%   ,&&&&&&.                          
                             @@&&&&@&   @@&@&&&&&&&&&&@&&&&&&&&&&&&&&&&&&&&&&&&@.   @&&&@&@(                           
                             /&&&&&&@&/  ,&@&&&&&&&&&&&&&&&&&&&&&&&&&&&&&@&&@@(   /&&&&&&&&,                           
                             ,@&&&&@&&@&.  #&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&,   %&&&&&&&&#                            
                              #&&&&&&&&&@(  .&@&&&&&&&&&&&&&&&&&&&&&&&&&&@&/   *&&&&&&&&&&*                            
                              /&&&&&&&&&&&&,  (&&&&&&&&&&&&&&&&&&&&&&&&&&%,  .%&@&&&&&&&&%.                            
                               %&&&&&&&&&&&@#  ,@&&&&&&&&&&&&&&&&&&&&&&@/   #&&&&&&&&&&&@/                             
                               (&&&&&&&&&&&&&&*  (&@&&&@&&&&&&&&@&@&@&%.  *&&&&&&&&&&&&@@.                             
                                @@&&&&&&&&&&&&@#  .%@&&&&&&&&&&&&@&&@*   #&@&&&&&&&@&&@@(                              
                                  ,#@@@&&@&&@&&@@/  /@&&&@&&&&&&&&@#   /&&@&&&&&&&@@%/.            
                                        .(&@&&&&@@%. .%&&@&&&&&&&&*  .#&&&&&&@%*                                       
                                              ,(&@&@(  /&@&&&&&@(   /&&&&*.                                            
                                                    ,*. .%@&@&&,  .*.                                                  
                                                          *&@(                                                        
        
        
                                                     @CODE BY PATPURALU      
                                           
        """,

    ]
    
    stderr.write("\n".join(L) + "\n")
    time.sleep(0.3)


# While loop instead of recursion to avoid RecursionError in long sessions
def main():
    while True:
        clear()
        option()
        time.sleep(0.5)
        try:
            opt = int(input(f"{Wh}\n [ + ] {Gr}Select Option : {Wh}"))
            if not is_in_options(opt):
                print(f'\n{Wh}[ {Re}! {Wh}] {Re}Invalid option')
                time.sleep(1.5)
                continue
            call_option(opt)
            input(f'\n{Wh}[ {Gr}+ {Wh}] {Gr}Press enter to continue')
        except ValueError:
            print(f'\n{Wh}[ {Re}! {Wh}] {Re}Please input a number')
            time.sleep(1.5)
        except KeyboardInterrupt:
            print(f'\n{Wh}[ {Re}! {Wh}] {Re}Exit')
            time.sleep(1)
            exit()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f'\n{Wh}[ {Re}! {Wh}] {Re}Exit')
        time.sleep(1)
        exit()
