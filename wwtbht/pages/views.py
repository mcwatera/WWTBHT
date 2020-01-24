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

from .scripts.datakeywords import datakeywords

def index(request):
    template = loader.get_template('pages/index.html')
    return render(request, 'pages/index.html')
    
def graphs(request):
    template = loader.get_template('pages/graphs.html')
    
    results = datakeywords()
    scriptanddivdict = dict()
    for result in results.keys():
        currentlist = []
        year = int(result)
        keywords = results[result]
        script, div = YearsOnlyCharter(keywords, year)
        currentlist.append(script)
        currentlist.append(div)
        scriptanddivdict[result] = currentlist
        
    context = {
            'graphsdict': scriptanddivdict,
    }
    
    return render(request, 'pages/graphs.html', context)
    
def data(request):
    template = loader.get_template('pages/data.html')
    return render(request, 'pages/data.html')
    
def about(request):
    template = loader.get_template('pages/about.html')
    return render(request, 'pages/about.html')    
    
def background(request):
    template = loader.get_template('pages/background.html')
    return render(request, 'pages/background.html')
    
def contact(request):
    template = loader.get_template('pages/contact.html')
    return render(request, 'pages/contact.html')


# ---------------------NON-VIEW METHODS -------------------------------

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