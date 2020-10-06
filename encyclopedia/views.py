import random
import os.path
from os import path
import markdown
from django import forms
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from . import util

class CreateEntryForm(forms.Form):
    heading = forms.CharField(label="Post Title:", widget=forms.TextInput, max_length=30, required=True)
    content = forms.CharField(label="Post Content:", widget=forms.Textarea, max_length=300, required=True)

class EditEntryForm(forms.Form):
    content = forms.CharField(label="Post Content:", widget=forms.Textarea, max_length=300, required=True)


def index(request):
    return render(request, "encyclopedia/index.html", {"entries": util.list_entries()})


def entry(request, title):
    text = util.get_entry(title)

    if text is not None:
        context = {'html': markdown.markdown(text), 'title':title}

        return render(request, "encyclopedia/entry.html", context)


    else:
        messages.error(request, 'Error: No such entry exists')
        return redirect(reverse(error))


def create(request):
    if request.method == 'POST':

        form =  CreateEntryForm(request.POST)

        if form.is_valid():
            heading = form.cleaned_data["heading"]

            for entryName in util.list_entries():
                if heading.lower() == entryName.lower():
                    messages.error(request, 'Error: Entry with that name already exists.')
                    return redirect(reverse(error))

                else:
                    continue

            content = form.cleaned_data["content"]

        new_entry = open(f"entries/{heading}.md", "w", encoding="utf-8")
        new_entry.write(f"# {heading}\n\n{content}")
        new_entry.close()
        messages.success(request, 'Sucessfully created new entry')

        return redirect(reverse(entry, kwargs={'title': heading}))

    else:
        context = {
            "form": CreateEntryForm()
        }

        return render(request, "encyclopedia/create.html", context)

def random_page(request):
    return redirect(reverse(entry, kwargs=
        {'title': random.choice(util.list_entries())
    }))

def search(request):
    if request.method == 'POST':

        query = request.POST['q']

        for entryName in util.list_entries():
            if query.lower() == entryName.lower():

                return redirect(reverse(entry, kwargs={'title': entryName}))
            
            else:
                continue

        return redirect(reverse(results, kwargs={'query': query}))


def results(request, query):

    results = []

    for entryName in util.list_entries():
        if query.lower() in entryName.lower():
            results.append(entryName)

    if len(results) == 0:
        messages.error(request, 'Error: No such entry exists')
        return redirect(reverse(error))

    else:
        return render(request, "encyclopedia/results.html", {'entries': results})


def editpage(request, title):
    if request.method == 'POST':
        form = EditEntryForm(request.POST)

        if form.is_valid():
            content = form.cleaned_data["content"]

        new_entry = open(f"entries/{title}.md", "w", encoding="utf-8")
        new_entry.write(f"# {title}\n\n{content}")
        new_entry.close()
        messages.success(request, 'Sucessfully edited entry')
        return redirect(reverse(entry, kwargs={'title':title}))

    else:
        context = {
            "form": EditEntryForm(),
            'title':title
        }
        return render(request, "encyclopedia/editpage.html", context)


def error(request):
    return render(request, "encyclopedia/error.html")
    