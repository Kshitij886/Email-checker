import tldextract
import whois 
from datetime import datetime
import re 

def check_phishing(links):
    results = {}
    for link in links: 
        score = 0
        score += check_symbols(link)
        score += check_domain(link)
        score += regex_match(link)
        if score > 20:
            print(f"Phishing link {link}, score = {score}")
        elif score > 15:
            print(f"Likely phishing {link}, score = {score}")
        else:
            print(f"Link is secure: {link}, score = {score}")
        results[link] = score
    return results

def check_symbols(link: str) -> int:
    score = 0
    if len(link) > 75:
        score += 2
    suspicious_symbols = {
        "@": 5,
        "-": 3,
        ".": 3,
        "_": 3,
        "%": 3,
        "#": 3,
        "&": 3,
        "*": 3,
        "(": 3,
        ")": 3,
        "!": 3,
        "$": 3,
        "~": 3,
        "`": 3
    }
    for symbol, weight in suspicious_symbols.items():
        count = link.count(symbol)
        if symbol in [".", "-"] and count > 3:
            score += weight
        elif count > 2:
            score += weight
    if link.startswith("http:"):
        score += 5
    return score

def check_domain(link):
    points = 0
    extracted_link = tldextract.extract(link)
    domain = extracted_link.registered_domain
    try:
        domain_info = whois.whois(domain)
        if domain_info.creation_date:
            if isinstance(domain_info.creation_date, list):
                creation_date = domain_info.creation_date[0]
            else:
                creation_date = domain_info.creation_date
            domain_age = datetime.now() - creation_date
            if domain_age.days < 30: 
                points += 6
            elif 30 <= domain_age.days < 90:
                points += 4
    except Exception as e:
        # If WHOIS fails, add points for suspicious domain
        points += 6
    return points

def regex_match(link):
    points = 0
    regexes = [
        r"https?:\/\/[^\s]*\.(?:tk|ml|ga|cf|gq|zip|xyz|top|work|click|fit|loan|men|party|review|stream|trade|download)(?:\/[^\s]*)?",
        r"https?:\/\/(?:[a-z0-9-]+\.){3,}[a-z]{2,}(?:\/[^\s]*)?",
        r"https?:\/\/[^\s]*@[^\/\s]?",
        r"https?:\/\/[^\s]*(?:login|secure|account|update|verify|banking|confirm|password|bank)[^\s]*"
    ]
    for rgx in regexes:
        if re.search(rgx, link):
            points += 6

    if re.search(r"https?:\/\/(?:\d{1,3}\.){3}\d{1,3}(?:\/[^\s]*)?", link):
        points += 8
    return points

check_phishing([
    "https://www.google.com/search?q=openai",
    "https://www.bankofamerica.com/secure-login",
    "http://paypal.verify-account.security-check.tk/login",
    "https://192.168.1.50/secure-login",
    "https://secure-login.paypal.com.account.verify-update.ru/confirm"
])