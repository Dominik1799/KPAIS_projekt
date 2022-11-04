from datetime import datetime

def approve_transaction(Ownership, Transaction, session, transactionID):
        transaction = session.query(Transaction).get(transactionID)
        transaction.state = "approved"
        new_ownership = session.query(Ownership).filter(Ownership.transactionID == transactionID).first()
        new_ownership.isActive = True

        car_to_transfer = new_ownership.carID
        old_owner = transaction.initiator

        old_ownership = session.query(Ownership).filter(Ownership.carID == car_to_transfer).filter( Ownership.ownerID == old_owner).filter(Ownership.isActive == True).first()
        old_ownership.isActive = False
        session.commit()

def deny_transaction(Ownership, Transaction, session, transactionID):
        transaction = session.query(Transaction).get(transactionID)
        transaction.state = "denied"
        session.query(Ownership).filter(Ownership.transactionID == transactionID).delete()
        session.commit()

def transfer_vehicle(Ownership, session, Transaction, old_ownerID, new_ownerID, carID, price):
        transaction = Transaction(type="purchase", price=price, date=datetime.today().strftime("%Y-%m-%d"), city="Online", state="pending", initiator=old_ownerID)
        session.add(transaction)
        session.commit()
        ownership = Ownership(ownerID=new_ownerID, carID=carID, isActive=False, transactionID=transaction.id)
        session.add(ownership)
        session.commit()