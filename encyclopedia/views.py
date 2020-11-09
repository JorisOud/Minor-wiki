from django.shortcuts import render
from markdown2 import markdown
from random import choice

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry_name):
    if entry_name in util.list_entries():
        return render(request, "encyclopedia/entry.html",{
            "entry_name": entry_name,
            "entry_text": markdown(util.get_entry(entry_name))
        })

    return render(request, "encyclopedia/entry_error.html")

def search(request):
    query = request.GET.get("q", "")
    results_list = []

    for ent in util.list_entries():
        if query.lower() == ent.lower():
            return entry(request, ent)
        elif query.lower() in ent.lower():
            results_list.append(ent)

    return render(request, "encyclopedia/results.html",{
        "query": query,
        "results_list": results_list
    })

def new_page(request):
    return render(request, "encyclopedia/new_page.html")

def random(request):
    return entry(request, choice(util.list_entries()))
    