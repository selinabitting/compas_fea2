from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# Author(s): Francesco Ranaudo (github.com/franaudo)

import sys

__all__ = [
    'Model',
    'Instance',
]

class Model():
    """Initialises the Model object. This is in many aspects equivalent to an
    `Assembly` in Abaqus.

    Parameters
    ----------
    name : str
        Name of the Model.

    Attributes
    ----------
    name : str
        Name of the Model.
    parts : list
        A list with the Part objects referenced in the Model.
    instances : list
        A list with the Instance objects belonging to the Model.
    parts : list
        A list with the Part objects referenced in the Model.
    surfaces : list
        A list with the Surface objects belonging to the Model.
    constraints : list
        A list with the Constraint objects belonging to the Model.
    materials : list
        A list of all the materials defined int the Model.

    """

    def __init__(self, name, ):
        self.__name__           = 'Model'
        self.name               = name
        self.instances          = {}
        self.parts              = {}
        self.surfaces           = []
        self.constraints        = []
        self.add_interactions   = []
        self.materials          = {}
        self.sections           = {}
        self.sets               = {}
        # self.materials      = self._get_materials()

        # self.data           = self._generate_data()

    def __str__(self):
        title = 'compas_fea2 {0} object'.format(self.__name__)
        separator = '-' * (len(self.__name__) + 19)
        data = []
        for attr in ['name']:
            data.append('{0:<15} : {1}'.format(attr, getattr(self, attr)))

        data.append('{0:<15} : {1}'.format('# of parts', len(self.parts)))
        data.append('{0:<15} : {1}'.format('# of instances', len(self.instances)))
        return """\n{}\n{}\n{}""".format(title, separator, '\n'.join(data))

    def __repr__(self):
        return '{0}({1})'.format(self.__name__, self.name)

    def _get_materials(self):
        materials = []
        for i in self.instances:
            for mat in i.part.elements_by_material.keys():
                materials.append(mat)
        return list(set(materials))

    def _generate_data(self):
        line = '*Assembly, name={}\n**\n'.format(self.name)
        section_data = [line]
        for instance in self.instances.values():
            section_data.append(instance._generate_data())
            for iset in instance.sets:
                section_data.append(iset._generate_data())
        # for surface in self.surfaces:
        #     section_data.append(surface.data)
        # for constraint in self.constraints:
        #     section_data.append(constraint.data)
        line = '*End Assembly\n**'
        section_data.append(line)
        return ''.join(section_data)

    # =========================================================================
    #                            General methods
    # =========================================================================

    def from_network(self, network):
        pass

    def from_mesh(self, mesh):
        pass

    def from_volmesh(self, volmesh):
        pass

    def from_solid(self, solid):
        pass

    # =========================================================================
    #                             Parts methods
    # =========================================================================

    def add_part(self, part, transformation={}):
        """Adds a Part to the Model and creates an Instance object from the
        specified Part and adds it to the Assembly. If a transformation matrix
        is specified, the instance is creteated in the transformed location.

        Parameters
        ----------
        part : obj
            Part object from which the Instance is created.
        transformation : dict
            Dictionary containing the trasformation matrices to apply to the Part
            before creating the Instances.
            key: (str) instance name
            value: (matrix) transformation matrix

        Returns
        -------
        None

        Examples
        --------
        In this example a part is added to the model and two instances are created
        using two transformation matrices.
        >>> model = Assembly('mymodel')
        >>> part = Part('mypart')
        >>> model.add_part(part=part, transformation=[M1, M2])
        """

        if part.name in self.parts:
            print("WARNING: Part {} already in the Model. Part not added!".format(part.name))
        else:
            self.parts[part.name] = part

        # TODO: implement transfromation operations
        if transformation:
            for i in transformation.keys():
                instance = self._instance_from_part(part, i, transformation[i])
                self.add_instance(instance)
        else:
            self.add_instance(Instance('{}-{}'.format(part.name, 1), part))

    def remove_part(self, part):
        """ Removes the part from the Model and all the referenced instances
        of that part.

        Parameters
        ----------
        part : str
            Name of the Part to remove.

        Returns
        -------
        None
        """

        self.parts.pop(part)

        for instance in self.instances:
            if self.instances[instance].part.name == part:
                self.instances.pop(instance)

    # =========================================================================
    #                          Instances methods
    # =========================================================================
    def add_instance(self, instance):
        """Adds a compas_fea2 Instance object to the Model. If the Part to
        which the instance is referred to does not exist, it is automatically
        created.

        Parameters
        ----------
        instance : obj
            compas_fea2 Instance object.

        Returns
        -------
        None
        """

        if instance.name not in self.instances:
            self.instances[instance.name] = instance
            if instance.part.name not in self.parts:
                self.parts[part.name] = instance.part
        else:
            print('Duplicate instance {} will be ignored!'.format(instance.name))

    def remove_instance(self, instance):
        """ Removes the part from the Model and all the referenced instances.

        Parameters
        ----------
        instace : str
            Name of the Instance object to remove.

        Returns
        -------
        None
        """

        self.instances.pop(instance)

    def _instance_from_part(self, part, instance_name, transformation):
        pass

    # =========================================================================
    #                           Nodes methods
    # =========================================================================

    def add_node(self, node, part):
        """Adds a compas_fea2 Node object to a Part in the Model.
        If the Node object has no label, one is automatically assigned. Duplicate
        nodes are autmatically excluded.
        The part must have been previously added to the Model.

        Parameters
        ----------
        node : obj
            compas_fea2 Node object.
        part : str
            Name of the part where the node will be added.

        Returns
        -------
        None
        """
        error_code=0
        if part in self.parts:
            self.parts[part].add_node(node)
            error_code = 1

        if error_code == 0:
            sys.exit('ERROR: part {} not found in the Model!'.format(part))

    def add_nodes(self, nodes, part):
        """Add multiple compas_fea2 Node objects a Part in the Model.
        If the Node object has no label, one is automatically assigned. Duplicate
        nodes are autmatically excluded.
        The part must have been previously added to the Model.

        Parameters
        ----------
        nodes : list
            List of compas_fea2 Node objects.
        part : str
            Name of the part where the node will be added.

        Returns
        -------
        None
        """

        for node in nodes:
            self.add_node(node, part)

    def remove_node(self, node_key, part):
        '''Remove the node from a Part in the Model. If there are duplicate nodes,
        it removes also all the duplicates.

        Parameters
        ----------
        node_key : int
            Key number of the node to be removed.
        part : str
            Name of the part where the node will be removed from.

        Returns
        -------
        None
        '''

        error_code=0
        if part in self.parts:
            self.parts[part].remove_node(node_key)
            error_code=1

        if error_code == 0:
            sys.exit('ERROR: part {} not found in the Model!'.format(part))

    def remove_nodes(self, nodes, part):
        '''Remove the nodes from a Part in the Model. If there are duplicate nodes,
        it removes also all the duplicates.

        Parameters
        ----------
        node : list
            List with the key numbers of the nodes to be removed.
        part : str
            Name of the part where the nodes will be removed from.

        Returns
        -------
        None
        '''

        for node in nodes:
            self.remove_node(node, part)



    # ==============================================================================
    # Nodes
    # ==============================================================================

    # def check_node_exists(self, xyz):
    #     """Check if a node already exists at given x, y, z co-ordinates.

    #     Parameters
    #     ----------
    #     xyz : list
    #         [x, y, z] co-ordinates of node to check.

    #     Returns
    #     -------
    #     int
    #         The node index if the node already exists, None if not.

    #     Notes
    #     -----
    #     Geometric key check is made according to self.tol [m] tolerance.
    #     """
    #     xyz = [float(i) for i in xyz]
    #     return self.node_index.get(geometric_key(xyz, '{0}f'.format(self.tol)), None)

    # def edit_node(self, key, attr_dict):
    #     """Edit the data of a node.

    #     Parameters
    #     ----------
    #     key : int
    #         Key of the node to edit.
    #     attr_dict : dict
    #         Attribute dictionary of data to edit.

    #     Returns
    #     -------
    #     None
    #     """
    #     gkey = geometric_key(self.node_xyz(key), '{0}f'.format(self.tol))
    #     del self.node_index[gkey]
    #     for attr, item in attr_dict.items():
    #         setattr(self.nodes[key], attr, item)
    #     self.add_node_to_node_index(key, self.node_xyz(key))

    # def node_bounds(self):
    #     """Return the bounds formed by the Structure's nodal co-ordinates.

    #     Parameters
    #     ----------
    #     None

    #     Returns
    #     -------
    #     list
    #         [xmin, xmax].
    #     list
    #         [ymin, ymax].
    #     list
    #         [zmin, zmax].
    #     """
    #     n = self.node_count()
    #     x = [0] * n
    #     y = [0] * n
    #     z = [0] * n
    #     for c, node in self.nodes.items():
    #         x[c] = node.x
    #         y[c] = node.y
    #         z[c] = node.z
    #     xmin, xmax = min(x), max(x)
    #     ymin, ymax = min(y), max(y)
    #     zmin, zmax = min(z), max(z)
    #     return [xmin, xmax], [ymin, ymax], [zmin, zmax]

    # def node_count(self):
    #     """Return the number of nodes in the Structure.

    #     Parameters
    #     ----------
    #     None

    #     Returns
    #     -------
    #     int
    #         Number of nodes stored in the Structure object.
    #     """
    #     return len(self.nodes) + len(self.virtual_nodes)


    def nodes_xyz(self, nodes=None):
        """Return the xyz co-ordinates of given or all nodes.

        Parameters
        ----------
        nodes : list
            Node numbers, give None for all nodes.

        Returns
        -------
        list
            [[x, y, z] ...] co-ordinates.
        """
        if nodes is None:
            nodes = sorted(self.nodes, key=int)

        return [self.node_xyz(node=node) for node in nodes]


    # def check_element_exists(self, nodes=None, xyz=None, virtual=False):
    #     """Check if an element already exists based on nodes or centroid.

    #     Parameters
    #     ----------
    #     nodes : list
    #         Node numbers the element is connected to.
    #     xyz : list
    #         Direct co-ordinates of the element centroid to check.
    #     virtual: bool
    #         Is the element to be checked a virtual element.

    #     Returns
    #     -------
    #     int
    #         The element index if the element already exists, None if not.

    #     Notes
    #     -----
    #     Geometric key check is made according to self.tol [m] tolerance.
    #     """
    #     if not xyz:
    #         xyz = centroid_points([self.node_xyz(node) for node in nodes])
    #     gkey = geometric_key(xyz, '{0}f'.format(self.tol))
    #     if virtual:
    #         return self.virtual_element_index.get(gkey, None)
    #     else:
    #         return self.element_index.get(gkey, None)

    # def edit_element(self):
    #     raise NotImplementedError

    # def element_count(self):
    #     """Return the number of elements in the Structure.

    #     Parameters
    #     ----------
    #     None

    #     Returns
    #     -------
    #     int
    #         Number of elements stored in the Structure object.
    #     """
    #     return len(self.elements) + len(self.virtual_elements)

    # def element_centroid(self, element):
    #     """Return the centroid of an element.

    #     Parameters
    #     ----------
    #     element : int
    #         Number of the element.

    #     Returns
    #     -------
    #     list
    #         Co-ordinates of the element centroid.
    #     """
    #     return centroid_points(self.nodes_xyz(nodes=self.elements[element].nodes))

    # def add_virtual_element(self, nodes, type, thermal=False, axes={}):
    #     """Adds a virtual element to structure.elements and to element set 'virtual_elements'.

    #     Parameters
    #     ----------
    #     nodes : list
    #         Nodes the element is connected to.
    #     type : str
    #         Element type: 'HexahedronElement', 'BeamElement, 'TrussElement' etc.
    #     thermal : bool
    #         Thermal properties on or off.
    #     axes : dict
    #         The local element axes 'ex', 'ey' and 'ez'.

    #     Returns
    #     -------
    #     int
    #         Key of the added virtual element.

    #     Notes
    #     -----
    #     Virtual elements are numbered sequentially starting from 0.
    #     """
    #     ekey = self.check_element_exists(nodes, virtual=True)

    #     if ekey is None:

    #         ekey            = self.element_count()
    #         element         = func_dict[type]()
    #         element.axes    = axes
    #         element.nodes   = nodes
    #         element.number  = ekey
    #         element.thermal = thermal

    #         self.virtual_elements[ekey] = element
    #         self.add_element_to_element_index(ekey, nodes, virtual=True)

    #         if 'virtual_elements' in self.sets:
    #             self.collections['virtual_elements']['selection'].append(ekey)
    #         else:
    #             self.collections['virtual_elements'] = {'type': 'virtual_element', 'selection': [ekey],
    #                                              'index': len(self.sets)}

    #     return ekey




    # =========================================================================
    #                           Elements methods
    # =========================================================================
    def add_element(self, element, part):
        """Adds a compas_fea2 Element object to a Part in the Model.

        Parameters
        ----------
        element : obj
            compas_fea2 Element object.
        part : str
            Name of the part where the nodes will be removed from.

        Returns
        -------
        None
        """

        error_code=0
        if part in self.parts:
            self.parts[part].add_element(element)
            if element.section not in self.sections:
                sys.exit('ERROR: section {} not found in the Model!'.format(element.section))
            elif element.section not in self.parts[part].sections:
                self.parts[part].sections[element.section] = self.sections[element.section]
            error_code=1

        if error_code == 0:
            sys.exit('ERROR: part {} not found in the Model!'.format(part))

    def add_elements(self, elements, part):
        """Adds multiple compas_fea2 Element objects to a Part in the Model.

        Parameters
        ----------
        elements : list
            List of compas_fea2 Element objects.
        part : str
            Name of the part where the nodes will be removed from.

        Returns
        -------
        None
        """

        for element in elements:
            self.add_element(element, part)

    def remove_element(self, element_key, part):
        '''Removes the element from a Part in the Model.

        Parameters
        ----------
        element_key : int
            Key number of the element to be removed.
        part : str
            Name of the part where the nodes will be removed from.

        Returns
        -------
        None
        '''
        error_code=0
        if part in self.parts:
            self.parts[part].remove_element(element_key)
            error_code=1

        if error_code == 0:
            sys.exit('ERROR: part {} not found in the Model!'.format(part))

    def remove_elements(self, elements, part):
        '''Removes the elements from a Part in the Model.

        Parameters
        ----------
        elements : list
            List with the key numbers of the element to be removed.
        part : str
            Name of the part where the nodes will be removed from.

        Returns
        -------
        None
        '''

        for element in elements:
            self.remove_node(element, part)

    # =========================================================================
    #                               Sets methods
    # =========================================================================
    def add_part_node_set(self, part, nset):
        pass

    def add_assembly_set(self, set, instance):
        '''Adds a Set object to the Model.

        Parameters
        ----------
        set : obj
            node set object.
        instance : str
            Name of the instance where the set belongs to.

        Returns
        -------
        None
        '''
        if instance not in self.instances:
            sys.exit('ERROR: instance {} not found in the Model!'.format(instance))
        set.instance = instance
        self.instances[instance].sets.append(set)

        self.sets[set.name] = set

    # =========================================================================
    #                           Materials methods
    # =========================================================================

    def add_material(self, material):
        '''Adds a Material object to the Model so that it can be later refernced
        and used in the Section and Element definitions.

        Parameters
        ----------
        material : obj
            compas_fea2 material object.

        Returns
        -------
        None
        '''
        if material.name not in self.materials:
            self.materials[material.name] = material

    def add_materials(self, materials):
        '''Adds multiple Material objects to the Model so that they can be later refernced
        and used in the Section and Element definitions.

        Parameters
        ----------
        material : list
            List of compas_fea2 material objects.

        Returns
        -------
        None
        '''
        for material in materials:
            self.add_material(material)

    def assign_material_to_element(self, material, part, element):
        NotImplemented

    # =========================================================================
    #                           Sections methods
    # =========================================================================

    def add_section(self, section):
        """Adds a compas_fea2 Section object to the Model.

        Parameters
        ----------
        element : obj
            compas_fea2 Element object.
        part : str
            Name of the part where the nodes will be removed from.

        Returns
        -------
        None
        """

        if section.name not in self.sections:
            self.sections[section.name] = section
            if section.material not in self.materials.keys():
                sys.exit('ERROR: material {} not found in the Model!'.format(section.material))
            self.add_material(self.materials[section.material])

    def assign_section_to_element(self, material, part, element):
        NotImplemented


    # =========================================================================
    #                        Surfaces methods
    # =========================================================================
    def add_surface(self, surface):
        self.surfaces.append(surface)


    # =========================================================================
    #                       Constraints methods
    # =========================================================================
    def add_constraint(self, constraint):
        self.constraints.append(constraint)

    # def add_instance_set(self, iset, instance):
    #     """ Adds a set to a previously defined Instance.

    #     Parameters
    #     ----------
    #     part : obj
    #         Part object from which the Instance is created.
    #     transformation : matrix
    #         Trasformation matrix to apply to the Part before creating the Instance.
    #     """
    #     self.instances[instance].sets.append(iset)

    # =========================================================================
    #                        Interaction methods
    # =========================================================================

    def add_interactions(self, interactions):
        pass


    # =========================================================================
    #                          Helper methods
    # =========================================================================

    # TODO change to check through the instance
    def get_node_from_coordinates(self, xyz):
        node_dict = {}
        for part in self.parts.values():
            for node in part.nodes:
                if node.xyz == xyz:
                    node_dict[part.name] = node.key
        return node_dict

