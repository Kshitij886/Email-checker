import tldextract
import whois
from datetime import datetime
import re

def check_phishing(links):
    results = {}
    for link in links[0]:
        extracted_link = tldextract.extract(link)
        domain = extracted_link.top_domain_under_public_suffix
        score = 0
        score += check_symbols(link)
        score += check_domain(domain)
        score += regex_match(link)
        score += check_subdomains(link)
        score += check_path_tricks(link)
        score += check_TLD(domain)

        probability = min(int((score / 60) * 100), 100)
        results[link] = probability
    status = False
    for url, prob in results.items():
        if prob > 60:
            status = True
            break
    print(results)
    return {
        "status" : status,
        "urls": results
    }
    
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
    elif not link.startswith("https:"):
        score += 10
    return score


def check_domain(domain):
    points = 0
    if len(domain) > 15 :
       points += len(domain) - 9
    elif len(domain) < 5:
        points += 11 - len(domain) 
    
    count = len(domain.split('-'))
    if count >= 3 :
       points += count + 2
    elif 2 <= count < 3:
       points += 5
    try:
        domain_info = whois.whois(domain)
        if domain_info.creation_date:
            if isinstance(domain_info.creation_date, list):
                creation_date = domain_info.creation_date[0]
            else:
                creation_date = domain_info.creation_date
            domain_age = datetime.now() - creation_date
            if domain_age.days < 20:
                points += domain_age.days + 12
            elif domain_age.days < 30:
                points += 8
            elif 30 <= domain_age.days < 90:
                points += 4
    except Exception:
        points += 8
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
        if sub_count >= 9:
            score += sub_count
        elif sub_count >= 3:
            score += 6

        if any(word in subdomain.lower() for word in ["login", "secure", "update", "verify", "paypal", "account"]):
            score += 6
    return score


def check_path_tricks(link):
    score = 0
    extensions = {
        ".html": 8,
        ".htm" : 8,
        ".php": 8,
        ".js": 8,
        ".aspx": 5,
        ".asp": 5,
    }
    for ext, weight in extensions.items():
        if(link.endswith(ext)):
            score += weight
    path_match = re.search(r"https?:\/\/[^\/]+(\/[^\s]*)", link)
    if path_match:
        path = path_match.group(1)
        if len(path) > 65:
            score += len(path) - 61
        elif len(path) > 50:
            score += 4
        if any(word in path.lower() for word in ["confirm", "update", "verify", "secure", "signin", "banking", "password", "login"]):
            score += 5
        if path.count("/") > 6:
            score += path.count('/') -1
        
            score += 5

    return score

def check_TLD(domain):
    score = 0
    TDL = {
        ".com":1,
        ".org":1,
        ".app": 4,
        ".info":8,
        ".top":	9,
        ".xyz":	8,
        ".ru ": 9,
        ".cn ":	8,
        ".php": 7
    }
    for tld, weight in TDL.items():
        if domain.endswith(tld):
            score += weight
        if domain.count(tld) > 1:
            score += 6 * domain.count(tld)
        elif tld in domain and not domain.endswith(tld):
            score += weight
        
        
    numbers = len(re.findall(r'\d', domain))
    if 1 <= numbers <= 2:
        score += 4
    elif 3 <= numbers <= 4:
        score += 7
    else:  # >4
        score += 10
    return score