from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home (request):
    return render(request,'home.html',{'name':'Daniel Alberto Posada Murillo'})

def about (request):   
    return HttpResponse('<h1>Page about</h1>')

