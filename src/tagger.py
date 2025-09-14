# src/tagger.py
def tag_email(subject, body):
    text = (subject + " " + body).lower()
    if any(word in text for word in ["enquiry", "product", "pricing"]):
        return "Business Lead"
    elif any(word in text for word in ["report", "status", "update"]):
        return "Reporting"
    else:
        return "General"
