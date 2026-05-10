# views.py

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import World, WikiPage, Wiki

import markdown

def index(request):
    return render(request, "scribedown/index.html")

@login_required
def elements(request):
    worlds = World.objects.filter(owner=request.user)
    return render(request, "scribedown/elements.html", {
        "worlds": worlds
    })

@login_required
def elements_world(request, worldname):
    world = get_object_or_404(World, name=worldname, owner=request.user)
    characters = world.character_set.all()
    locations = world.location_set.all()
    events = world.event_set.all()
    items = world.item_set.all()

    return render(request, "scribedown/elements_world.html", {
        "world": world,
        "characters": characters,
        "locations": locations,
        "events": events,
        "items": items
    })

@login_required
def new_world(request):

    if request.method == "POST":

        name = request.POST.get("name")
        description = request.POST.get("description")

        if not name:
            return render(request, "scribedown/new_world.html", {
                "message": "Name is required."
            })

        if World.objects.filter(name=name).exists():
            return render(request, "scribedown/new_world.html", {
                "message": "World with this name already exists."
            })

        World.objects.create(
            owner=request.user,
            name=name,
            description=description
        )

        return redirect("elements")

    return render(request, "scribedown/new_world.html")

@login_required
def edit_world(request, worldname):

    world = get_object_or_404(World, name=worldname, owner=request.user)

    if request.method == "POST":

        name = request.POST.get("name")
        description = request.POST.get("description")

        if not name:
            return render(request, "scribedown/edit_world.html", {
                "world": world,
                "message": "Name is required."
            })

        if World.objects.filter(name=name).exclude(name=world.name).exists():
            return render(request, "scribedown/edit_world.html", {
                "world": world,
                "message": "World with this name already exists."
            })

        world.name = name
        world.description = description
        world.save()

        return redirect("elements")

    return render(request, "scribedown/edit_world.html", {
        "world": world
    })

@login_required
def delete_world(request, worldname):

    world = get_object_or_404(
        World,
        name=worldname,
        owner=request.user
    )

    if request.method == "POST":

        world.delete()

        return redirect("elements")

    return render(request, "scribedown/delete_world.html", {
        "world": world
    })

@login_required
def new_element(request, worldname):
    world = get_object_or_404(World, name=worldname, owner=request.user)

    if request.method == "POST":

        element_type = request.POST.get("element_type")
        name = request.POST.get("name")
        description = request.POST.get("description")

        if not name:
            return render(request, "scribedown/new_element.html", {
                "world": world,
                "message": "Name is required."
            })

        if element_type == "character":
            world.character_set.create(name=name, description=description)
        elif element_type == "location":
            world.location_set.create(name=name, description=description)
        elif element_type == "event":
            world.event_set.create(name=name, description=description)
        elif element_type == "item":
            world.item_set.create(name=name, description=description)

        return redirect("elements_world", worldname=world.name)

    return render(request, "scribedown/new_element.html", {
        "world": world
    })

@login_required
def edit_element(request, worldname, elementtype, elementname):
    world = get_object_or_404(World, name=worldname, owner=request.user)
    element = None
    if elementtype == "character":
        element = get_object_or_404(world.character_set, name=elementname)
    elif elementtype == "location":
        element = get_object_or_404(world.location_set, name=elementname)
    elif elementtype == "event":
        element = get_object_or_404(world.event_set, name=elementname)
    elif elementtype == "item":
        element = get_object_or_404(world.item_set, name=elementname)

    if request.method == "POST":

        name = request.POST.get("name")
        description = request.POST.get("description")

        if not name:
            return render(request, "scribedown/edit_element.html", {
                "world": world,
                "element": element,
                "message": "Name is required."
            })

        element.name = name
        element.description = description
        element.save()

        return redirect("elements_world", worldname=world.name)
    return render(request, "scribedown/edit_element.html", {
        "world": world,
        "element": element
    })

