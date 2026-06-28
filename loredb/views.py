# views.py

from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import World, WikiPage, Wiki, Collaborator, Character, Location, Event, Object, Faction, Group

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
def elements_world(request, world_id):
    world = get_object_or_404(World, id=world_id, owner=request.user)
    characters = world.character_set.all()
    locations = world.location_set.all()
    events = world.event_set.all()
    objects = world.object_set.all()
    races = world.race_set.all()
    factions = world.faction_set.all()
    groups = world.group_set.all()

    return render(request, "scribedown/elements_world.html", {
        "world": world,
        "characters": characters,
        "locations": locations,
        "events": events,
        "objects": objects,
        "races": races,
        "factions": factions,
        "groups": groups
    })

@login_required
def new_world(request):

    if request.method == "POST":

        name = request.POST.get("name")
        description = request.POST.get("description")

        if not name:
            messages.error(request, "Name is required.")
            return redirect("new_world")

        if World.objects.filter(name=name).exists():
            messages.error(request, "World with this name already exists.")
            return redirect("new_world")

        World.objects.create(
            owner=request.user,
            name=name,
            description=description
        )
        messages.success(request, "World created successfully.")

        return redirect("elements")

    return render(request, "scribedown/new_world.html")

@login_required
def edit_world(request, world_id):

    world = get_object_or_404(World, id=world_id, owner=request.user)

    if request.method == "POST":
        # Handle world edit logic here
        return redirect("elements")

    return render(request, "scribedown/edit_world_index.html", {
        "world": world
    })

@login_required
def edit_world_basic(request, world_id):
    world = get_object_or_404(World, id=world_id, owner=request.user)

    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")

        if not name:
            messages.error(request, "Name is required.")
            return redirect("edit_world_basic", world_id=world.id)

        if World.objects.filter(name=name).exclude(name=world.name).exists():
            messages.error(request, "World with this name already exists.")
            return redirect("edit_world_basic", world_id=world.id)

        world.name = name
        world.description = description
        world.save()

        messages.success(request, "World updated successfully.")
        return redirect("elements")

    return render(request, "scribedown/edit_world_basic.html", {
        "world": world
    })

@login_required
def edit_world_access(request, world_id):
    world = get_object_or_404(World, id=world_id, owner=request.user)
    users = User.objects.exclude(id=request.user.id)
    collaborators = Collaborator.objects.filter(
        world=world
    ).select_related("user")

    users = User.objects.exclude(
        id=request.user.id
    ).exclude(
        id__in=collaborators.values_list("user_id", flat=True)
    )

    if request.method == "POST":
        user_id = request.POST.get("new_collaborator")

        if user_id:
            user = get_object_or_404(User, id=user_id)

            Collaborator.objects.get_or_create(
                world=world,
                user=user
            )

            messages.success(
                request,
                f"{user.username} added as collaborator."
            )

        return redirect("edit_world_access", world_id=world.id)
    return render(request, "scribedown/edit_world_access.html", {
        "world": world,
        "collaborators": collaborators,
        "users": users
    })

@login_required
def remove_collaborator(request, world_id, user_id):
    world = get_object_or_404(World, id=world_id, owner=request.user)
    collaborator = get_object_or_404(
        Collaborator,
        world=world,
        user_id=user_id
    )

    if request.method == "POST":
        collaborator.delete()
        messages.success(
            request,
            f"{collaborator.user.username} removed as collaborator."
        )
        return redirect("edit_world_access", world_id=world.id)

    return render(request, "scribedown/remove_collaborator.html", {
        "world": world,
        "collaborator": collaborator
    })

@login_required
def edit_collaborator(request, world_id, user_id):
    world = get_object_or_404(World, id=world_id, owner=request.user)
    collaborator = get_object_or_404(
        Collaborator,
        world=world,
        user_id=user_id
    )

    if request.method == "POST":
        can_view = request.POST.get("can_view") == "on"
        can_create = request.POST.get("can_create") == "on"
        can_edit = request.POST.get("can_edit") == "on"
        can_delete = request.POST.get("can_delete") == "on"
        can_delegate = request.POST.get("can_delegate") == "on"

        collaborator.can_view = can_view
        collaborator.can_create = can_create
        collaborator.can_edit = can_edit
        collaborator.can_delete = can_delete
        collaborator.can_delegate = can_delegate
        collaborator.save()

        messages.success(
            request,
            f"{collaborator.user.username}'s permissions updated."
        )
        return redirect("edit_world_access", world_id=world.id)

    return render(request, "scribedown/edit_collaborator.html", {
        "world": world,
        "collaborator": collaborator
    })

