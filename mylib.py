import pymysql

def make_connection():
    conn = pymysql.connect(host="localhost", port=3306, user="root", passwd="", db="python",autocommit=True)
    cur = conn.cursor()
    return cur

def check_photo(email):
    cur = make_connection()
    cur.execute("SELECT * FROM photodata where email='" + email + "'")
    n=cur.rowcount
    photo="no"
    if n>0:
        row=cur.fetchone()
        photo=row[1]
    return photo

def get_admin_name(email):
    cur = make_connection()
    cur.execute("SELECT * FROM admindata where email='" + email + "'")
    n = cur.rowcount
    name = "no"
    if n > 0:
        row = cur.fetchone()
        name = row[0]
    return name
def get_doctors(email):
    cur = make_connection()
    cur.execute("SELECT * FROM doctordata where email_of_hospital='"+email+"'")
    data=cur.fetchall()
    return data

def getdoctor(name,spec,email):
    cur = make_connection()
    cur.execute("SELECT * FROM doctordata where name='"+name+"' AND speciality='"+spec+"' AND email_of_hospital='" + email + "'")
    data = cur.fetchone()
    return data