@login_required
def delete_element(request, worldname, elementtype, elementname):
    world = get_object_or_404(World, name=worldname, owner=request.user)
    element = None
    if elementtype == "character":
        element = get_object_or_404(world.character_set, name=elementname)
    elif elementtype == "location":
        element = get_object_or_404(world.location_set, name=elementname)
    elif elementtype == "event":
        element = get_object_or_404(world.event_set, name=elementname)
    elif elementtype == "item":
        element = get_object_or_404(world.item_set, name=elementname)

    if request.method == "POST":

        element.delete()

        return redirect("elements_world", worldname=world.name)

    return render(request, "scribedown/delete_element.html", {
        "world": world,
        "element": element
    })

@login_required
def characters(request, worldname):
    world = get_object_or_404(World, name=worldname, owner=request.user)
    characters = world.character_set.all()
    return render(request, "scribedown/characters.html", {
        "world": world,
        "characters": characters
    })

@login_required
def character_detail(request, worldname, charactername):
    world = get_object_or_404(World, name=worldname, owner=request.user)
    character = get_object_or_404(world.character_set, name=charactername)
    return render(request, "scribedown/character_detail.html", {
        "world": world,
        "character": character
    })

@login_required
def locations(request, worldname):
    world = get_object_or_404(World, name=worldname, owner=request.user)
    locations = world.location_set.all()
    return render(request, "scribedown/locations.html", {
        "world": world,
        "locations": locations
    })

@login_required
def location_detail(request, worldname, locationname):
    world = get_object_or_404(World, name=worldname, owner=request.user)
    location = get_object_or_404(world.location_set, name=locationname)
    return render(request, "scribedown/location_detail.html", {
        "world": world,
        "location": location
    })

@login_required
def events(request, worldname):
    world = get_object_or_404(World, name=worldname, owner=request.user)
    events = world.event_set.all()
    return render(request, "scribedown/events.html", {
        "world": world,
        "events": events
    })

@login_required
def event_detail(request, worldname, eventname):
    world = get_object_or_404(World, name=worldname, owner=request.user)
    event = get_object_or_404(world.event_set, name=eventname)
    return render(request, "scribedown/event_detail.html", {
        "world": world,
        "event": event
    })

@login_required
def items(request, worldname):
    world = get_object_or_404(World, name=worldname, owner=request.user)
    items = world.item_set.all()
    return render(request, "scribedown/items.html", {
        "world": world,
        "items": items
    })

@login_required
def item_detail(request, worldname, itemname):
    world = get_object_or_404(World, name=worldname, owner=request.user)
    item = get_object_or_404(world.item_set, name=itemname)
    return render(request, "scribedown/item_detail.html", {
        "world": world,
        "item": item
    })

def delete_element(request, worldname, elementtype, elementname):
    world = get_object_or_404(World, name=worldname, owner=request.user)
    element = None
    if elementtype == "character":
        element = get_object_or_404(world.character_set, name=elementname)
    elif elementtype == "location":
        element = get_object_or_404(world.location_set, name=elementname)
    elif elementtype == "event":
        element = get_object_or_404(world.event_set, name=elementname)
    elif elementtype == "item":
        element = get_object_or_404(world.item_set, name=elementname)

    if request.method == "POST":

        element.delete()

        return redirect("elements_world", worldname=world.name)

    return render(request, "scribedown/delete_element.html", {
        "world": world,
        "element": element
    })

def community(request):
    return render(request, "scribedown/community.html")

def login_view(request):

    if request.method == "POST":

        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect("index")

        else:

            return render(request, "scribedown/login.html", {
                "message": "Invalid username or password."
            })

    return render(request, "scribedown/login.html")

def logout_view(request):

    logout(request)

    return redirect("index")

def register_view(request):

    if request.method == "POST":

        username = request.POST["username"]
        email = request.POST["email"]

        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        # Check passwords match
        if password != confirmation:

            return render(request, "scribedown/register.html", {
                "message": "Passwords must match."
            })

        # Create user
        try:

            user = User.objects.create_user(
                username,
                email,
                password
            )

            user.save()

        except IntegrityError:

            return render(request, "scribedown/register.html", {
                "message": "Username already taken."
            })

        login(request, user)

        return redirect("index")

    return render(request, "scribedown/register.html")


