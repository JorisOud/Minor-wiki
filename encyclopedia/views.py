
from django import forms
from django.core.exceptions import ValidationError
from django.db import models
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from markdown2 import markdown
from random import choice

from . import util

def validate_title(title):
    for entry in util.list_entries():
        if title.lower() == entry.lower():
            raise ValidationError(
                ('A page with the name %(title)s already exists.'),
                params = {'title': title},
            )

class New_page_form(forms.Form):
    title = forms.CharField(label="Page Title", validators=[validate_title])
    page_contents = forms.CharField(label="page Contents", widget=forms.Textarea)

class Existing_page_form(forms.Form):
    title = forms.CharField(label="Page Title")
    page_contents = forms.CharField(label="page Contents", widget=forms.Textarea)

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
    if request.method == "POST":
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

    return render(request, "encyclopedia/new_page.html", {
        "form": New_page_form()
    })

def edit_page(request, entry_name):
    if request.method == "POST":
        form = Existing_page_form(request.POST)
        if form.is_valid():
            title = entry_name
            page_contents = form.cleaned_data["page_contents"]
            util.save_entry(title, page_contents)
            return HttpResponseRedirect(reverse("encyclopedia:entry", args=[title]))
        else:
            return render(request, "encyclopedia/new_page.html", {
                "form": form
            })

    form = New_page_form(initial={"title": entry_name,
            "page_contents": util.get_entry(entry_name)})

    return render(request, "encyclopedia/edit_page.html", {
        "entry_name": entry_name,
        "form": form
    })

def random(request):
    return entry(request, choice(util.list_entries()))
