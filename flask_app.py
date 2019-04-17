import os
from flask import Flask, flash, request, redirect, url_for, send_from_directory, render_template
from werkzeug.utils import secure_filename
import exiftool
import json



app = Flask(__name__)
UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'dll', 'exe'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return render_template('./upload.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    file = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    #access file

    #exif

    with exiftool.ExifTool() as et:
        metadata = json.dumps(et.get_metadata_batch([file]))
    print(metadata)
    os.remove(file)
    return render_template('./result.html', metadata= metadata)
    #send_from_directory(app.config['UPLOAD_FOLDER'], filename)