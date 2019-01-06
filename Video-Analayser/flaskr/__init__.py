import os
from flask import (Flask, flash, render_template, request, redirect, url_for)
from werkzeug.utils import secure_filename

from VideoStitcher import video_to_frames

UPLOAD_FOLDER = 'uploads/'
APP_FOLDERS = ['Frames/']
ALLOWED_EXTENSIONS = set(['mp4'])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def create_app(test_config=None):
    # Create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        UPLOAD_FOLDER=UPLOAD_FOLDER,
        APP_FOLDERS=APP_FOLDERS,
        # DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite')
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test confign if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        if not(os.path.isdir(app.instance_path)):
            os.makedirs(app.instance_path)
        for di in app.config['APP_FOLDERS']:
            if not(os.makedirs(di)):
                os.makedirs(di)

    except OSError as e:
        print(e)
        pass

    # a simple page that says hello
    @app.route('/upload', methods=('GET', 'POST'))
    def upload():
        if request.method == 'POST':
            # check if the post request has the file part
            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)
            file = request.files['file']
            # if user does not select file, browser also
            # submit an empty part without filename
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                results = video_to_frames.FrameCapture(file_path)
                return render_template('stitchedImage.html.j2', stitchedImage=results['save_path'])

        return render_template('upload.html.j2')

    @app.route('/image', methods=['GET'])
    def showImage():
        return render_template('stitchedImage.html.j2', stitchedImage='stitched.png')

    return app
