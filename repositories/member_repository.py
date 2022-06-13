from db.run_sql import run_sql

from models.member import Member

#CRUD: Create, Read, Update and Delete


#Create
def save(member):
    sql = "INSERT INTO members (name, dob, membership, active) VALUES (%s, %s, %s, %s) RETURNING id"
    values = [member.name, member.dob, member.membership, member.active]
    results = run_sql(sql, values)
    member.id = results[0]["id"]
    return member


#Read
def select_all():
    members = []
    sql = "SELECT * FROM members"
    results = run_sql(sql)

    for result in results:
        member = Member(result["name"], result["dob"], result["membership"], result["active"], result["id"])
        members.append(member)
    return members

#added below already for future use
def select(id):
    sql="SELECT * FROM members WHERE id = %s"
    values = [id]
    result = run_sql(sql, values)[0]
    member = Member(result["name"], result["dob"], result["membership"], result["active"], result["id"])
    return member


#Update
def update(member):
    sql = "UPDATE members SET (name, dob, membership, active) = (%s, %s, %s, %s) WHERE id = %s"
    values = [member.name, member.dob, member.membership, member.active, member.id]
    run_sql(sql, values)


#Delete
def delete_all():
    sql = "DELETE FROM members"
    run_sql(sql)

def delete(id):
    sql = "DELETE FROM members WHERE id = %s"
    values = [id]
    run_sql(sql, values)