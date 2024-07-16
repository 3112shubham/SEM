from flask import Flask, render_template, request, redirect, url_for
import os
import easyocr
import requests
import re
import pandas as pd
import csv
import cv2
from model import mod,value
from utils.maps import gen,loc,med,pol,dia,pla,spe,mapss

def extract(text):
    da = {}
    b = ""
    data = ["PolicyHolder ID","Age","Gender","Location","Medical History","Policy Type","Procedure Code","Diagnosis Codes","Treatment Cost","Place Of Service","Provider ID","Specialization"]
    ma = ["Gender","Location","Medical History","Policy Type","Diagnosis Codes","Place Of Service","Specialization"]
    for match in text:
        if b != "" :
            if(b in ma):
                da[b]=mapss[b][match]
            else:
                da[b]=match
            b = ""
        else :
            if(match in data):
                b = match
            else:
                b = ""

    return mod(da)

def ocr(img):
    reader = easyocr.Reader(['en'],gpu=True)
    result = reader.readtext(img,detail=0)
    result = extract(result)
    return result

app = Flask(__name__, static_url_path='/static')

# Set the upload folder
UPLOAD_FOLDER = os.path.join('static', 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Allowed extensions for file upload
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Function to check if the file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Route for the home page
@app.route('/')
def home():
    return render_template('index.html')

# Route for handling file upload
@app.route('/upload', methods=['POST'])
def upload_file():
    # Check if a file was submitted
    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']

    # If the user does not select a file, the browser submits an empty file without a filename
    if file.filename == '':
        return redirect(request.url)

    # If the file exists and has the allowed extension
    if file and allowed_file(file.filename):
        # Save the file to the uploads folder
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        p = ocr('static/uploads/'+filename)
        return render_template('resultPage.html',prob=p[0],prediction=p[1])

    return 'Invalid file format'

if __name__ == '__main__':
    app.run(debug=True)

