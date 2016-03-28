from django.db import IntegrityError
from django.test import TestCase

from .models import (Kingdom,
                     Node,
                     Property,
                     PropertyStation,
                     Resource,
                     Territory)
from crafting.models import Material, Station


class KingdomTerritoryRelationTests(TestCase):
    """
    A Kingdom should have a Queryset of Territories and a Territory should have
    one Kingdom.
    """
    @classmethod
    def setUpTestData(cls):
        # This works because any modification to the territory set are negated
        # by the removal of territories between tests
        cls.kingdom = Kingdom.objects.create(name='Test Kingdom')

    def test_no_territory(self):
        """
        Test Kingdom with no Territory.
        """
        self.assertQuerysetEqual(self.kingdom.territories.all(),
                                 [])

    def test_one_territory(self):
        """
        Test Kingdom with one Territory.
        """
        territory = Territory.objects.create(name='Test Territory',
                                                kingdom=self.kingdom)
        self.assertQuerysetEqual(self.kingdom.territories.all(),
                                 [territory.__repr__()])
        self.assertEqual(territory.kingdom,
                         self.kingdom)

    def test_two_territories(self):
        """
        Test Kingdom with two Territories.
        """
        territory1 = Territory.objects.create(name='Test Territory 1',
                                              kingdom=self.kingdom)
        territory2 = Territory.objects.create(name='Test Territory 2',
                                              kingdom=self.kingdom)
        self.assertQuerysetEqual(self.kingdom.territories.all()\
                                                         .order_by('name'),
                                 [territory1.__repr__(),
                                  territory2.__repr__()])
        self.assertEqual(territory1.kingdom,
                         self.kingdom)
        self.assertEqual(territory2.kingdom,
                         self.kingdom)

    def test_no_kingdom(self):
        """
        Test Territory with no Kingdom.
        """
        with self.assertRaises(IntegrityError):
            Territory.objects.create(name='Test Territory')


class TerritoryNodeRelationTests(TestCase):
    """
    A Territory should have a Queryset of Nodes and a Node should have one
    Territory.
    """
    @classmethod
    def setUpTestData(cls):
        # Tests won't need access to Kingdom instance
        kingdom = Kingdom.objects.create(name='Test Kingdom')
        # This works because any modification to the node set are negated by the
        # removal of nodes between tests
        cls.territory = Territory.objects.create(name='Test Territory',
                                                 kingdom=kingdom)

    def test_no_nodes(self):
        """
        Test Territory with no Node.
        """
        self.assertQuerysetEqual(self.territory.nodes.all(),
                                 [])

    def test_one_node(self):
        """
        Test Territory with one Node.
        """
        node = create_node(name='Test Node',
                           territory=self.territory)
        self.assertQuerysetEqual(self.territory.nodes.all(),
                                 [node.__repr__()])
        self.assertEqual(node.territory,
                         self.territory)

    def test_two_nodes(self):
        """
        Test Territory with two Nodes.
        """
        node1 = create_node(name='Test Node 1',
                            territory=self.territory)
        node2 = create_node(name='Test Node 2',
                            territory=self.territory)
        self.assertQuerysetEqual(self.territory.nodes.all()\
                                                     .order_by('name'),
                                 [node1.__repr__(),
                                  node2.__repr__()])
        self.assertEqual(node1.territory,
                         self.territory)
        self.assertEqual(node2.territory,
                         self.territory)

    def test_no_territory(self):
        """
        Test Node with no Territory.
        """
        with self.assertRaises(IntegrityError):
            create_node(name='Test Node',
                        territory=None)


