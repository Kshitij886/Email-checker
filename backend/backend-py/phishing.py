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
        score += check_subdomains(link)
        score += check_path_tricks(link)

        probability = min(int((score / 50) * 100), 100)

        if probability >= 60:
            print(f" Phishing link: {link}\n   Phishing Probability: {probability}%\n")
        elif probability >= 50:
            print(f" Suspicious link: {link}\n   Phishing Probability: {probability}%\n")
        else:
            print(f" Safe link: {link}\n   Phishing Probability: {probability}%\n")

        results[link] = probability
    return results


def check_symbols(link: str) -> int:
    score = 0
    if len(link) > 75:
        score += 2
    suspicious_symbols = {
        "@": 6, "-": 3, ".": 3, "_": 3, "%": 3, "#": 3, "&": 3,
        "*": 3, "(": 3, ")": 3, "!": 3, "$": 3, "~": 3, "`": 3,
        "=": 2, "+": 2, ";": 2, ":": 2
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
    except Exception:
        points += 6
    return points


def regex_match(link):
    points = 0
    regexes = [
        r"https?:\/\/[^\s]*\.(?:tk|ml|ga|cf|gq|zip|xyz|top|work|click|fit|loan|men|party|review|stream|trade|download)(?:\/[^\s]*)?",
        r"https?:\/\/(?:[a-z0-9-]+\.){3,}[a-z]{2,}(?:\/[^\s]*)?",
        r"https?:\/\/[^\s]*@[^\/\s]?",
        r"https?:\/\/[^\s]*(?:login|secure|account|update|verify|banking|confirm|password|signin|support|wallet)[^\s]*",
        r"https?:\/\/[^\s]*:[0-9]{2,5}\/"
    ]
    for rgx in regexes:
        if re.search(rgx, link, re.IGNORECASE):
            points += 6

    if re.search(r"https?:\/\/(?:\d{1,3}\.){3}\d{1,3}(?:\/[^\s]*)?", link):
        points += 8
    return points


def check_subdomains(link):
    score = 0
    extracted = tldextract.extract(link)
    subdomain = extracted.subdomain
    if subdomain:
        sub_count = len(subdomain.split("."))
        if sub_count >= 3:
            score += 6
        if any(word in subdomain.lower() for word in ["login", "secure", "update", "verify", "paypal", "account"]):
            score += 6
    return score


def check_path_tricks(link):
    score = 0
    path_match = re.search(r"https?:\/\/[^\/]+(\/[^\s]*)", link)
    if path_match:
        path = path_match.group(1)
        if len(path) > 50:
            score += 4
        if any(word in path.lower() for word in ["confirm", "update", "verify", "secure", "signin", "banking", "password", "login"]):
            score += 5
        if path.count("/") > 5:
            score += 4
    return score


# Test
check_phishing([
    "https://nouvellelivraison-retrait-locker.com/",
    "https://nouvellelivraison-retrait-locker.com/pages/index.php...",
    "https://bauerhockey.top/",
    "http://bauerhockey.top",
    "https://straightforward-darling-532744.framer.app/...",
    "https://commerz-dienstleistungen.com/cmr/",
    ""
])