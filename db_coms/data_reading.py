from sqlalchemy import func
from sqlalchemy.orm import aliased


    # returns a list of tuples. First in each tuple is car, then it's owner
def get_all_cars(Car, Owner, Ownership, session, filter_make=None, filter_year_from=None, filter_year_to=None):
    query = session.query(Car, Owner, Ownership).join(Owner, 
    Ownership.ownerID == Owner.id).join(Car, 
    Ownership.carID == Car.id).filter(Ownership.isActive == True)
    if filter_make is not None:
        query = query.filter(Car.make == filter_make)
    if filter_year_from is not None:
        query = query.filter(Car.year >= filter_year_from)
    if filter_year_to is not None:
        query = query.filter(Car.year <= filter_year_to)

    result = query.all()
    return result

def get_car_details(Car, session, carID):
    result = session.query(Car).get(carID)
    return result

    # returns list of tuples. Data in each tuple is in this order: ownership, owner, transaction
def get_car_owners(Owner, Ownership, Transaction, session, carID):
    query = session.query(Ownership, Owner, Transaction).join(Owner, 
    Ownership.ownerID == Owner.id).join(Transaction,
    Transaction.id == Ownership.transactionID).filter(Ownership.carID == carID).order_by(Transaction.date.desc())
    result = query.all()
    return result

def get_user(Owner, session, userID):
    result = session.query(Owner).get(userID)
    return result
    
def get_user_by_name(Owner, session, name):
    query = session.query(Owner).filter(func.lower(Owner.name) == func.lower(name))
    print(query)
    result = query.first()
    return result

def get_user_cars(Car, Ownership, session, userID):
    result = session.query(Ownership, Car).filter(Ownership.ownerID == userID).filter(Ownership.isActive == True).join(Car,
    Car.id == Ownership.carID).all()
    return result

    # items in tuple are ordered the same way as objects in query()
def get_all_pending_transactions(Car, Owner, Ownership, Transaction ,session):
    initiator = aliased(Owner)
    query = session.query(Transaction, initiator, Owner, Ownership, Car).filter(Transaction.state == "pending").join(Ownership, 
    Ownership.transactionID == Transaction.id).join(Car, Car.id == Ownership.carID).join(Owner,
    Owner.id == Ownership.ownerID).join(initiator, initiator.id == Transaction.initiator)
    results = query.all()
    return results