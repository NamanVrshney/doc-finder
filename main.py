from flask import Flask, render_template, request, session, url_for, redirect
from werkzeug.utils import secure_filename

from mylib import *

import time
import pymysql
import os

app = Flask(__name__)

app.secret_key = "super secret key"
app.config['UPLOAD_FOLDER'] = './static/photos'


@app.route('/')
def hello_world():
    cur = make_connection()
    cur.execute("SELECT * FROM hospitals")
    result = cur.fetchall()
    return render_template('index.html', result=result)


@app.route('/Login')
def login():
    return render_template('Login.html')


@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        spec = request.form['T1']
        sql = "select * from doctors where speciality='" + spec + "'"
        cur = make_connection()
        cur.execute(sql)
        result = cur.fetchall()
        return render_template('Search.html', result=result)
    else:
        return render_template('Search.html')


@app.route('/checklogin', methods=['GET', 'POST'])
def checklogin():
    if (request.method == 'POST'):
        email = request.form["T1"]
        password = request.form["T2"]
        # connection

        sql = "SELECT * FROM logindata where email='" + email + "' and password='" + password + "'"
        cur = make_connection()
        cur.execute(sql)
        n = cur.rowcount
        if (n > 0):
            # create cookie
            row = cur.fetchone()
            usertype = row[2]
            session["usertype"] = usertype
            session["email"] = email
            if (usertype == "admin"):
                return redirect(url_for('adminhome'))
            elif (usertype == "hospital"):
                return redirect(url_for('hospital_home'))
        else:
            return render_template("loginerror.html")


@app.route('/logout')
def logout():
    if 'usertype' in session:
        session.pop('usertype', None)
        session.pop('email', None)
        return render_template('Login.html')
    else:
        return render_template('Login.html')


@app.route('/autherror')
def autherror():
    return render_template('autherror.html')


@app.route('/adminhome')
def adminhome():
    if 'usertype' in session:
        usertype = session['usertype']
        email = session['email']
        if usertype == 'admin':
            photo = check_photo(email)
            name = get_admin_name(email)
            return render_template('adminhome.html', e1=email, photo=photo, name=name)
        else:
            return redirect(url_for('autherror'))
    else:
        return redirect(url_for('autherror'))


@app.route('/adminreg', methods=['GET', 'POST'])
def adminreg():
    if 'usertype' in session:
        usertype = session['usertype']
        email = session['email']
        if usertype == 'admin':
            if request.method == 'POST':
                name = request.form['T1']
                address = request.form['T3']
                contact = request.form['T5']
                email = request.form['T6']
                password = request.form['T7']
                ut = "admin"
                cur = make_connection()
                sql = "insert into admindata values('" + name + "','" + address + "','" + contact + "','" + email + "')"
                sql2 = "insert into logindata values('" + email + "','" + password + "','" + ut + "')"
                cur.execute(sql)
                cur.execute(sql2)
                return render_template('AdminReg.html', result="Data Saved")
            else:
                return render_template('AdminReg.html')
        else:
            return redirect(url_for('autherror'))
    else:
        return redirect(url_for('autherror'))


@app.route('/hospital_reg', methods=['GET', 'POST'])
def hospital_reg():
    if 'usertype' in session:
        usertype = session['usertype']
        email = session['email']
        if usertype == 'admin':
            if request.method == 'POST':
                name = request.form['T1']
                address = request.form['T3']
                contact = request.form['T5']
                email = request.form['T6']
                password = request.form['T7']
                ut = "hospital"
                photo = 'no'
                cur = make_connection()
                sql = "insert into hospitals values('" + name + "','" + address + "','" + contact + "','" + email + "','" + photo + "')"
                sql2 = "insert into logindata values('" + email + "','" + password + "','" + ut + "')"
                cur.execute(sql)
                n = cur.rowcount
                cur.execute(sql2)
                m = cur.rowcount
                if n == 1 and m == 1:
                    return render_template('HospitalReg.html', result="Data Saved")
                elif n == 1:
                    return render_template('HospitalReg.html', result="Data Saved but login not created")
                elif m == 1:
                    return render_template('HospitalReg.html', result="Login created but data not saved")
                else:
                    return render_template('HospitalReg.html', result="Error : Cannot Saved data")
            else:
                return render_template('HospitalReg.html')
        else:
            return redirect(url_for('autherror'))
    else:
        return redirect(url_for('autherror'))


@app.route('/hospital_home')
def hospital_home():
    if 'usertype' in session:
        usertype = session['usertype']
        email = session['email']
        if usertype == 'hospital':
            doctors = get_doctors(email)
            return render_template('HospitalHome.html', doctors=doctors)
        else:
            return redirect(url_for('autherror'))
    else:
        return redirect(url_for('autherror'))


