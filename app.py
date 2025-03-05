from sqlalchemy import or_
from flask import Flask, render_template, request, redirect, url_for, flash, session
from Models.model import *
from sqlalchemy.exc import IntegrityError
from datetime import datetime


app = Flask(__name__)
app.config['SECRET_KEY'] = 'East'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gs_store.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_SILENCE_UBER_WARNING'] = 1

db.init_app(app)



with app.app_context():
    db.create_all()


@app.route('/', methods=['GET'])
def home():
    return redirect(url_for('logout'))

@app.route('/signup',methods=['GET',"POST"])
def signup():
    if request.method == "POST":
        username=request.form['username']
        email=request.form['email']
        password=request.form['password']
        admin=False
        
        if request.form.get('admin_key')=="Asharma":
            admin=True
            
            
        try:
            user=User(username=username,email=email,password=password,admin=admin)
            db.session.add(user)
            db.session.commit()
            flash('Your account is created successfully',"success")
            return redirect(url_for('login'))
        
        except IntegrityError:
            db.session.rollback()
            flash('Username or email already existed, Please change')
            return redirect(url_for('signup'))
        
        
    return render_template('signup.html')        
        
        
@app.route('/login',methods=["GET","POST"])
def login():
    if request.method =="POST":
        username_or_email=request.form['username']
        password=request.form['password']
        
        user=User.query.filter(
            or_(User.username==username_or_email,User.email==username_or_email)).first()
        
        if user and user.password==password:
            session['user_id']=user.id
            return redirect(f'/dashboard/{user.id}')
        
        else:
            error_msg='Invalid Username or Password'
            if not user:
                error_msg="No user found"
                return render_template('login.html',error_msg)
            
    return render_template('login.html')        
    
    
 
 
    
    
    
    
    
    
        


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))



if __name__=="__main__":
    app.run(port=5000,debug=True)

