from flask import Flask, Request, jsonify
from flask_cors import CORS
import phishing 
import texts
import malware


app = Flask(__name__)
CORS(app)

@app.route("/api/check_email", methods = ["POST"])
def check_email():
        data = Request.get_json()
        if data.attachment:
                malware_result = malware.check_malware(data.attachment)
        if data.url:
                phishing_result = phishing.check_phishing(data.url);
        
        if malware_result == True:
                texts_result = texts.check_text(data.body, "malware")
        else :
                texts_result = texts.check_text(data.body)

        if malware_result.status == True and phishing_result.status == True:
                result = {
                        "malware ": True,
                        "phishing": True,
                        "file" : malware_result.file_path,
                        "urls" : phishing_result.urls,
                        "Suspicious words" : texts_result.words
                }
                return jsonify({result})
        
        elif malware_result.status == True and phishing_result.status == False:
                result = {
                        "malware ": True,
                        "phishing": False,
                        "file" : malware_result.file_path,
                        "Suspicious words" : texts_result.words
                }
                return jsonify({result})
        elif phishing_result.status == True:
                result = {
                        "phishing": True,
                        "malware" : False,
                        "urls" : phishing_result.urls,
                        "suspicious words" : texts_result.words
                }
                return jsonify({result})
        else :
                result = {
                        "phishing": False,
                        "malware": False,
                        "email" : "safe"
                }
                return jsonify({result})

if __name__ == "__main__":
        app.run(debug = True)