@login_required
def delete_world(request, world_id):

    world = get_object_or_404(
        World,
        id=world_id,
        owner=request.user
    )

    if request.method == "POST":

        world.delete()

        messages.success(request, "World deleted successfully.")
        return redirect("elements")

    return render(request, "scribedown/delete_world.html", {
        "world": world
    })

@login_required
def new_element(request, world_id):
    world = get_object_or_404(World, id=world_id, owner=request.user)

    if request.method == "POST":

        element_type = request.POST.get("element_type")
        name = request.POST.get("name")
        description = request.POST.get("description")

        if not name:
            messages.error(request, "Name is required.")
            return redirect("new_element", world_id=world.id)

        if element_type == "character":
            family_name = request.POST.get("family_name")
            age = request.POST.get("age")
            race_id = request.POST.get("race")
            race = None
            if race_id:
                race = Race.objects.get(id=race_id)
            birthplace_id = request.POST.get("birthplace")
            birthplace = None
            if birthplace_id:
                birthplace = Location.objects.get(id=birthplace_id)
            deathplace_id = request.POST.get("deathplace")
            deathplace = None
            if deathplace_id:
                deathplace = Location.objects.get(id=deathplace_id)
            world.character_set.create(
                name=name,
                description=description,
                family_name=family_name,
                age=age,
                race=race,
                birthplace=birthplace,
                deathplace=deathplace
            )
        elif element_type == "location":
            world.location_set.create(name=name, description=description)
        elif element_type == "event":
            world.event_set.create(name=name, description=description)
        elif element_type == "object":
            world.object_set.create(name=name, description=description)
        elif element_type == "race":
            world.race_set.create(name=name, description=description)
        elif element_type == "":
            messages.error(request, "Select an element type.")
            return redirect("new_element", world_id=world.id)
        elif not element_type:
            messages.error(request, "Select an element type.")
            return redirect("new_element", world_id=world.id)
        messages.success(request, f"{element_type.capitalize()} created successfully.")

        return redirect("elements_world", world_id=world.id)

    return render(request, "scribedown/new_element.html", {
        "world": world
    })

@login_required
def edit_element(request, world_id, element_type, element_id):
    world = get_object_or_404(World, id=world_id, owner=request.user)
    element = None
    if element_type == "character":
        element = get_object_or_404(world.character_set, id=element_id)
    elif element_type == "location":
        element = get_object_or_404(world.location_set, id=element_id)
    elif element_type == "event":
        element = get_object_or_404(world.event_set, id=element_id)
    elif element_type == "object":
        element = get_object_or_404(world.object_set, id=element_id)

    if request.method == "POST":

        name = request.POST.get("name")
        description = request.POST.get("description")

        if not name:
            messages.error(request, "Name is required.")
            return redirect("edit_element", world_id=world.id, element_type=element_type, element_id=element.id)

        element.name = name
        element.description = description
        element.save()

        messages.success(request, f"{element_type.capitalize()} updated successfully.")
        return redirect("elements_world", world_id=world.id)
    return render(request, "scribedown/edit_element.html", {
        "world": world,
        "element": element
    })

@login_required
def delete_element(request, world_id, element_type, element_id):
    world = get_object_or_404(World, id=world_id, owner=request.user)
    element = None
    if element_type == "character":
        element = get_object_or_404(world.character_set, id=element_id)
    elif element_type == "location":
        element = get_object_or_404(world.location_set, id=element_id)
    elif element_type == "event":
        element = get_object_or_404(world.event_set, id=element_id)
    elif element_type == "object":
        element = get_object_or_404(world.object_set, id=element_id)

    if request.method == "POST":

        element.delete()
        messages.success(request, f"{element_type.capitalize()} deleted successfully.")

        return redirect("elements_world", world_id=world.id)

    return render(request, "scribedown/delete_element.html", {
        "world": world,
        "element": element
    })

@login_required
def characters(request, world_id):
    world = get_object_or_404(World, id=world_id, owner=request.user)
    characters = world.character_set.all()
    return render(request, "scribedown/characters.html", {
        "world": world,
        "characters": characters
    })

@login_required
def character_detail(request, world_id, character_id):
    world = get_object_or_404(World, id=world_id, owner=request.user)
    character = get_object_or_404(world.character_set, id=character_id)
    return render(request, "scribedown/character_detail.html", {
        "world": world,
        "character": character
    })

@login_required
def locations(request, world_id):
    world = get_object_or_404(World, id=world_id, owner=request.user)
    locations = world.location_set.all()
    return render(request, "scribedown/locations.html", {
        "world": world,
        "locations": locations
    })

@login_required
def location_detail(request, world_id, location_id):
    world = get_object_or_404(World, id=world_id, owner=request.user)
    location = get_object_or_404(world.location_set, id=location_id)
    return render(request, "scribedown/location_detail.html", {
        "world": world,
        "location": location
    })

