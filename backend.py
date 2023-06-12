import json
import requests

from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api', methods=['POST'])
def process_request():
    # Extract request data
    request_data = request.json
    prompt = request_data.get('prompt')

    # Make API call to OpenAI Completion API
    completion_api_url = 'https://api.openai.com/v1/completions'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer  <TOKEN>'
    }
    data = {
        'prompt': prompt,
        'max_tokens': 100,
        'temperature': 0.8
    }
    response = requests.post(completion_api_url, headers=headers, data=json.dumps(data))
    print ("Response from OpenAI=",response);
    response_data = response.json()


    # Extract relevant information from OpenAI response
    completion_text = response_data['choices'][0]['text']
    parsed_data = json.loads(completion_text)

    # Prepare and return the response
    response = {
        'vin': parsed_data.get('vin'),
        'make': parsed_data.get('make'),
        'model': parsed_data.get('model'),
        'trim': parsed_data.get('trim'),
        'body_style': parsed_data.get('body_style'),
        'dealer': {
            'name': parsed_data.get('dealer', {}).get('name')
        }
    }
    return jsonify(response), 200

if __name__ == '__main__':
    app.run()
