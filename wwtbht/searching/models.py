from django.db import models

#Article/Document Model
class Document(models.Model):
    title = models.TextField
    body = models.TextField
    date = models.CharField(max_length=128)
    year = models.IntegerField
    creator = models.TextField
    publication = models.CharField(max_length=500)
    citation = models.TextField
    
class Article(models.Model):
    title = models.TextField
    body = models.TextField
    date = models.CharField(max_length=128)
    year = models.IntegerField
    creator = models.TextField
    publication = models.CharField(max_length=500)
    citation = models.TextField
    
class Insight(models.Model):
    title = models.TextField()
    body = models.TextField()
    date = models.CharField(max_length=128)
    year = models.IntegerField()
    creator = models.TextField()
    publication = models.CharField(max_length=500)
    citation = models.TextField()