import os
from flask import Flask, request, redirect, url_for, render_template, session
from markupsafe import escape
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
IMAGE_FOLDER = os.getcwd() + "/static/uploads"
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config["IMAGE_UPLOADS"] = IMAGE_FOLDER

# Used get_all_files() to find file to delete in the index ("/") route.


def get_all_files_by_user(active_dir):
    '''Looks for all files of in root directory, and all subdirectories. Returns a list of file names'''
    all_file_paths = []
    for path, dirs, files in os.walk(active_dir):
        for f in files:
            if f in all_file_paths:
                pass
            elif session['username'] in path:
                all_file_paths.append(f)
    return all_file_paths


def get_all_dirs(active_dir):
    '''Takes active directory and returns all subdirectories. Example argument: /Users/your_pc/chosen_dir'''
    for path, dirs, files in os.walk(active_dir):
        return dirs


@app.route("/")
def index():
    '''Home Page. Should show all uploaded files.'''
    data = {"images": get_all_files_by_user(
        IMAGE_FOLDER)}
    return render_template('partials/index.html', data=data)


@app.route("/README.html")
def readme():
    return render_template('partials/README.html')


@app.route("/login", methods=['GET', 'POST'])
def login():
    '''Shows login form and handles creating user.'''
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index')
                        )
    return render_template('partials/login.html')


@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route("/upload-image", methods=["GET", "POST"])
def upload_image():
    '''Shows image upload form, and posts selected image to the uploads folder.'''
    if request.method == "POST":
        if request.files:
            image = request.files["image"]
            username = session['username']
            print(get_all_dirs(IMAGE_FOLDER))
            if username not in get_all_dirs(IMAGE_FOLDER):
                os.mkdir(os.path.join(IMAGE_FOLDER, username))
            imagename = username + "/" + image.filename
            if imagename == '':
                return render_template('partials/upload-image.html', error="Please enter a file to upload")
            if imagename not in get_all_files_by_user(IMAGE_FOLDER):
                image.save(os.path.join(
                    app.config["IMAGE_UPLOADS"], imagename))
                return redirect(imagename)
            if imagename in get_all_files_by_user(IMAGE_FOLDER):
                return render_template('partials/upload-image.html', error="File already exists")
    return render_template("partials/upload-image.html")


@app.route("/delete/<username>/<image>", methods=["GET", "POST"])
def delete_image(username, image):
    if request.method == "POST":

        if image in os.listdir(os.path.join(IMAGE_FOLDER, username)):
            os.remove(os.path.join(IMAGE_FOLDER, f"{username}/{image}"))
            return redirect(url_for('index'))

        if image not in os.listdir(os.path.join(IMAGE_FOLDER, username)):
            return render_template('partials/error-page.html', error="File not found")

    return render_template('partials/delete-confirmation.html', image=image)


@app.route("/<username>/<image>")
def show_image(username, image):
    return render_template('partials/image-card.html', username=session['username'], image=image)