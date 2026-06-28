from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("elements/", views.elements, name="elements"),
    path("elements/world/<int:world_id>/", views.elements_world, name="elements_world"),
    path("elements/new/", views.new_world, name="new_world"),
    path("elements/world/<int:world_id>/edit/", views.edit_world, name="edit_world"),
    path("elements/world/<int:world_id>/edit/basic/", views.edit_world_basic, name="edit_world_basic"),
    path("elements/world/<int:world_id>/edit/access/", views.edit_world_access, name="edit_world_access"),
    path("elements/world/<int:world_id>/edit/access/remove/<int:user_id>/", views.remove_collaborator, name="remove_collaborator"),
    path("elements/world/<int:world_id>/delete/", views.delete_world, name="delete_world"),
    path("elements/world/<int:world_id>/newelement/", views.new_element, name="new_element"),
    path("elements/world/<int:world_id>/editelement/<str:element_type>/<int:element_id>/", views.edit_element, name="edit_element"),
    path("elements/world/<int:world_id>/deleteelement/<str:element_type>/<int:element_id>/", views.delete_element, name="delete_element"),
    path("elements/world/<int:world_id>/characters/", views.characters, name="characters"),
    path("elements/world/<int:world_id>/locations/", views.locations, name="locations"),
    path("elements/world/<int:world_id>/events/", views.events, name="events"),
    path("elements/world/<int:world_id>/items/", views.items, name="items"),
    path("elements/world/<int:world_id>/races/", views.races, name="races"),
    path("elements/world/<int:world_id>/characters/<int:character_id>/", views.character_detail, name="character_detail"),
    path("elements/world/<int:world_id>/locations/<int:location_id>/", views.location_detail, name="location_detail"),
    path("elements/world/<int:world_id>/events/<int:event_id>/", views.event_detail, name="event_detail"),
    path("elements/world/<int:world_id>/items/<int:item_id>/", views.item_detail, name="item_detail"),
    path("elements/world/<int:world_id>/races/<int:race_id>/", views.race_detail, name="race_detail"),
    path("wikis/", views.wiki_home, name="wiki_home"),
    path("wikis/new/", views.new_wiki, name="new_wiki"),
    path("wikis/wiki/<int:wiki_id>/", views.wiki_index, name="wiki_index"),
    path("wikis/wiki/<int:wiki_id>/newpage/", views.new_page, name="new_page"),
    path("wikis/wiki/<int:wiki_id>/page/<int:page_id>/", views.wiki_page, name="wiki_page"),
    path("wikis/wiki/<int:wiki_id>/page/<int:page_id>/edit/", views.edit_page, name="edit_page"),
    path("wikis/wiki/<int:wiki_id>/page/<int:page_id>/delete/", views.delete_page, name="delete_page"),
    path("wikis/wiki/<int:wiki_id>/edit/", views.edit_wiki, name="edit_wiki"),
    path("wikis/wiki/<int:wiki_id>/delete/", views.delete_wiki, name="delete_wiki"),
    path("wikis/wiki/<int:wiki_id>/search/", views.search, name="search"),
    path("community/", views.community, name="community"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("profile/", views.profile, name="profile"),
    path("settings/", views.settings_view, name="settings"),
    path("settings/profile/", views.profile_settings, name="profile_settings"),
    path("settings/visual/", views.visual_settings, name="visual_settings")
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)