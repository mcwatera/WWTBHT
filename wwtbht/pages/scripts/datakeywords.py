import os
import re
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer, TfidfTransformer
import pandas as pd
from collections import OrderedDict
from operator import getitem 

def datakeywords():
    #for each year
    #get tfidf
    #sort tfidf scores
    #print out top terms per year
    
    dirname = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '.', 'clean_text'))
    all_files = os.listdir(dirname)
    
    all_text = ""
    years_dict = dict()
    
    #import files' text by putting individuals in dict and overall in BIG string
    for file in all_files:
        fd = open(os.path.join(dirname, file), 'r')
        
        #get filename as int for dictionary tracking and ease of access
        filename = file[0:4]
        filename = int(filename)
        
        year_text = open(os.path.join(dirname, file),'r').read()
        year_text = "".join(year_text.splitlines())
        
        def preprocess(text):
            text = text.lower()
            text=re.sub("<!--?.*?-->","",text)
            text=re.sub("(\\d|\\W)+"," ",text)
            return text
 
        year_text = preprocess(year_text)
        
        all_text = all_text + year_text
        years_dict[filename] = year_text
        
        fd.close()
        
    cv= CountVectorizer()
    word_count_vector=cv.fit_transform(years_dict.values())
    
    tfidf_transformer=TfidfTransformer(smooth_idf=True,use_idf=True)
    tfidf_transformer.fit(word_count_vector)
    
    feature_names = cv.get_feature_names()
    
    outputdict = dict()
    
    for year in years_dict.keys():
        doc = years_dict[year]
        tf_idf_vector=tfidf_transformer.transform(cv.transform([doc]))
        
        sorted_items=sort_coo(tf_idf_vector.tocoo())
        
        keywords=extract_topn_from_vector(feature_names,sorted_items,15)
        
        outputdict[year] = keywords
        
    return outputdict
        
        
        
def sort_coo(coo_matrix):
    tuples = zip(coo_matrix.col, coo_matrix.data)
    return sorted(tuples, key=lambda x: (x[1], x[0]), reverse=True)
    
def extract_topn_from_vector(feature_names, sorted_items, topn=15):
    """get the feature names and tf-idf score of top n items"""
    
    #use only topn items from vector
    sorted_items = sorted_items[:topn]
 
    score_vals = []
    feature_vals = []
    
    # word index and corresponding tf-idf score
    for idx, score in sorted_items:
        
        #keep track of feature name and its corresponding score
        score_vals.append(round(score, 3))
        feature_vals.append(feature_names[idx])
 
    #create a tuples of feature,score
    #results = zip(feature_vals,score_vals)
    results = {}
    for idx in range(len(feature_vals)):
        results[feature_vals[idx]]=score_vals[idx]
    
    return results
        
    