from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.urls import reverse
import plotly.express as px
from bokeh.plotting import figure, output_file, show
from bokeh.layouts import gridplot
from bokeh.embed import components
from bokeh.models import HoverTool, SaveTool, LabelSet, ColumnDataSource
from pandas.core.frame import DataFrame
import collections
import sqlite3

from .scripts.termonly import KeywordSearchTFIDF
from .scripts.yearsonly import YearSearchTFIDF

from .models import Insight

#VIEWS

#index of searching... takes you to the searching central page
def index(request):
    con = sqlite3.connect('db.sqlite3')
    template = loader.get_template('searching/index.html')
    if request.method == 'POST':
        keyword = None
        years = None
        keyword = request.POST.get("keyword")
        years = request.POST.get("year")
        
        if years is not None:
            years = int(years)
            documents = Insight.objects.filter(year=years)
            results = YearSearchTFIDF(years)
            script, div = YearsOnlyCharter(results, years)
        elif keyword is not None:
            keyword_for_query = " " + keyword + " "
            keyword_for_query = keyword_for_query.lower()
            documents = Insight.objects.filter(body__contains=keyword)
            results = KeywordSearchTFIDF(keyword.lower())
            if results == "No results found":
                div = "<div>No results found.  Try again.</div>"
                return render(request, 'searching/index.html', {'errorsearch': "No documents found.  Please try again."})
            else:  
                ordereddict1 = collections.OrderedDict(sorted(results.items(), key = lambda t: t[0]))
                results = dict(ordereddict1)
                script, div = KeywordOnlyCharter(results, keyword)
        else:
            print("tbd")
        
        context = {
            'keyword':keyword,
            'years':years,
            'results': results,
            'script': script,
            'div': div,
            'documents': documents,
        }
            
        return render(request, 'searching/index.html', context)
    else:
        return render(request, 'searching/index.html')
    
def results(request):
    template = loader.get_template('searching/index.html')
    keyword = request.POST.get("keyword")
    context = {
        'keyword': keyword,
    }
    return redirect('/searching/', context)
    
def search(request):
    #try get keyword
    #try get year(s)
    #send to python script which is appropriate
    #return from python script and load into context
    #don't forget graphing data so you can create plotly graph
    keyword = request.POST.get("keyword")
    context = {
        'keyword': keyword,
    }
    return reverse(results, keyword)
    
def KeywordOnlyCharter(results, keyword):
    years = []
    for key in results.keys():
        year = str(key)
        years.append(year)
        
    save = SaveTool()
    
    title = keyword + " TF-IDF"
    
    p = figure(title=title,
        x_axis_label='Year',
        y_axis_label='TF-IDF Score',
        x_range = years,
        plot_height = 500,
        plot_width = 1000,
        tools = [save],
    )
    
    p.toolbar.active_drag = None
    p.toolbar.active_scroll = None
    p.toolbar.active_tap = None
    p.toolbar.active_inspect = None
    
    scores = []
    for value in results.values():
        scores.append(value)
    
    scores2 = []
    
    for score in scores:
        score2 = round(score, 3)
        scores2.append(score2)
    
    p.vbar(x=years, top=scores, width=0.9, color='#469438')
    
    p.add_tools(HoverTool(tooltips=[("YEAR", "@x"), ("TF-IDF SCORE", "@top")]))
    
    p.toolbar.logo = None
    
    source = DataFrame(dict(years=years, scores=scores, names=scores2))
    
    labels = LabelSet(x='years', y='scores', text='names', source=ColumnDataSource(source), render_mode='css', text_font_size="10pt", text_color="black")
    
    p.xgrid.grid_line_color = None
    p.y_range.start = 0
    
    p.add_layout(labels)
    
    script, div = components(p)
    return script, div
    
def YearsOnlyCharter(results, year):
    words = []
    for key in results.keys():
        word = str(key)
        words.append(word)
        
    save = SaveTool()
    
    title = str(year) + " TF-IDF"
    
    p = figure(title=title,
        x_axis_label = 'Words', 
        y_axis_label = 'TF-IDF Score',
        x_range = words,
        plot_height = 500,
        plot_width = 1000,
        tools = [save],
    )
    
    p.toolbar.active_drag = None
    p.toolbar.active_scroll = None
    p.toolbar.active_tap = None
    p.toolbar.active_inspect = None
    
    scores = []
    for value in results.values():
        scores.append(value)
        
    scores2 = []
    
    for score in scores:
        score2 = round(score, 3)
        scores2.append(score2)
        
    p.vbar(x=words, top=scores, width=0.9, color='#469438')
    
    p.add_tools(HoverTool(tooltips=[("WORD", "@x"), ("TF-IDF SCORE", "@top")]))
    
    p.toolbar.logo = None
    
    source = DataFrame(dict(words=words, scores=scores, names=scores2))
    
    labels = LabelSet(x='words', y='scores', text='names', source=ColumnDataSource(source), render_mode='css', text_font_size="10pt", text_color="black")
    
    p.xgrid.grid_line_color = None
    p.y_range.start = 0
    
    p.add_layout(labels)
    
    script, div = components(p)
    return script, div