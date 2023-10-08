from flask_app import app
from flask_app.models.user import User
from flask_app.models.parking import Parking
from flask_app.models.pj import PrivateJet
from flask import render_template, redirect, session, request, flash, jsonify
import os
import random
import string
from datetime import datetime
from .env import UPLOAD_FOLDER
from .env import ALLOWED_EXTENSIONS
from flask_cors import CORS
CORS(app)
from werkzeug.utils import secure_filename

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#app.config['MAX_CONTENT_LENGTH'] = 30 * 1024 * 1024 

#Check if the format is right
def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/add/jet')
def addJet():
    if 'user_id' in session:
        data = {
            'user_id': session['user_id'] }
        loggedUser = User.get_user_by_id(data)
        return render_template('newJet.html', loggedUser=loggedUser)
    return redirect('/')


@app.route('/create/jet', methods=['POST'])
def newJet():
    if 'user_id' in session:
        data= {

        }
    
        if not request.files['image']:
            flash('Please upload a jet image!', 'jetImage')
            return redirect(request.referrer)
    
        image = request.files['image'] #image

        if not allowed_file(image.filename):
            flash('Image should be in png, jpeg or jpg format!', 'jetImage')
            return redirect(request.referrer)
        
        if image and allowed_file(image.filename):
            filename1 = secure_filename(image.filename)
            time = datetime.now().strftime('%d%m%Y%S%f')
            filename1 = time + filename1
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename1))

        data = {
            'model': request.form['model'],
            'registration_nr': request.form['registration_nr'],
            'fuel_type': request.form.get('fuel_type', ''),
            'user_id': session['user_id'],
            'image': filename1
        }

        if not PrivateJet.validate_jet(data):
            return redirect(request.referrer)

        print(data)
        PrivateJet.save(data)
        return redirect('/dashboard')
    return redirect('/')

@app.route('/delete/jet/<int:id>')
def deleteJet(id):
    if 'user_id' in session:
        data = {
            'user_id': session['user_id'],
            'private_jet_id': id
        }
        
        loggedUser = User.get_user_by_id(data)
        jet = PrivateJet.get_private_jet_by_id(data)

        if loggedUser['id'] == jet['user_id']:
            PrivateJet.deleteAllParkings(data)
            PrivateJet.delete(data)

            return redirect('/')
        return redirect('/')
    return redirect('/')


@app.route('/edit/jet/<int:id>')
def editJet(id):
    if 'user_id' in session:
        data = {
            'user_id': session['user_id'],
            'private_jet_id': id
        }
        loggedUser = User.get_user_by_id(data)
        jet = PrivateJet.get_private_jet_by_id(data)

        if loggedUser['id'] == jet['user_id']:
            return render_template('editJet.html', loggedUser = loggedUser, jet = jet)
        return redirect('/dashboard')
    return redirect('/')


@app.route('/update/jet/image/<int:id>', methods = ['POST'])
def updateJetIMG(id):
    if 'user_id' in session:
        data1 = {
            'user_id': session['user_id'],
            'private_jet_id': id
        }
        
        loggedUser = User.get_user_by_id(data1)
        jet = PrivateJet.get_private_jet_by_id(data1)

        if loggedUser['id'] == jet['user_id']:

            if not request.files['image']:
                flash('Please upload a Jet image!', 'JetImage')
                return redirect(request.referrer)

            image = request.files['image'] #image

            if not allowed_file(image.filename):
                flash('Image should be in png, jpeg or jpg format!', 'JetImage')
                return redirect(request.referrer)

            if image and allowed_file(image.filename):
                filename1 = secure_filename(image.filename)
                time = datetime.now().strftime('%d%m%Y%S%f')
                filename1 = time + filename1
                image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename1))


            data = {
                    'image': filename1,
                    'private_jet_id': id
                }
            
            PrivateJet.updateIMG(data)
            flash('Update was successfull.', 'JetUpdate')
            return redirect(request.referrer)
        return redirect('/dashboard')
    return redirect('/')


@app.route('/update/jet/<int:id>', methods = ['POST'])
def updateJet(id):
    if 'user_id' in session:
        data1 = {
            'user_id': session['user_id'],
            'private_jet_id': id
        }
        
        loggedUser = User.get_user_by_id(data1)
        jet = PrivateJet.get_private_jet_by_id(data1)

        if loggedUser['id'] == jet['user_id']:
            if not PrivateJet.validate_jet(request.form):
                return redirect(request.referrer)

            data = {
                    'model': request.form['model'],
                    'registration_nr': request.form['registration_nr'],
                    'fuel_type': request.form.get('fuel_type', ''),
                    'private_jet_id': id
                }
            
            PrivateJet.update(data)
            return redirect('/dashboard')
        return redirect('/dashboard')
    return redirect('/')