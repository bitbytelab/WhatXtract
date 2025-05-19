<!-- README.md -->

<div align="center">
  
  <img src="https://bitbytelab.github.io/assets/logos/bitbytelab.png" alt="BitByteLab Logo" height="120">
  <h1 align="center">📞 WhatXtract</h1>

  <p>
    🕵️‍♂️ A powerful multithreaded CLI tool to <strong>extract and verify WhatsApp numbers</strong> using <strong>WhatsApp Web</strong> — no API needed.
  </p>

  <p>
    WhatXtract is a <strong>robust</strong>, <strong>easy-to-use</strong> WhatsApp data extraction and automation toolkit built in Python. It lets you <strong>verify, extract, and validate contact numbers</strong> directly via WhatsApp Web with headless automation — powered by <code>selenium</code> and <code>undetected-chromedriver</code>.
  </p>

  <p>
    Designed for <strong>developers</strong>, <strong>growth hackers</strong>, <strong>marketers</strong>, and <strong>data analysts</strong>, WhatXtract enables you to:
    <ul align="left" style="text-align: left;">
      <li>✅ Verify which numbers are active WhatsApp users</li>
      <li>📤 Extract and clean up phone lists for lead gen or CRM sync</li>
      <li>⚙️ Build custom WhatsApp workflows with automation at the core</li>
    </ul>
  </p>

  <p>
    <img src="https://img.shields.io/github/v/release/bitbytelab/whatxtract?style=flat-square" alt="GitHub Release Badge" />
    <img src="https://img.shields.io/badge/license-Proprietary-red?style=flat-square" alt="License Badge" />
    <img src="https://img.shields.io/pypi/pyversions/whatxtract?style=flat-square" alt="Python Version" />
    <img src="https://img.shields.io/badge/status-Beta-orange?style=flat-square" alt="Project Status" />
    <img src="https://img.shields.io/pypi/dm/whatxtract?style=flat-square" alt="PyPI Downloads" />
    <img src="https://img.shields.io/github/languages/top/bitbytelab/whatxtract?style=flat-square" alt="Top Language" />
    <a href="https://github.com/astral-sh/ruff">
      <img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json" alt="Ruff Code Quality" />
    </a>
  </p>
</div>


<div align="center">
  <img src="assets/logo.png" alt="WhatsChecker Logo" height="150"/>
  <h1 align="center">WhatXtract</h1>

  <p>
    🕵️‍♂️ A powerful multithreaded CLI tool to <strong>check WhatsApp number validity</strong> via WhatsApp Web.
  </p>

  <p>
    Whatxtract is a powerful and easy-to-use WhatsApp data extraction and automation toolkit built in Python. It allows you to extract, verify, and validate contact numbers directly through WhatsApp Web — without using the official API. Designed for developers, marketers, and analysts, Whatxtract automates WhatsApp web sessions using Selenium and undetected-chromedriver, helping you check which numbers are active WhatsApp users and gather contact data efficiently.

    Whether you're verifying leads, cleaning up phone number lists, or building your own WhatsApp automation workflows, Whatxtract streamlines the process securely and reliably.
  </p>

  <p>
    <img src="https://img.shields.io/badge/version-0.0.1-blue?style=flat-square" alt="Version Badge" />
    <img src="https://img.shields.io/badge/license-MIT-green?style=flat-square" alt="License Badge" />
    <img src="https://img.shields.io/badge/python-3.9%2B-yellow?style=flat-square" alt="Python Badge" />
    <img src="https://img.shields.io/badge/status-beta-orange?style=flat-square" alt="Status Badge" />
    <a href="https://github.com/astral-sh/ruff"><img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json" alt="Ruff" style="max-width:100%;"></a>
  </p>
</div>

---

## 🌟 Features

- ✅ **Detect Active/Inactive WhatsApp Numbers**
- 🧠 **Intelligent Login Handling** (QR scan and session reuse)
- 🔀 **Concurrent Multi-Account Checking**
- 🛡️ **Proxy Support** (optional, per account)
- 🗃️ **Persistent Profiles** – saves WhatsApp login sessions
- 🕶️ **Headless Mode** – optional
- 🕓 **Customizable Delays** – mimic human-like behavior
- 📂 **Custom Config Support** (`whatschecker.config.json`)
- 📈 **Built with Selenium + Undetected ChromeDriver**
- 💥 **Auto dependency installs on first run**
- 📇 **Extracts valid WhatsApp numbers from saved contacts on the device**

