from flask import Flask, render_template, request, redirect, url_for
import pandas as pd

import os

import mysql.connector

app = Flask(__name__)

app.config['DEBUG'] = True

UPLOAD_FOLDER = 'uploads'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "",
    database = "exceldb"
)

mycursor = mydb.cursor()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods = ['POST'])
def UploadFiles():
    
    uploaded_file = request.files['file']

    if uploaded_file.filename != "":
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
        uploaded_file.save(file_path)
        parseCSV(file_path)
    
    return redirect(url_for("index"))

def parseCSV(filePath):
    col_names = ['Name', 'Age', 'Country']

    csvData = pd.read_csv(filePath, names=col_names, header=None)

    for i,row in csvData.iterrows():
        sql = "INSERT INTO users (Name, Age, Country) VALUES (%s, %s, %s)"
        value = (row['Name'], row['Age'], row['Country'])
        mycursor.execute(sql, value)
        mydb.commit()

if __name__ == "__main__":
    app.run(port = 5000)