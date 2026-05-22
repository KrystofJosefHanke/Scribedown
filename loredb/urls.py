from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("elements/", views.elements, name="elements"),
    path("elements/world/<str:worldname>/", views.elements_world, name="elements_world"),
    path("elements/new/", views.new_world, name="new_world"),
    path("elements/world/<str:worldname>/edit/", views.edit_world, name="edit_world"),
    path("elements/world/<str:worldname>/delete/", views.delete_world, name="delete_world"),
    path("elements/world/<str:worldname>/newelement/", views.new_element, name="new_element"),
    path("elements/world/<str:worldname>/editelement/<str:elementtype>/<str:elementname>/", views.edit_element, name="edit_element"),
    path("elements/world/<str:worldname>/deleteelement/<str:elementtype>/<str:elementname>/", views.delete_element, name="delete_element"),
    path("elements/world/<str:worldname>/characters/", views.characters, name="characters"),
    path("elements/world/<str:worldname>/locations/", views.locations, name="locations"),
    path("elements/world/<str:worldname>/events/", views.events, name="events"),
    path("elements/world/<str:worldname>/items/", views.items, name="items"),
    path("elements/world/<str:worldname>/races/", views.races, name="races"),
    path("elements/world/<str:worldname>/characters/<str:charactername>/", views.character_detail, name="character_detail"),
    path("elements/world/<str:worldname>/locations/<str:locationname>/", views.location_detail, name="location_detail"),
    path("elements/world/<str:worldname>/events/<str:eventname>/", views.event_detail, name="event_detail"),
    path("elements/world/<str:worldname>/items/<str:itemname>/", views.item_detail, name="item_detail"),
    path("elements/world/<str:worldname>/races/<str:racename>/", views.race_detail, name="race_detail"),
    path("wikis/", views.wiki_home, name="wiki_home"),
    path("wikis/new/", views.new_wiki, name="new_wiki"),
    path("wikis/wiki/<str:wikiname>/", views.wiki_index, name="wiki_index"),
    path("wikis/wiki/<str:wikiname>/newpage/", views.new_page, name="new_page"),
    path("wikis/wiki/<str:wikiname>/page/<str:title>/", views.wiki_page, name="wiki_page"),
    path("wikis/wiki/<str:wikiname>/page/<str:title>/edit/", views.edit_page, name="edit_page"),
    path("wikis/wiki/<str:wikiname>/page/<str:title>/delete/", views.delete_page, name="delete_page"),
    path("wikis/wiki/<str:wikiname>/edit/", views.edit_wiki, name="edit_wiki"),
    path("wikis/wiki/<str:wikiname>/delete/", views.delete_wiki, name="delete_wiki"),
    path("wikis/wiki/<str:wikiname>/search/", views.search, name="search"),
    path("community/", views.community, name="community"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("createaccount/", views.register_view, name="register"),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)