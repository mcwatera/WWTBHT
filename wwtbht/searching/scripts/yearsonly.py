import os
import re
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer, TfidfTransformer
import pandas as pd
import numpy as np
from collections import Counter

def YearSearchTFIDF(year):
    
    dirname = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '.', 'clean_text'))
    all_files = os.listdir(dirname)
    
    all_text = ""
    years_dict = dict()
    
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
    
    #select year and get the tfidf for that year
    #return top 10 terms and their values
    
    doc = years_dict[year]
    tf_idf_vector=tfidf_transformer.transform(cv.transform([doc]))
    
    df = pd.DataFrame(tf_idf_vector.toarray(), columns = cv.get_feature_names())
    
    word_value_dict = dict()
    
    for (columnName, columnData) in df.iteritems():
        word = columnName
        value = df[word].iloc[0]
        word_value_dict[word] = value
        
    word_value_counter = Counter(word_value_dict)
    
    top_15 = word_value_counter.most_common(15)
    
    # Python code to convert into dictionary 
    def Convert(tup, di): 
        di = dict(tup) 
        return di 
          
    # Driver Code 
    dictionary = dict()
    final_dict = Convert(top_15, dictionary)
    
    return final_dict
    
        
    