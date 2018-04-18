from flask import render_template, url_for
from flask import redirect, request, send_from_directory
from werkzeug import secure_filename
from app import app
import subprocess
import os


def colorize(filename):
    """Colorization of grayscale image"""

    app.logger.debug("In function: colorize()")

    cmd = 'optirun python ' + app.config['COLORIZE_PATH'] \
        + ' -img_in ' + os.path.join(app.config['UPLOAD_FOLDER'], filename) \
        + ' -img_out ' \
        + os.path.join(app.config['COLORIZED_FOLDER'], filename)

    devnull = open(os.devnull, 'w')
    subprocess.call(cmd, shell=True, stdout=devnull, stderr=devnull)

    app.logger.debug("Colorization completed!")

    app.logger.debug('Saved file to: ' + os.path.join(
                                    app.config['COLORIZED_FOLDER'],
                                    filename))


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            app.logger.debug('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            app.logger.debug('No selected file')
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            app.logger.debug('Saving file to: ' + os.path.join(
                                            app.config['UPLOAD_FOLDER'],
                                            filename))
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            colorize(filename)
            return redirect(url_for('colorized_file',
                                    filename=filename))

    return render_template('index.html')


@app.route('/colorized_out/<filename>')
def colorized_file(filename):
    """File retrieval from server to user"""

    app.logger.debug("In function: colorized_file()")
    # here we used different config var because send_from_directory
    # uses root as flaskolorization/app/ instead of our root
    # i.e. flaskolorization/
    return send_from_directory(app.config['COLORIZED_FROM_DIR'],
                               filename)
