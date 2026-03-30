from flask import Flask, render_template, request, redirect, session, send_from_directory
from flask_sqlalchemy import SQLAlchemy
import os

# CREATE APP FIRST ✅
app = Flask(__name__)
app.secret_key = 'secret123'

# DATABASE CONFIG
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'
db = SQLAlchemy(app)

# UPLOAD FOLDER
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ================= MODELS =================

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    filename = db.Column(db.String(100))
    user_id = db.Column(db.Integer)

# CREATE DATABASE
with app.app_context():
    db.create_all()

# ================= ROUTES =================

@app.route('/')
def home():
    if 'user_id' not in session:
        return redirect('/login')

    search = request.args.get('search')

    if search:
        notes = Note.query.filter(
            Note.user_id == session['user_id'],
            Note.title.contains(search)
        ).all()
    else:
        notes = Note.query.filter_by(user_id=session['user_id']).all()

    return render_template('index.html', notes=notes)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        existing_user = User.query.filter_by(username=username).first()

        if existing_user:
            return "User already exists!"

        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()

        return redirect('/login')

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username, password=password).first()

        if user:
            session['user_id'] = user.id
            return redirect('/')

        return "Invalid credentials!"

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect('/login')


@app.route('/upload', methods=['POST'])
def upload():
    if 'user_id' not in session:
        return redirect('/login')

    file = request.files['file']
    title = request.form['title']

    if file:
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

        note = Note(title=title, filename=file.filename, user_id=session['user_id'])
        db.session.add(note)
        db.session.commit()

    return redirect('/')


@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)


@app.route('/delete/<int:id>')
def delete(id):
    note = Note.query.get(id)
    if note:
        db.session.delete(note)
        db.session.commit()
    return redirect('/')


@app.route('/rename/<int:id>', methods=['POST'])
def rename(id):
    note = Note.query.get(id)
    if note:
        note.title = request.form['title']
        db.session.commit()
    return redirect('/')


# RUN APP
if __name__ == '__main__':
    app.run(debug=True)