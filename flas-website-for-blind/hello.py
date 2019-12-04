#pip install Flask-gTTS

    # return render_template('aliveReport.html', marks = score)
# def result():
#     dict = {'phy':50,'che':60,'maths':70}
#     return render_template('liveReport.html', result = dict)

# from flask import Flask, render_template, request
# app = Flask(__name__)
#
# @app.route('/')
# def student():
#    return render_template('liveReport.html')
#
# @app.route('/result',methods = ['POST', 'GET'])
# def result():
#    if request.method == 'POST':
#       result = request.form
#       return 'test server ok'
#       # print(result)
#       #
#       # return render_template("result.html",result = result)
#
# if __name__ == '__main__':
#    app.run(debug = True)
#########################################
from flask import Flask
import os
import subprocess

UPLOAD_FOLDER = '/home/abc/abhi/flask'

app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
import os,sys
import subprocess
#import magic
import urllib.request
# from app import app
from flask import Flask, flash, request, redirect, render_template
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
# ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
###########################################################################
###########################################################################





###########################################################################
###########################################################################
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def upload_form():
    return render_template('liveReport.html')

@app.route('/', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part << python server')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            print(file.filename)
            print("file.filename")
            flash('No file selected for uploading << python server')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('File successfully uploaded  /// img processing /// << python server ')
            # os.system("x.py")
            print("[]",filename)
            subprocess.Popen("python3 imgPROS.py", shell=True)
            # subprocess.Popen("python3 x.py 1", shell=True)
            print("[]","going to img process")

            return redirect('/')
            # NO CODE WILL WORKE BELOW HEAR !!
        else:
            flash('Allowed file types are png,jpg,jpeg,gif !! << python server')
            return redirect(request.url)

if __name__ == "__main__":
    # app.run(debug = True)
    app.run(host = '0.0.0.0',port=5001)
