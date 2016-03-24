from django.db import models


class Material(models.Model):
    """
    A type of crafting material.
    """
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=100)

    # There should be some link to whether this is gatherable by the player
    # directly. In fact, is there a gathered resource that the player is unable
    # to gather personally?

    def __str__(self):
        return self.name


class Station(models.Model):
    """
    A crafting station or method (i.e. grinding by hand).
    """
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """
    A recipe takes a set of :model:`crafting.Material` that is used at a
    :model:`crafting.Station` and produces a set of :model:`crafting.Material`.
    """
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=100)
    input_materials = models.ManyToManyField(Material,
                                             related_name='input_recipes')
    station = models.ForeignKey(Station,
                                related_name='recipes')
    output_materials = models.ManyToManyField(Material,
                                              related_name='output_recipes')

    def __str__(self):
        return self.name
