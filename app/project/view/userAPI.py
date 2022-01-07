import hashlib #sha256
import sqlite3 as sql
from flask import Blueprint, render_template, request, redirect, url_for, session
from .dao import userDAO

# #create table
# conn = sql.connect('duck.db')
# print('db opened successfully')
# conn.execute(
#     'CREATE TABLE IF NOT EXISTS users (email TEXT, pw PASSWORD, birth TEXT, sex NUMBER)')
# print("Table created successfully")
# conn.close()
# #end create table

userAPI = Blueprint('userAPI', __name__, template_folder='/templates')

@userAPI.route('/', methods=['GET'])
def base():
    if request.method == 'GET':
        if 'email' in session:
            email = session['email'].split('@')
            return render_template('base.html', info = email[0])
        else:
            return render_template('base.html')


@userAPI.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        if 'email' in session:
            return redirect(url_for('userAPI.base'))
        else:
            if request.form['pw'] == request.form['pw2'] and request.form['email'] != '' and request.form['pw'] != '' and request.form['pw2'] != '' and request.form['birth'] != '':
                user = userDAO.User(request.form['email'], request.form['pw'], request.form['birth'], request.form['sex'])
                if user.create_user():
                    session['email'] = request.form['email']
                    print("회원가입 완료")
                    return redirect(url_for('userAPI.base'))
                else:
                    print("이미 중복된 아이디가 존재함")
                    return redirect(url_for('userAPI.signup'))
            else:
                print("비밀번호가 다르거나 비어있는 칸이 존재함")
                return redirect(url_for('userAPI.signup'))
    else:   #GET
        if 'email' in session:
            return redirect(url_for('userAPI.base'))
        else:
            return render_template('signup.html')

@userAPI.route('/signin', methods=['POST', 'GET'])
def signin():
    if request.method == 'POST':
        if 'email' in session:
            return redirect(url_for('userAPI.base'))
        else:
            if request.form['email'] != '' and request.form['pw']:
                user = userDAO.User(request.form['email'], request.form['pw'])
                if user.login_user():
                    session['email'] = request.form['email']
                    return redirect(url_for('userAPI.base'))
                else:
                    print("존재하는 아이디가 없거나 비밀번호가 다름")
                    return redirect(url_for('userAPI.signin'))
            else:
                print("이메일 혹은 비밀번호가 비어있음")
                return redirect(url_for('userAPI.signin'))
    else:
        if 'email' in session:
            return redirect(url_for('userAPI.base'))
        else:
            return render_template('signin.html')

@userAPI.route('/logout')
def logout():
    if 'email' in session:
        session.pop('email')
        return redirect(url_for('userAPI.base'))
    return redirect(url_for('userAPI.base'))