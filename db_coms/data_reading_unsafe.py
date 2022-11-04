import psycopg2
from psycopg2 import sql


__BASE_QUERY = """
SELECT car.id AS car_id, car.make AS car_make, car.model AS car_model, car.year AS car_year, car.category AS car_category, owner.name AS owner_name
FROM ownership JOIN owner ON ownership."ownerID" = owner.id JOIN car ON ownership."carID" = car.id
WHERE ownership."isActive" = true"""

def get_all_cars_unsafe(filter_make=None, filter_year_from=None, filter_year_to=None):
    conn = psycopg2.connect(database="postgres", user="postgres", password="admin", host="127.0.0.1", port="5432")
    cursor = conn.cursor()
    final_q = __BASE_QUERY + __apply_filer_unsafe(filter_make, filter_year_from, filter_year_to)
    cursor.execute(final_q)
    items = cursor.fetchall()
    return __format_return(items)


def __apply_filer_unsafe(filter_make, filter_year_from, filter_year_to):
    filter = ""
    if filter_make is not None:
        filter += " AND car.make = '" + filter_make + "'"
    if filter_year_from is not None:
        filter += " AND car.year >= " + filter_year_from
    if filter_year_to is not None:
        filter += " AND car.year <= " + filter_year_to
    return filter


def __format_return(items):
    final_items = []
    for item in items:
        car = {
            "id": item[0],
            "make": item[1],
            "model": item[2],
            "year": item[3],
            "category": item[4],
        }
        owner = {
            "name": item[5]
        }
        tup = (car, owner)
        final_items.append(tup)
    
    return final_items