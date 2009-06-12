from django.db import models, connection, transaction
from django.template.defaultfilters import slugify
from nr.contributions.models import Contribution
import datetime, os
from django.core.cache import cache

CACHE_PREFIX = "comic_model_"

class ComicsManager(models.Manager):
    def public(self):
        return self.filter(date__lte=datetime.date.today)

def upload_to(instance, filename):
    return "comics/%s-%s%s" % (str(instance.date), slugify(instance.title), os.path.splitext(filename)[1])

class Comic(models.Model):
    """
    A comic. Unique by date, and has an integer corresponding to its sequence
    in the stream of dates.
    """
    comics = ComicsManager()
    date = models.DateField(unique=True)
    sequence = models.IntegerField(blank=True, null=True, editable=False)
    title = models.CharField(max_length=100)
    transcript = models.TextField()
    newstitle = models.CharField(max_length=100, verbose_name="news title")
    news = models.TextField()
    comic = models.ImageField(upload_to=upload_to, height_field="height", width_field="width")
    height = models.IntegerField(blank=True, null=True, editable=False)
    width = models.IntegerField(blank=True, null=True, editable=False)
    origin = models.ManyToManyField(Contribution, limit_choices_to={'flagged': True}, null=True, blank=True)
    starts_storyline = models.BooleanField(default=False)
    storyline_title = models.CharField(max_length=100, verbose_name="storyline title", blank=True)
    storyline_description = models.TextField(verbose_name="storyline description", blank=True)
    
    class Meta:
        ordering = ('sequence',)

    def __unicode__(self):
        return u"%s (%s)" % (self.title, self.date)
    
    @models.permalink
    def get_absolute_url(self):
        return ("nr.comics.views.comic", [self.sequence])

    def is_public(self):
        """
        True if the date on the comic is in the past, or today.
        """
        return self.date <= datetime.date.today()
    is_public.boolean = True
    
    def first(self):
        return 1
    
    def previous(self):
        return self.sequence - 1
    
    def last(self):
        cache_key = CACHE_PREFIX + "sequence_total"
        c = cache.get(cache_key)
        if c is None:
            c = Comic.comics.public().count()
            cache.set(cache_key, c, 600)
        return c
    
    def next(self):
        return self.sequence + 1
    

def update_comic_sequence(sender, instance, **kwargs):
    """
    After a save, or a delete, updates the sequence of all comics by date.
    Not in save() in the Comics model because it affects all Comics.
    """
    query = "UPDATE comics_comic SET sequence=(select count(*) from comics_comic where comics_comic.date <= %s) WHERE id=%s"
    cursor = connection.cursor()
    for comic in Comic.comics.all():
        cursor.execute(query,[comic.date, comic.id])
    transaction.commit()
    cache.set(CACHE_PREFIX + "sequence_total", Comic.comics.public().count(), 600)

models.signals.post_save.connect(update_comic_sequence,sender=Comic)
models.signals.post_delete.connect(update_comic_sequence,sender=Comic)
