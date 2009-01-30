from django.db import models
from comics.models import Comic

class Question(models.Model):
    """A question asked and possibly answered, about a single comic."""
    submitted = models.DateField(auto_now_add=True)
    answered = models.DateField(auto_now=True)
    public = models.BooleanField(default=False)
    asker = models.CharField(max_length=40)
    question = models.TextField()
    answer = models.TextField(blank=True)
    comic = models.ForeignKey(Comic)
    
    def __unicode__(self):
        return u", ".join(self.submitted, self.asker, self.comic.title)
