from flask import Flask, jsonify, request
import random
import wikipedia
import subprocess

app = Flask(__name__)

def generate_place_fact(place_name):
    try:
        # Get the Wikipedia page for the place
        page = wikipedia.page(place_name)

        # Extracting a random sentence from the summary for simplicity
        summary_sentences = page.summary.split(".")
        fact = random.choice(summary_sentences)

        return fact.strip()

    except wikipedia.exceptions.PageError:
        return "Sorry, I couldn't find any information about that place."
    except wikipedia.exceptions.DisambiguationError:
        return "It seems there are multiple meanings for that place. Please be more specific."

@app.route('/', methods=['GET'])
def get_student_number():
    return jsonify({"student_number": "200538095"})

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json()
    query_text = req.get('queryResult').get('queryText')

    # Extract the place name from the query text
    place_name = query_text.split('about')[-1].strip()

    # Run the script with subprocess and get the output
    process = subprocess.Popen(['python', 'fetch_facts.py', place_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    # Return the output as the fulfillment text
    fulfillmentText = stdout.decode("utf-8")
    
    return jsonify({"fulfillmentText": fulfillmentText})

if __name__ == '__main__':
    app.run(debug=True)
