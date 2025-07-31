import re
import random
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpRequest, HttpResponseRedirect
from markdown2 import Markdown
from pathlib import Path
from . import util

markdowner = Markdown()


def index(request):
    return render(request, "encyclopedia/index.html", {"entries": util.list_entries()})


def entry_page(request: HttpRequest, title: str):
    for entry in util.list_entries():
        if title.lower() == entry.lower():
            p = Path(f"entries/{entry}.md")
            page = p.read_text()
            return render(
                request,
                "encyclopedia/entry.html",
                {"entry": markdowner.convert(page), "title": entry}
            )

    return render(request, "encyclopedia/entry.html") 


def search(request: HttpRequest):
    query = request.GET.get("q")

    if not query:
        return HttpResponseRedirect("/")

    for entry in util.list_entries():
        if query.lower() == entry.lower():
            return HttpResponseRedirect(reverse("entry_page", args=[entry]))

    pattern = re.compile(f".*{re.escape(query)}.*", re.IGNORECASE)
    results = [entry for entry in util.list_entries() if pattern.match(entry)]
    
    return render(request, "encyclopedia/search.html", {"results": results})


def new_page(request: HttpRequest):
    if request.method == "GET":
        return render(request, "encyclopedia/new.html")
    elif request.method == "POST":
        title = request.POST.get("title")
        desc = request.POST.get("description")

        if not title or not desc:
            return HttpResponseRedirect("/new")

        for entry in util.list_entries():
            if title.lower() == entry.lower():
                return render(
                    request, "encyclopedia/new.html", {"error": "Entry already exists"}
                )

        title_path = Path(f"entries/{title}.md")

        with title_path.open("w") as f:
            f.write("# " + title + "\n" + desc)

        return HttpResponseRedirect(reverse("entry_page", args=[title]))


def edit_page(request: HttpRequest, title: str):
    if request.method == "GET":
        title_path = Path(f"entries/{title}.md")

        if not title_path.exists():
            return render(request, "encyclopedia/entry.html")

        entry = title_path.read_text().splitlines()
        title = entry[0].strip("# ")
        desc = "\n".join(entry[1:])

        return render(request, "encyclopedia/edit.html", {"title": title, "desc": desc})

    elif request.method == "POST":
        title = request.POST.get("title")
        desc = request.POST.get("description")

        title_path = Path(f"entries/{title}.md")

        with title_path.open("w") as f:
            f.write("#" + title + "\n" + desc)

        return HttpResponseRedirect(reverse("entry_page", args=[title]))


def random_page(request):
    choice = random.choice(util.list_entries())

    return HttpResponseRedirect(reverse("entry_page", args=[choice]))