class NodeNodeRelationTests(TestCase):
    """
    A Node can be related to other Nodes
    """
    def test_one_node(self):
        node = create_node(name='Test Node')
        self.assertQuerysetEqual(node.connected_nodes.all(),
                                 [])

    def test_two_connected_nodes(self):
        node1 = create_node(name='Test Node 1')
        node2 = create_node(name='Test Node 2')
        node1.connected_nodes.add(node2)
        self.assertQuerysetEqual(node1.connected_nodes.all(),
                                 [node2.__repr__()])
        self.assertQuerysetEqual(node2.connected_nodes.all(),
                                 [node1.__repr__()])

    def test_three_interconnected_nodes(self):
        node1 = create_node(name='Test Node 1')
        node2 = create_node(name='Test Node 2')
        node3 = create_node(name='Test Node 3')
        node1.connected_nodes.add(node2, node3)
        node2.connected_nodes.add(node3)
        self.assertQuerysetEqual(node1.connected_nodes.all()\
                                                      .order_by('name'),
                                 [node2.__repr__(),
                                  node3.__repr__()])
        self.assertQuerysetEqual(node2.connected_nodes.all()\
                                                      .order_by('name'),
                                 [node1.__repr__(),
                                  node3.__repr__()])
        self.assertQuerysetEqual(node3.connected_nodes.all()\
                                                      .order_by('name'),
                                 [node1.__repr__(),
                                  node2.__repr__()])

    def test_three_partially_connected_nodes(self):
        node1 = create_node(name='Test Node 1')
        node2 = create_node(name='Test Node 2')
        node3 = create_node(name='Test Node 3')
        node1.connected_nodes.add(node2)
        node2.connected_nodes.add(node3)
        self.assertQuerysetEqual(node1.connected_nodes.all(),
                                 [node2.__repr__()])
        self.assertQuerysetEqual(node2.connected_nodes.all()\
                                                      .order_by('name'),
                                 [node1.__repr__(),
                                  node3.__repr__()])
        self.assertQuerysetEqual(node3.connected_nodes.all(),
                                 [node2.__repr__()])

    def test_two_pair_sets_of_connected_nodes(self):
        node1 = create_node(name='Test Node 1')
        node2 = create_node(name='Test Node 2')
        node3 = create_node(name='Test Node 3')
        node4 = create_node(name='Test Node 4')
        node1.connected_nodes.add(node2)
        node3.connected_nodes.add(node4)
        self.assertQuerysetEqual(node1.connected_nodes.all(),
                                 [node2.__repr__()])
        self.assertQuerysetEqual(node2.connected_nodes.all(),
                                 [node1.__repr__()])
        self.assertQuerysetEqual(node3.connected_nodes.all(),
                                 [node4.__repr__()])
        self.assertQuerysetEqual(node4.connected_nodes.all(),
                                 [node3.__repr__()])


class ResourceNodeRelationTests(TestCase):
    """
    A Node should have a Queryset of Resources and a Resource should have one
    Node.
    """
    @classmethod
    def setUpTestData(cls):
        # Tests won't need access to Kingdom or Territory instances
        kingdom = Kingdom.objects.create(name='Test Kingdom')
        territory = Territory.objects.create(name='Test Territory',
                                             kingdom=kingdom)
        # This works because any modification to the Resource set are negated by
        # the removal of Resources between tests
        cls.node = Node.objects.create(name='Test Node',
                                       territory=territory)

    def test_no_resources(self):
        """
        Test Node with no Resource.
        """
        self.assertQuerysetEqual(self.node.resources.all(),
                                 [])

    def test_one_resource(self):
        """
        Test Node with one Resource.
        """
        resource = create_resource(node=self.node)
        self.assertQuerysetEqual(self.node.resources.all(),
                                 [resource.__repr__()])
        self.assertEqual(resource.node,
                         self.node)

    def test_two_resources(self):
        """
        Test Node with two Resources.
        """
        resource1 = create_resource(node=self.node)
        resource2 = create_resource(node=self.node)
        self.assertQuerysetEqual(self.node.resources.all()\
                                                    .order_by('material'),
                                 [resource1.__repr__(),
                                  resource2.__repr__()])
        self.assertEqual(resource1.node,
                         self.node)
        self.assertEqual(resource2.node,
                         self.node)

    def test_no_node(self):
        """
        Test Resource with no Node.
        """
        with self.assertRaises(IntegrityError):
            create_resource()


