from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sweater import db, app
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from sweater.models import users, User
from werkzeug.security import check_password_hash, generate_password_hash
import smtplib
from sweater import EMAIL_ADMIN, PASSWORD_ADMIN_EMAIL
import random


@app.route('/', methods=['POST', 'GET'])
@login_required
def ocnova():
    if request.method == 'POST':
        n = request.form['title']
        m = request.form['mik']
        name2 = users(name=n, mik=m)
        try:
            db.session.add(name2)
            db.session.commit()
            return redirect('/names')
        except:
            return "problem"
    else:
        return render_template("basa.html")


@app.route('/names')
@login_required
def names():
    users1 = users.query.order_by(users.time.desc()).all()
    return render_template("names.html", users=users1)


@app.route('/names/<int:id>')
@login_required
def namesdop(id):
    users2 = users.query.get(id)
    return render_template("firstnames.html", users=users2)


@app.route('/names/<int:id>/delete')
@login_required
def namesdelete(id):
    users3 = users.query.get_or_404(id)
    try:
        db.session.delete(users3)
        db.session.commit()
        return redirect('/names')
    except:
        return "problem"


@app.route('/names/<int:id>/update', methods=['POST', 'GET'])
@login_required
def namesupdata(id):
    users4 = users.query.get(id)
    if request.method == 'POST':
        users4.name = request.form['title']
        users4.mik = request.form['mik']
        users4.time = datetime.utcnow()
        try:
            db.session.commit()
            return redirect('/names')
        except:
            return "problem"
    else:

        return render_template("updatenames.html", users=users4)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    login = request.form.get('login')
    password = request.form.get('password')
    if login and password:
        user = User.query.filter_by(login=login).first()
        if user and check_password_hash(user.password, password):
            login_user(user)

            next_page = request.args.get('next')

            return redirect("/")
        else:
            flash('Неправильный логин или пароль')
    else:
        pass

    return render_template('login2.html')


M = []


@app.route('/checkemail', methods=['POST', 'GET'])
def send_emails():
    if request.method == 'POST':

        email1 = request.form.get('email')
        try:
            def send_emails2():
                subject = "Your cod registration"
                msg = str(random.randint(10000, 100000))
                M.clear()
                M.append(msg)
                server = smtplib.SMTP('smtp.gmail.com:587')
                server.ehlo()
                server.starttls()
                server.login(EMAIL_ADMIN, PASSWORD_ADMIN_EMAIL)
                message = 'Subject: {}\n\n{}'.format(subject, msg)
                server.sendmail(EMAIL_ADMIN, email1, message)
                server.quit()

            if email1:
                send_emails2()
            else:
                flash("вы не ввели почту")
                return render_template("email_check.html")
        except:
            flash("Возникла проблема при отправке сообщения")
            return render_template("email_check.html")

        return redirect("/check")
    else:
        return render_template("email_check.html")


@app.route('/check', methods=['POST', 'GET'])
def check():
    if request.method == 'POST':
        try:
            number = request.form.get('number')
            if int(M[0]) == int(number):
                return redirect(url_for('reg'))
            else:
                flash("отправленный на почту код не совпадает с тем который вы ввели")
            return render_template("check.html")
        except:
            flash("Возникла ошибка, попробуйте ввести число ещё раз")
    else:
        pass
    return render_template("check.html")


@app.route('/reg', methods=['POST', 'GET'])
def reg():
    login = request.form.get('login')
    password = request.form.get('password')
    password2 = request.form.get('password2')
    if request.method == 'POST':
        if not (login or password or password2):
            flash('заполните все поля')
            return render_template("regpage2.html")
        elif password != password2:
            flash("пароли не сопадают")
            return render_template("regpage2.html")
        elif len(str(password)) < 3:
            flash("пароль слишком маленький")
            return render_template("regpage2.html")
        else:
            try:
                hash_pwd = generate_password_hash(password)
                new_user = User(login=login, password=hash_pwd)
                db.session.add(new_user)
                db.session.commit()
                user = User.query.filter_by(login=login).first()
                login_user(user)
                return redirect('/')
            except:
                flash("данный логин уже кем-то используется, попробуйте другой ")
                return render_template("regpage2.html")
    else:
        pass
    return render_template("regpage2.html")


@app.route('/logout', methods=['POST', 'GET'])
@login_required
def logout():
    logout_user()
    return redirect("/login")


@app.route('/deleteaccount', methods=['POST', 'GET'])
@login_required
def delacc():
    login = request.form.get('login')
    password = request.form.get('password')
    if request.method == 'POST':
        if login and password:
            user = User.query.filter_by(login=login).first()
            if user and check_password_hash(user.password, password):
                login2 = User.query.get(user.id)
                try:
                    db.session.delete(login2)
                    db.session.commit()
                    return redirect(url_for('logout'))
                except:
                    flash("Возникла проблема при удалении аккаунта")
                    return render_template("deleteaccount.html")
            else:
                flash("Неправильный пароль")
                return render_template("deleteaccount.html")
    return render_template("deleteaccount.html")


@app.after_request
def redirect_to(response):
    if response.status_code == 401:
        return redirect(url_for("login_page") + "?next_page=" + request.url)
    return response
