from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class PrivateJet:
    db_name = 'parking_jets'

    def __init__( self , data ):
        self.id = data['id']
        self.fuel_type = data['fuel_type']
        self.model = data['model']
        self.registration_nr = data['registration_nr']
        self.image = data['image']
        self.user_id = data['user_id']

    @classmethod
    def get_private_jet_by_id(cls, data):
        query = "SELECT * FROM private_jets WHERE private_jets.id = %(private_jet_id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if results:
            return results[0]
        return False
    
    @classmethod
    def get_all(cls, data):
        query = "SELECT * FROM private_jets WHERE private_jets.user_id=%(user_id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        private_jets = []
        if results:
            for private_jet in results:
                private_jets.append(private_jet)
            return private_jets
        return private_jets

    @classmethod
    def save(cls, data):
        query = "INSERT INTO private_jets (fuel_type, model, registration_nr, image,  user_id) VALUES ( %(fuel_type)s, %(model)s, %(registration_nr)s, %(image)s, %(user_id)s );"
        return connectToMySQL(cls.db_name).query_db(query, data)   

    @classmethod
    def updateIMG(cls, data):
        query = "UPDATE private_jets SET image = %(image)s WHERE private_jets.id = %(private_jet_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def update(cls, data):
        query = "UPDATE private_jets SET fuel_type = %(fuel_type)s, model = %(model)s, registration_nr = %(registration_nr)s WHERE private_jets.id = %(private_jet_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data) 

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM private_jets WHERE private_jets.id = %(private_jet_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def deleteAllParkings(cls, data):
        query = "DELETE FROM reserved WHERE reserved.private_jet_id = %(private_jet_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @staticmethod
    def validate_jet(jet):
        is_valid = True
        if jet['fuel_type'] == '':
            flash('Fuel type is required.', 'fuelType')
            is_valid = False
        if len(jet['model']) <= 3:
            flash('Model should be more than 3 characters!', 'modelJet')
            is_valid = False
        if len(jet['registration_nr']) < 5:
            flash('Registration number should be at least 5 characters!', 'registrationNr')
            is_valid = False
        return is_valid