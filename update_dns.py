import requests
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# 🔐 Cloudflare API Token from .env file
API_TOKEN = os.getenv("CLOUDFLARE_API_TOKEN")

# 🛠 Configuration
SUBDOMAINS_TO_UPDATE = ['@']  # Add subdomains here
CREATE_IF_MISSING = False  # Set to True if you want to auto-create missing A records
IP_FILE = 'last_ip.txt'

# Headers for Cloudflare API
HEADERS = {
    'Authorization': f'Bearer {API_TOKEN}',
    'Content-Type': 'application/json',
}

def get_public_ip():
    return requests.get("https://api.ipify.org").text.strip()

def read_saved_ip():
    if os.path.exists(IP_FILE):
        with open(IP_FILE, 'r') as f:
            return f.read().strip()
    return None

def save_current_ip(ip):
    with open(IP_FILE, 'w') as f:
        f.write(ip)

def get_all_zones():
    zones = []
    page = 1
    per_page = 50

    while True:
        response = requests.get(
            f'https://api.cloudflare.com/client/v4/zones?page={page}&per_page={per_page}',
            headers=HEADERS
        )
        result = response.json()
        if not result['success']:
            raise Exception(f"Failed to fetch zones: {result}")
        zones.extend(result['result'])

        if page * per_page >= result['result_info']['total_count']:
            break
        page += 1

    return zones

def get_record_id(zone_id, full_record_name):
    response = requests.get(
        f'https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records?type=A&name={full_record_name}',
        headers=HEADERS
    )
    result = response.json()
    if result['success'] and result['result']:
        return result['result'][0]['id'], result['result'][0]['content']
    return None, None

def update_or_create_record(zone_id, full_record_name, ip):
    record_id, current_ip = get_record_id(zone_id, full_record_name)

    if record_id is None:
        if CREATE_IF_MISSING:
            print(f"➕ Creating new A record for {full_record_name}")
        else:
            print(f"⚠️  Record for {full_record_name} does not exist. Skipping (CREATE_IF_MISSING = False).")
            return

    if current_ip == ip:
        print(f"✔ No update needed for {full_record_name}, IP unchanged.")
        return

    data = {
        "type": "A",
        "name": full_record_name,
        "content": ip,
        "ttl": 1,
        "proxied": True
    }

    if record_id:
        url = f'https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{record_id}'
        response = requests.put(url, headers=HEADERS, json=data)
        action = "🔄 Updated"
    elif CREATE_IF_MISSING:
        url = f'https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records'
        response = requests.post(url, headers=HEADERS, json=data)
        action = "✅ Created"
    else:
        print(f"⚠️  Record for {full_record_name} not found and CREATE_IF_MISSING is False. Skipping.")
        return

    if response.ok:
        print(f"{action} record for {full_record_name} → {ip}")
    else:
        print(f"❌ Error updating {full_record_name}: {response.json()}")

def main():
    current_ip = get_public_ip()
    saved_ip = read_saved_ip()

    if current_ip == saved_ip:
        print(f"✔ IP unchanged ({current_ip}), skipping updates.")
        return

    print(f"🌐 IP changed to {current_ip}, updating Cloudflare records...")

    try:
        zones = get_all_zones()
    except Exception as e:
        print(f"❌ Error fetching zones: {e}")
        return

    for zone in zones:
        domain = zone['name']
        zone_id = zone['id']
        try:
            for sub in SUBDOMAINS_TO_UPDATE:
                record_name = domain if sub == '@' else f"{sub}.{domain}"
                update_or_create_record(zone_id, record_name, current_ip)
        except Exception as e:
            print(f"❌ Error processing {domain}: {e}")

    save_current_ip(current_ip)

if __name__ == "__main__":
    main()