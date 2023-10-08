from flask_app import app
from flask_app.models.user import User
from flask_app.models.parking import Parking
from flask_app.models.pj import PrivateJet
from flask_app.models.reserved import Reserved

from flask import render_template, redirect, session, request, flash, jsonify
import os
import random
import string
from datetime import datetime
from .env import UPLOAD_FOLDER
from .env import ALLOWED_EXTENSIONS
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
from flask_cors import CORS
CORS(app)
from werkzeug.utils import secure_filename

@app.route('/locations')
def locations():
    if 'user_id' not in session:
        return redirect('/')
    
    locations=Parking.get_all()
    return render_template('locations.html', locations=locations)


@app.route('/reserve/<int:id>')
def reserveP(id):
    if 'user_id' in session:
        data1 = {
            'user_id': session['user_id'],
            'parking_id': id
        }
        parking = Parking.get_parking_by_id(data1)
        myJets = PrivateJet.get_all(data1)

        return render_template('reserve.html', parking = parking, myJets = myJets)
    return redirect('/')



@app.route('/create/reservation', methods = ['POST'])
def createReservation():
    if 'user_id' in session:
        
        data1 = {
            'user_id': session['user_id'],
            'private_jet_id': request.form['private_jet_id']
        }
        
        loggedUser = User.get_user_by_id(data1)
        jet = PrivateJet.get_private_jet_by_id(data1)

        if loggedUser['id'] == jet['user_id']:
            data = {
                
                    'notes': request.form['notes'],
                    'check_in': request.form.get('check_in', ''),
                    'check_out': request.form.get('check_out', ''),
                    'private_jet_id': request.form['private_jet_id'],
                    'space': request.form.get('space', ''),
                    'parking_id': request.form['parking_id']
                }
            if not Reserved.validate_reservation(data):
                return redirect(request.referrer)
            
            check_in = request.form.get('check_in')
            check_out = request.form.get('check_out')
            
            #print(check_in)
            #print(check_out)
            #print(check_out < check_in)
            if check_out < check_in:
                flash('Please check the dates. Check out should be after the check in.', 'checkError')
                return redirect(request.referrer)

            check = Reserved.check_reservation(data)
            print(check['count'])
            if check['count'] != 0:
                flash('Please chose another parking space. This space is not available.', 'notAvailable')
                return redirect(request.referrer)


            #print(data)
            Reserved.save(data)
            return redirect('/')
        return redirect('/')
    return redirect('/')

@app.route('/policy')
def policy():
    return render_template('policy.html')

@app.route('/payment')
def payment():
    return render_template('payment.html')