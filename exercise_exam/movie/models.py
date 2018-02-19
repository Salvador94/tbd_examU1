from django.db import models
from django.utils.encoding import smart_text
from django.utils import timezone
from django.utils.text import slugify
from django.utils.timesince import timesince
from django.db.models.signals import post_save, pre_save
from datetime import timedelta, datetime, date

from .validators import Validate_studio

GENRE_CHOICES = (
('seleccionar', 'Seleccionar'),
('Accion', 'Accion'),
('Comedia', 'Comedia'),
('Terror', 'Terror'),
('Romance', 'Romance'),
('Infantil', 'Infantil'),
('Anime', 'Anime'),
('Dorama', 'Dorama'),
('Drama', 'Drama'),
)


## Custom QuerySet Methods

class MovieModelQuery(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)

    def nuevo_title_items(self, value):
        return self.filter(title__icontains=value)

## Model manager
class MovieModelManager(models.Manager):
    def get_queryset(self):
        return MovieModelQuerySet(self.model, using=self._db)

    def all(se  , *args, **kwargs):
        qs = super(MovieModelManager, self).all(*args, **kwargs).active()
        return qs

class Movie(models.Model):
    name    = models.CharField(max_length = 120)
    year    = models.CharField(max_length = 120, default='Year', blank=True, null=True)
    studio  = models.CharField(max_length= 120, validators = [Validate_studio], null=True, blank=True)
    genre   = models.CharField(max_length = 120, choices = GENRE_CHOICES, default= "seleccionar")
    slug    = models.SlugField(null=True, blank=True)
    active  = models.BooleanField(default = True)
    created = models.DateField(auto_now = False, auto_now_add=False, default = timezone.now)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return smart_text(self.name)

    def save(self, *args, **kwargs):
        print ("Guarde algo")
        #super(Post, self).save(*args, **kwargs)
        if not self.slug:
            if self.name:
                self.slug = slugify(self.name)
        super(Movie, self).save(*args, **kwargs)

    @property
    def age(self):
            if self.created == 'Create':
                now = datetime.now()
                created = datetime.combine(
                               self.created,
                               datetime.now().min.time()
                               )
            try:
                difference = now - created
                print(difference)
            except:
                difference = "No hay creacion"

            if difference <= datetime.timedelta(minutes=10):
                print(difference)
                return "Ahora"
            return "{time} ago".format(time=timestamp(created).split(",")[0])


## Save y pre_save

def movie_model_post_save_receiver(sender, instance, *args, **kwargs):
    print ("Despues Almacenar")
    if not instance.slug and instance.name:
        instance.slug = slugify (instance.name)
        instance.save()
post_save.connect(movie_model_post_save_receiver, sender=Movie)

def movie_model_pre_save_receiver(sender, instance, *args, **kwargs):
    print ("Antes de Alamacenar")
    if not instance.slug and instance.name:
        instance.slug = slugify (instance.name)
        instance.save()
pre_save.connect(movie_model_post_save_receiver, sender=Movie)
