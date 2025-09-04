from flask import Flask, request, jsonify
from flask_cors import CORS
import phishing 
import texts
import malware


app = Flask(__name__)
CORS(app)

@app.route("/api/check_email", methods = ["POST"])
def check_email():
        data = request.get_json()
        malware_result = None
        phishing_result = None
        if "attachment" in data and data["attachment"] is not None:
                malware_result = malware.check_malware(data['attachment'])
        if 'url' in data and data['url'] != []:
                phishing_result = phishing.check_phishing(data['url'])
        
        if  malware_result is not None:
                texts_result = texts.check_text(data['body'], "malware")
        else :
                texts_result = texts.check_text(data['body'])

        if malware_result is not None and phishing_result is not None:
                result = {
                        "malware ": True,
                        "phishing": True,
                        "file" : malware_result['file'],
                        "urls" : phishing_result['urls'],
                        "Suspicious words" : texts_result['words']
                }
                return jsonify(result)
        
        elif malware_result is not None and phishing_result is None:
                result = {
                        "malware ": True,
                        "phishing": False,
                        "file" : malware_result['file'],
                        "Suspicious words" : texts_result['words']
                }
                return jsonify(result)
        elif phishing_result is not None :
                result = {
                        "phishing": True,
                        "malware" : False,
                        "urls" : phishing_result['urls'],
                        "suspicious words" : texts_result['words']
                }
                return jsonify(result)
        else:
                result = {
                        "phishing": False,
                        "malware": False,
                        "email" : "safe"
                }
                return jsonify(result)

if __name__ == "__main__":
        app.run(debug = True)