@login_required
def events(request, world_id):
    world = get_object_or_404(World, id=world_id, owner=request.user)
    events = world.event_set.all()
    return render(request, "scribedown/events.html", {
        "world": world,
        "events": events
    })

@login_required
def event_detail(request, world_id, event_id):
    world = get_object_or_404(World, id=world_id, owner=request.user)
    event = get_object_or_404(world.event_set, id=event_id)
    return render(request, "scribedown/event_detail.html", {
        "world": world,
        "event": event
    })

@login_required
def objects(request, world_id):
    world = get_object_or_404(World, id=world_id, owner=request.user)
    objects = world.object_set.all()
    return render(request, "scribedown/objects.html", {
        "world": world,
        "objects": objects
    })

@login_required
def object_detail(request, world_id, object_id):
    world = get_object_or_404(World, id=world_id, owner=request.user)
    object = get_object_or_404(world.object_set, id=object_id)
    return render(request, "scribedown/object_detail.html", {
        "world": world,
        "object": object
    })

@login_required
def races(request, world_id):
    world = get_object_or_404(World, id=world_id, owner=request.user)
    races = world.race_set.all()
    return render(request, "scribedown/races.html", {
        "world": world,
        "races": races
    })

@login_required
def race_detail(request, world_id, race_id):
    world = get_object_or_404(World, id=world_id, owner=request.user)
    race = get_object_or_404(world.race_set, id=race_id)
    return render(request, "scribedown/race_detail.html", {
        "world": world,
        "race": race
    })

@login_required
def factions(request, world_id):
    world = get_object_or_404(World, id=world_id, owner=request.user)
    factions = world.faction_set.all()
    return render(request, "scribedown/factions.html", {
        "world": world,
        "factions": factions
    })

@login_required
def faction_detail(request, world_id, faction_id):
    world = get_object_or_404(World, id=world_id, owner=request.user)
    faction = get_object_or_404(world.faction_set, id=faction_id)
    return render(request, "scribedown/faction_detail.html", {
        "world": world,
        "faction": faction
    })

@login_required
def groups(request, world_id):
    world = get_object_or_404(World, id=world_id, owner=request.user)
    groups = world.group_set.all()
    return render(request, "scribedown/groups.html", {
        "world": world,
        "groups": groups
    })

@login_required
def group_detail(request, world_id, group_id):
    world = get_object_or_404(World, id=world_id, owner=request.user)
    group = get_object_or_404(world.group_set, id=group_id)
    return render(request, "scribedown/group_detail.html", {
        "world": world,
        "group": group
    })

@login_required
def delete_element(request, world_id, element_type, element_id):
    world = get_object_or_404(World, id=world_id, owner=request.user)
    element = None
    if element_type == "character":
        element = get_object_or_404(world.character_set, id=element_id)
    elif element_type == "location":
        element = get_object_or_404(world.location_set, id=element_id)
    elif element_type == "event":
        element = get_object_or_404(world.event_set, id=element_id)
    elif element_type == "object":
        element = get_object_or_404(world.object_set, id=element_id)

    if request.method == "POST":

        element.delete()
        messages.success(request, f"{element_type.capitalize()} deleted successfully.")

        return redirect("elements_world", world_id=world.id)

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
            messages.success(request, "Logged in successfully.")
            return redirect("index")

        else:

            messages.error(
                request,
                "Invalid username or password."
            )
        return redirect("login")

    return render(request, "scribedown/login.html")

def logout_view(request):

    logout(request)
    messages.success(request, "Logged out successfully.")

    return redirect("index")

@login_required
def profile(request):
    return render(request, "scribedown/profile.html")

@login_required
def settings_view(request):
    return render(request, "scribedown/settings_index.html")

@login_required
def profile_settings(request):

    if request.method == "POST":

        user = request.user

        current_password = request.POST.get("current_password")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        password_change_requested = (
            current_password or
            new_password or
            confirm_password
            )

        if password_change_requested:

            if not current_password:
                messages.error(
                    request,
                    "Current password is required."
                )
                return redirect("profile_settings")

            if not new_password:
                messages.error(
                    request,
                    "New password is required."
                )
                return redirect("profile_settings")

            if new_password != confirm_password:
                messages.error(
                    request,
                    "New password and confirmation do not match."
                )
                return redirect("profile_settings")

            if not user.check_password(current_password):
                messages.error(
                    request,
                    "Current password is incorrect."
                )
                return redirect("profile_settings")

            user.set_password(new_password)

        user.save()
        update_session_auth_hash(request, user)

        messages.success(
            request,
            "Settings saved successfully."
        )

        return redirect("profile_settings")

    return render(
        request,
        "scribedown/profile_settings.html"
    )

