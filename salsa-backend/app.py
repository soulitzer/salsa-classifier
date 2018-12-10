#!flask/bin/python

import os, sys
import simplejson
import traceback
from flask import Flask, request
from werkzeug import secure_filename
from flask_cors import CORS, cross_origin
from predictor import predict, GENRES, GENRE_DESCRIPTS
import flask_cors
import numpy as np

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['UPLOAD_FOLDER'] = 'data/'
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['mp3', 'mp4'])
IGNORED_FILES = set(['.gitignore'])

flask_cors.CORS(app, expose_headers='Authorization')

def log(s):
    print(s, file=sys.stderr)

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def gen_file_name(filename):
    i = 1
    while os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], filename)):
        name, extension = os.path.splitext(filename)
        filename = '%s_%s%s' % (name, str(i), extension)
        i += 1
    return filename

@app.route("/process", methods=['POST'])
def process():
    files = request.files['filepond']
    if files:
        filename = secure_filename(files.filename)
        filename = gen_file_name(filename)

        # if not allowed_file(files.filename):
        #     return simplejson.dumps({"status": 0, "result": {}})

        # save file to disk temporarily
        uploaded_file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        files.save(uploaded_file_path)

        # TODO: perform musical analysis
        result = predict(uploaded_file_path)
        print(result)
        predicted_genre = np.argmax(result) # Get max probability

        # example output:
        example = {
            "predicted_class": GENRES[predicted_genre],
            "probability": "{:.2f}".format(result[predicted_genre]),
            "description": GENRE_DESCRIPTS[predicted_genre]
            # "all_probs" : tuple(result)
        }
        result = example

        # Delete uploaded file
        os.remove(uploaded_file_path)

        # Return result as json
        return simplejson.dumps({"status": 1, "result": result})


if __name__ == '__main__':
    app.run(debug=True)
