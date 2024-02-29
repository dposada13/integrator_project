from django.shortcuts import render
from django.http import HttpResponse

from .models import Movie

import matplotlib.pyplot as plt
import matplotlib
import io
import urllib, base64

# Create your views here.
def home (request):
    searchTerm=request.GET.get('searchMovie')
    if searchTerm:
        movies = Movie.objects.filter(title__icontains = searchTerm)
    else:
        movies = Movie.objects.all()
    return render(request,'home.html',{'searchTerm':searchTerm, 'movies':movies})

def about (request):   
    return render(request,'about.html')

def signup(request):
    email= request.GET.get('email')
    return render(request,'signup.html',{'email':email})

def statistics_view(request):
    matplotlib.use('Agg')
    years = Movie.objects.values_list('year', flat=True).distinct().order_by('year')
    movie_counts_by_year = {}
    for year in years:
        if year:
            movies_in_year = Movie.objects.filter(year=year)
        else:
            movies_in_year = Movie.objects.filter(year__isnull=True)
            year="None"
        count = movies_in_year.count()
        movie_counts_by_year[year]= count
        
    bar_width = 0.5 #Ancho de barras
    bar_spacing = 0.5 #Separacion de Barras        
    bar_positions = range(len(movie_counts_by_year)) #Posiciones de las barras
    
    #Crear la grafica de barras
    plt.bar(bar_positions, movie_counts_by_year.values(), width = bar_width,align='center')
    #Personalizar grafica
    plt.title('Movies per year')
    plt.xlabel('Year')
    plt.ylabel('Number of movies')
    plt.xticks(bar_positions, movie_counts_by_year.keys(), rotation=90)
    #Ajustar el espacio entre las barras
    plt.subplots_adjust(bottom=0.3)
    #Guardar la grafica en un objeto BytesIO
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()
     
    #Convertir la grafica base64
    image_png= buffer.getvalue()
    buffer.close()
    graphic = base64.b64decode(image_png)
    graphic = graphic.decode('utf-8')
     
    #Renderizar la plantilla statistics.html con la grafica
    return render(request, 'statistics.html',{'graphic':graphic})
#Grafico por genero        
def statistics_view_genere(request):
    matplotlib.use('Agg')
    generes = Movie.objects.values_list('genere', flat=True).distinct().order_by('genere')
    movie_counts_by_genere = {}
    for genere in generes:
        if genere:
            movies_in_genere = Movie.objects.filter(genere=genere)
        else:
            movies_in_genere = Movie.objects.filter(genere__isnull=True)
            genere="None"
        count = movies_in_genere.count()
        movie_counts_by_genere[genere]= count
        
    bar_width = 0.5 #Ancho de barras
    bar_spacing = 0.5 #Separacion de Barras        
    bar_positions = range(len(movie_counts_by_genere)) #Posiciones de las barras
    
    #Crear la grafica de barras
    plt.bar(bar_positions, movie_counts_by_genere.values(), width = bar_width,align='center')
    #Personalizar grafica
    plt.title('Movies per genere')
    plt.xlabel('Genere')
    plt.ylabel('Number of movies')
    plt.xticks(bar_positions, movie_counts_by_genere.keys(), rotation=90)
    #Ajustar el espacio entre las barras
    plt.subplots_adjust(bottom=0.3)
    #Guardar la grafica en un objeto BytesIO
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()
     
    #Convertir la grafica base64
    image_png= buffer.getvalue()
    buffer.close()
    graphic_genere = base64.b64decode(image_png)
    graphic_genere = graphic_genere.decode('utf-8')
     
    #Renderizar la plantilla statistics.html con la grafica
    return render(request, 'statistics.html',{'graphic_genere':graphic_genere})       
        

