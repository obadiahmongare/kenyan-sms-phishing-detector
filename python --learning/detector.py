# KENYAN SMS PHISHING DETECTOR - FINAL VERSION (No sklearn, Pure Python)
import re, csv, math, os
from collections import Counter

TRUSTED_SENDERS = ["safaricom", "mpesa", "kplc", "equity", "kcb", "nhif", "helb", "kra"]

# ---------- RULE ENGINE ----------
def rule_engine(message, sender="Unknown"):
    msg = message.lower()
    sender_lower = sender.lower()
    score = 0
    reasons = []

    # 1. Urgent language
    for w in ["urgent", "immediately", "blocked", "suspended", "verify now", "act now", "last warning"]:
        if w in msg:
            score += 25; reasons.append(f"Urgent / fear language: '{w}'"); break
    # 2. Suspicious Link
    if any(x in msg for x in ["http", "www.", "bit.ly", ".xyz", ".top", ".click", "tinyurl"]):
        if sender_lower not in TRUSTED_SENDERS:
            score += 35; reasons.append("Suspicious link from unknown sender")
            if any(x in msg for x in ["mpesa-", "safaricom-", "kra-", "equity-"]):
                score += 15; reasons.append("Fake brand in link (e.g. mpesa-)")
    # 3. Asks for PIN / OTP
    if any(x in msg for x in ["pin", "otp", "password", "puk"]):
        if any(x in msg for x in ["your pin", "your otp", "send", "share", "enter"]):
            score += 40; reasons.append("Asks for PIN / OTP / Password - Safaricom NEVER asks this")
    # 4. Asks to send money
    if re.search(r"send (ksh )?\d+", msg) or "send money" in msg or "double your money" in msg:
        score += 25; reasons.append("Asks you to send money to claim something")
    # 5. Fake Prize / Job / Loan
    for w in ["you have won", "congratulations", "claim your prize", "you have been selected", "double your money", "free loan", "pay for training"]:
        if w in msg:
            score += 30; reasons.append(f"Prize / Job / Loan trick: '{w}'"); break
    # 6. Fake Sender
    if any(x in msg for x in ["safaricom", "m-pesa", "mpesa", "kra", "equity", "kcb", "kplc"]):
        if sender.startswith("07") or sender.startswith("01") or sender.startswith("+254"):
            score += 20; reasons.append("Claims to be official but sent from 07xx personal number")

    return min(score, 100), reasons

# ---------- PURE PYTHON ML (Naive Bayes, no sklearn) ----------
word_counts = {0: Counter(), 1: Counter()}
class_counts = Counter()
vocab = set()

def train_ml(data):
    global word_counts, class_counts, vocab
    for text, label in data:
        class_counts[label] += 1
        for w in text.lower().split():
            word_counts[label][w] += 1
            vocab.add(w)
    return True

def predict_ml(message):
    if sum(class_counts.values()) == 0:
        return 0
    words = message.lower().split()
    scores = {}
    total = sum(class_counts.values())
    for label in [0, 1]:
        score = math.log((class_counts[label] + 1) / (total + 2))
        total_words = sum(word_counts[label].values()) + len(vocab) + 1
        for w in words:
            score += math.log((word_counts[label][w] + 1) / total_words)
        scores[label] = score
    diff = scores[1] - scores[0]
    if diff > 20: prob = 1.0
    elif diff < -20: prob = 0.0
    else: prob = 1 / (1 + math.exp(-diff))
    return int(prob * 100)

def load_data():
    data = []
    if os.path.exists("messages.csv"):
        with open("messages.csv", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                try: data.append((row["message"], int(row["is_scam"])))
                except: pass
    return data

def analyze(message, sender="Unknown"):
    rule_score, reasons = rule_engine(message, sender)
    ml_score = predict_ml(message)
    # If ML trained, combine 50/50. If not, use Rule only.
    if sum(class_counts.values()) > 0:
        final = int(rule_score * 0.5 + ml_score * 0.5)
    else:
        final = rule_score
        reasons.append("ML not trained - add messages.csv")
    if final >= 70: verdict = "🔴 HIGH RISK - LIKELY SCAM"
    elif final >= 40: verdict = "🟡 MEDIUM RISK - SUSPICIOUS"
    else: verdict = "🟢 LIKELY SAFE"
    return rule_score, ml_score, final, verdict, reasons

def show_result(message, sender):
    rule_score, ml_score, final, verdict, reasons = analyze(message, sender)
    print("\n" + "="*60)
    print(f"FROM: {sender}")
    print(f"MESSAGE: {message}")
    print(f"RULE: {rule_score} | ML: {ml_score} | FINAL: {final}/100")
    print(f"RESULT: {verdict}")
    print("WHY:")
    if not reasons: print("- No scam patterns found, but stay alert.")
    for r in reasons: print(f"- {r}")
    print("="*60 + "\n")

# ---------- MAIN ----------
if __name__ == "__main__":
    data = load_data()
    if data:
        train_ml(data)
        print(f"ML Trained on {len(data)} messages ✅")
    else:
        print("ML not trained - messages.csv not found ❌")

    print("KENYAN SMS PHISHING DETECTOR - FINAL VERSION")
    print("1 = Test examples | 2 = Evaluate for report | 4 = Test your own SMS")
    choice = input("Choose 1/2/4: ").strip()

    if choice == "1":
        tests = [
            ("Your M-PESA account has been deactivated. Send your PIN to unlock", "0707123456"),
            ("You have received Ksh 1000 from JOHN DOE", "M-PESA"),
            ("Congratulations you have won Ksh 50000 send Ksh 500 to claim", "0700111222"),
        ]
        for m, s in tests: show_result(m, s)
    elif choice == "2":
        if not data: print("No data to evaluate")
        else:
            correct = 0
            for m, label in data:
                _, _, final, _, _ = analyze(m, "test")
                pred = 1 if final >= 50 else 0
                if pred == label: correct += 1
            acc = correct / len(data) * 100
            print(f"\n✅ EVALUATION FOR REPORT:")
            print(f"Total messages: {len(data)}")
            print(f"Correct: {correct}")
            print(f"Accuracy: {acc:.1f}%")
            print(f"Use this in your report: Rule Engine + Naive Bayes, Accuracy = {acc:.1f}%")
    elif choice == "4":
        sms = input("Paste SMS: ").strip()
        sender = input("Sender: ").strip() or "Unknown"
        show_result(sms, sender)
    else:
        print("Choose 1, 2 or 4")