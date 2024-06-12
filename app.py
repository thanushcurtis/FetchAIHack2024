from flask import Flask, jsonify, request  # Import Flask and its necessary modules
from flask_cors import CORS  # Import CORS for handling Cross-Origin Resource Sharing
from uagents.query import query  # Import the query function from uagents
from uagents import Model  # Import Model from uagents for defining request and response models
import json  # Import json for handling JSON data


app = Flask(__name__)
CORS(app)  

analysis_address = 'agent1qvshnse5680dlthrzygny3y9nvvvvsdl8t7hr6f78jy3d59645j8qateu70!'

class analysisRequest(Model):
    request: str

class analysisResponse(Model):
    response: str


@app.route('/')
def home():
    return "Welcome to the Document Analysis API!"


@app.route('/query/<string:request>', methods=['GET'])
async def get_details(request):
    response = await query(destination=analysis_address, message=analysisRequest(request=request), timeout=60.0)
    data = json.loads(response.decode_payload())
    print(data)
    return data


if __name__ == '__main__':
    app.run(debug=True)
