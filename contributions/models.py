from django.db import models

class Contributor(models.Model):
    name = models.CharField(max_length=100, help_text="The real name of the submitter. Or whatever most closely approximates same.")
    info = models.TextField(help_text="A bio blurb.")
    slug = models.SlugField()
    
    class Meta:
        ordering = ['name']
    
    def __unicode__(self):
        return u"%s" % self.name
    
    def get_absolute_url(self):
        return "/contribute/#%s" % self.slug

class ContributionManager(models.Manager):
    def get_query_set(self):
        return super(SingularContributions, self).get_query_set().filter(flagged=True).exclude(aka='None')

def get_None_contributor():
    """Returns the Contributor named 'None', making him if necessary"""
    obj, created = Contributor.objects.get_or_create(
        slug = 'none',
        defaults = {'info': 'Nothing special', 'name': 'None'}
    )
    return obj

class Contribution(models.Model):
    CONTRIBUTION_TYPES = (
        ('suggested', 'suggested'),
        ('drew', 'drew'),
        ('wrote', 'wrote'),
        ('photographed', 'photographed'),
        ('modelled','modelled'),
        ('fourth_panelled', 'fourth panelled'),
        ('guested','guest comicked'),
    )
    
    contribution_type = models.SlugField(choices=CONTRIBUTION_TYPES, default="suggested")
    contributor = models.ForeignKey(Contributor, default=get_None_contributor, verbose_name="plural contributor")
    aka = models.CharField(max_length=100, verbose_name="contributor", help_text="Example: Daniel C. Dennett")
    content = models.TextField(verbose_name="contribution", help_text="Example: Rabid eat all the sandwiches now he cry.")
    submitted = models.DateField(auto_now_add=True)
    flagged = models.BooleanField(default=False)
    
    objects = models.Manager()
    not_none = ContributionManager()

    def __unicode__(self):
        return u"%s %s %s" % (self.aka, self.contribution_type, self.content)

    def get_absolute_url(self):
        return '/contribute/#%d' % self.id
    
    def is_contributor(self):
        """Does this contribution have an associated Contributor?"""
        if self.contributor: return True
        else: return False
    is_contributor.boolean = True
