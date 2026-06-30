import re

from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import Character, Event, Faction, Group, Location, Object, Race, WikiPage

ELEMENT_MODELS = {
    "character": Character,
    "event": Event,
    "location": Location,
    "object": Object,
    "group": Group,
    "faction": Faction,
    "race": Race,
}

WIKILINK_PATTERN = re.compile(r"\[\[(.*?)\]\]")

def replace_wikilink(match, wiki):
    content = match.group(1)
    parts = content.split("|", 1)

    page_title = parts[0].strip()

    if len(parts) == 2:
        link_text = parts[1].strip()
    else:
        link_text = page_title
    
    page = WikiPage.objects.filter(
        wiki=wiki,
        title=page_title
    ).first()

    if page is None:
        return f'<span class="text-danger">{link_text}</span>'

    url = reverse(
        "wiki_page",
        kwargs={
            "wiki_id": wiki.id,
            "page_id": page.id,
        },
    )

    return f'<a href="{url}">{link_text}</a>'

def render_wikilinks(text, wiki):

    html = WIKILINK_PATTERN.sub(
        lambda match: replace_wikilink(match, wiki),
        text,
    )

    return mark_safe(html)