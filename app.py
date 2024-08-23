import pandas as pd
import nltk
from nltk import sent_tokenize, word_tokenize, pos_tag
from utils import analyze_each_text
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)


@app.route('/')
def home():
    """
    Renders the home page of the website
    """
    return render_template('index.html')


@app.route('/analyze_input', methods=["POST"])
def analyzer():
    """
    analyzes the input text written, compares it with the aggregated results
    and displays the results in a new webpage
    """
    input_txt = request.form.get('input_text')
    
    aggregated_statistics = pd.read_csv('./statistics/aggregate_stats.csv').to_dict(orient='records')[0] 
    
    if not input_txt:
        return "No text provided", 400
    else:
        print(input_txt)
    
    input_txt_stats = analyze_each_text(text=input_txt)
    print(input_txt_stats)
    comparison = {
        'num_sentences_input': input_txt_stats['num_sentences'],
        'num_sentences_avg': aggregated_statistics['num_sentences'],
        'num_words_input': input_txt_stats['num_words'],
        'num_words_avg': aggregated_statistics['num_words'],
        'num_nouns_input': input_txt_stats['num_nouns'],
        'num_nouns_avg': aggregated_statistics['num_nouns'],
        'num_verbs_input': input_txt_stats['num_verbs'],
        'num_verbs_avg': aggregated_statistics['num_verbs'],
        'avg_word_length_input': input_txt_stats['average_word_length'],
        'avg_word_length_avg': aggregated_statistics['average_word_length']
    }
            
    return render_template('comparison.html', **comparison)


if __name__=='__main__':
    app.run(debug=True)