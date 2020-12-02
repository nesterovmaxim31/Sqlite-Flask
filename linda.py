from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pas.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    mik = db.Column(db.String(20), unique=True, nullable=False)
    time = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self):
        return '<users %r>' % self.name


@app.route('/', methods=['POST', 'GET'])
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
def names():
    users1 = users.query.order_by(users.time.desc()).all()
    return render_template("names.html", users=users1)


@app.route('/names/<int:id>')
def namesdop(id):
    users2 = users.query.get(id)
    return render_template("firstnames.html", users=users2)


@app.route('/names/<int:id>/delete')
def namesdelete(id):
    users3 = users.query.get_or_404(id)
    try:
        db.session.delete(users3)
        db.session.commit()
        return redirect('/names')
    except:
        return "problem"


@app.route('/names/<int:id>/update', methods=['POST', 'GET'])
def namesupdata(id):
    users4 = users.query.get(id)
    if request.method == 'POST':
        users4.name = request.form['title']
        users4.mik = request.form['mik']
        try:
            db.session.commit()
            return redirect('/names')
        except:
            return "problem"
    else:

        return render_template("updatenames.html", users=users4)


if __name__ == "__main__":
    app.run(debug=True)
