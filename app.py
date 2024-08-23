import pandas as pd
import nltk
from nltk import sent_tokenize, word_tokenize, pos_tag

from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

class StatisticAnalyzer:
    
    def __init__(self,texts, page_numbers ) -> None:
        self.texts = texts
        self.page_numbers = page_numbers
        self.statistics = []
        
    def analyze_each_text(self, text):
        
        sentences = sent_tokenize(text)
        words = word_tokenize(text)
        pos_tags = pos_tag(words)
        
        
        nouns = []
        verbs = []
        # Findinf nouns and verbs
        for word, tag in pos_tags:
            if tag.startswith('NN'):
                nouns.append(word)
            elif tag.startswith('VB'):
                verbs.append(word)
                
        # finding the average length
        if len(words)>0:
            avg_word_length = sum(len(word) for word in words)/len(words)
        else:
            avg_word_length = 0
                
        num_nouns = len(nouns)
        num_verbs = len(verbs)
        num_sentences = len(sentences)
        num_words = len(words)
        
        return {
            'num_sentences': num_sentences,
            'num_words': num_words,
            'num_verbs': num_verbs,
            'num_nouns': num_nouns,
            'average_word_length': avg_word_length
        }
        
    def analyze_texts(self):
        for i, text in enumerate(self.texts):
            each_text_stats = self.analyze_each_text(text)
            each_text_stats['page_number'] = self.page_numbers[i]
            self.statistics.append(each_text_stats)
        return self.statistics
    
    def save_stats(self, output_file='../statistics/nlp_stats.csv'):
        df = pd.DataFrame(self.statistics)
        df.to_csv(output_file, index=False)
        
        print("Successfully saved statictic to statistics directory")
        
    def aggregate_stats(self, output_file = '../statistics/aggregate_stats.csv' ):
        df = pd.DataFrame(self.statistics)
        aggregated_statistics = df.mean().to_dict()
        aggregated_statistics_df = pd.DataFrame([aggregated_statistics])
        aggregated_statistics_df.to_csv(output_file, index=False)
        
        print("Aggregate statistics saved to statistics directory")
        

@app.route('/')
def home():
    return render_template('./templates/index.html')


@app.route('/analyze_input', methods=["POST"])
def analyzer():
    input_txt = request.form.get('input_text')
    
    aggregated_statistics = pd.read_csv('./statistics/aggregate_stats.csv') 
    
    analyzer = StatisticAnalyzer([input_txt])
    
    input_txt_stats = analyzer.analyze_each_text(input_txt)
    
    comparison = {}
    for key in aggregated_statistics:
        comparison[key] = {
            'Input Text': input_txt_stats[key],
            'Aggregated': aggregated_statistics[key]
        }
        
    return render_template('./templates/comparison.html', comparison=comparison)


if __name__=='__main__':
    app.run(debug=True)