# =========================
# Main wiki homepage
# =========================

@login_required
def wiki_home(request):

    wikis = Wiki.objects.filter(owner=request.user)

    return render(request, "scribedown/wiki_home.html", {
        "wikis": wikis
    })


# =========================
# Create new wiki/world
# =========================

@login_required
def new_wiki(request):

    worlds = World.objects.filter(
        owner=request.user,
        wiki__isnull=True
    )

    if request.method == "POST":

        title = request.POST.get("title")

        world_id = request.POST.get("world")

        is_public = request.POST.get("is_public") == "on"

        world = get_object_or_404(
            World,
            id=world_id,
            owner=request.user
        )

        Wiki.objects.create(
            owner=request.user,
            world=world,
            title=title,
            is_public=is_public
        )

        return redirect("wiki_home")

    return render(request, "scribedown/new_wiki.html", {
        "worlds": worlds
    })


# =========================
# Specific wiki homepage
# =========================

@login_required
def wiki_index(request, wikiname):

    wiki = get_object_or_404(Wiki, title=wikiname, owner=request.user)

    pages = WikiPage.objects.filter(wiki=wiki)

    return render(request, "scribedown/wiki_index.html", {
        "wiki": wiki,
        "pages": pages
    })


# =========================
# Create new page
# =========================

@login_required
def new_page(request, wikiname):

    wiki = get_object_or_404(Wiki, title=wikiname, owner=request.user)

    if request.method == "POST":

        title = request.POST.get("title")
        content = request.POST.get("content")

        if not title or not content:
            return render(request, "scribedown/new_page.html", {
                "wiki": wiki,
                "message": "Both title and content are required."
            })

        if WikiPage.objects.filter(wiki=wiki, title=title).exists():
            return render(request, "scribedown/new_page.html", {
                "wiki": wiki,
                "message": "Page already exists in this wiki."
            })

        page = WikiPage.objects.create(
            wiki=wiki,
            title=title,
            content=content
        )

        return redirect(
            "wiki_page",
            wikiname=wiki.title,
            title=page.title
        )

    return render(request, "scribedown/new_page.html", {
        "wiki": wiki
    })


# =========================
# Specific wiki page
# =========================

@login_required
def wiki_page(request, wikiname, title):

    wiki = get_object_or_404(Wiki, title=wikiname, owner=request.user)

    page = get_object_or_404(
        WikiPage,
        wiki=wiki,
        title=title
    )

    html = markdown.markdown(page.content)

    return render(request, "scribedown/wiki_page.html", {
        "wiki": wiki,
        "page": page,
        "content": html
    })

@login_required
def edit_page(request, wikiname, title):

    wiki = get_object_or_404(Wiki, title=wikiname, owner=request.user)

    page = get_object_or_404(
        WikiPage,
        wiki=wiki,
        title=title
    )

    if request.method == "POST":

        content = request.POST.get("content")

        if not content:
            return render(request, "scribedown/edit_page.html", {
                "wiki": wiki,
                "page": page,
                "message": "Content cannot be empty."
            })

        page.content = content
        page.save()

        return redirect(
            "wiki_page",
            wikiname=wiki.title,
            title=page.title
        )

    return render(request, "scribedown/edit_page.html", {
        "wiki": wiki,
        "page": page
    })

@login_required
def delete_page(request, page_id):

    page = get_object_or_404(WikiPage, id=page_id)

    wikiname = page.wiki.title

    page.delete()

    return redirect("wiki_index", wikiname=wikiname)

# =========================
# Search inside wiki
# =========================

@login_required
def search(request, wikiname):

    wiki = get_object_or_404(Wiki, title=wikiname, owner=request.user)

    query = request.GET.get("q")

    results = WikiPage.objects.filter(
        wiki=wiki,
        title__icontains=query
    )

    return render(request, "scribedown/search.html", {
        "wiki": wiki,
        "query": query,
        "results": results
    })