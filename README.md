# 🌐 Cloudflare DDNS Updater

A lightweight Python script to automatically update your Cloudflare A records (like `@`, `www`, `dev`, etc.) whenever your public IP changes.

---

## 🏠 Why Use This?

If you're self-hosting services at home — like a web server, media server (Plex, Jellyfin), or remote access tool — and your ISP changes your IP from time to time, this tool keeps your domain pointed to the right IP address **automatically**.

It's perfect for:
- Home labs with dynamic or semi-static IPs
- Personal websites or portfolios hosted from home
- Remote access to Raspberry Pi, NAS, Docker stacks, or VMs
- Anyone who doesn’t want to manually update DNS records on every IP change

All you need is:
- A domain managed on Cloudflare
- A public IP address (dynamic or static)
- Python installed on your server or machine

---

## ⚙️ Features

✅ Detects IP changes  
✅ Updates A records only if needed  
✅ Works with multiple domains (zones)  
✅ Auto TTL  
✅ Supports `proxied` (orange cloud)  
✅ Environment-based token (no hardcoded secrets)  
✅ Select specific subdomains to update  
✅ Optionally skip creating records if they don’t exist

---

## 🚀 Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/ashfaqahmed/cloudflare-ddns-updater
cd cloudflare-ddns-updater
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up your `.env` file

Create a `.env` file in the root folder:

```env
CLOUDFLARE_API_TOKEN=your_cloudflare_api_token_here
```

> 🔐 Create a token from https://dash.cloudflare.com/profile/api-tokens with:
> - Zone: Read
> - DNS: Edit

### 4. Configure subdomains and record creation behavior

In `update_dns.py`, customize the top section:

```python
SUBDOMAINS_TO_UPDATE = ['@']  # List of subdomains (e.g., ['@', 'www', 'dev'])
CREATE_IF_MISSING = False     # Set to True to auto-create records if not found
```

- Use `'@'` to update the **root domain** (e.g., `example.com`)
- Add any subdomain strings to update additional A records
- By default, the script will **not create records** — only update existing ones

---

## 🧪 Run the Script

```bash
python update_dns.py
```

- Only updates DNS records if your public IP has changed
- Saves the last known IP in `last_ip.txt` locally

---

## 🕒 Automate with Cron (Linux/macOS)

To run the script automatically every 30 minutes:

```bash
crontab -e
```

Add this line:

```bash
*/30 * * * * /usr/bin/python3 /path/to/update_dns.py >> /path/to/ddns.log 2>&1
```

---

## 📁 Project Structure

```
cloudflare-ddns-updater/
├── update_dns.py         # Main script
├── .env                  # API token (not committed)
├── .gitignore            # Prevents secret files from being pushed
├── requirements.txt      # Python dependencies
└── README.md             # This file
```

---

## ✅ Example .env File

```
CLOUDFLARE_API_TOKEN=sk_test_your_cloudflare_api_token_here
```

---

## 🛡 License

**MIT License**

Free to use, modify, and share. Just don’t publish your own API tokens 😉

---

## 💬 Feedback / Contributions

Pull requests and issues are welcome!  
If you find this useful, drop a star ⭐ or share it with other homelabbers!

---

## ☕ Support My Work

If this tool saved you time or effort, consider buying me a coffee.  
Your support helps me keep building and maintaining open-source projects like this!

You can either scan the QR code below or click the link to tip me:

👉 [**buymeacoffee.com/ashfaqueali**](https://buymeacoffee.com/ashfaqueali)

<img src="https://ashfaqsolangi.com/images/bmc_qr.png" alt="Buy Me a Coffee QR" width="220" height="220" />