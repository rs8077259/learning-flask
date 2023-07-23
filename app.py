from flask import Flask,request,render_template,redirect,url_for,abort,session,flash,jsonify
from form import *
import os
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail,Message
from threading import Thread
app=Flask(__name__)
app.config["SECRET_KEY"]="dihdhdkshdkhskjdhksjhdjks"#os.environ.get("SECRETKEY")
app.config["SQLALCHEMY_DATABASE_URI"]=os.environ.get("POSTGRESQL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['MAIL_SERVER']='smtp.googlemail.com'
app.config['MAIL_PORT']=587
app.config['MAIL_USE_TLS']=True
app.config['MAIL_USERNAME']=os.environ.get('MAILUSERNAME')
app.config['MAIL_PASSWORD']=os.environ.get('MAILPASSWORD')
db=SQLAlchemy(app)
mail=Mail(app)

class User(db.Model):
    __tablename__='user'
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(64))
    email=db.Column(db.String(74),unique=True,nullable=False)
    password=db.Column(db.String(100),nullable=False)

    def __repr__(self):
        return "%s,%s,%s"%(self.name,self.email,self.password)
    def has_email(self,uemail):
        if not (self.query.filter_by(email=uemail).first()):
            return False
        return True
    def check(self):
        if not (self.query.filter_by(email=self.email,password=self.password).first()):
            return False
        return True
@app.route('/')
def index():
    return render_template("home.html")
@app.route("/user/profile/<name>")
def user(name):
    return render_template("great.html",name=name,lis=[1,2,3,4,54,5,6,6,343,7,7,7,43])
@app.route("/user/feedback/<error_>")
def feedback(error_):
    feed=FeedBack()
    return render_template("feedback.html",form=feed,error=error_)
@app.route("/user/signup",methods=["POST","GET"])
def sign_up():
    signup=SignUp()
    if request.method=="POST":
        if signup.validate_on_submit():
            user=User()
            if not(user.has_email(signup.email.data)):
                username=signup.email.data[:(signup.email.data).find("@")]
                user=User(name=username,email=signup.email.data,password=signup.password.data)
                db.session.add(user)
                #db.session.commit()
                session["Username"]=username
                msg=Message('noreply',sender=app.config['MAIL_USERNAME'],recipients=[signup.email.data])
                msg.body="your are registered succesfully to website"
                msg.html="<h3>%s</h3>"%username
                #mail.send(msg)
                flash("Registered Successfully")
                return redirect(url_for('user',name=username))
            else:
                flash("provided email account alredy Exist")
    return render_template("signup.html",form=signup)

"""

def send_async_mail(app,msg):
    with app.app_context():
        mail.send(msg)

def send_mail(to,subject,template,**kwergs):
    msg=Message(subject,sender=app.config['MAIL_USERNAME'],recipients=[to])
    msg.html=render_template(template+".html",**kwergs)
    thr=Thread(target=send_async_mail,args=[app,msg])
    thr.start()
    return thr """
@app.route('/user/signin',methods=['POST',"GET"])
def sign_in():
    if request.method=='POST':
        try:
            data=request.get_json()
            print(data)
        except Exception as E:
            print(E)
            error_response={
                'status':'error'
            }
            return error_response
        auth=User()
        auth.email=data['email']
        auth.password=data['password']
        response_data={"message":auth.check(),'url':url_for('sign_up',_external=True)}
        return jsonify(response_data)
    else: 
        signin=SignIN()
        return render_template('signin.html',form=signin)

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"),404
@app.errorhandler(500)
def Internal_Server_Error(e):
    return render_template("500.html"),500
    
