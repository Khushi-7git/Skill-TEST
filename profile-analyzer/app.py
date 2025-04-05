import hashlib
from flask import Flask , render_template ,request ,session,redirect,url_for,jsonify
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
@app.route('/home')
def home():
    return render_template('home.html')

#dispaly connect
@app.route('/dispaly')
def display():
    return render_template('display.html')

@app.route('/analyze', methods=['POST'])  

#start page 
@app.route('/')
def start():
    username=session.get('username',None)
    return render_template('start.html',username=username)
#login page 
@app.route('/login',method=['GET','POST'])
def login():
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']
        hashed_password=hashlib.sha256(password.encode()).hexdigest()
        user=sqlite3.Cursor.fetchone()
        if user:
            session['username']=username
            return redirect(url_for('home'))
        else:
           return "Invalid username or password"
    return render_template('login.html')

 # Guest Login Route 
@app.route('/guest')
def guest():
    # Redirect guest users directly to the home page
    session['username'] = 'Guest'
    return redirect(url_for('home'))

# Logout Route
@app.route('/logout')
def logout():
    session.pop('username', None)  # Remove the username from the session
    return redirect(url_for('home'))

# User Registration Route (Signup)
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        
        # Hash the password before saving it (security best practice)
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        with sqlite3.connect('db.sqlite') as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO users (email, username, password) VALUES (?, ?, ?)",
                               (email, username, hashed_password))
                conn.commit()
                return redirect(url_for('login'))  # After registration, redirect to login
            except sqlite3.IntegrityError:
                return "Email or Username already exists"
    return render_template('register.html')
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

