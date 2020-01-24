import os
import re
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer, TfidfTransformer
import pandas as pd

def KeywordSearchTFIDF(keyword):
    #get overall text
    #get individual text for year
    #tfidf
    #ppmi
    #return these datas
    
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
    
    keyword_year_values = dict()
    
    for year in years_dict.keys():
        doc = years_dict[year]
        tf_idf_vector=tfidf_transformer.transform(cv.transform([doc]))
        
        df = pd.DataFrame(tf_idf_vector.toarray(), columns = cv.get_feature_names())
        
        if keyword in df.columns:
            keyword_value = df[keyword].iloc[0]
        
            keyword_year_values[year] = keyword_value
        else: 
            return "No results found"
        
    return keyword_year_values
    
def KeywordSearchPPMI(keyword):
    print("tbd")
    
def KeywordSearchRawFrequency(keyword):
    print("tbd")