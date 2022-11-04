from sqlalchemy import Table


class Models:
    owner = None
    car = None
    address = None
    transaction = None
    ownership = None

    def __init__(self, base, engine):
        Models.owner = base.classes.owner
        Models.car = base.classes.car
        Models.address = base.classes.address
        Models.transaction = base.classes.transaction
        Models.ownership = base.classes.ownership
        