class Instance():
    """Initialises base Instance object.

    Parameters
    ----------
    name : str
        Name of the set.
    part : obj
        The Part from which the instance is created.
    sets : list
        A list with the Set objects belonging to the instance.

    Attributes
    ----------
    name : str
        Name of the set.
    part : Part object
        The part from which create the instance.
    sets : list
        A list with the Set objects belonging to the instance.
    data : str
        The data block for the generation of the input file.
    """

    def __init__(self, name, part, sets=[]):
        self.__name__ = 'Instance'
        self.name = name
        self.part = part
        self.sets = sets
        for iset in sets:
            iset.instance = self.name
            iset.data = iset._generate_data()

        self.data = """*Instance, name={}, part={}\n*End Instance\n**\n""".format(self.name, self.part.name)

    def __str__(self):
        print('\n')
        print('compas_fea {0} object'.format(self.__name__))
        print('-' * (len(self.__name__) + 18))

        for attr in ['name']:
            print('{0:<10} : {1}'.format(attr, getattr(self, attr)))

        return ''

    def __repr__(self):
        return '{0}({1})'.format(self.__name__, self.part.name)

    def _generate_data(self):
        return """*Instance, name={}, part={}\n*End Instance\n**\n""".format(self.name, self.part.name)


# =============================================================================
#                               Debugging
# =============================================================================

if __name__ == "__main__":
    pass




