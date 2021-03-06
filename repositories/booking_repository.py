from db.run_sql import run_sql
from models.booking import Booking
from models.gymclass import Gymclass
from models.member import Member

import repositories.gymclass_repository as gymclass_repository
import repositories.member_repository as member_repository


#CRUD: Create, Read, Update and Delete


#Create
def save(booking):
    sql = "INSERT INTO bookings (member_id, gymclass_id) VALUES (%s, %s) RETURNING id"
    values = [booking.member.id, booking.gymclass.id]
    results = run_sql(sql, values)
    id = results[0]["id"]
    booking.id = id
    return booking


#Read
def select_all():
    bookings = []
    sql = "SELECT * FROM bookings"
    results = run_sql(sql)

    for result in results:
        member = member_repository.select(result["member_id"])
        gymclass = gymclass_repository.select(result["gymclass_id"])
        booking = Booking(member, gymclass, result["id"])
        bookings.append(booking)
    return bookings


def select(id):
    sql = "SELECT * FROM bookings WHERE id = %s"
    values = [id]
    result = run_sql(sql, values)[0]
    member = member_repository.select(result["member_id"])
    gymclass = gymclass_repository.select(result["gymclass_id"])
    booking = Booking(member, gymclass, result["id"])
    return booking


#Delete
def delete_all():
    sql = "DELETE FROM bookings"
    run_sql(sql)


def delete(id):
    sql = "DELETE FROM bookings WHERE id = %s"
    values = [id]
    run_sql(sql, values)


#Update - not needed here


#gym class capacity check
def check_capacity(booking):
    gymclass = booking.gymclass
    members_added = len(gymclass_repository.list_of_members_booked(gymclass.id))
    if members_added < gymclass.capacity:
        return False
    else:
        return True
    
#duplicated bookings check
def check_duplicated_bookings(booking):
    member = booking.member
    members_added = member_repository.list_of_gymclasses_booked(member.id)
    for member in members_added:
        if member == member:
            return True
        else: 
            continue
    return False