class ResourceMaterialRelationTests(TestCase):
    """
    A Material should have a Queryset of Resources and a Resource should have
    one Material.
    """
    @classmethod
    def setUpTestData(cls):
        # Tests won't need access to Kingdom or Territory instances
        kingdom = Kingdom.objects.create(name='Test Kingdom')
        territory = Territory.objects.create(name='Test Territory',
                                             kingdom=kingdom)
        # This is a dummy node
        cls.node = Node.objects.create(name='Test Node',
                                       territory=territory)
        # This works because any modification to the Resource set are negated by
        # the removal of Resources between tests
        cls.material = Material.objects.create(name='Test Material')

    def test_no_resources(self):
        """
        Test Material with no Resource.
        """
        self.assertQuerysetEqual(self.material.resources.all(),
                                 [])

    def test_one_resource(self):
        """
        Test Material with one Resource.
        """
        resource = create_resource(material=self.material,
                                   node=self.node)
        self.assertQuerysetEqual(self.material.resources.all(),
                                 [resource.__repr__()])
        self.assertEqual(resource.material,
                         self.material)

    def test_two_resources(self):
        """
        Test Material with two Resources.
        """
        resource1 = create_resource(material=self.material,
                                   node=self.node)
        resource2 = create_resource(material=self.material,
                                   node=self.node)
        self.assertQuerysetEqual(self.material.resources.all()\
                                                    .order_by('material'),
                                 [resource1.__repr__(),
                                  resource2.__repr__()])
        self.assertEqual(resource1.material,
                         self.material)
        self.assertEqual(resource2.material,
                         self.material)

    def test_no_material(self):
        """
        Test Resource with no material.
        """
        with self.assertRaises(IntegrityError):
            create_resource(node=self.node,
                            material=None)


class PropertyNodeRelationTests(TestCase):
    """
    A Node should have a Queryset of Properties and a Property should have one
    Node.
    """
    @classmethod
    def setUpTestData(cls):
        # Tests won't need access to Kingdom or Territory instances
        kingdom = Kingdom.objects.create(name='Test Kingdom')
        territory = Territory.objects.create(name='Test Territory',
                                             kingdom=kingdom)
        # This works because any modification to the Property set are negated by the
        # removal of Propertys between tests
        cls.node = Node.objects.create(name='Test Node',
                                       territory=territory)

    def test_no_properties(self):
        """
        Test Node with no Property.
        """
        self.assertQuerysetEqual(self.node.properties.all(),
                                 [])

    def test_one_property(self):
        """
        Test Node with one Property.
        """
        property = Property.objects.create(name='Test Property 1',
                                           node=self.node)
        self.assertQuerysetEqual(self.node.properties.all(),
                                 [property.__repr__()])
        self.assertEqual(property.node,
                         self.node)

    def test_two_properties(self):
        """
        Test Node with two Properties.
        """
        property1 = Property.objects.create(name='Test Property 1',
                                           node=self.node)
        property2 = Property.objects.create(name='Test Property 2',
                                           node=self.node)
        self.assertQuerysetEqual(self.node.properties.all()\
                                                     .order_by('name'),
                                 [property1.__repr__(),
                                  property2.__repr__()])
        self.assertEqual(property1.node,
                         self.node)
        self.assertEqual(property2.node,
                         self.node)

    def test_no_node(self):
        """
        Test Property with no Node.
        """
        with self.assertRaises(IntegrityError):
            Property.objects.create(name='Test Property')


class PropertyPropertyRelationTests(TestCase):
    """
    A Property should have a queryset of Properties (child_properties) and an
    optional Property (parent_property)
    """
    @classmethod
    def setUpTestData(cls):
        # Tests won't need access to Kingdom or Territory instances
        kingdom = Kingdom.objects.create(name='Test Kingdom')
        territory = Territory.objects.create(name='Test Territory',
                                             kingdom=kingdom)
        # This is a dummy node
        cls.node = Node.objects.create(name='Test Node',
                                       territory=territory)
    def test_one_property(self):
        """
        Test a single Property.
        """
        property = Property.objects.create(name='Test Property',
                                           node=self.node)
        self.assertQuerysetEqual(property.child_properties.all(),
                                 [])
        self.assertIsNone(property.parent_property)

    def test_two_properties(self):
        """
        Test two connected Properties.
        """
        property1 = Property.objects.create(name='Test Property 1',
                                           node=self.node)
        property2 = Property.objects.create(name='Test Property 2',
                                           node=self.node)
        property2.parent_property = property1
        property2.save()
        self.assertQuerysetEqual(property1.child_properties.all(),
                                 [property2.__repr__()])
        self.assertIsNone(property1.parent_property)
        self.assertQuerysetEqual(property2.child_properties.all(),
                                 [])
        self.assertEqual(property2.parent_property,
                         property1)

    def test_one_parent_two_children(self):
        """
        Test three Properties with one parent and two children.
        """
        property1 = Property.objects.create(name='Test Property 1',
                                           node=self.node)
        property2 = Property.objects.create(name='Test Property 2',
                                           node=self.node)
        property3 = Property.objects.create(name='Test Property 3',
                                           node=self.node)
        property2.parent_property = property1
        property2.save()
        property3.parent_property = property1
        property3.save()
        self.assertQuerysetEqual(property1.child_properties.all()\
                                                           .order_by('name'),
                                 [property2.__repr__(),
                                  property3.__repr__()])
        self.assertIsNone(property1.parent_property)
        self.assertQuerysetEqual(property2.child_properties.all(),
                                 [])
        self.assertEqual(property2.parent_property,
                         property1)
        self.assertQuerysetEqual(property3.child_properties.all(),
                                 [])
        self.assertEqual(property3.parent_property,
                         property1)

    def test_three_generations(self):
        """
        Test three Properties with a child of a child.
        """
        property1 = Property.objects.create(name='Test Property 1',
                                           node=self.node)
        property2 = Property.objects.create(name='Test Property 2',
                                           node=self.node)
        property3 = Property.objects.create(name='Test Property 3',
                                           node=self.node)
        property2.parent_property = property1
        property2.save()
        property3.parent_property = property2
        property3.save()
        self.assertQuerysetEqual(property1.child_properties.all(),
                                 [property2.__repr__()])
        self.assertIsNone(property1.parent_property)
        self.assertQuerysetEqual(property2.child_properties.all(),
                                 [property3.__repr__()])
        self.assertEqual(property2.parent_property,
                         property1)
        self.assertQuerysetEqual(property3.child_properties.all(),
                                 [])
        self.assertEqual(property3.parent_property,
                         property2)


