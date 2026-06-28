from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class World(models.Model):
    id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)


    def __str__(self):
        return self.name

class Character(models.Model):
    id = models.AutoField(primary_key=True)
    world = models.ForeignKey(World, on_delete=models.CASCADE)

    name = models.CharField(max_length=100)
    family_name = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    age = models.IntegerField(null=True, blank=True)
    race = models.ForeignKey(
        'Race',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    birthplace = models.ForeignKey(
        'Location',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='birthplace_characters'
    )
    deathplace = models.ForeignKey(
        'Location',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='deathplace_characters'
    )

class Location(models.Model):
    id = models.AutoField(primary_key=True)
    world = models.ForeignKey(World, on_delete=models.CASCADE)

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    founder = models.CharField(max_length=100, blank=True)
    founding_date = models.DateField(null=True, blank=True)
    decline_date = models.DateField(null=True, blank=True)
    characters = models.ManyToManyField(Character, blank=True)


class Event(models.Model):
    id = models.AutoField(primary_key=True)
    world = models.ForeignKey(World, on_delete=models.CASCADE)

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    date = models.DateField(null=True, blank=True)
    characters = models.ManyToManyField(Character, blank=True)
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

class Object(models.Model):
    id = models.AutoField(primary_key=True)
    world = models.ForeignKey(World, on_delete=models.CASCADE)

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    locations = models.ManyToManyField(Location, blank=True)
    characters = models.ManyToManyField(Character, blank=True)

class Race(models.Model):
    id = models.AutoField(primary_key=True)
    world = models.ForeignKey(World, on_delete=models.CASCADE)

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

class Faction(models.Model):
    id = models.AutoField(primary_key=True)
    world = models.ForeignKey(World, on_delete=models.CASCADE)

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    members = models.ManyToManyField(Character, blank=True)

class Group(models.Model):
    id = models.AutoField(primary_key=True)
    world = models.ForeignKey(World, on_delete=models.CASCADE)

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    members = models.ManyToManyField(Character, blank=True)

class Wiki(models.Model):
    id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    world = models.OneToOneField(World, on_delete=models.CASCADE)

    title = models.CharField(max_length=100)

    is_public = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class WikiPage(models.Model):
    id = models.AutoField(primary_key=True)
    PAGE_TYPES = [
        ("home", "Home Page"),
        ("normal", "Normal Page"),
        ("elementless", "Elementless Page"),
        ("category", "Category Page"),
    ]
    wiki = models.ForeignKey(Wiki, on_delete=models.CASCADE)

    title = models.CharField(max_length=200)
    content = models.TextField()  # Markdown stored here

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    page_type = models.CharField(max_length=20, choices=PAGE_TYPES, default="normal")

    categories = models.ManyToManyField("CategoryPage", symmetrical=False, blank=True, related_name='categorized_pages')
    class Meta:
        unique_together = ("wiki", "title")

    def __str__(self):
        return f"{self.wiki.title} - {self.title}"

class CategoryPage(models.Model):
    id = models.AutoField(primary_key=True)
    page = models.OneToOneField(
        WikiPage,
        on_delete=models.CASCADE
    )

class HomePage(models.Model):
    id = models.AutoField(primary_key=True)
    page = models.OneToOneField(
        WikiPage,
        on_delete=models.CASCADE
    )

class NormalPage(models.Model):
    id = models.AutoField(primary_key=True)
    page = models.OneToOneField(
        WikiPage,
        on_delete=models.CASCADE
    )

class ElementlessPage(models.Model):
    id = models.AutoField(primary_key=True)
    page = models.OneToOneField(
        WikiPage,
        on_delete=models.CASCADE
    )

class WikiLink(models.Model):
    id = models.AutoField(primary_key=True)
    wiki_page = models.ForeignKey(WikiPage, on_delete=models.CASCADE)

    content_type = models.CharField(max_length=20)
    object_id = models.IntegerField()

class Collaborator(models.Model):
    id = models.AutoField(primary_key=True)
    world = models.ForeignKey(World, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    can_view = models.BooleanField(default=True)
    can_create = models.BooleanField(default=False)
    can_edit = models.BooleanField(default=False)
    can_delete = models.BooleanField(default=False)
    can_delegate = models.BooleanField(default=False)

    class Meta:
        unique_together = ("world", "user")