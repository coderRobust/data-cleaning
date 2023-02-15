from flask import Flask, request, render_template
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from collections import Counter

app = Flask(__name__)

# Route for the homepage


@app.route('/')
def index():
    return render_template('index.html')

# Route for the data cleaning


@app.route('/clean', methods=['POST'])
def clean():
    # Get the user input text from the form
    data = request.form['text']

    # Convert text to lowercase
    data = data.lower()

    # Remove numbers and special characters
    data = re.sub(r'\d+', '', data)
    data = re.sub(r'[^\w\s]', '', data)

    # Tokenize and lemmatize text using NLTK
    lemmatizer = WordNetLemmatizer()
    tokens = nltk.word_tokenize(data)
    tokens = [lemmatizer.lemmatize(token) for token in tokens]

    # Remove stopwords using NLTK
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if not token in stop_words]

    # Remove tokens that are not alphabetic
    tokens = [token for token in tokens if token.isalpha()]

    # Remove tokens that are only one character long
    tokens = [token for token in tokens if len(token) > 1]

    # Remove common words using a frequency distribution
    freq_dist = Counter(tokens)
    common_words = freq_dist.most_common(10)
    common_words = [word[0] for word in common_words]
    tokens = [token for token in tokens if not token in common_words]

    # Join tokens into cleaned text
    cleaned_text = ' '.join(tokens)

    # Return the cleaned text to the results page
    return cleaned_text


if __name__ == '__main__':
    app.run(debug=True)
