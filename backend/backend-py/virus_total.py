import requests
import hash_db

def virusTotal (file_hash):
    VT_API_KEY = "30e7264c1b380d692a785e777adf58f525c3dfdc99a5553301a354831f1c3a2e"  
    file_hash = "178ba564b39bd07577e974a9b677dfd86ffa1f1d0299dfd958eb883c5ef6c3e1"  
    url = f"https://www.virustotal.com/api/v3/files/{file_hash}"

    headers = {
        "x-apikey": VT_API_KEY
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        stats = data.get("data", {}).get("attributes", {}).get("last_analysis_stats", {})
        malicious_count = stats.get("malicious", 0)
        print(stats)
    
        if malicious_count > 0:
            hash_db.content_array.append(file_hash)
            return 10
        else:
           return 0
    else:
       return 0

