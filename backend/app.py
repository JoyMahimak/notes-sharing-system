from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash
import os

app = Flask(__name__)
app.secret_key = "secretkey"

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# HOME (READ)
@app.route('/')
def home():
    files = os.listdir(UPLOAD_FOLDER)
    return render_template('index.html', files=files)

# UPLOAD (CREATE)
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash("No file selected")
            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':
            flash("No file selected")
            return redirect(request.url)

        file.save(os.path.join(UPLOAD_FOLDER, file.filename))
        flash(f"{file.filename} uploaded successfully!")

        return redirect(url_for('home'))

    return render_template('upload.html')

# DOWNLOAD
@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)

# DELETE
@app.route('/delete/<filename>')
def delete_file(filename):
    path = os.path.join(UPLOAD_FOLDER, filename)

    if os.path.exists(path):
        os.remove(path)
        flash(f"{filename} deleted successfully!")
    else:
        flash("File not found")

    return redirect(url_for('home'))

# UPDATE (RENAME)
@app.route('/rename/<old_name>', methods=['POST'])
def rename_file(old_name):
    new_name = request.form['new_name']

    old_path = os.path.join(UPLOAD_FOLDER, old_name)
    new_path = os.path.join(UPLOAD_FOLDER, new_name)

    if os.path.exists(old_path):
        os.rename(old_path, new_path)
        flash(f"{old_name} renamed to {new_name}")
    else:
        flash("File not found")

    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)