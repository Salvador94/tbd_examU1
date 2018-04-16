
from django.shortcuts import render, redirect
import redis
from .models import Movie


r=redis.Redis(host='localhost',port=6379,db=0)

def sql_to_redis(request):
    mov=Movie.objects.all()

    movie_list=[]

    for peli in mov:
        lolo={
        'Movie':{mov.get(id=peli.id).id:
       [mov.get(id=peli.id).name,
        mov.get(id=peli.id).year,
        mov.get(id=peli.id).studio,
        mov.get(id=peli.id).genre,
        mov.get(id=peli.id).active,
        mov.get(id=peli.id).created
        ]
    }}

    movie_list.append(lolo)

    r.set('Movies', movie_list)
    return redirect('/')

def home (request):
    context = {'Movie': r.get('Movie')}

    return render(quest, 'index.html',context)
