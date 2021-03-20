from app import app
from flask import render_template, redirect, request, url_for




#---------------------------- Manage routes -----------------------------------

@app.route("/")
def home():

    return render_template("home.html")

    
