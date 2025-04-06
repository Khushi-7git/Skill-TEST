import hashlib
from flask import Flask , render_template ,request ,session,redirect,url_for,jsonify
from ai_model import analyze_profile
from database import get_db_connection
import requests
import os
import sqlite3
from dotenv import load_dotenv
load_dotenv()

app=Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FOLDER = os.path.join(BASE_DIR, "database")
os.makedirs(DB_FOLDER, exist_ok=True)  
DB_PATH = os.path.join(DB_FOLDER, "profiles.db")

# Connect to Database
def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn
#fetch github  
@app.route('/github/<username>', methods=['GET'])
def get_github_pro(username):
    github_api_url= f"https://api.github.com/users/{username}"
    github_token = os.getenv("GITHUB_TOKEN")
    header = {"Authorization": f"token {github_token}"}
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



#homepage
@app.route('/home')
def home():
    return render_template('home.html')

#dispaly connect
@app.route('/dispaly')
def display():
    return render_template('display.html')

@app.route('/analyze', methods=['POST'])  
def analyze():
    data=request.json
    profile_text=data.get("profile_text")
    if not profile_text:
        return jsonify({"error":" no profile founded"}),400
    result=analyze_profile(profile_text)
    return jsonify(result)

#start page 
@app.route('/')
def start():
    username=session.get('username',None)
    return render_template('start.html',username=session.get('username'))
#login page 
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']

        conn = get_db_connection()
        cursor = conn.cursor()

        if role == 'developer':
            cursor.execute("SELECT * FROM developers WHERE username=? AND password=?", (username, password))
        elif role == 'recruiter':
            cursor.execute("SELECT * FROM recruiters WHERE username=? AND password=?", (username, password))

        user = cursor.fetchone()
        conn.close()

        if user:
            session['username'] = username
            session['role'] = role
            if role == 'developer':
                return redirect(url_for('developer_dashboard'))
            elif role == 'recruiter':
                return redirect(url_for('home'))
        else:
            return render_template('login.html', error="Invalid credentials")
    return render_template('login.html',username=session.get('username'))
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
    return redirect(url_for('start'))

# User Registration Route (Signup)
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']

        conn = get_db_connection()
        cursor = conn.cursor()

        if role == 'developer':
            cursor.execute("INSERT INTO developers (username, password) VALUES (?, ?)", (username, password))
        elif role == 'recruiter':
            cursor.execute("INSERT INTO recruiters (username, password) VALUES (?, ?)", (username, password))

        conn.commit()
        conn.close()

        return redirect(url_for('login'))

    return render_template('register.html',username=session.get('username'))
# dashboard of recruiter
@app.route('/recruiter_dashboard')
def recruiter_dashboard():
    if 'role' in session and session['role'] == 'recruiter':
        return render_template('recruiter_dashboard.html')
    return redirect(url_for('login'))

@app.route('/developer_dashboard')
def developer_dashboard():
    if 'role' in session and session['role'] == 'Developer':
        return render_template('display.html', username=session['username'])
    return redirect(url_for('login'))


if __name__== '__main__':
    app.run(debug=True)