@login_required
def visual_settings(request):
    return render(request, "scribedown/visual_settings.html")


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

        if not title:
            messages.error(request, "Title is required.")
            return redirect("new_wiki")
        
        if Wiki.objects.filter(title=title).exists():
            messages.error(request, "Wiki with this title already exists.")
            return redirect("new_wiki")

        if not world:
            messages.error(request, "Select a world.")
            return redirect("new_wiki")

        wiki = Wiki.objects.create(
            owner=request.user,
            world=world,
            title=title,
            is_public=is_public
        )

        WikiPage.objects.create(
            wiki=wiki,
            title="Home",
            page_type="home"
        )

        WikiPage.objects.create(
            wiki=wiki,
            title="Featured Pages",
            page_type="category"
        )

        WikiPage.objects.create(
            wiki=wiki,
            title="Featured Categories",
            page_type="category"
        )
        messages.success(request, "Wiki created successfully.")
        
        return redirect("wiki_home")

    return render(request, "scribedown/new_wiki.html", {
        "worlds": worlds
    })


# =========================
# Specific wiki homepage
# =========================

@login_required
def wiki_index(request, wiki_id):

    wiki = get_object_or_404(Wiki, id=wiki_id, owner=request.user)

    pages = WikiPage.objects.filter(wiki=wiki)

    return render(request, "scribedown/wiki_index.html", {
        "wiki": wiki,
        "pages": pages
    })


# =========================
# Create new page
# =========================

@login_required
def new_page(request, wiki_id):

    wiki = get_object_or_404(Wiki, id=wiki_id, owner=request.user)

    if request.method == "POST":

        title = request.POST.get("title")
        content = request.POST.get("content")
        type = request.POST.get("page_type")

        if not title or not content:
            messages.error(request, "Title and content are required.")
            return redirect("new_page", wiki_id=wiki.id)

        if WikiPage.objects.filter(wiki=wiki, title=title).exists():
            messages.error(request, "Page with this title already exists.")
            return redirect("new_page", wiki_id=wiki.id)

        page = WikiPage.objects.create(
            wiki=wiki,
            title=title,
            content=content,
            page_type=type
        )

        messages.success(request, "Page created successfully.")
        return redirect(
            "wiki_page",
            wiki_id=wiki.id,
            title=page.title
        )
        if not type:
            messages.error(request, "Select a page type.")
            return redirect("new_page", wiki_id=wiki.id)

    return render(request, "scribedown/new_page.html", {
        "wiki": wiki
    })


# =========================
# Specific wiki page
# =========================

@login_required
def wiki_page(request, wiki_id, title):

    wiki = get_object_or_404(Wiki, id=wiki_id, owner=request.user)

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
            messages.error(request, "Content cannot be empty.")
            return redirect("edit_page", wikiname=wiki.title, title=page.title)

        page.content = content
        page.save()

        messages.success(request, "Page updated successfully.")
        return redirect(
            "wiki_page",
            wiki_id=wiki.id,
            title=page.title
        )

    return render(request, "scribedown/edit_page.html", {
        "wiki": wiki,
        "page": page
    })

@login_required
def delete_page(request, wiki_id, title):
    wiki = get_object_or_404(Wiki, id=wiki_id, owner=request.user)
    page = get_object_or_404(WikiPage, wiki=wiki, title=title)

    if request.method == "POST":

        wiki = page.wiki
        page.delete()

        messages.success(request, "Page deleted successfully.")
        return redirect("wiki_index", wiki_id=wiki.id)

    return render(request, "scribedown/delete_page.html", {
        "page": page,
        "wiki": wiki
    })

@login_required
def edit_wiki(request, wiki_id):
    wiki = get_object_or_404(Wiki, id=wiki_id, owner=request.user)

    if request.method == "POST":

        title = request.POST.get("title")
        is_public = request.POST.get("is_public") == "on"

        if not title:
            messages.error(request, "Title is required.")
            return redirect("edit_wiki", wiki_id=wiki.id)

        if Wiki.objects.filter(title=title).exclude(id=wiki.id).exists():
            messages.error(request, "Wiki with this title already exists.")
            return redirect("edit_wiki", wiki_id=wiki.id)

        wiki.title = title
        wiki.is_public = is_public
        wiki.save()
        messages.success(request, "Wiki updated successfully.")

        return redirect("wiki_index", wiki_id=wiki.id)

    return render(request, "scribedown/edit_wiki.html", {
        "wiki": wiki
    })

@login_required
def delete_wiki(request, wiki_id):
    wiki = get_object_or_404(Wiki, id=wiki_id, owner=request.user)

    if request.method == "POST":

        wiki.delete()
        messages.success(request, "Wiki deleted successfully.")

        return redirect("wiki_home")

    return render(request, "scribedown/delete_wiki.html", {
        "wiki": wiki
    })

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