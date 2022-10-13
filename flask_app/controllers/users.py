from flask_app.models.user import User
from flask import render_template, redirect, url_for, request, session, flash
from flask_app import app
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)


@app.route('/', methods=['POST', 'GET'])
def main():
    if request.method == 'POST':
        data = {
            "first_name": request.form['fname'],
            "last_name": request.form['lname'],
            "email": request.form['email'],
            "password" : request.form['password']
        } 
        if User.validate_user(data):
            data['password'] = bcrypt.generate_password_hash(data['password'])
            user_id = User.save(data)
            session['user_id'] = user_id
            return redirect("/dashboard")
        else:
            return redirect('/')
    return render_template('main.html')

@app.route('/login', methods=['POST'])
def login():
    data = { "email" : request.form["email"] }
    user_in_db = User.get_by_email(data)
    if not user_in_db:
        flash("Invalid Email/Password")
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid Email/Password")
        return redirect('/')
    session['user_id'] = user_in_db.id
    session['first_name'] = user_in_db.first_name
    return redirect("/dashboard")

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')