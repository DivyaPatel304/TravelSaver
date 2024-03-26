from flask import Flask, jsonify, request
import random
from nltk.corpus import wordnet
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import wikipedia
import nltk
import re

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

def preprocess_text(text):
    stop_words = set(stopwords.words('english'))
    # Remove special characters and numbers
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    # Tokenize the text
    words = word_tokenize(text)
    # Remove stopwords
    filtered_words = [w.lower() for w in words if w.lower() not in stop_words]
    return filtered_words

def generate_place_fact(place_name):
    try:
        # Get the Wikipedia page for the place
        page = wikipedia.page(place_name)

        # Tokenize the content into sentences
        sentences = sent_tokenize(page.content)

        # Preprocess the sentences
        preprocessed_sentences = [preprocess_text(sentence) for sentence in sentences]

        # Flatten the list of sentences into a list of words
        all_words = [word for sentence in preprocessed_sentences for word in sentence]

        # Select a random word from the processed text
        random_word = random.choice(all_words)

        # Get synonyms for the random word
        synonyms = get_synonyms(random_word)

        # Select a random synonym
        random_synonym = random.choice(synonyms)

        # Generate a fact using the random synonym
        fact = f"{random_synonym.capitalize()} is a synonym of {random_word.capitalize()}."

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
    query_text = req.get('queryResult').get('queryText')

    # Extract the location name from the query text
    if 'to' in query_text:
        place_name = query_text.split('to')[1].strip()
    else:
        place_name = query_text

    fact = generate_place_fact(place_name)
    fulfillmentText = f"Here's an interesting fact about {place_name}: {fact}"

    return jsonify({"fulfillmentText": fulfillmentText})

if __name__ == '__main__':
    app.run(debug=True)
