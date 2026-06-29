from django.db.models import Q
from .models import World, Wiki, Collaborator

# Permission checking functions

def is_world_owner(user, world):
    return world.owner == user

def get_collaborator(user, world):
    return Collaborator.objects.filter(
        world=world,
        user=user
    ).first()

def user_can_view(user, world):
    if is_world_owner(user, world):
        return True

    collaborator = get_collaborator(user, world)
    return collaborator and collaborator.can_view

def user_can_create(user, world):
    if is_world_owner(user, world):
        return True

    collaborator = get_collaborator(user, world)
    return collaborator and collaborator.can_create

def user_can_edit(user, world):
    if is_world_owner(user, world):
        return True

    collaborator = get_collaborator(user, world)
    return collaborator and collaborator.can_edit

def user_can_delete(user, world):
    if is_world_owner(user, world):
        return True

    collaborator = get_collaborator(user, world)
    return collaborator and collaborator.can_delete

def user_can_delegate(user, world):
    if is_world_owner(user, world):
        return True

    collaborator = get_collaborator(user, world)
    return collaborator and collaborator.can_delegate

def visible_worlds(user):
    return World.objects.filter(
        Q(owner=user) |
        Q(
            collaborator__user=user,
            collaborator__can_view=True
        )
    ).distinct()