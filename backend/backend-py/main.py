from flask import Flask, Request, jsonify
from flask_cors import CORS
import malware
import phishing 
import texts


app = Flask(__name__)
CORS(app)

@app.route("/api/check_email", methods = ["POST"])
def check_email():
        data = Request.get_json()
        malware_result = malware.check_malware(data['files']);
        phishing_result = phishing.check_phishing(data['links']);
        if malware_result == True :
                texts_result = texts.check_text(data['body'], "malware")
        else :
                texts_result = texts.check_text(data['body'])
        
        average = (malware_result + phishing_result + texts_result) / 3
        if( average  >= 5) :
                return jsonify({"result": "malicious"})
        return jsonify({"result": "safe"})

if __name__ == "__main__":
        app.run(debug = True)