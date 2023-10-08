from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session

class Parking:
    db_name = 'parking_jets'

    def __init__( self , data ):
        self.id = data['id']
        self.location = data['location']
        self.is_occupied = data['is_occupied']
        self.capacity = data['capacity']
        self.tariff = data['tariff']

    @classmethod
    def save(cls, data):
        query = "INSERT INTO parkings (location, is_occupied, capacity, tariff) VALUES ( %(location)s, '0', %(capacity)s, %(tariff)s );"
        return connectToMySQL(cls.db_name).query_db(query, data)  

    @classmethod
    def get_parking_by_id(cls, data):
        query = "SELECT * FROM parkings WHERE parkings.id = %(parking_id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if results:
            return results[0]
        return False

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM parkings WHERE parkings.is_occupied = 0;"
        results = connectToMySQL(cls.db_name).query_db(query)
        parkings = []
        if results:
            for parking in results:
                parkings.append(parking)
            return parkings
        return parkings

    @classmethod
    def get_user_parkings(cls, data):
        query = "SELECT parkings.*, private_jets.model as model, private_jets.id as pj_id, users.id as user_id, reserved.* FROM users JOIN private_jets ON private_jets.user_id = users.id JOIN reserved ON reserved.private_jet_id = private_jets.id JOIN parkings ON reserved.parking_id  = parkings.id WHERE users.id=%(user_id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        parkings = []
        if results:
            for parking in results:
                parkings.append(parking)
            return parkings
        return parkings

    @classmethod
    def update(cls, data):
        query = "UPDATE parkings SET location = %(location)s, capacity = %(capacity)s, tariff = %(tariff)s, WHERE parkings.id = %(parking_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)  

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM parkings WHERE parkings.id = %(parking_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @staticmethod
    def validate_workout(workout):
        is_valid = True
        
        if len(workout['title']) <= 0:
            flash('Workout Title should not be empty!', 'titleWorkout')
            is_valid= False
        if len(workout['age']) <= 0:
            flash('Invalid Age', 'ageWorkout')
            is_valid= False
        if len(workout['weight']) <= 0:
            flash('Invalid Weight', 'weightWorkout')
            is_valid= False
        if len(workout['height']) <= 0:
            flash('Invalid Height', 'heightWorkout')
            is_valid= False
        if len(workout['gender']) <= 0:
            flash('Workout Gender should not be empty!', 'genderWorkout')
            is_valid= False
        if len(workout['medical_history']) <= 0:
            flash('Medical History should not be empty!', 'medicalHistoryWorkout')
            is_valid= False
        if len(workout['fitness_level']) <= 0:
            flash('Fitness Level should not be empty!', 'fitnessLevelWorkout')
            is_valid= False
        if len(workout['goal']) <= 0:
            flash('Workout Goal should not be empty!', 'goalWorkout')
            is_valid= False
        if len(workout['time_commitment']) <= 0:
            flash('Time Commitment should not be empty!', 'timeCommitmentWorkout')
            is_valid= False        
        if len(workout['equipment']) <= 0:
            flash('Workout Equipment should not be empty!', 'equipmentWorkout')
            is_valid= False     
        return is_valid