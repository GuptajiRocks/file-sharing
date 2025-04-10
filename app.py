import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, send_file, Response
from pymongo import MongoClient
import gridfs
from bson.objectid import ObjectId
from io import BytesIO

#jesus12
load_dotenv()

app = Flask(__name__)

MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["file_db"]
fs = gridfs.GridFS(db)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    if file:
        fs.put(file, filename=file.filename)
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    files = db.fs.files.find().sort("uploadDate", -1)
    return render_template('dashboard.html', files=files)

@app.route('/download/<file_id>')
def download_file(file_id):
    file = fs.get(ObjectId(file_id))
    return Response(file.read(), 
                    mimetype='application/octet-stream',
                    headers={'Content-Disposition': f'attachment;filename={file.filename}'})

if __name__ == '__main__':
    app.run(debug=True)
