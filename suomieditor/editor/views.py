import datetime
import logging
import time
from django.contrib.syndication.views import Feed
from django.urls import reverse
from django.shortcuts import render, redirect
from .constants import EXAMPLE_NOUN_FORMS, FORM_MAPPING

from voikko import libvoikko

# Create your views here.
from django.views import generic
from django.http import HttpResponse
from .models import BaseForm, ExampleCache, WordForm


# {'BASEFORM': 'kääre', 'CLASS': 'nimisana',
# 'FSTOUTPUT': '[Ln][Xp]kääre[X]kääre[Sg][Nm]iden',
# 'NUMBER': 'plural', 'SIJAMUOTO': 'omanto',
# 'STRUCTURE': '=ppppppppp', 'WORDBASES': '+kääre(kääre)'}


def form_mapper(kotus_result, word_form):
    """Map Kotus JSON result to BaseForm and WordForm."""
    # check that all the fields are there
    # if not, just return None
    if (
        "BASEFORM" not in kotus_result
        or "NUMBER" not in kotus_result
        or "SIJAMUOTO" not in kotus_result
    ):
        return False

    # get baseform or return False
    try:
        baseforms = BaseForm.objects.filter(word=kotus_result["BASEFORM"])
    except BaseForm.DoesNotExist:
        return False

    for baseform_ in baseforms:
        baseform = BaseForm.objects.get(pk=baseform_.id)
        form_number = (
            WordForm.Number.SINGULAR
            if kotus_result["NUMBER"] == "singular"
            else WordForm.Number.PLURAL
        )
        form = FORM_MAPPING[kotus_result["SIJAMUOTO"]]
        # check if the wordform already exists
        # if it does, skip it
        if (
            WordForm.objects.filter(baseform=baseform)
            .filter(wordform=word_form)
            .filter(number=form_number)
            .filter(case=form)
            .exists()
        ):
            continue

        wordform, created = WordForm.objects.update_or_create(
            baseform=baseform,
            wordform=word_form,
            number=form_number,
            source="editor",
            case=form,
        )
        if created:
            wordform.save()
    return True


def index(request):
    """List 50 base forms."""
    base_forms = BaseForm.objects.order_by("word")[:50]
    context = {"base_forms": base_forms}
    return render(request, "editor/index.html", context)


def listify(word_forms):
    """Turn word forms into a dictionary."""
    result_dict = {}
    for number in WordForm.Number.choices:
        result = []
        for case in WordForm.Case.choices:
            forms = word_forms.filter(number=number[0], case=case[0])
            text = []
            for word_form in forms:
                text.append(word_form.wordform)
            result.append(
                {
                    "number_label": number[1],
                    "number": number[0],
                    "case_label": case[1],
                    "case": case[0],
                    "text": " ".join(text) if text else "",
                }
            )
        result_dict[number[1]] = result
    return result_dict


# show one with id
def detail(request, baseform_id):
    """Show one base form."""
    base_form = BaseForm.objects.get(pk=baseform_id)
    word_forms = listify(WordForm.objects.filter(baseform=base_form))
    similar_forms = (
        BaseForm.objects.filter(gradation=base_form.gradation)
        .filter(declension=base_form.declension)
        .exclude(word=base_form.word)
    )[:5]
    numbers = WordForm.Number.choices
    cases = WordForm.Case.choices
    context = {
        "base_form": base_form,
        "word_forms": word_forms,
        "numbers": numbers,
        "cases": cases,
        "same_type_words": similar_forms,
    }
    return render(request, "editor/detail.html", context)


# POST a word, get it analyzed, only allow POST
def analyze(request):
    """Analyze a word."""
    # if GET, show form
    if request.method == "POST":
        words = request.POST["word"].split()
        v = libvoikko.Voikko("fi", "/usr/local/Cellar/libvoikko/4.3.2/lib/voikko")
        for word in words:
            word_results = v.analyze(word.lower())
            for word_result in word_results:
                form_mapper(word_result, word.lower())

        return redirect("editor:recent")
    else:
        # throw method not allowed
        return HttpResponse("Method not allowed", status=405)


