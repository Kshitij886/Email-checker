phishing_words = [
    "urgent", "immediately", "final warning", "act now", "limited time", "verify now",
    "account suspended", "account locked", "service termination", "penalty", "restricted access",
    "click here", "confirm your identity", "enter password", "provide details", 
    "login below", "update information",
    "payment declined", "verify credit card", "transaction failed", 
    "refund available", "prize", "lottery", "winnings",
    "download file", "open document", "secure link", "access form", "attachment included",
    "dear user", "dear customer", "valued member",
    "threatening", "pushy", "free gift", "winner"
]

malware_words = [
    "download now", "free download", "setup.exe", "install update", "run file",
    "open attachment", "double click", "launch program", "install driver",
    "critical update", "security update required", "system patch", 
    "update available", "urgent software update", "activate software",
    "your computer is infected", "virus detected", "trojan found", 
    "remove spyware", "clean your pc", "security risk", "scan immediately",
    "crack", "keygen", "license key", "unlock full version", 
    "premium access free", "free activation", "download hack tool",
    "zip file", "rar archive", "extract package", "encrypted file", 
    "unlock attachment", "open document securely",
    "act fast", "install immediately", "limited offer", 
    "do not ignore", "execute file now"
]

def check_text(body, text = 'phishing'):
    if text == 'phishing':
        words = check_phishingWords(body)
        result = {
            "words" : words
        }
        return result
    words = check_malwareWords(body)
    result = {
            "words" : words
        }
    return result

def check_phishingWords(content):
    words = []
    for word in phishing_words:
        if word in content:
            words.append(word)

    return words

def check_malwareWords(content):
    words = []
    for word in malware_words:
        if word in content:
            words.append(word)

    return words