@app.route('/showadmins')
def showadmins():
    if 'usertype' in session:
        usertype = session['usertype']
        email = session['email']
        if usertype == 'admin':
            cur = make_connection()
            cur.execute("SELECT * FROM admindata")
            result = cur.fetchall()
            return render_template('showadmins.html', result=result)
        else:
            return redirect(url_for('autherror'))
    else:
        return redirect(url_for('autherror'))


@app.route('/adminphoto')
def adminphoto():
    return render_template('photoupload_admin.html')


@app.route('/adminphoto1', methods=['GET', 'POST'])
def adminphoto1():
    if 'usertype' in session:
        usertype = session['usertype']
        email = session['email']
        if usertype == 'admin':
            if request.method == 'POST':
                file = request.files['F1']
                if file:
                    path = os.path.basename(file.filename)
                    file_ext = os.path.splitext(path)[1][1:]
                    filename = str(int(time.time())) + '.' + file_ext
                    filename = secure_filename(filename)
                    cur = make_connection()
                    sql = "insert into photodata values('" + email + "','" + filename + "')"

                    try:
                        cur.execute(sql)
                        n = cur.rowcount
                        if n == 1:
                            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                            return render_template('photoupload_admin1.html', result="success")
                        else:
                            return render_template('photoupload_admin1.html', result="failure")
                    except:
                        return render_template('photoupload_admin1.html', result="duplicate")
            else:
                return render_template('photoupload_admin.html')
        else:
            return redirect(url_for('autherror'))
    else:
        return redirect(url_for('autherror'))


@app.route('/adminphoto2', methods=['GET', 'POST'])
def adminphoto2():
    if 'usertype' in session:
        usertype = session['usertype']
        email = session['email']
        if usertype == 'admin':
            if request.method == 'POST':
                file = request.files['F1']
                if file:
                    filename = secure_filename(file.filename)
                    cur = make_connection()
                    sql = "insert into photodata values('" + email + "','" + filename + "')"

                    try:
                        cur.execute(sql)
                        n = cur.rowcount
                        if n == 1:
                            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                            return render_template('photoupload_admin1.html', result="success")
                        else:
                            return render_template('photoupload_admin1.html', result="failure")
                    except:
                        return render_template('photoupload_admin1.html', result="duplicate")
            else:
                return render_template('photoupload_admin.html')
        else:
            return redirect(url_for('autherror'))
    else:
        return redirect(url_for('autherror'))


@app.route('/change_adminphoto')
def change_adminphoto():
    if 'usertype' in session:
        usertype = session['usertype']
        email = session['email']
        if usertype == 'admin':
            photo = check_photo(email)
            cur = make_connection()
            sql = "delete from photodata where email='" + email + "'"
            cur.execute(sql)
            n = cur.rowcount
            if n > 0:
                os.remove("./static/photos/" + photo)
                return render_template('change_adminphoto.html', data="success")
            else:
                return render_template('change_adminphoto.html', data="failure")
        else:
            return redirect(url_for('autherror'))
    else:
        return redirect(url_for('autherror'))


@app.route('/show_hospitals')
def show_hospitals():
    if 'usertype' in session:
        usertype = session['usertype']
        email = session['email']
        if usertype == 'admin':
            cur = make_connection()
            cur.execute("SELECT * FROM hospitals")
            result = cur.fetchall()
            return render_template('show_hospitals.html', result=result)
        else:
            return redirect(url_for('autherror'))
    else:
        return redirect(url_for('autherror'))


@app.route('/edit_hospital', methods=['GET', 'POST'])
def edit_hospital():
    if 'usertype' in session:
        usertype = session['usertype']
        e1 = session['email']
        if usertype == 'admin':
            email_of_hospital = request.form['H1']
            cur = make_connection()
            cur.execute("SELECT * FROM hospitals where email='" + email_of_hospital + "'")
            result = cur.fetchall()
            return render_template('EditHospital.html', result=result)
        else:
            return redirect(url_for('autherror'))


@app.route('/edit_hospital1', methods=['GET', 'POST'])
def edit_hospital1():
    if 'usertype' in session:
        usertype = session['usertype']
        e1 = session['email']
        if usertype == 'admin':
            name = request.form['T1']
            address = request.form['T2']
            contact = request.form['T3']
            email_of_hospital = request.form['T4']
            sql = "update hospitals set name='" + name + "',address='" + address + "',contact='" + contact + "' where email='" + email_of_hospital + "'"
            cur = make_connection()
            cur.execute(sql)
            n = cur.rowcount
            return redirect(url_for('hospital_home'))
        else:
            return redirect(url_for('autherror'))


