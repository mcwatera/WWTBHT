#!/usr/bin/env python
# -*- coding: utf-8 -*-
#todo: stop words and symbols are mucking things up
import os
import os.path
import nltk
import operator
from nltk import word_tokenize
import collections
import math
import sklearn
import sklearn.cluster
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from collections import OrderedDict
from sklearn.feature_extraction.text import TfidfVectorizer


def ppmitopwords():
	d = os.getcwd()
	
	stupid_symbols = ["(", ")", ".", ",", "'s", "``", "''", "'", "n't", ": ", ";", "?"]
	common_words_to_ignore = ["walt", "whitman", "mr", "and", "own", "thy", "thee"]
	
	#import docs into program, placing each in dictionary with content as the key
	
	docs_dict = {}
	the_big_corpus = ""
	
	path = 'pages/scripts/ppmi/source_text/'
	
	path = os.path.join(d, path)
	
	for filename in os.listdir(path):
		with open(os.path.join(path, filename)) as currentfile:
			current_file = currentfile.read()
			current_file = current_file.replace('xml', '')
			for word in stupid_symbols:
				current_file = current_file.replace(word, '')
			for word in common_words_to_ignore:
				current_file = current_file.replace(word, '')
			#current_file = current_file.decode('utf-8')
			the_big_corpus = the_big_corpus + current_file
			docs_dict[current_file] = filename
	
	#change to numbers so I can print in order of years, otherwise it comes out out of order and I'm picky.
	for now in docs_dict.keys():
		filename = docs_dict[now]
		filename = filename.replace('.txt', '')
		file_number = int(filename)
		docs_dict[now] = file_number
	
	#ppmi
	print("------------------PMI RESULTS, TOP 10 WORDS PER YEAR-----------------------\n")
		
	raw_matrix_words = []
	raw_matrix_counts = []
	token_to_index = {}
	#raw counts of words into matrix, put tokens in raw_matrix_words to create matrix of words
	for key in docs_dict.keys():
		tokens_dict = {}
		content = key
		tokens = word_tokenize(content)
		raw_matrix_words.append(tokens)
	#get raw token count
	for token_set in raw_matrix_words:
		counter_dict = {}
		for token in token_set:
			counter_dict[token] = 0
		for token in token_set:
			counter_dict[token] = counter_dict[token] + 1
		list_for_tokens_tups = []
		for word in counter_dict.keys():
			word_tup = (word, counter_dict[word])
			list_for_tokens_tups.append(word_tup)
		raw_matrix_counts.append(list_for_tokens_tups)
	#now the raw_matrix_counts contains an entry for each list of tuples, for alignment
	#idea, don't make a matrix, for each doc find entire sum, find sum of all matching words in lists, work from there...
	total = 0	#sum of full 'matrix' starts here
	for a_list in raw_matrix_counts:
		for a_tup in a_list:
			total = total + a_tup[1]
	
	#now get each column (word)
	word_dict = {}   #represent sum of columns
	the_big_tokens = word_tokenize(the_big_corpus)
	for a_list in raw_matrix_counts:
		for a_tup in a_list:
			word = a_tup[0]
			word_dict[word] = 0
	for a_list in raw_matrix_counts:
		for a_tup in a_list:
			word = a_tup[0]
			word_dict[word] = word_dict[word] + a_tup[1]
	#col_dict stores the sum of the column divided by the total
	col_dict = {}
	for word in word_dict:
		value = float(word_dict[word])
		value = float(value/total)
		col_dict[word] = value
	
	#doc dict will contain sum of all words in a document
	docu_dict = {}
	
	list_of_years = list(docs_dict.values())
	year_index = 0
	for a_list in raw_matrix_counts:
		total_in_doc = 0
		for a_tup in a_list:
			total_in_doc = total_in_doc + a_tup[1]
		docu_dict[list_of_years[year_index]] = total_in_doc
		year_index = year_index + 1
	
	#so now we have the sum of the rows in docu_dict, with the key being the year the document is associated with
	#we also have the sum of the columns, with the word being the key for the raw count, the col_dict contains the sum divided by the scalar value
	row_dict = docu_dict
	for key in row_dict.keys():
		value = row_dict[key]
		value = float(value)
		value = float(value/total)
		row_dict[key] = value
	
	#row_dict = sum/value of docs // col_dict = sum/value of words
	col_dict_len = len(col_dict)
	row_dict_len = len(row_dict)
	
	#going to do the scalar product now... difficult! (actually, coming back, not scalar, misnamed it, oh well)
	scalar_dict = {}
	for key_row, value_row in row_dict.items():
		scalar_dict_value = {}
		for key_col, value_col in col_dict.items():
			value = float(col_dict[key_col]*row_dict[key_row])
			scalar_dict_value[key_col] = value
		scalar_dict[key_row] = scalar_dict_value #keeps in order of year and word for later extraction
	
	#next, we get the "real" values, observed values, all above are "predictive values"... how much we EXPECT to see a word in each doc.
	real_count_dict = {}
	for key_doc, value_filename in docs_dict.items():
		filename = value_filename
		content = key_doc
		tokens = word_tokenize(content)
		tokens_dict = {}
		for token in tokens:		#initalize all to 0 before raw count
			tokens_dict[token] = 0
		for token in tokens:
			tokens_dict[token] = tokens_dict[token] + 1  #raw counts for THIS DOC should be aquired
		#now store doc
		for token in tokens:
			value = float(tokens_dict[token])
			tokens_dict[token] = float(value/total)
		real_count_dict[filename] = tokens_dict
	
	#now get the ratio of the observed/predicted
	for key in real_count_dict.keys():
		for key2 in real_count_dict[key].keys():
			real_count_dict[key][key2] = float(real_count_dict[key][key2] / scalar_dict[key][key2])
	
	#now take the log of the new matrix (real_count_dict), according to online that implies taking the log of each value... lets hope this works.
	for key in real_count_dict.keys():
		for key2 in real_count_dict[key].keys():
			if real_count_dict[key][key2] > 0.0:
				real_count_dict[key][key2] = float(math.log(real_count_dict[key][key2]))
			else:
				real_count_dict[key][key2] = 0.0
	
	for key in real_count_dict.keys():
		dict_to_sort = real_count_dict[key]
		sorted_dict = OrderedDict(sorted(dict_to_sort.items(), key=operator.itemgetter(1)))
		real_count_dict[key] = sorted_dict
	
	for key in real_count_dict.keys():
		print(key)  																#key is year
		print("-------------------------")
		for key2 in real_count_dict[key].keys()[:10]:								#key2 is word
			#print only top 10
			word = key2
			value = real_count_dict[key][key2]
			print_string = " {} : {} "
			print(word, value)
			#myprintout.format(unicode(word).encode("iso-8859-2", "replace"), value) 
		print("\n")
	return real_count_dict


		



#cooccurrence by year
#keyword search
