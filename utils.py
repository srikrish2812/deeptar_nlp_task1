import nltk
from nltk import sent_tokenize, word_tokenize, pos_tag

def analyze_each_text(text):
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