@app.route('/hospital_photo', methods=['GET', 'POST'])
def hospital_photo():
    if 'usertype' in session:
        usertype = session['usertype']
        email = session['email']
        if usertype == 'admin':
            if request.method == 'POST':
                file = request.files['F1']
                email_hos = request.form['H1']
                if file:
                    path = os.path.basename(file.filename)
                    file_ext = os.path.splitext(path)[1][1:]
                    filename = str(int(time.time())) + '.' + file_ext
                    filename = secure_filename(filename)
                    cur = make_connection()
                    sql = "update hospitals set photo='" + filename + "' where email='" + email_hos + "'"

                    try:
                        cur.execute(sql)
                        n = cur.rowcount
                        if n == 1:
                            file.save(os.path.join('./static/hospital_photos', filename))
                            return render_template('hospital_photo.html', result="success")
                        else:
                            return render_template('hospital_photo.html', result="failure")
                    except:
                        return render_template('hospital_photo.html', result="duplicate")
            else:
                return render_template('show_hospitals.html')

        else:
            return redirect(url_for('autherror'))
    else:
        return redirect(url_for('autherror'))


@app.route('/chnage_hospital_photo', methods=['GET', 'POST'])
def chnage_hospital_photo():
    if 'usertype' in session:
        usertype = session['usertype']
        email = session['email']
        if usertype == 'admin':
            if request.method == 'POST':
                email_hos = request.form['H1']
                photo = request.form['H2']

                cur = make_connection()
                sql = "update hospitals set photo='no' where email='" + email_hos + "'"
                cur.execute(sql)
                n = cur.rowcount
                if n > 0:
                    os.remove("./static/hospital_photos/" + photo)
                    return render_template('chnage_hospital_photo.html', data="success")
                else:
                    return render_template('chnage_hospital_photo.html', data="failure")
            else:
                return render_template('show_hospitals.html')
        else:
            return redirect(url_for('autherror'))
    else:
        return redirect(url_for('autherror'))


@app.route('/doctor_reg', methods=['GET', 'POST'])
def doctor_reg():
    if 'usertype' in session:
        usertype = session['usertype']
        e1 = session['email']
        if usertype == 'hospital':
            if request.method == 'POST':
                name = request.form['T1']
                spec = request.form['T2']
                quali = request.form['T3']
                tm = request.form['T4']
                daylist = request.form.getlist('C1')
                mon = 'no'
                tue = 'no'
                wed = 'no'
                thu = 'no'
                fri = 'no'
                sat = 'no'
                sun = 'no'
                if 'mon' in daylist:
                    mon = 'yes'
                if 'tue' in daylist:
                    tue = 'yes'
                if 'wed' in daylist:
                    wed = 'yes'
                if 'thu' in daylist:
                    thu = 'yes'

                if 'fri' in daylist:
                    fri = 'yes'
                if 'sat' in daylist:
                    sat = 'yes'
                if 'sun' in daylist:
                    sun = 'yes'

                email_of_hospital = e1
                photo = 'no'
                cur = make_connection()

                sql = "insert into doctordata values('" + name + "','" + spec + "','" + quali + "','" + tm + "','" + mon + "','" + tue + "','" + wed + "','" + thu + "','" + fri + "','" + sat + "','" + sun + "','" + email_of_hospital + "','" + photo + "')"
                cur.execute(sql)
                n = cur.rowcount
                if n == 1:
                    return render_template('DoctorReg.html', data="Doctor Added", args=daylist)
                else:
                    return render_template('DoctorReg.html', data="Error: Cannot add doctor")
            else:
                return render_template('DoctorReg.html')
        else:
            return redirect(url_for('autherror'))
    else:
        return redirect(url_for('autherror'))


@app.route('/edit_doctor', methods=['GET', 'POST'])
def edit_doctor():
    if 'usertype' in session:
        usertype = session['usertype']
        email = session['email']
        if usertype == 'hospital':
            if request.method == 'POST':
                name = request.form['H1']
                spec = request.form['H2']
                doctor = getdoctor(name, spec, email)
                if doctor:
                    return render_template('EditDoctor.html', data=doctor)
        else:
            return redirect(url_for('autherror'))
    else:
        return redirect(url_for('autherror'))


