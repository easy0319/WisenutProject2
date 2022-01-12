import hashlib #sha256
import sqlite3 as sql
from flask import Blueprint, render_template, request, redirect, url_for, session
from .dao import userDAO, countDAO
from .src import art, insta, book


##create table
# conn = sql.connect('duck.db')
# print('db opened successfully')
# conn.execute("""
#     CREATE TABLE IF NOT EXISTS users (
#         email TEXT(254) NOT NULL PRIMARY KEY, 
#         pw PASSWORD(128) NOT NULL, 
#         birth TEXT(30) NOT NULL, 
#         sex NUMBER NOT NULL DEFAULT 1)
# """)
# conn.execute("""
#     CREATE TABLE IF NOT EXISTS counts (
#         cal TEXT(30) NOT NULL PRIMARY KEY,
#         cnt NUMBER NOT NULL DEFAULT 1)
# """)
# print("Table created successfully")
# conn.close()
##end create table

userAPI = Blueprint('userAPI', __name__, template_folder='/templates')

@userAPI.route('/', methods=['GET'])
def base():
    line = art.art()
    line.append(insta.insta())
    line.append(book.book())
    if request.method == 'GET':
        if 'email' in session:
            session['cnt'] = countDAO.select_cnt()
            email = session['email']
            cnt = session['cnt']
            return render_template('base.html', cnt = cnt,
                                                info = email,
                                                art1 = line[0], #천경자 데이터 시각화 1번
                                                art2 = line[1], #천경자 데이터 시각화 2번
                                                insta = line[2],#인스타 데이터 시각화
                                                book = line[3]
                                                )
        elif 'check_signin' in session:
            check = session['check_signin']
            return render_template('base.html', check_signin = check)
        elif 'check_signup' in session:
            check = session['check_signup']
            return render_template('base.html', check_signup = check)
        else:
            return render_template('base.html')


@userAPI.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        if 'email' in session:
            return redirect(url_for('userAPI.base'))
        else:
            if 'check_signin' in session:
                session.pop('check_signin')
            if request.form['pw'] == request.form['pw2'] and request.form['email'] != '' and request.form['pw'] != '' and request.form['pw2'] != '' and request.form['birth'] != '':
                user = userDAO.User(request.form['email'], request.form['pw'], request.form['birth'], request.form['sex'])
                if user.create_user():
                    session['email'] = request.form['email']
                    print("회원가입 완료")
                    countDAO.create_cnt()
                    if 'check_signup' in session:
                        session.pop('check_signup')
                    return redirect(url_for('userAPI.base'))
                else:
                    print("이미 중복된 아이디가 존재함")
                    session['check_signup'] = False
                    return redirect(url_for('userAPI.base'))
            else:
                print("비밀번호가 다르거나 비어있는 칸이 존재함")
                session['check_signup'] = False
                return redirect(url_for('userAPI.base'))
    else:   #GET
        if 'email' in session:
            return redirect(url_for('userAPI.base'))
        else:
            return render_template('userAPI.base')

@userAPI.route('/signin', methods=['POST', 'GET'])
def signin():
    if request.method == 'POST':
        if 'email' in session:
            return redirect(url_for('userAPI.base'))
        else:
            if 'check_signup' in session:
                session.pop('check_signup')
            if request.form['email'] != '' and request.form['pw']:
                user = userDAO.User(request.form['email'], request.form['pw'])
                if user.login_user():
                    session['email'] = request.form['email']
                    countDAO.create_cnt()
                    if 'check_signin' in session:
                        session.pop('check_signin')
                    return redirect(url_for('userAPI.base'))
                else:
                    print("존재하는 아이디가 없거나 비밀번호가 다름")
                    session['check_signin'] = False
                    return redirect(url_for('userAPI.base'))
            else:
                print("이메일 혹은 비밀번호가 비어있음")
                session['check_signin'] = False
                return redirect(url_for('userAPI.base'))
    else:
        if 'email' in session:
            return redirect(url_for('userAPI.base'))
        else:
            return render_template('userAPI.base')

@userAPI.route('/logout')
def logout():
    if 'email' in session:
        session.pop('email')
        return redirect(url_for('userAPI.base'))
    return redirect(url_for('userAPI.base'))
