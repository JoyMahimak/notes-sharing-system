from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Database setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# 👤 User Model (FIXED ✅ for pytest)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(200))

# 📄 Notes Model
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    filename = db.Column(db.String(100))

# Upload folder
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Create DB
with app.app_context():
    db.create_all()

# 🔐 LOGIN PAGE
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == "admin" and password == "admin@123":
            return redirect(url_for('home'))
        else:
            return "Invalid credentials!"

    return render_template('login.html')


# 🏠 HOME PAGE
@app.route('/home')
def home():
    notes = Note.query.all()
    return render_template('index.html', notes=notes)


# 📤 UPLOAD NOTE
@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    title = request.form['title']

    if file:
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

        note = Note(title=title, filename=file.filename)
        db.session.add(note)
        db.session.commit()

    return redirect(url_for('home'))


# 📥 DOWNLOAD NOTE
@app.route('/uploads/<filename>')
def download_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)


# ❌ DELETE NOTE
@app.route('/delete/<int:id>')
def delete(id):
    note = Note.query.get(id)

    if note:
        file_path = os.path.join(UPLOAD_FOLDER, note.filename)

        if os.path.exists(file_path):
            os.remove(file_path)

        db.session.delete(note)
        db.session.commit()

    return redirect(url_for('home'))


# ▶️ RUN APP
if __name__ == '__main__':
    app.run(debug=True)