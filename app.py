from flask import Flask, render_template, request, redirect, url_for
import os
import easyocr
import requests

def ocr(img):
    reader = easyocr.Reader(['en'])
    result = reader.readtext(img,detail=0)
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
    return render_template('upload.html')

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
        return render_template('result.html',prediction=p)

    return 'Invalid file format'

# Route for displaying the uploaded file
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return render_template('uploaded.html', filename=filename)

if __name__ == '__main__':
    app.run(debug=True)


# from flask import Flask, render_template,request,redirect
# import easyocr
# import requests

# def ocr(img):
#     reader = easyocr.Reader(['en'])
#     result = reader.readtext(img,detail=0)
#     return result

# app = Flask(__name__)

# @app.route('/',methods=['POST','GET'])
# def index():
#     return render_template("index.html")

# @app.route('/upload',methods=['GET','POST'])
# def upload():
#     if request.method == 'POST':
#         if 'file' not in request.files:
#             return redirect(request.url)
#         file = request.files.get('file')
#         if not file:
#             return "Error1"
#         try:
#             img = file.read()
#             prediction = ocr(img)
#             return render_template("result.html", prediction=prediction)
#         except:
#             pass
#     return "Error2"

# @app.route('/print')
# def print():
#     p = "Hello World"
#     return render_template("result.html",prediction = p)

# if __name__ == '__main__':
#    app.run()