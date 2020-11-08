from django.shortcuts import render
from markdown2 import markdown

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry_name):
    return render(request, "encyclopedia/entry.html",{
        "entry_name": entry_name,
        "entry_text": markdown(util.get_entry(entry_name))
    })
