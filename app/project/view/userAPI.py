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
            email = session['email']
            return render_template('base.html', info = email)
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

@userAPI.route('/pandas', methods=['POST', 'GET'])
def pandas():
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns
    import numpy as np
    import matplotlib
    matplotlib.use('Agg')
    from io import BytesIO
    import base64

    img = BytesIO()
    #0-price, 1-year, 2-date
    art_df = pd.read_csv('static/csv/art.csv')

    #각 년도별 최고 금액
    maxs = art_df['0'].max()
    art_df_group = art_df.groupby('1')
    art_df_group = art_df_group['0'].max()
    art_df_group = art_df_group.reset_index()

    # 시각화1
    art_df['2'] = pd.to_datetime(art_df['2'])
    maxs = art_df["0"].max()
    plt.scatter(x=art_df['2'],y=art_df['0'])
    plt.style.use(['tableau-colorblind10'])
    plt.yticks(np.arange(0,maxs, step=maxs // 10))
    plt.savefig(img, format='png')
    plt.close()
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')

    img = BytesIO()
    # 시각화2
    plt.plot(art_df_group['1'],art_df_group['0'])
    plt.style.use(['tableau-colorblind10'])
    plt.yticks(np.arange(0,maxs, step=maxs // 10))
    plt.savefig(img, format='png')
    plt.close()
    img.seek(0)
    plot_url2 = base64.b64encode(img.getvalue()).decode('utf8')

    return render_template('plot.html', plot_url=plot_url, plot_url2=plot_url2)