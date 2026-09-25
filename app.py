import os 
from flask import Flask, render_template, request, redirect, session 
from dotenv import load_dotenv
from database import create_tables, create_user, verify_user, add_material, get_all_materials 
from cloud_storage import upload_file

load_dotenv() 

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")

def is_logged_in():
    return "user_id" in session

@app.route("/whoami")
def whoami():
    if "user_id" in session:
        return f"Logged in as: {session['user_name']} (ID: {session['user_id']})"
    else:
        return "Not logged in"

@app.route("/")
def home():
    create_tables()
    materials = get_all_materials()
    return render_template("home.html", materials=materials)

@app.route("/signup", methods = ["GET", "POST"])
def signup_page():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"] 
        password = request.form["password"]
        department = request.form["department"] 
        year = int(request.form["year"])

        success = create_user(email, password, name, department, year)

        if success:
            return "Signup completed! <a href='/login'>Log in</a>"
        else:
            return "Email already registered. <a href='/signup'>Try again</a>"
        

    return render_template("signup.html")   

@app.route("/login", methods=["GET", "POST"])
def login_page():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        
        user = verify_user(email, password)
        
        if user:
            session["user_id"] = user[0]
            session["user_name"] = user[3]
            return "Login successful! <a href='/'>Go home</a>"
        else:
            return "Invalid email or password. <a href='/login'>Try again</a>"
    
    return render_template("login.html") 

@app.route("/upload", methods=["GET", "POST"])
def upload_page():
    if not is_logged_in():
        return redirect("/login")
    
    if request.method == "POST":
        title = request.form["title"]
        course = request.form["course"]
        file = request.files["file"]
        
        file_url = upload_file(file)
        add_material(title, course, file_url, session["user_id"])
        
        return "Material uploaded! <a href='/'>Go home</a>"
    
    return render_template("upload.html")

@app.route("/logout")
def logout():
    session.clear()
    return "Logged out! <a href='/'>Go home</a>"
        
if __name__ == "__main__":
    app.run(debug=True)
