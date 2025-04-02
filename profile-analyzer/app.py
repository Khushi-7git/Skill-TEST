from flask import Flask , render_template ,request ,redirect,url_for,jsonify
from ai_model import analyze_profile
import sqlite3
app=Flask(__name__)
@app.route('/analyze',method=['POST']) # analyze as a endpoint
def analyze():
    data=request.json
    profile_text=data.get("profile_text")
    if not profile_text:
        return jsonify({"error":" no profile etxt provided"}),400
    result=analyze_profile(profile_text)
    return jsonify(result)
if __name__=='_main_':
    app.run(debug=True)

