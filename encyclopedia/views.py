from django.shortcuts import render
from django.http import HttpResponse
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
