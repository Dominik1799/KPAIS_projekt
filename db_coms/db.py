from models.models import Models
from sqlalchemy.orm import Session
from datetime import datetime
from sqlalchemy import func
from sqlalchemy.orm import aliased
import db_coms.data_reading as data_reading
import os
import db_coms.data_writing as data_writing
import db_coms.data_reading_safety_fix as data_reading_safety_fix

class DB_connector:
    # static variables
    db = None
    base = None
    session = None

    # DB Models
    Owner = None
    Car = None
    Transaction = None
    Address = None
    Ownership = None



    @staticmethod
    def initialize_connector(db, base):
        DB_connector.db = db
        DB_connector.base = base
        DB_connector.models = Models(DB_connector.base, DB_connector.db.engine)
        DB_connector.session = Session(DB_connector.db.engine)
        # init models
        DB_connector.Owner = DB_connector.models.owner
        DB_connector.Car = DB_connector.models.car
        DB_connector.Transaction = DB_connector.models.transaction
        DB_connector.Address = DB_connector.models.address
        DB_connector.Ownership = DB_connector.models.ownership



    # returns a list of tuples. First in each tuple is car, then it's owner
    def get_all_cars(self, filter_make=None, filter_year_from=None, filter_year_to=None):
        if os.environ.get("SAFE_SEARCH") == "1":
            if os.environ.get("ORM_SEARCH") == "1":
                print("Communicating safely with the DB - ORM")
                return data_reading.get_all_cars(DB_connector.Car, DB_connector.Owner, DB_connector.Ownership, DB_connector.session,  filter_make, filter_year_from, filter_year_to)
            else:
                print("Communicating safely with the DB - parameterized  queries")
                return data_reading_safety_fix.get_all_cars_safe(filter_make, filter_year_from, filter_year_to)
        else:
            print("Communicating !!unsafely!! with the DB")
            return data_reading_safety_fix.get_all_cars_unsafe(filter_make, filter_year_from, filter_year_to)
                

    def get_car_details(self, carID):
        return data_reading.get_car_details(DB_connector.Car, DB_connector.session, carID)

    # returns list of tuples. Data in each tuple is in this order: ownership, owner, transaction
    def get_car_owners(self, carID):
        return data_reading.get_car_owners(DB_connector.Owner, DB_connector.Ownership, DB_connector.Transaction, DB_connector.session, carID)

    def get_user(self, userID):
        return data_reading.get_user(DB_connector.Owner, DB_connector.session, userID)
    
    def get_user_by_name(self, name):
        return data_reading.get_user_by_name(DB_connector.Owner, DB_connector.session, name)

    def get_user_cars(self, userID):
        return data_reading.get_user_cars(DB_connector.Car, DB_connector.Ownership, DB_connector.session, userID)

    def transfer_vehicle(self, old_ownerID, new_ownerID, carID, price):
        data_writing.transfer_vehicle(DB_connector.Ownership, DB_connector.session, DB_connector.Transaction,
        old_ownerID, new_ownerID, carID, price)

    # items in tuple are ordered the same way as objects in query()
    def get_all_pending_transactions(self):
        return data_reading.get_all_pending_transactions(DB_connector.Car, DB_connector.Owner, DB_connector.Ownership, 
        DB_connector.Transaction, DB_connector.session)

    def approve_transaction(self, transactionID):
        data_writing.approve_transaction(DB_connector.Ownership, DB_connector.Transaction, DB_connector.session, transactionID)

    def deny_transaction(self, transactionID):
        data_writing.deny_transaction(DB_connector.Ownership, DB_connector.Transaction, DB_connector.session, transactionID)