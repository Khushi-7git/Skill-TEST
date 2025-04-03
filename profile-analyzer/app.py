from flask import Flask , render_template ,request ,redirect,url_for,jsonify
from ai_model import analyze_profile
import requests
import os
import sqlite3
app=Flask(__name__,)
DB_PATH = os.path.join("database", "profiles.db")

#fetch github  
@app.route('/github/<username>', methods=['GET'])
def get_github_pro(username):
    github_api_url= f"https://api.github.com/users/{username}"
    github_token= "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"
    header={"Authorization":"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"}
    response=requests.get(github_api_url,headers=header)
    if response.status_code!=200:
        return jsonify({"error":"github user not found or reached api limits"}),404
    user_data=response.json()
    profile_data={
        "user_name":user_data.get("login"),
        "name":user_data.get("name"),
        "bio":user_data.get("bio"),
        "public_repos": user_data.get("public_repos"),
        "followers": user_data.get("followers"),
        "following": user_data.get("following"),
        "profile_url": user_data.get("html_url"),
        "avatar_url": user_data.get("avatar_url"),

    }
    return jsonify(profile_data)

# Connect to Database
def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

#homepage
@app.route('/')
def home():
    return render_template('home.html')

#dispaly connect
@app.route('/dispaly')
def display():
    return render_template('display.html')

@app.route('/analyze', methods=['POST'])  
 # analyze as a endpoint
def analyze():
    data=request.json
    profile_text=data.get("profile_text")
    if not profile_text:
        return jsonify({"error":" no profile text provided"}),400
    result=analyze_profile(profile_text)
    return jsonify(result)
if __name__== '__main__':
    app.run(debug=True)

