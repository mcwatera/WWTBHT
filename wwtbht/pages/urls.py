from django.urls import path

from . import views

app_name = 'pages'
urlpatterns = [
    path('', views.index, name='index'),
    path('graphs', views.graphs, name="graphs"),
    path('data', views.data, name="data"),
    path('about', views.about, name="about"),
    path('background', views.background, name="background"),
    path('contact', views.contact, name="contact"),
]

#def select(request, text_id):
    #get keyword (try)
    #get year(s) (try)
    #send to appropriate script
    #return from appropriate script with data
    #query db for appropriate documents
    #load documents and data into context
    #send on its way
   # word = request.POST.get("word")
    #text = get_object_or_404(Text, pk=text_id)
    #count = text.overall_text.lower().count(word.lower())
    #context = {
    #    'text_id': text.id,
    #    'word': word,
    #    'count': count,
    #}
    #return render(request, 'textentry/results.html', context)
    
def select(request):
    keyword = request.POST.get("keyword")