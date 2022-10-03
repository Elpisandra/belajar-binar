# Import library for ReGex, SQLite, and Pandas
import re
import sqlite3
from tkinter.tix import COLUMN
import pandas as pd

# Import library for Flask
from flask import Flask, jsonify
from flask import request
from flasgger import Swagger, LazyString, LazyJSONEncoder
from flasgger import swag_from

# Define Swagger UI description
app = Flask(__name__)
app.json_encoder = LazyJSONEncoder
swagger_template = dict(
info = {
    'title': LazyString(lambda: 'API Documentation for Data Processing and Modeling'),
    'version': LazyString(lambda: '1.0.0'),
    'description': LazyString(lambda: 'Dokumentasi API untuk Data Processing dan Modeling'),
    },
    host = LazyString(lambda: request.host)
)
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'docs',
            "route": '/docs.json',
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/docs/"
}
swagger = Swagger(app, template=swagger_template,             
                  config=swagger_config)

# Connect to db
conn = sqlite3.connect('data/contoh.db', check_same_thread=False)

# Define and execute query for create table "data" if not exist
# Table "Data" contains "text" coloumn and "text_clean" coloumn. The two columns have "varchar" data type
conn.execute('''CREATE TABLE IF NOT EXISTS data (text varchar(100), text_clean varchar(100));''')

# Define endpoint for "input teks via form"
@swag_from("docs/contoh_text.yml", methods=['POST'])
@app.route('/Text_Processing', methods=['POST'])
def text_processing():

    # Get text file
    text = request.form.get('text')
    
    # Cleansing Process. Remove "Emoticon" and "Punctuation"
    text_clean = re.sub(r"@\S+","",text)
    text_clean1 = re.sub(r"#\S+","",text_clean)
    text_clean2 = re.sub(r"http[s]?\://\S+","",text_clean1)
    text_clean3 = re.sub(r'[^0-9a-zA-Z]+','', text_clean2)
    text_clean4 = re.sub(r"\s"," ",text_clean3)
    text_clean5 = re.sub(r"RT","", text_clean4)
    text_clean6 = re.sub(r"USER","", text_clean5)
    text_clean7 = re.sub(r"\n","",text_clean6)
    text_clean8 = re.sub(r"URL","",text_clean7)

    # Define and execute query for insert original text and cleaned text to sqlite database
    conn.execute("INSERT INTO data (text, text_clean) VALUES ('" + text + "', '" + text_clean8 + "')")
    conn.commit()

    # Define API response
    json_response = {
        'status_code': 200,
        'description': "Teks yang sudah diproses",
        'data': text_clean8,
    }
    response_data = jsonify(json_response)
    return response_data

#Define endpoint for "input File via form"
@swag_from("docs/r_csv.yml", methods=['POST'])
@app.route('/File_Processing', methods=['POST'])
def file_processing():

    # Get CSV file
    file = request.files['file']
    data = str(pd.read_csv(file, encoding='iso-8859-1'))
    
    # Cleansing Process. Remove "Emoticon" and "Punctuation"
    text_clean = re.sub(r"\s"," ",data)
    text_clean1 = re.sub(r"([@#][A-Za-z0-9_]+)","",text_clean)
    text_clean2 = re.sub(r"\n","",text_clean1)
    text_clean3 = re.sub(r'((www\.[^\s]+)|(https?://[^\s]+)|(http?://[^\s]+))','',text_clean2)
    text_clean4 = re.sub(r'  +', '', text_clean3)
    text_clean5 = re.sub(r'[^0-9a-zA-Z]+', '', text_clean4)
    text_clean6 = re.sub(r"RT","", text_clean5)
    text_clean7 = re.sub(r"USER\s","", text_clean6)
    text_clean8 = re.sub(r"URL\s","", text_clean7)

    # Define and execute query for insert original text and cleaned text to sqlite database
    conn.execute("INSERT INTO data (text, text_clean) VALUES ('" + data + "', '" + text_clean8 + "')")
    conn.commit()

    # Define API response
    json_response = {
        'status_code': 200,
        'description': "Teks yang sudah diproses",
        'data': text_clean8,
    }
    response_data = jsonify(json_response)
    return response_data

if __name__ == '__main__':
   app.run()