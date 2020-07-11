"""Blogly application."""

from flask import Flask, request, redirect, render_template
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

from flask_debugtoolbar import DebugToolbarExtension
app.config['SECRET_KEY'] = "SECRET!"
debug = DebugToolbarExtension(app)

db.create_all()


@app.route('/')
def root():
    return redirect('/users')

@app.route('/users')
def users():
    users = User.query.all()
    return render_template("users_table.html", users = users)

@app.route('/users/new', methods=('POST', 'GET'))
def add_user():
    if request.method == 'POST':
        first_name = request.form['first']
        last_name = request.form['last']
        image_url = request.form['pic']

        user = User(first_name=first_name, last_name=last_name, image_url=image_url)
        db.session.add(user)
        db.session.commit()
        return redirect('/users')
    else:
        return render_template('add_user.html')

@app.route('/users/<int:user_id>', methods=("POST","GET"))
def user_detail(user_id):
    user = User.query.get_or_404(user_id)
    return render_template("details.html", user=user)


@app.route('/users/<int:user_id>/edit', methods=('POST', 'GET'))
def user_edit(user_id):
    if request.method == 'POST':
        first_name = request.form['first']
        last_name = request.form['last']
        image_url = request.form['pic']

        user = User.query.get(user_id)
        user.first_name = first_name
        user.last_name = last_name
        user.image_url = image_url
        db.session.commit()
        return redirect(f'/users/{user_id}')
    else:
        user = User.query.get_or_404(user_id)
        return render_template("edit_details.html", user=user)

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect('/users')