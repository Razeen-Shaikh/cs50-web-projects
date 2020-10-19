from django.shortcuts import render, redirect
from django import forms
from . import util
from random import choice


class NewEntryForm(forms.Form):
    title = forms.CharField(
        label="Title",
        widget=forms.TextInput(
            attrs={
                'class': 'ml-2 px-2'
            }
        )
    )
    content = forms.CharField(
        label="",
        widget=forms.Textarea(
            attrs={
                'class': 'my-2'
            }
        )
    )


def index(request):
    entries = util.list_entries()
    return render(request, "encyclopedia/index.html", {
        "entries": entries,
    })


def create(request):
    entries = util.list_entries()
    if request.method == 'POST':
        form = NewEntryForm(request.POST)
        if form.is_valid:
            title = request.POST['title']
            content = request.POST['content']
            for entry in entries:
                if entry.upper() == title.upper():
                    return render(request, "encylopedia/add.html", {
                        "name": "Create Page",
                        "form": "Page Already Exist",
                    })
                else:
                    util.save_entry(title, content)
                    return redirect("wiki:entry", title=title)
    else:
        return render(request, "encyclopedia/add.html", {
            "name": "Create Page",
            "form": NewEntryForm(),
        })


def edit(request, title):
    entries = util.list_entries()
    content = util.get_entry(title)
    form = NewEntryForm(initial={'title': title, 'content': content})
    form.fields['title'].widget.attrs['readonly'] = True
    if request.method == 'POST':
        if form.is_valid:
            content = request.POST.get('content')
            for entry in entries:
                util.save_entry(title, content)
                return redirect("wiki:entry", title=title)
    else:
        return render(request, "encyclopedia/add.html", {
            "name": "Edit Page",
            "form": form,
        })


def entry(request, title):
    content = util.get_entry(title)
    if content == None:
        return render(request, "encyclopedia/error.html")
    else:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": content,
        })


def random(request):
    entries = util.list_entries()
    title = choice(entries)
    return redirect("wiki:entry", title=title)


def search(request):
    entries = util.list_entries()
    query = request.GET['q']
    if len(query) != 0:
        listEntries = []
        for entry in entries:
            if query.upper() in entry.upper():
                listEntries.append(entry)
            if query.upper() == entry.upper():
                return redirect("wiki:entry", entry=entry)
        return render(request, "encyclopedia/index.html", {
            "entries": listEntries,
        })
    else:
        return redirect(("wiki:index"))
