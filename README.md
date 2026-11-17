# 🇰🇪 Kenyan SMS Phishing Detector

Hybrid **Rule-Based + Machine Learning** detector for Kenyan SMS phishing (M-PESA, Safaricom, KRA, bank scams).

Built with Python to protect users from fake messages like *"Your M-PESA account is blocked, click here"*.

## 🚀 Features
- Detects M-PESA / Safaricom / KRA / Bank impersonation
- Rule-based detection for known scam patterns (fake links, urgency, PIN requests)
- Machine Learning classifier trained on Kenyan SMS dataset
- Works offline, fast and lightweight
- Simple CLI - paste any SMS and get result instantly

## 📂 Project Structure
kenyan-sms-phishing-detector/
├── python --learning/
│   ├── detector.py
│   └── messages.csv
└── README.md

## ▶️ How to Run
1. Clone the repo:
git clone https://github.com/obadiahmongare/kenyan-sms-phishing-detector.git

2. Run the detector:
python detector.py

3. Paste an SMS when asked, e.g:
> "Dear customer your M-PESA PIN has expired, verify here http://bit.ly/fake"

Result: ⚠️ PHISHING DETECTED

## 🧪 Example
| SMS | Result |
| :--- | :--- |
| "Your OTP is 4567. Do not share it" | ✅ SAFE |
| "Your M-PESA account blocked. Click http://mpesa-verify.com" | ⚠️ PHISHING |

## 📊 Dataset
`messages.csv` contains labeled Kenyan SMS messages (phishing vs legit) used for training and testing.

## 🛠️ Tech Stack
- Python 3
- Scikit-learn
- Pandas

## 👨‍💻 Author
**Obadiah Mongare** - Cybersecurity Student, Kenya
GitHub: https://github.com/obadiahmongare

## ⭐ Support
If you find this useful, give it a star!
