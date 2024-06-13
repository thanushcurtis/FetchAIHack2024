from flask import Flask, jsonify, request  # Import Flask and its necessary modules
from flask_cors import CORS  # Import CORS for handling Cross-Origin Resource Sharing
from uagents.query import query  # Import the query function from uagents
from uagents import Model  # Import Model from uagents for defining request and response models
import json  # Import json for handling JSON data


app = Flask(__name__)
CORS(app)  

analysis_address = 'agent1qtzlyzgh4wezr86s96j56zkdjrzuyylkegdp7egpkfqys4kpvf3c5hm0cnx'

class documentAnalysis(Model):
    request: str

class documentAnalysisResponse(Model):
    response: str


@app.route('/')
def home():
    return "Welcome to the Document Analysis API!"


@app.route('/query/', methods=['GET'])
async def get_details():
    response = await query(destination=analysis_address, message=documentAnalysis(request='Hello message'), timeout=60.0)
    print(response)
    data = json.loads(response.decode_payload())
    print(data)
    return data



if __name__ == '__main__':
    app.run(debug=True)