@app.route('/edit_doctor1', methods=['GET', 'POST'])
def edit_doctor1():
    if 'usertype' in session:
        usertype = session['usertype']
        e1 = session['email']
        if usertype == 'hospital':
            if request.method == 'POST':
                name = request.form['T1']
                oldname = request.form['oldname']
                spec = request.form['T2']
                spec1 = request.form['spec']
                if spec == 'Select To Change':
                    spec = spec1
                quali = request.form['T3']
                tm = request.form['T4']
                daylist = request.form.getlist('C1')
                mon = 'no'
                tue = 'no'
                wed = 'no'
                thu = 'no'
                fri = 'no'
                sat = 'no'
                sun = 'no'
                if 'mon' in daylist:
                    mon = 'yes'
                if 'tue' in daylist:
                    tue = 'yes'
                if 'wed' in daylist:
                    wed = 'yes'
                if 'thu' in daylist:
                    thu = 'yes'

                if 'fri' in daylist:
                    fri = 'yes'
                if 'sat' in daylist:
                    sat = 'yes'
                if 'sun' in daylist:
                    sun = 'yes'

                email_of_hospital = e1
                photo = 'no'
                cur = make_connection()

                sql = "update doctordata set name='" + name + "',speciality='" + spec + "',qualification='" + quali + "',t='" + tm + "',mon='" + mon + "',tue='" + tue + "',wed='" + wed + "',thu='" + thu + "',fri='" + fri + "',sat='" + sat + "',sun='" + sun + "' where name='" + oldname + "' AND speciality='" + spec1 + "' AND email_of_hospital='" + email_of_hospital + "'"
                cur.execute(sql)
                n = cur.rowcount
                if n == 1:
                    return redirect(url_for('hospital_home'))
                else:
                    return redirect(url_for('hospital_home'))
            else:
                return redirect(url_for('hospital_home'))
        else:
            return redirect(url_for('autherror'))
    else:
        return redirect(url_for('autherror'))


@app.route('/delete_doctor', methods=['GET', 'POST'])
def delete_doctor():
    if 'usertype' in session:
        usertype = session['usertype']
        email = session['email']
        if usertype == 'hospital':
            if request.method == 'POST':
                name = request.form['H1']
                spec = request.form['H2']
                doctor = getdoctor(name, spec, email)
                if doctor:
                    return render_template('DeleteDoctor.html', row=doctor, )
        else:
            return redirect(url_for('autherror'))
    else:
        return redirect(url_for('autherror'))


@app.route('/delete_doctor1', methods=['GET', 'POST'])
def delete_doctor1():
    if 'usertype' in session:
        usertype = session['usertype']
        e1 = session['email']
        if usertype == 'hospital':
            if request.method == 'POST':
                name = request.form['H1']
                spec = request.form['H2']
                cur = make_connection()

                sql = "delete FROM doctordata where name='" + name + "' AND speciality='" + spec + "' AND email_of_hospital='" + e1 + "'"
                cur.execute(sql)
                n = cur.rowcount
                return redirect(url_for('hospital_home'))
            else:
                return redirect(url_for('hospital_home'))
        else:
            return redirect(url_for('autherror'))
    else:
        return redirect(url_for('autherror'))


@app.route('/hospital_profile')
def hospital_profile():
    if 'usertype' in session:
        usertype = session['usertype']
        email = session['email']
        if usertype == 'hospital':
            cur = make_connection()
            cur.execute("SELECT * FROM hospitals where email='" + email + "'")
            result = cur.fetchone()
            return render_template('HospitalProfile.html', row=result)
        else:
            return redirect(url_for('autherror'))
    else:
        return redirect(url_for('autherror'))


@app.route('/hospital_password', methods=['GET', 'POST'])
def hospital_password():
    if 'usertype' in session:
        usertype = session['usertype']
        email = session['email']
        if usertype == 'hospital':
            if request.method == 'POST':
                oldpass = request.form['T1']
                newpass = request.form['T2']
                cur = make_connection()
                cur.execute(
                    "update logindata set password='" + oldpass + "' where password='" + newpass + "' AND email='" + email + "'")
                n = cur.rowcount
                if n > 0:
                    return render_template('HospitalPassword.html', result="Password Changed")
                else:
                    return render_template('HospitalPassword.html', result="Invalid Old Password")
            else:
                return render_template('HospitalPassword.html')
        else:
            return redirect(url_for('autherror'))
    else:
        return redirect(url_for('autherror'))


@app.route('/admin_password', methods=['GET', 'POST'])
def admin_password():
    if 'usertype' in session:
        usertype = session['usertype']
        email = session['email']
        if usertype == 'admin':
            if request.method == 'POST':
                oldpass = request.form['T1']
                newpass = request.form['T2']
                cur = make_connection()
                cur.execute(
                    "update logindata set password='" + oldpass + "' where password='" + newpass + "' AND email='" + email + "'")
                n = cur.rowcount
                if n > 0:
                    return render_template('AdminPassword.html', result="Password Changed")
                else:
                    return render_template('AdminPassword.html', result="Invalid Old Password")
            else:
                return render_template('AdminPassword.html')
        else:
            return redirect(url_for('autherror'))
    else:
        return redirect(url_for('autherror'))


if __name__ == '__main__':
    app.run(debug=True)
