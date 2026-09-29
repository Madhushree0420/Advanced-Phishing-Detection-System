from flask import Flask, render_template, request
from urllib.parse import urlparse
import os
import easyocr

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "static/uploads"

# ---------------- OFFICIAL DOMAINS ----------------
OFFICIAL_DOMAINS = {
    "bank": {
        "sbi": "sbi.co.in",
        "hdfc": "hdfcbank.com",
        "icici": "icicibank.com"
    }
}

# ---------------- OCR ----------------
reader = easyocr.Reader(['en'], gpu=False)

# ---------------- HELPERS ----------------
def extract_domain(url):
    try:
        return urlparse(url).netloc.lower()
    except:
        return ""

def extract_text_from_image(image_path):
    text = reader.readtext(image_path, detail=0)
    return " ".join(text).lower()

# ---------------- MAIN ROUTE ----------------
@app.route("/", methods=["GET", "POST"])
def index():
    output = None

    if request.method == "POST":

        sender_type = request.form.get("sender_type", "").lower()
        sender_name = request.form.get("sender_name", "").lower()
        sms_text = request.form.get("sms_text", "").lower()
        url = request.form.get("url", "").strip()
        image = request.files.get("image")

        # ---------- BASE SCORES ----------
        risk = 0
        trust = 100

        threats = []
        emotions = []
        reasoning = []
        trust_steps = []
        awareness = []
        recommendations = []

        scam_category = "None"
        attack_intent = "Unknown"

        combined_text = sms_text

        # ---------- IMAGE + OCR ----------
        if image and image.filename:
            os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
            image_path = os.path.join(app.config["UPLOAD_FOLDER"], image.filename)
            image.save(image_path)

            ocr_text = extract_text_from_image(image_path)
            combined_text += " " + ocr_text

            risk += 25
            trust -= 15
            threats.append("Social Engineering")
            trust_steps.append("Image-based message detected (-15%)")
            awareness.append("Images are used to bypass text-based security filters.")

        # ---------- URGENCY ----------
        if any(w in combined_text for w in ["urgent", "immediately", "blocked", "suspend", "24 hours", "verify now"]):
            emotions.append("Fear / Urgency")
            risk += 30
            trust -= 25
            trust_steps.append("Urgency language detected (-25%)")
            awareness.append("Urgency pressures victims into impulsive actions.")

        # ---------- BANK IMPERSONATION ----------
        if any(bank in combined_text for bank in ["sbi", "state bank", "hdfc", "icici"]):
            risk += 30
            trust -= 30
            threats.append("Phishing")
            scam_category = "Bank Impersonation"
            attack_intent = "Credential Theft"
            trust_steps.append("Bank impersonation detected (-30%)")
            reasoning.append("Message claims to be from a bank.")

        # ---------- DOMAIN CHECK ----------
        if url:
            received_domain = extract_domain(url)
            official_domain = OFFICIAL_DOMAINS.get(sender_type, {}).get(sender_name)

            if official_domain and not received_domain.endswith(official_domain):
                risk = 95
                trust = 20
                threats.extend(["Phishing", "Social Engineering"])
                scam_category = "Fake Website"
                attack_intent = "Credential Theft"
                trust_steps.append("Domain mismatch detected (-80%)")
                reasoning.extend([
                    f"Claimed sender: {sender_name.upper()}",
                    f"Official domain: {official_domain}",
                    f"Received domain: {received_domain}",
                    "Domain mismatch confirms phishing."
                ])

        # ---------- KEYWORD SCAMS ----------
        if "otp" in combined_text:
            scam_category = "OTP Scam"
            attack_intent = "OTP Theft"
            risk += 40
            trust -= 40
            trust_steps.append("OTP scam pattern detected (-40%)")

        if "kyc" in combined_text or "account blocked" in combined_text:
            scam_category = "KYC Scam"
            attack_intent = "Credential Theft"
            risk += 35
            trust -= 35
            trust_steps.append("KYC/account block scam detected (-35%)")

        # ---------- NORMALIZE ----------
        risk = min(max(risk, 0), 100)
        trust = min(max(trust, 0), 100)

        # ---------- FINAL DECISION (STRICT RULE) ----------
        if risk >= 70 or trust <= 40:
            decision = "PHISHING"
            recommendations = [
                "Do NOT click links or download attachments",
                "Never share OTP, PIN, or passwords",
                "Block and report the sender",
                "Contact the organization using official apps/websites"
            ]
        else:
            decision = "SAFE"
            recommendations = ["No immediate threat detected. Remain cautious."]

        # ---------- OUTPUT ----------
        output = {
            "decision": decision,
            "risk": risk,
            "trust": trust,
            "threats": list(set(threats)) or ["Safe"],
            "reasoning": reasoning or ["No strong phishing indicators found."],
            "scam_category": scam_category,
            "attack_intent": attack_intent,
            "emotions": emotions,
            "trust_steps": trust_steps,
            "awareness": list(set(awareness)),
            "recommendations": recommendations
        }

    return render_template("index.html", output=output)

if __name__ == "__main__":
    app.run(debug=True)
