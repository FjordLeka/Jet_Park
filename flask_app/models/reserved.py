from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
from datetime import datetime


class Reserved:
    db_name = 'parking_jets'

    def __init__( self , data ):
        self.id = data['id']
        self.parking_id = data['parking_id']
        self.private_jet_id = data['private_jet_id']
        self.check_in = data['check_in']
        self.check_out = data['check_out']
        self.is_paid = data['is_paid']
        self.space = data['space']
        self.notes = data['notes']


    #CREATE
    @classmethod
    def save(cls, data):
        query = "INSERT INTO reserved (parking_id, private_jet_id, check_in, check_out, is_paid, space, notes) VALUES ( %(parking_id)s, %(private_jet_id)s, %(check_in)s, %(check_out)s, 0, %(space)s, %(notes)s );"
        return connectToMySQL(cls.db_name).query_db(query, data)   


    @classmethod
    def get_reservation_by_id(cls, data):
        query = "SELECT * FROM reserved WHERE reserved.id = %(reservation_id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if results:
            return results[0]
        return False


    
    @classmethod
    def check_reservation(cls, data):
        query = "SELECT COUNT(*) as count FROM reserved WHERE parking_id = %(parking_id)s AND space = %(space)s AND (check_in = %(check_in)s OR check_out = %(check_out)s);"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if results:
            return results[0]
        return False


    """     
    #UPDATE pay
    @classmethod
    def update(cls, data):
        query = "UPDATE reserved SET is_paid = '1' WHERE reserved.id = %(reservation_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)  """ 
    

    #READ
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM reserved;"
        results = connectToMySQL(cls.db_name).query_db(query)
        reserved = []
        if results:
            for x in results:
                reserved.append(x)
            return reserved
        return reserved


    #DELETE
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM reserved WHERE reserved.id = %(reservation_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)


    @staticmethod
    def validate_reservation(reservation):
        is_valid = True
    
        """         
        if reservation['is_paid'] == 0:
            flash('You should pay the parking spot!', 'paySpot')
            is_valid= False """
        
        if reservation['check_in'] == '':
            flash('Please enter the date of the check in!', 'check_in')
            is_valid= False
        if reservation['check_out'] == '':
            flash('Please enter the date of the check out!', 'check_out')
            is_valid= False
        if reservation['space'] == '':
            flash('Parking space is required.', 'space')
            is_valid= False
        return is_valid


    @staticmethod
    def calculate_cost(cost, check_in, check_out):
        diff = check_out - check_in
        return cost * diff 


"""     
    @staticmethod
    def cost(reservation):
        cost = 0
        a=reservation['check_in']
        b=reservation['check_out'] 

        cost = (b-a)*20
        return cost """