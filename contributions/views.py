# Create your views here.
from models import Contributor, Contribution
from nr.utils import render_with_request

def contribution_list(request):
    """the contributions list page!!"""
    return render_with_request(
        "contributions/list.html",
        {
            "plural": Contributor.objects.exclude(slug='none').order_by('name').select_related(),
            "singular": Contribution.objects.exclude(aka='None').filter(contributor__slug='none').order_by('aka'),
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

def thanks(request):
    return render_with_request('contributions/thanks.html',{},request)
