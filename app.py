import os
from flask import (Flask, request, redirect, url_for,
                   render_template, session, send_from_directory, abort)
from markupsafe import escape
from werkzeug.utils import secure_filename
import json
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
IMAGE_FOLDER = os.getcwd() + "/static/uploads"
app = Flask(__name__)

# CHANGE THESE DURING PRODUCTION
json_data = open('config.json')
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
PASSWORD = json.load(json_data)["password"]


app.config["IMAGE_UPLOADS"] = IMAGE_FOLDER

# Used get_all_files() to find file to delete in the index ("/") route.


def get_all_files(active_dir):
    '''Looks for all files of in root directory, and all subdirectories. Returns a list of file names'''
    all_file_paths = []
    for path, dirs, files in os.walk(active_dir):
        for f in files:
            if f in all_file_paths:
                pass
            else:
                all_file_paths.append(f)

    return all_file_paths


def get_all_dirs(active_dir):
    '''Takes active directory and returns all subdirectories. Example argument: /Users/your_pc/chosen_dir'''
    for path, dirs, files in os.walk(active_dir):
        return dirs


@app.route("/")
def index():
    if not session:
        return redirect(url_for('login'))
    '''Home Page. Should show all uploaded files.'''
    return render_template('partials/index.html', images=get_all_files(IMAGE_FOLDER))


@app.route("/login", methods=['GET', 'POST'])
def login():
    '''Shows login form and handles creating user.'''
    if request.method == 'POST':
        if request.form['password'] == PASSWORD:
            session["username"] = "User"
            return redirect(url_for('index')
                            )
        return render_template('partials/login.html', error="Invalid Password")

    return render_template('partials/login.html')


@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route("/upload", methods=["GET", "POST"])
def upload_image():
    '''Shows image upload form, and posts selected image to the uploads folder.'''
    if request.method == "POST":
        if request.files:
            f = request.files["file"]
            filename = f.filename

            if filename == '':
                return render_template('partials/upload.html', error="Please enter a file to upload")

            if filename not in get_all_files(IMAGE_FOLDER):
                f.save(os.path.join(
                    app.config["IMAGE_UPLOADS"], filename))
                return redirect(filename)

            if filename in get_all_files(IMAGE_FOLDER):
                return render_template('partials/upload.html', error="File already exists")

    return render_template('/partials/upload.html')


@app.route("/download/<filename>", methods=["GET", "POST"])
def download_file(filename):
    if request.method == "POST":
        try:
            return send_from_directory(IMAGE_FOLDER, filename, as_attachment=True)
        except FileNotFoundError:
            abort(404)

    return render_template("partials/download-confirmation.html", filename=filename)


@app.route("/delete/<image>", methods=["GET", "POST"])
def delete_image(image):
    if request.method == "POST":
        if image in os.listdir(IMAGE_FOLDER):
            os.remove(os.path.join(IMAGE_FOLDER, image))
            return redirect(url_for('index'))

        if image not in os.listdir(IMAGE_FOLDER):
            return render_template('partials/error-page.html', error="File not found")

    return render_template('partials/delete-confirmation.html', image=image)


@app.route("/<filename>")
def show_file(filename):
    return render_template('partials/image-card.html', filename=filename)


@app.route("/README.html")
def readme():
    return render_template('partials/readme.html')