---

## 🚀 Usage

### 1. 📦 Installation

```bash
git clone https://github.com/bitbytelab/WhatsChecker.git
cd WhatXtract
chmod +x whatxtract.py
```

### 2. 🧪 First-time Setup (Scan QR)

```bash
./whatxtract.py --add-account
```

Scan the QR code to save your WhatsApp session. You can add multiple accounts this way.

---

### 3. 📤 Checking Numbers

Prepare an input file (e.g., `numbers.txt`) with **one number per line**:

```
+12025550123
+447911123456
+8801711123456
```

Run the checker:

```bash
./whatxtract.py --input numbers.txt --valid active.txt --invalid inactive.txt
```

You can also run in headless mode:

```bash
./whatxtract.py --input numbers.txt --valid active.txt --invalid inactive.txt --headless
```

---

### 4. 📇 Contacts Extraction

To extract valid WhatsApp numbers from your saved contacts:

```bash
python -m whatxtract --input contacts
```

This will:

1. Launch WhatsApp Web and log you in.
2. Extract contacts from WhatsApp database. 
3. Save valid WhatsApp numbers along with name, about, and avatar info to a CSV.

The generated CSV will be saved as:

```
valid_whatsapp_contacts_YYYY_mm_dd_HH_MM.csv
```

📁 Example output preview:

| name         | about                        | user_avatar                                     |
|--------------|------------------------------|-------------------------------------------------|
| 019xxxxxxxxx | Always learning               | https://media.whatsapp.net/...                  |
| 018xxxxxxxxx | Big brother watching you 😊   | default                                         |

📝 **Note:** Contact names must be saved as numbers (i.e., "017xxxxxxx") to work properly with this feature.



### 5. 🧩 Optional Arguments

| Flag            | Description                                      |
|-----------------|--------------------------------------------------|
| `--input`       | Input file with numbers                          |
| `--valid`       | Output file for active numbers                   |
| `--invalid`     | Output file for inactive numbers                 |
| `--delay`       | Base delay in seconds between number checks      |
| `--proxies`     | List of proxies (e.g., `http://ip:port`)         |
| `--headless`    | Run Chrome in headless mode                      |
| `--add-account` | Launch new profile and scan QR to add account    |

---

### 6. ⚙️ Config File Support

You can also define your settings in a `whatschecker.config.json` file:

```json
{
  "input": "numbers.txt",
  "valid": "active.txt",
  "invalid": "inactive.txt",
  "delay": 8,
  "proxies": ["http://127.0.0.1:8000", null]
}
```

Then just run:

```bash
./whatxtract.py
```

---

## 🔐 Session Management

Saved WhatsApp sessions are stored in:

```bash
./Profiles/account1
./Profiles/account2
...
```

Remove a folder to reset that session.

---

## 🧰 Dependencies

- Python `3.9+`
- [undetected-chromedriver](https://github.com/ultrafunkamsterdam/undetected-chromedriver)
- [selenium](https://pypi.org/project/selenium)

📦 Auto-installs on first run if not found!

---

## ❓ FAQ

**Q: Will my WhatsApp account get banned?**  
A: This script mimics human behavior using real browser sessions and delays. Use proxies and multiple accounts to reduce risk. No API violations.

**Q: Is this open source?**  
A: Yes! MIT licensed. Use it responsibly and contribute back.

---

## 👨‍💻 Author

Made with ❤️ by [BitByteLab](https://github.com/bitbytelab)  
📧 Contact: [bbytelab@gmail.com](mailto:bbytelab@gmail.com)

---

## 📄 License

MIT License – see [LICENSE](LICENSE) file for details.

---

## ⭐️ Star this project

If you find this useful, please consider starring the repo!  
👉 [github.com/bitbytelab/WhatsChecker](https://github.com/bitbytelab/WhatsChecker)
