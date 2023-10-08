from flask_app import app
import os
from flask_app.controllers.qr import qrgen
from flask_app.models.user import User
from flask_app.models.parking import Parking
from flask_app.models.pj import PrivateJet
from flask_app.models.reserved import Reserved
from flask import render_template, send_file, redirect, session, request, flash
from builtins import zip
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


project_directory = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # Go up one level from the flask_app directory

@app.errorhandler(404) 
def invalid_route(e): 
    return render_template('404.html')

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect('/dashboard')
    return render_template('index.html')

@app.route('/login.html')
def login_html():
    return render_template('login.html')

@app.route('/register', methods = ['POST'])
def register():
    if 'user_id' in session:
        return redirect('/')
    if User.get_user_by_email(request.form):
        flash('This email already exists', 'emailRegister')
        return redirect(request.referrer)
    if not User.validate_user(request.form):
        flash('You have some errors! Fix them to sign Up', 'registrationFailed')
        return redirect(request.referrer)
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'phone_number': request.form['phone_number'],
        'email': request.form['email'],
        'password': bcrypt.generate_password_hash(request.form['password'])
    }
    User.save(data)
    flash('Successfully registered! You can now login!', 'success')
    return redirect('/login.html')

@app.route('/login', methods = ['POST'])
def login():
    if 'user_id' in session:
        return redirect('/')
    if not User.get_user_by_email(request.form):
        flash('This email doesnt appear to be in our system! Try another one!', 'emailLogin')
        return redirect(request.referrer)
    
    user = User.get_user_by_email(request.form)
    if user:
        if not bcrypt.check_password_hash(user['password'], request.form['password']):
            flash('Wrong Password', 'passwordLogin')
            return redirect(request.referrer)
    
    session['user_id'] = user['id']
    return redirect('/')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'user_id': session['user_id']
    }
    myJets = PrivateJet.get_all(data)
    loggedUser = User.get_user_by_id(data)
    myParkings = Parking.get_user_parkings(data)
    costs = []
    for parking in myParkings:
        cost = ((parking['check_out'] - parking['check_in']).days + 1) * parking['tariff']
        costs.append(int(cost))
    print(costs)
    return render_template('dashboard.html', loggedUser=loggedUser, myJets=myJets, myParkings=myParkings, costs=costs)

@app.route('/profile/<int:id>')
def viewProfile(id):
    if 'user_id' in session:
        data = {
            'user_id': session['user_id'],
        }
        myJets = PrivateJet.get_all(data)
        loggedUser = User.get_user_by_id(data)        
        return render_template('profile.html', myJets=myJets, loggedUser = loggedUser)
    return redirect('/')

@app.route('/map')
def map():  
    return render_template('map.html')

@app.route('/QR_Code_Generater')
def home():
    return render_template('index.html')

@app.route('/converted',methods = ['POST'])
def convert():
    global tex
    tex = request.form['test']
    return render_template('converted.html')

@app.route('/download')
def download():
    global tex
    qrgen(tex)
    filename = tex+'.png'
    file_path = os.path.join(project_directory, filename)  # Build the absolute file path
    return send_file(file_path, as_attachment=False,  mimetype='image/png')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')