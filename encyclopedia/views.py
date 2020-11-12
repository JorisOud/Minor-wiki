###################################################################
# views.py
#
# Programmeerplatform
# Joris Oud
#
# - Implements the views for the encyclopedia application
###################################################################


from django import forms
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from markdown2 import markdown
from random import choice

from . import util

def validate_title(title):
    """Validation function for the Django form 'New_page_form'. Raises a
      ValidationError when a newly created page name already exists."""

    for entry in util.list_entries():
        if title.lower() == entry.lower():
            raise ValidationError(f"A page with the name {title} already exists.")

class New_page_form(forms.Form):
    """Creates a Django form to create a new wiki page. Attrubutes:
      - title(string): The title of the page.
      - page_contentes(string): The contents of the page in markdown format."""

    title = forms.CharField(label="Page Title", validators=[validate_title])
    page_contents = forms.CharField(label="page Contents", widget=forms.Textarea)

class Edit_page_form(forms.Form):
    """Creates a Django form to edit a wiki page. Attrubute:
      - page_contentes(string): The contents of the page in markdown format."""

    page_contents = forms.CharField(label="page Contents", widget=forms.Textarea)

def index(request):
    """Renders the home page of the encyclopedia app."""

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry_name):
    """Renders the requested entry page. If requested entry page does not exist,
      renders an error page. Needs an entry name (string) as second argument."""

    if entry_name not in util.list_entries():
        return render(request, "encyclopedia/entry_error.html")

    return render(request, "encyclopedia/entry.html",{
        "entry_name": entry_name,
        "entry_text": markdown(util.get_entry(entry_name))
    })

def search(request):
    """Renders an entry page if the search query matches the entry name exactly,
      or else renders a page with a list of entries of which the query is a substring. 
      The search is case insensitive."""

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
    """When requested with GET, renders a page where the user can create a new page. 
      When requested with POST, saves the page and redirects to the created page. If 
      the posted page was not valid, returns to the create page with an error message."""

    if request.method != "POST":
        return render(request, "encyclopedia/new_page.html", {
            "form": New_page_form()
        })

    form = New_page_form(request.POST)
    if form.is_valid():
        title = form.cleaned_data["title"]
        page_contents = form.cleaned_data["page_contents"]
        util.save_entry(title, page_contents)

        return HttpResponseRedirect(reverse("encyclopedia:entry", args=[title]))
    else:
        return render(request, "encyclopedia/new_page.html", {
            "form": form
        })

def edit_page(request, entry_name):
    """Accepts an entry name (string) as second argument. When requested with GET, 
      renders a page where the user can edit that page. When requested with POST, saves 
      the changes and redirects to the edited page. If the posted page was not valid, 
      returns to the edit page with an error message."""

    if request.method != "POST":
        return render(request, "encyclopedia/edit_page.html", {
            "entry_name": entry_name,
            "form": Edit_page_form(initial={"page_contents": util.get_entry(entry_name)})
        })

    form = Edit_page_form(request.POST)
    if form.is_valid():
        util.save_entry(entry_name, form.cleaned_data["page_contents"])
        return HttpResponseRedirect(reverse("encyclopedia:entry", args=[entry_name]))
    else:
        return render(request, "encyclopedia/new_page.html", {
            "form": form
        })

def random(request):
    """Calls the entry function with a random entry name."""

    return entry(request, choice(util.list_entries()))
