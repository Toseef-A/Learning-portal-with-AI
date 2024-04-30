from flask import Flask, request, jsonify, render_template
from openai import AzureOpenAI

app = Flask(__name__)

# Set Azure OpenAI parameters
ENDPOINT = "https://polite-ground-030dc3103.4.azurestaticapps.net/api/v1"
API_KEY = "3ea1fcad-2863-46a5-8660-d92de22cb118"
API_VERSION = "2024-02-01"
MODEL_NAME = "gpt-35-hackathon"

# Initialize Azure OpenAI client
client = AzureOpenAI(
    azure_endpoint=ENDPOINT,
    api_key=API_KEY,
    api_version=API_VERSION,
)

# Function to generate response using Azure OpenAI
def ask_azure_gpt(prompt, client, model_name):
    try:
        completion = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
        )
        return completion.choices[0].message.content
    except Exception as e:
        print("Error:", e)
        return None

@app.route('/')
def index():
    return render_template('Index.html')

@app.route('/query', methods=['POST'])
def handle_query():
    query = request.json['query']
    gpt_response = ask_azure_gpt(query, client, MODEL_NAME)
    # Replace newline characters with <br> tags
    gpt_response = gpt_response.replace('\n', '<br>')
    return jsonify({'response': gpt_response})

@app.route('/story_generator')
def story_generator():
    return render_template('Story.html')

if __name__ == '__main__':
    app.run(debug=True)