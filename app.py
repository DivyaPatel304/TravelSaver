from flask import Flask, jsonify, request
import random
from nltk.corpus import wordnet
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import wikipedia
import nltk

nltk.download('wordnet')
nltk.download('stopwords')
nltk.download('punkt')

app = Flask(__name__)

def get_synonyms(word):
    synonyms = []
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            synonyms.append(lemma.name())
    return synonyms

def generate_place_fact(place_name):
    try:
        # Get the Wikipedia page for the place
        page = wikipedia.page(place_name)

        # Tokenize the content into sentences
        sentences = sent_tokenize(page.content)

        # Remove stopwords from the sentences
        stop_words = set(stopwords.words('english'))
        filtered_sentences = []
        for sentence in sentences:
            word_tokens = word_tokenize(sentence)
            filtered_sentence = [w for w in word_tokens if not w.lower() in stop_words]
            filtered_sentences.append(' '.join(filtered_sentence))

        # Select a random fact
        fact = random.choice(filtered_sentences)

        return fact

    except wikipedia.exceptions.PageError:
        return "Sorry, I couldn't find any information about that place."
    except wikipedia.exceptions.DisambiguationError:
        return "It seems there are multiple meanings for that place. Please be more specific."

@app.route('/', methods=['GET'])
def get_student_number():
    return jsonify({"student_number": "200538095"})

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    fulfillmentText = ''
    query_result = req.get('queryResult')
    if query_result.get('action') == 'input.location':
        place_name = query_result.get('queryText')
        fact = generate_place_fact(place_name)
        fulfillmentText = f"Here's an interesting fact about {place_name}: {fact}"

    return jsonify({"fulfillmentText": fulfillmentText})

if __name__ == '__main__':
    app.run(debug=True)
