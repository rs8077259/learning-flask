from flask import Flask,request,render_template

app=Flask(__name__)

@app.route('/')
def index():
    return "restarting python"
@app.route("/user/<name>")
def user(name):
    return render_template("great.html",name=name,lis=[1,2,3,4,54,5,6,6,343,7,7,7,43])
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"),404
@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"),500
