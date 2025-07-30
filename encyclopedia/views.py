import re
import random
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from markdown2 import Markdown
from pathlib import Path
from . import util

markdowner = Markdown()

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry_page(request, title):
    for entry in util.list_entries():
        if title.lower() == entry.lower():
            p = Path(f"entries/{entry}.md")
            page = p.read_text()
            return render(request, "encyclopedia/entry.html", {
                "entry": markdowner.convert(page),
                "title": entry
            })

    return HttpResponse("404 Page not Found")

def search(request: HttpRequest):
    query = request.GET.get("q")

    if not query:
        return HttpResponseRedirect("/")
    
    for entry in util.list_entries():
        if query.lower() == entry.lower():
            return HttpResponseRedirect(reverse("entry_page", args=[entry]))

    pattern = re.compile(f".*{re.escape(query)}.*", re.IGNORECASE)
    results = [entry for entry in util.list_entries() if pattern.match(entry)]

    return render(request, "encyclopedia/search.html", {
        "results": results
    })

def random_page(request):
    choice = random.choice(util.list_entries())

    return HttpResponseRedirect(reverse("entry_page", args=[choice]))
    
    
    
