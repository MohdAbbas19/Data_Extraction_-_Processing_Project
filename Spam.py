from flask import Flask,render_template,url_for,request
import pandas as pd 
import pickle
import re
import string
from flask import Flask, request, render_template

app = Flask(__name__)
model = pickle.load(open('Modelf2_1.pkl', 'rb'))
vecter = pickle.load(open('Modef2_2.pkl', 'rb'))

def process_text(text):
    # Convert to lowercase
    text = text.lower()
    # Remove square brackets
    text = re.sub('\[.\]', '', text)
    # Remove non-word characters (symbols, punctuation)
    text = re.sub("\\W", " ", text)
    # Remove URLs
    text = re.sub('https?://\S+|www\.\S+', '', text)
    # Remove HTML tags
    text = re.sub('<.*?>+', '', text)
    # Remove punctuation
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    # Remove newline characters
    text = re.sub('\n', '', text)
    # Remove words containing numbers
    text = re.sub('\w*\d\w*', '', text)
    return text

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/predict', methods=['POST'])
def get_data():
    try:
        if request.method == 'POST':
             text = str(request.form.get('News'))
             processed_text = process_text(text)
             a = vecter.transform([processed_text])
             var = model.predict(a)[0]
             return render_template("home.html",data=var)

    except Exception as e:
        return str(e)

if __name__ == '__main__':
    app.run(debug=True)


