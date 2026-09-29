# Advanced-Phishing-Detection-System
A Flask-based intelligent Phishing Detection application that analyzes SMS messages, URLs, sender profiles, and uploaded screenshot images (via OCR) to detect social engineering and phishing attacks.

---

## 🌟 Key Features

- **Multi-Modal Threat Detection**:
  - **Text Analysis**: Identifies fear/urgency keywords, OTP lures, and KYC verification scams.
  - **OCR Integration**: Extracts and analyzes text from uploaded screenshot images using [EasyOCR].
  - **Domain Verification**: Validates URLs against official whitelisted domains to identify domain mismatches and spoofing attempts.
  - **Impersonation Checking**: Flags brand and bank impersonation attempts (e.g., SBI, HDFC, ICICI).
- **Explainable AI Scoring**:
  - Computes clear **Risk (%)** and **Trust (%)** scores.
  - Step-by-step breakdown of score deductions and threats.
  - Categorizes scam types (e.g., *Bank Impersonation*, *OTP Scam*, *KYC Scam*, *Fake Website*).
- **Security Guidance**:
  - Provides situational awareness insights.
  - Generates actionable safety recommendations and next steps for the user.

---

## 🏗️ Project Structure

```
GenAI_Phishing_Project/
│
├── app.py                  # Main Flask application and detection logic
├── templates/
│   └── index.html          # Web interface for input and results display
├── static/
│   └── uploads/            # Temporary directory for uploaded screenshot images
├── .env                    # Environment configuration
├── requirements.txt        # Python package dependencies
└── README.md               # Project documentation
```

---

## 🚀 Getting Started

### 1. Prerequisites

- Python 3.10+ installed on your system.

### 2. Setup Virtual Environment

Create and activate a virtual environment:

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

Install the required packages using `pip`:

```bash
pip install -r requirements.txt
```

*(Alternatively, install the core packages directly: `pip install flask easyocr torch torchvision`)*

---

## 💻 Running the Application

Start the Flask development server:

```bash
python app.py
```

Once started, open your web browser and navigate to:
```
http://127.0.0.1:5000
```

---

## 🔍 How to Use

1. **Sender Details**: Select the sender category (e.g., *Bank*, *E-commerce*, *Payment App*) and enter the claimed sender name.
2. **Message Text**: Paste any suspicious SMS or email body text.
3. **Link / URL**: Enter any URL received in the message for domain authenticity verification.
4. **Screenshot / Image**: Upload an image or screenshot of a message (text will be automatically extracted using OCR).
5. **Analyze**: Click **Analyze Threat** to view the safety verdict, risk meter, detected threats, and safety advice.

---

## 🛠️ Tech Stack

- **Backend**: Python, [Flask](https://flask.palletsprojects.com/)
- **OCR / Vision**: [EasyOCR](https://github.com/JaidedAI/EasyOCR), PyTorch
- **Frontend**: HTML5, CSS3, Jinja2 Templates