# POST word forms, get them analyzed, only allow POST
def add_cases(request):
    """Analyze a word."""
    # if GET, show form
    if request.method == "POST":
        words = []
        for key in request.POST.keys():
            if key == "csrfmiddlewaretoken" or key == "base_form":
                continue
            values = request.POST.getlist(key)
            # skip csrf token and base_form
            for value in values:
                field_words = value.split()
                for field_word in field_words:
                    words.append(field_word)
        v = libvoikko.Voikko("fi", "/usr/local/Cellar/libvoikko/4.3.2/lib/voikko")
        for word in words:
            logging.info(word)
            word_results = v.analyze(word.lower())
            for word_result in word_results:
                form_mapper(word_result, word.lower())

        return redirect("editor:detail", baseform_id=request.POST["base_form"])
    else:
        # throw method not allowed
        return HttpResponse("Method not allowed", status=405)


# search for a word
def search(request):
    if request.method == "GET":
        word = request.GET["word"]
        wordforms = WordForm.objects.filter(wordform__icontains=word)
        context = {
            "results": wordforms,
            "message": f"Got {wordforms.count()} results for {word}",
            # full dump of GET parameters
            "params": request.GET,
        }
        return render(request, "editor/search_results.html", context)
    else:
        # throw method not allowed
        return HttpResponse("Method not allowed", status=405)


def recent(request):
    """List 50 recent forms."""
    word_forms = WordForm.objects.order_by("-timestamp")[:50]
    context = {"word_forms": word_forms}
    return render(request, "editor/recent.html", context)


def raw(request):
    """Analyze a word."""
    if request.method == "POST":
        words = []
        words = request.POST["word"].split()
        v = libvoikko.Voikko("fi", "/usr/local/Cellar/libvoikko/4.3.2/lib/voikko")
        for word in words:
            result = []
            word_results = v.analyze(word.lower())
            for word_result in word_results:
                result.append(word_result)

        context = {"results": result}

        return render(request, "editor/raw_analyze.html", context)

    else:
        # throw method not allowed
        return HttpResponse("Method not allowed", status=405)


def raw_analyze(request):
    """render raw analyze page"""
    return render(request, "editor/raw_analyze.html")


def by_type_list(request):
    """List all the declensions and gradations types with examples"""
    examples = ExampleCache.objects.all().order_by("declension", "gradation")
    context = {"examples": examples}
    return render(request, "editor/by_type_list.html", context)


def by_type_word_list(request, declension_id, gradation_id):
    """List all the declensions and gradations types with examples"""
    baseforms = BaseForm.objects.filter(declension=declension_id).filter(
        gradation=gradation_id
    )
    context = {
        "baseforms": baseforms,
        "declension": declension_id,
        "gradation": gradation_id,
    }
    return render(request, "editor/by_type_word_list.html", context)


def recent_as_file(request):
    """generate a file of recent words"""

    one_day_ago = (datetime.datetime.now() - datetime.timedelta(days=1)).isoformat()
    word_forms = (
        WordForm.objects.filter(source="editor")
        .filter(timestamp__gte=one_day_ago)
        .order_by("-timestamp")
    )
    file_data = " ".join([word_form.wordform for word_form in word_forms])
    file_name = f"recent_{time.time()}.txt"
    response = HttpResponse(file_data, content_type="application/text charset=utf-8")
    response["Content-Disposition"] = "attachment; filename=" + file_name.encode(
        "utf-8"
    ).decode("latin-1")
    return response


class LatestEntriesFeed(Feed):
    # TODO: there is a smarter way to do this
    # group by day and add words
    title = "Latest words added to Keinonto.com"
    link = "/"
    description = "Latest words added to Keinonto.com"

    def items(self):
        #  return wordforms from last 1 day
        one_day_ago = (datetime.datetime.now() - datetime.timedelta(days=1)).isoformat()
        return (
            WordForm.objects.filter(source="editor")
            .filter(timestamp__gte=one_day_ago)
            .order_by("-timestamp")
        )

    def item_title(self, item):
        return item.wordform

    def item_description(self, item):
        return f"{item.baseform.word} {item.case} {item.number} {item.wordform}"

    def item_link(self, item):
        return reverse("editor:detail", args=[item.baseform.id])
