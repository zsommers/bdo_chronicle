from django.core.validators import MinValueValidator
from django.db import models


class Kingdom(models.Model):
    """
    One of the major kingdoms in the game which contains a set of
    :model:`nodes.Territory`.
    """
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Territory(models.Model):
    """
    A subdivision and child of :model:`nodes.Kingdom`. Territorys have a set of
    :model:`nodes.Node`.
    """
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=100)
    kingdom = models.ForeignKey(Kingdom,
                                on_delete=models.CASCADE,
                                related_name='territories')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'territories'


class Node(models.Model):
    """
    A point in the network of Nodes. Nodes are connected to other
    :model:`nodes.Node` and exist within a :model:`nodes.Territory`. Hub nodes
    are the starting points for node networks. Non-hub nodes require an
    investment of contribution points with the node manager. Additionally,
    many Nodes have a set of :model:`nodes.Property` and/or a one or two
    :model:`nodes.Resource`.
    """
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=100)
    territory = models.ForeignKey(Territory,
                                  on_delete=models.CASCADE,
                                  related_name='nodes')
    is_hub = models.BooleanField(default=False)
    contribution_cost = models.IntegerField(null=True,
                                            blank=True,
                                            validators=[MinValueValidator(0)])
    # TODO some sort of validation to ensure that hubs don't have contribution
    # costs, while non-hubs do
    node_manager = models.CharField(max_length=100,
                                    null=True,
                                    blank=True)
    connected_nodes = models.ManyToManyField('self',
                                             blank=True)

    def save(self, *args, **kwargs):
        """Overwrite save to set blank string to None/NULL"""
        if not self.node_manager:
            self.node_manager = None
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Resource(models.Model):
    """
    Resources are attached to :model:`nodes.Node` and can be exploited by NPC
    workers.
    """
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    material = models.ForeignKey('crafting.Material',
                                 on_delete=models.CASCADE,
                                 related_name='resources')
    node = models.ForeignKey(Node,
                             on_delete=models.CASCADE,
                             related_name='resources')
    contribution_cost = models.IntegerField(validators=[MinValueValidator(0)])

    def __str__(self):
        return 'Resource {} at Node {}'.format(self.material.name,
                                               self.node.name)


class Property(models.Model):
    """
    Properties belong to :model:`nodes.Node`. They can be rented in exchange for
    contribution points and put to a variety of uses, which are detailed by
    :model:`nodes.PropertyStation`.
    """
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=100)
    node = models.ForeignKey(Node,
                             on_delete=models.CASCADE,
                             related_name='properties')
    parent_property = models.ForeignKey('self',
                                        null=True,
                                        blank=True,
                                        related_name='child_properties')
    stations = models.ManyToManyField('crafting.Station',
                                      through='PropertyStation',
                                      related_name='properties')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'properties'


class PropertyStation(models.Model):
    """
    PropertyStations define the possible uses of a :model:`nodes.Property`. They
    show which :model:`crafting.Station` are available and what the maximum
    level is.
    """
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    property = models.ForeignKey(Property,
                                 on_delete=models.CASCADE)
    station = models.ForeignKey('crafting.Station',
                                on_delete=models.CASCADE)
    max_level = models.IntegerField()

    def __str__(self):
        return "Property: {} - Station: {}".format(self.property, self.station)

    class Meta:
        verbose_name_plural = 'property stations'

    # TODO: Some sort of fancy many to many to crafting.stations

    # All possible property uses
    # agerian_armor_forge
    # armor_workshop
    # azwell_amulet_forge
    # azwell_axe_forge
    # azwell_longsword_forge
    # azwell_long_bow_forge
    # azwell_shortsword_forge
    # azwell_staff_forge
    # bronze_dagger_forge
    # cannon_workshop
    # carpentry_workshop
    # costume_mill
    # crop_workbench
    # demihuman_amulet_forge
    # demihuman_axe_forge
    # demihuman_longsword_forge
    # demihuman_long_bow_forge
    # demihuman_shortsword_forge
    # demihuman_staff_forge
    # fish_workbench
    # furniture_workshop
    # goldsmith
    # handcraft_workshop
    # herrick_talisman_forge
    # horse_gear_workshop
    # horse_ranch
    # incense_trinket_forge
    # lodging
    # mineral_workbench
    # mushroom_workbench
    # refinery
    # residence
    # saiyer_ornamental_knot_forge
    # ship_part_workshop
    # shipyard
    # storage
    # tool_workshop
    # vangertz_shield_forge
    # wagon_part_workshop
    # weapon_workshop
    # wood_workbench
