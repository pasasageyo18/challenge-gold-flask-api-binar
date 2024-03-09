import re
import pandas as pd
from flask import Flask, jsonify, request
from flasgger import Swagger
from flasgger import swag_from
app = Flask(__name__)

swagger = Swagger(app)

ALLOWED_EXTENSIONS = {'txt'}

@app.route("/cleanse", methods=["POST"])
@swag_from("docs/textProcessing.yaml", methods=['POST'])
def cleanse_data():
    try:
        text = request.form.get('text')
        cleanedSym = re.sub(r'[^a-zA-Z0-9]', ' ', text)
        removingURL = re.sub('http\S+', ' ', cleanedSym)
        upperToLowerCase = re.sub(r'.', lambda match: match.group(0).lower(), removingURL)
        removingWhitespace = re.sub(r"\s+", "", upperToLowerCase)
        
        json_response = {
            'status_code': 200,
            'description': "Original Teks",
            'removing symbol in text': cleanedSym,
            'removing url in text': removingURL,
            'uppercase to lowercase in text': upperToLowerCase,
            'removing whitespace in text': removingWhitespace,
        }

        response_data = jsonify(json_response)
        return response_data
    except Exception as e:
        return jsonify({'error': str(e)})


@app.route("/cleanseFile", methods=["POST"])
@swag_from("docs/fileTextProcessing.yaml", methods=['POST'])
def cleanse_file_data():
    try:
        if 'file' in request.files:
            file = request.files['file']
            if file.filename != '':
                text = file.read().decode('utf-8')
            json_response = {
                'status_code': 200,
                'description': "Original Teks",
                'removing symbol in text': re.sub(r'[^a-zA-Z0-9]', ' ', text),
                'removing url in text': re.sub('http\S+', '', text)
            }

        response_data = jsonify(json_response)
        return response_data
    except Exception as e:
        return jsonify({'error': str(e)})


if __name__ == '__main__':
    app.run(debug=True)
