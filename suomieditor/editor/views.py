from django.shortcuts import render

from voikko import libvoikko

# Create your views here.
from django.http import HttpResponse
from .models import BaseForm


def index(request):
    """List 50 base forms."""
    base_forms = BaseForm.objects.order_by("word")[:50]
    context = {"base_forms": base_forms}
    return render(request, "editor/index.html", context)


# show one with id
def detail(request, baseform_id):
    """Show one base form."""
    base_form = BaseForm.objects.get(pk=baseform_id)
    context = {"base_form": base_form}
    return render(request, "editor/detail.html", context)


# POST a word, get it analyzed
def analyze(request):
    """Analyze a word."""
    # if GET, show form
    if request.method == "GET":
        return render(request, "editor/analyze.html")
    # if POST, analyze word
    elif request.method == "POST":
        word = request.POST["word"]
        v = libvoikko.Voikko("fi", "/usr/local/Cellar/libvoikko/4.3.2/lib/voikko")
        results = v.analyze(word)
        context = {"word": word, "analyzed": results}
        return render(request, "editor/analyze.html", context)
