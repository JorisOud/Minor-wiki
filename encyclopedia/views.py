
from django import forms
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from markdown2 import markdown
from random import choice

from . import util

def validate_title(title):
    for entry in util.list_entries():
        if title.lower() == entry.lower():
            raise ValidationError(f"A page with the name {title} already exists.", code="Error message")

class New_page_form(forms.Form):
    title = forms.CharField(label="Page Title", validators=[validate_title])
    page_contents = forms.CharField(label="page Contents", widget=forms.Textarea)

class Edit_page_form(forms.Form):
    page_contents = forms.CharField(label="page Contents", widget=forms.Textarea)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry_name):
    if entry_name not in util.list_entries():
        return render(request, "encyclopedia/entry_error.html")

    return render(request, "encyclopedia/entry.html",{
        "entry_name": entry_name,
        "entry_text": markdown(util.get_entry(entry_name))
    })

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
    if not request.method == "POST":
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
    if not request.method == "POST":
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
    return entry(request, choice(util.list_entries()))