class PropertyStationRelationTests(TestCase):
    """
    A Property should have a Queryset of Stations through the PropertyStation
    model. Similarly, a Station should have a Queryset of Properties.
    """
    @classmethod
    def setUpTestData(cls):
        # Tests won't need access to Kingdom or Territory instances
        kingdom = Kingdom.objects.create(name='Test Kingdom')
        territory = Territory.objects.create(name='Test Territory',
                                             kingdom=kingdom)
        # This is a dummy node
        cls.node = Node.objects.create(name='Test Node',
                                       territory=territory)

    def test_one_station(self):
        """
        Test a Station with no Properties.
        """
        station = Station.objects.create(name='Test Station')
        self.assertQuerysetEqual(station.properties.all(),
                                 [])

    def test_one_property(self):
        """
        Test a Property with no Stations.
        """
        property = Property.objects.create(name='Test Property',
                                           node=self.node)
        self.assertQuerysetEqual(property.stations.all(),
                                 [])

    def test_one_station_one_property(self):
        """
        Test a connected Station and Property.
        """
        station = Station.objects.create(name='Test Station')
        property = Property.objects.create(name='Test Property',
                                           node=self.node)
        PropertyStation.objects.create(station=station,
                                       property=property,
                                       max_level=1)
        self.assertQuerysetEqual(property.stations.all(),
                                 [station.__repr__()])
        self.assertQuerysetEqual(station.properties.all(),
                                 [property.__repr__()])
        self.assertEqual(property.propertystation_set\
                                 .get(station=station).max_level,
                         1)

    def test_two_stations_one_property(self):
        """
        Test a Property with two Stations.
        """
        station1 = Station.objects.create(name='Test Station 1')
        station2 = Station.objects.create(name='Test Station 2')
        property = Property.objects.create(name='Test Property',
                                           node=self.node)
        PropertyStation.objects.create(station=station1,
                                       property=property,
                                       max_level=1)
        PropertyStation.objects.create(station=station2,
                                       property=property,
                                       max_level=2)
        self.assertQuerysetEqual(property.stations.all().order_by('name'),
                                 [station1.__repr__(),
                                  station2.__repr__()])
        self.assertQuerysetEqual(station1.properties.all(),
                                 [property.__repr__()])
        self.assertQuerysetEqual(station2.properties.all(),
                                 [property.__repr__()])
        self.assertEqual(property.propertystation_set\
                                 .get(station=station1).max_level,
                         1)
        self.assertEqual(property.propertystation_set\
                                 .get(station=station2).max_level,
                         2)

    def test_one_station_two_properties(self):
        """
        Test a Station with two Properties.
        """
        station = Station.objects.create(name='Test Station')
        property1 = Property.objects.create(name='Test Property 1',
                                           node=self.node)
        property2 = Property.objects.create(name='Test Property 2',
                                           node=self.node)
        PropertyStation.objects.create(station=station,
                                       property=property1,
                                       max_level=1)
        PropertyStation.objects.create(station=station,
                                       property=property2,
                                       max_level=2)
        self.assertQuerysetEqual(property1.stations.all(),
                                 [station.__repr__()])
        self.assertQuerysetEqual(property2.stations.all(),
                                 [station.__repr__()])
        self.assertQuerysetEqual(station.properties.all().order_by('name'),
                                 [property1.__repr__(),
                                  property2.__repr__()])
        self.assertEqual(station.propertystation_set\
                                .get(property=property1).max_level,
                         1)
        self.assertEqual(station.propertystation_set\
                                .get(property=property2).max_level,
                         2)

    def test_two_stations_two_properties_all_linked(self):
        """
        Test two Stations and two Properties that are all related.
        """
        station1 = Station.objects.create(name='Test Station 1')
        station2 = Station.objects.create(name='Test Station 2')
        property1 = Property.objects.create(name='Test Property 1',
                                           node=self.node)
        property2 = Property.objects.create(name='Test Property 2',
                                           node=self.node)
        PropertyStation.objects.create(station=station1,
                                       property=property1,
                                       max_level=1)
        PropertyStation.objects.create(station=station1,
                                       property=property2,
                                       max_level=2)
        PropertyStation.objects.create(station=station2,
                                       property=property1,
                                       max_level=3)
        PropertyStation.objects.create(station=station2,
                                       property=property2,
                                       max_level=4)
        self.assertQuerysetEqual(property1.stations.all().order_by('name'),
                                 [station1.__repr__(),
                                  station2.__repr__()])
        self.assertQuerysetEqual(property2.stations.all().order_by('name'),
                                 [station1.__repr__(),
                                  station2.__repr__()])
        self.assertQuerysetEqual(station1.properties.all().order_by('name'),
                                 [property1.__repr__(),
                                  property2.__repr__()])
        self.assertQuerysetEqual(station2.properties.all().order_by('name'),
                                 [property1.__repr__(),
                                  property2.__repr__()])
        self.assertEqual(station1.propertystation_set\
                                 .get(property=property1).max_level,
                         1)
        self.assertEqual(station1.propertystation_set\
                                 .get(property=property2).max_level,
                         2)
        self.assertEqual(station2.propertystation_set\
                                 .get(property=property1).max_level,
                         3)
        self.assertEqual(station2.propertystation_set\
                                 .get(property=property2).max_level,
                         4)

    def test_two_stations_two_properties_two_pairs(self):
        """
        Test two Stations and two Properties with two separate Station-Property
        pairs.
        """
        station1 = Station.objects.create(name='Test Station 1')
        station2 = Station.objects.create(name='Test Station 2')
        property1 = Property.objects.create(name='Test Property 1',
                                           node=self.node)
        property2 = Property.objects.create(name='Test Property 2',
                                           node=self.node)
        PropertyStation.objects.create(station=station1,
                                       property=property1,
                                       max_level=1)
        PropertyStation.objects.create(station=station2,
                                       property=property2,
                                       max_level=2)
        self.assertQuerysetEqual(property1.stations.all(),
                                 [station1.__repr__()])
        self.assertQuerysetEqual(property2.stations.all(),
                                 [station2.__repr__()])
        self.assertQuerysetEqual(station1.properties.all(),
                                 [property1.__repr__()])
        self.assertQuerysetEqual(station2.properties.all(),
                                 [property2.__repr__()])
        self.assertEqual(station1.propertystation_set\
                                 .get(property=property1).max_level,
                         1)
        self.assertEqual(station2.propertystation_set\
                                 .get(property=property2).max_level,
                         2)

    def test_three_stations_two_properties_one_station_shared(self):
        """
        Test three Stations with two Properties. The Properties will share one
        Station and have one unshared Station each.
        """
        station1 = Station.objects.create(name='Test Station 1')
        station2 = Station.objects.create(name='Test Station 2')
        station3 = Station.objects.create(name='Test Station 3')
        property1 = Property.objects.create(name='Test Property 1',
                                           node=self.node)
        property2 = Property.objects.create(name='Test Property 2',
                                           node=self.node)
        PropertyStation.objects.create(station=station1,
                                       property=property1,
                                       max_level=1)
        PropertyStation.objects.create(station=station2,
                                       property=property1,
                                       max_level=2)
        PropertyStation.objects.create(station=station2,
                                       property=property2,
                                       max_level=3)
        PropertyStation.objects.create(station=station3,
                                       property=property2,
                                       max_level=4)
        self.assertQuerysetEqual(property1.stations.all().order_by('name'),
                                 [station1.__repr__(),
                                  station2.__repr__()])
        self.assertQuerysetEqual(property2.stations.all().order_by('name'),
                                 [station2.__repr__(),
                                  station3.__repr__()])
        self.assertQuerysetEqual(station1.properties.all(),
                                 [property1.__repr__()])
        self.assertQuerysetEqual(station2.properties.all().order_by('name'),
                                 [property1.__repr__(),
                                  property2.__repr__()])
        self.assertQuerysetEqual(station3.properties.all(),
                                 [property2.__repr__()])
        self.assertEqual(station1.propertystation_set\
                                 .get(property=property1).max_level,
                         1)
        self.assertEqual(station2.propertystation_set\
                                 .get(property=property1).max_level,
                         2)
        self.assertEqual(station2.propertystation_set\
                                 .get(property=property2).max_level,
                         3)
        self.assertEqual(station3.propertystation_set\
                                 .get(property=property2).max_level,
                         4)

    def test_two_stations_three_properties_one_property_shared(self):
        """
        Test two Stations with three Properties. The Stations will share one
        Property and have one unshared Property each.
        """
        station1 = Station.objects.create(name='Test Station 1')
        station2 = Station.objects.create(name='Test Station 2')
        property1 = Property.objects.create(name='Test Property 1',
                                           node=self.node)
        property2 = Property.objects.create(name='Test Property 2',
                                           node=self.node)
        property3 = Property.objects.create(name='Test Property 3',
                                           node=self.node)
        PropertyStation.objects.create(station=station1,
                                       property=property1,
                                       max_level=1)
        PropertyStation.objects.create(station=station1,
                                       property=property2,
                                       max_level=2)
        PropertyStation.objects.create(station=station2,
                                       property=property2,
                                       max_level=3)
        PropertyStation.objects.create(station=station2,
                                       property=property3,
                                       max_level=4)
        self.assertQuerysetEqual(property1.stations.all().order_by('name'),
                                 [station1.__repr__()])
        self.assertQuerysetEqual(property2.stations.all().order_by('name'),
                                 [station1.__repr__(),
                                  station2.__repr__()])
        self.assertQuerysetEqual(property3.stations.all().order_by('name'),
                                 [station2.__repr__()])
        self.assertQuerysetEqual(station1.properties.all().order_by('name'),
                                 [property1.__repr__(),
                                  property2.__repr__()])
        self.assertQuerysetEqual(station2.properties.all().order_by('name'),
                                 [property2.__repr__(),
                                  property3.__repr__()])
        self.assertEqual(station1.propertystation_set\
                                 .get(property=property1).max_level,
                         1)
        self.assertEqual(station1.propertystation_set\
                                 .get(property=property2).max_level,
                         2)
        self.assertEqual(station2.propertystation_set\
                                 .get(property=property2).max_level,
                         3)
        self.assertEqual(station2.propertystation_set\
                                 .get(property=property3).max_level,
                         4)


#
# Helper Methods
#
def create_node(**create_args):
    """
    Create a Node with select optional default values.
    """
    if 'is_hub' not in create_args:
        create_args['is_hub'] = False
    if 'contribution_cost' not in create_args:
        create_args['contribution_cost'] = 2
    if 'node_manager' not in create_args:
        create_args['node_manager'] = 'Test Manager'
    if 'territory' not in create_args:
        create_args['territory'] = Territory.objects.create(name='Test Territory',
                                                            kingdom=Kingdom.objects.create(name='Test Kingdom'))
    elif create_args['territory'] is None:
        create_args.pop('territory')
    return Node.objects.create(**create_args)


def create_resource(**create_args):
    """
    Create a Resource with select optional default values.
    """
    if 'material' not in create_args:
        create_args['material'] = Material.objects.create(name='Test Material')
    elif create_args['material'] is None:
        create_args.pop('material')
    if 'contribution_cost' not in create_args:
        create_args['contribution_cost'] = 1
    return Resource.objects.create(**create_args)
