import os
from flask import Flask, render_template, request, redirect, send_from_directory, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['SECRET_KEY'] = 'secret'

db = SQLAlchemy(app)

# -------- MODEL --------
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    filename = db.Column(db.String(200))
    favorite = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Create DB
with app.app_context():
    db.create_all()

# -------- LOGIN --------
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] == 'admin' and request.form['password'] == 'admin@123':
            session['user'] = request.form['username']
            return redirect('/home')
        return "Invalid credentials!"
    return render_template('login.html')

# -------- LOGOUT --------
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')

# -------- HOME --------
@app.route('/home')
def home():
    if 'user' not in session:
        return redirect('/')

    search = request.args.get('search')

    if search:
        notes = Note.query.filter(Note.title.contains(search)).all()
    else:
        notes = Note.query.order_by(Note.created_at.desc()).all()

    total_notes = Note.query.count()
    favorites = Note.query.filter_by(favorite=True).count()

    return render_template('index.html', notes=notes,
                           total_notes=total_notes,
                           favorites=favorites)

# -------- UPLOAD --------
@app.route('/upload', methods=['POST'])
def upload():
    if 'user' not in session:
        return redirect('/')

    file = request.files['file']

    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        new_note = Note(
            title=file.filename,
            filename=file.filename
        )

        db.session.add(new_note)
        db.session.commit()

    return redirect('/home')

# -------- DOWNLOAD --------
@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

# -------- DELETE --------
@app.route('/delete/<int:id>')
def delete(id):
    note = Note.query.get(id)
    db.session.delete(note)
    db.session.commit()
    return redirect('/home')

# -------- FAVORITE --------
@app.route('/favorite/<int:id>', methods=['POST'])
def favorite(id):
    note = Note.query.get(id)
    note.favorite = not note.favorite
    db.session.commit()
    return redirect('/home')

# -------- RENAME --------
@app.route('/rename/<int:id>', methods=['POST'])
def rename(id):
    note = Note.query.get(id)
    note.title = request.form['new_title']
    db.session.commit()
    return redirect('/home')

# -------- RUN --------
if __name__ == '__main__':
    app.run(debug=True)