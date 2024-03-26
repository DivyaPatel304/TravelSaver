from flask import Flask, jsonify, request
import random
import wikipedia

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

# @app.route('/get-fact/<place_name>', methods=['GET'])
# def get_fact(place_name):
#     place_name = place_name.split()[-1]
#     fact = generate_place_fact(place_name)
#     fulfillmentText = f"Here's an interesting fact about {place_name}: {fact}"
#     return jsonify({"fulfillmentText": fact})

@app.route('/webhook', methods=['POST'])
def get_fact(place_name):
    place_name = place_name.split()[-1]
    fact = generate_place_fact(place_name)
    fulfillmentText = f"Here's an interesting fact about {place_name}: {fact}"
    # return jsonify({"fulfillmentText": fulfillmentText})

    return jsonify({"fulfillmentText": fact})

if __name__ == '__main__':
    app.run(debug=True)
