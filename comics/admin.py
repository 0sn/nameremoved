from django.contrib import admin
from models import Comic

class ComicAdmin(admin.ModelAdmin):
    list_display = ('title','date','sequence', 'is_public', 'starts_storyline')
    list_filter = ('starts_storyline',)
    search_fields = ['title', 'transcript', 'newstitle', 'news']
    date_hierarchy = 'date'
    ordering = ['-sequence']
    fieldsets = (
        (None, {'fields': ('date','title','comic')}),
        ("Transcription", {'fields':('transcript',)}),
        ("News", {'fields':('newstitle', 'news')}),
        ("Suggestion", {'fields': ('origin',), 'classes': ('collapse','wide',),}),
        ("Storyline", {'fields': (('starts_storyline', 'storyline_title'), 'storyline_description'), 'classes':('collapse',)}),
    )
    filter_vertical = ('origin',)
    
admin.site.register(Comic,ComicAdmin)

