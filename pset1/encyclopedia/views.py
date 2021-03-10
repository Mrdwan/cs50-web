import random
import markdown2

from django.shortcuts import render, redirect, reverse
from . import util

def index(request):
    entries = util.list_entries()
    title = 'All Pages'

    if request.method == "POST":
        queryTitle = request.POST.get('q').lower()
        entry = util.get_entry(queryTitle)
        title = 'Search result for: ' + queryTitle

        if entry:
            return redirect(reverse('entry', args=[queryTitle]))

        entries = [entry for entry in entries if queryTitle in entry.lower()]
        if len(entries) == 0:
            return render(request, "encyclopedia/error.html", {
                "message": "The requested page was not found."
            })


    return render(request, "encyclopedia/index.html", {
        "title": title,
        "entries": entries
    })

def entry(request, title):
    entry = util.get_entry(title)

    if entry:
        return render(request, "encyclopedia/entry.html", {
            "entry":  markdown2.markdown(entry),
            "title": title
        })
    
    return render(request, "encyclopedia/error.html", {
        "message": "The requested page was not found."
    })

def add(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')

        if len(title) > 0 and len(content) > 0:
            entries = util.list_entries()
            if title in entries:
                return render(request, "encyclopedia/error.html", {
                    "message": "Page already exist"
                })
            else:
                util.save_entry(title, content)
                return redirect(reverse('entry', args=[title]))
    else:
        return render(request, "encyclopedia/add.html")

def edit(request, title):
    if request.method == 'GET':
        entry = util.get_entry(title)

        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "entry": entry
        })
    else:
        content = request.POST.get('content')

        if len(content) > 0:
            util.save_entry(title, content)

            return redirect(reverse('entry', args=[title]))

def randomEntry(request):
    entries = util.list_entries()
    randomNumber = random.randint(0, len(entries) - 1)
    randomEntry = entries[randomNumber]

    return redirect(reverse('entry', args=[randomEntry]))