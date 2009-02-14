# Create your views here.
from models import Contributor, Contribution
from nr.comics.models import Comic
from nr.utils import render_with_request
from django.contrib.admin.views.decorators import staff_member_required
from django.db import connection
import collections

def contribution_list(request):
    """the contributions list page!!"""
    # build the horrible list of contributors
    # (<Contributor Object>,[
    #  {
    #   id: contribution_id,
    #   aka: contribution_aka,
    #   type: contribution_type,
    #   content: contribution_content,
    #   comics: [{sequence,date,id,title}, ...]
    #  }, ...
    # ])
    # THIS IS SO GROSS but at least it doesn't hit the database 800 times.
    public_comics = Comic.comics.public().values('id','sequence','title','date')
    cursor = connection.cursor()
    cursor.execute('SELECT contribution_id, comic_id from comics_comic_origin')
    cc_relation = collections.defaultdict(list)
    for row in cursor.fetchall():
        comic = [x for x in public_comics if x["id"] == row[1]][0]
        cc_relation[row[0]].append(comic)
    full_list = []
    flagged_contributions = Contribution.objects.exclude(flagged=False).values()
    for contributor in Contributor.objects.all().iterator():
        contribution_comics = []
        flagged_for_contributor = [con for con in flagged_contributions if contributor.id == con['contributor_id']]
        for fcon in flagged_for_contributor:
            fcon["comics"] = cc_relation[fcon["id"]]
            contribution_comics.append(fcon)
        full_list.append((contributor,contribution_comics))
        
    return render_with_request(
        "contributions/list.html",
        {
            "contributions": [c for c in full_list if c[0].id != 666],
            "regular": [c for c in full_list if c[0].id == 666][0][1],
        },
        request
    )

from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.forms import ModelForm

class ContributionForm(ModelForm):
    class Meta:
        model = Contribution
        fields = ('aka', 'content')

def submit(request):
    if request.method == 'POST':
        form = ContributionForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/contribute/thanks/')
    else:
        form = ContributionForm()
    return render_with_request('contributions/submit.html',
                                      {'form':form}, request)

def submitjs(request):
    if request.method == 'POST':
        form = ContributionForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse("<span class='thanks'>THANK YOU FOR YOUR SUGGESTION</span>")
    else:
        form = ContributionForm()
    return render_with_request('contributions/jssubmit.html',{'form':form},request)
            

def thanks(request):
    return render_with_request('contributions/thanks.html',{},request)

@staff_member_required
def report(request):
    """makes the unused suggestions report"""
    return render_with_request(
        'admin/contributions/report.html',
        {'contribs': Contribution.objects.all().filter(flagged = False, contribution_type = 'suggested').order_by("-submitted")},
        request
    )
