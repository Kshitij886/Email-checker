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
        print(data['url'])
        if "attachment" in data and data["attachment"] is not None:
                malware_result = malware.check_malware(data['attachment'])
        if 'url' in data and data['url'] == []:
                phishing_result = phishing.check_phishing(data['url'])

        texts_result = texts.check_text(data['body'])
        if malware_result is not None and phishing_result is not None and phishing_result['status'] != "False" and malware_result['status'] != False:
                result = {
                        "status": True,
                        "malware ": malware_result['status'],
                        "phishing": phishing_result['status'],
                        "file" : malware_result['file'],
                        "urls" : phishing_result['urls'],
                        "malware_type" : malware_result['malware type'],
                        "Suspicious words" : texts_result['words']
                }
                return jsonify(result)
        
        elif malware_result is not None and phishing_result is None and malware_result['status'] !='False' :
                result = {
                        "status": True,
                        "malware ": malware_result['status'],
                        "phishing": False,
                        "file" : malware_result['file'],
                        "malware_type" : malware_result['malware type'],
                        "Suspicious words" : texts_result['words']
                }
                return jsonify(result)
        elif phishing_result is not None and phishing_result['status'] != "False":
                result = {
                        "status": True,
                        "phishing": phishing_result['status'],
                        "malware" : False,
                        "urls" : phishing_result['urls'],
                        "suspicious words" : texts_result['words']
                }
                return jsonify(result)
        else:
                result = {
                        "status": False,
                        "phishing": False,
                        "malware": False,
                        "email" : "safe"
                }
                return jsonify(result)

if __name__ == "__main__":
        app.run(debug = True)