from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import importlib
import numpy as np

from compas.geometry import normalize_vector

from compas_fea2.base import FEABase
from compas_fea2.model.materials import Material
from compas_fea2.model.sections import Section
from compas_fea2.model.sections import SolidSection
from compas_fea2.model.sections import ShellSection
from compas_fea2.model.groups import NodesGroup
from compas_fea2.model.groups import ElementsGroup


class Part(FEABase):
    """Part object.

    Parameters
    ----------
    name : str
        Name of the ``Part``.

    """

    def __init__(self, name):
        super(Part, self).__init__(name=name)

        self._nodes = []
        self._nodes_gkeys = []  # TODO check with dict and set

        self._materials = {}
        self._sections = {}

        self._elements = {}
        self._groups = {}
        self._releases = {}

    @property
    def nodes(self):
        """list : Sorted list (by `Node key`) with the :class:`Node` sub-class objects belonging to the ``Part``."""
        return self._nodes

    @property
    def materials(self):
        """dict : Dictionary with the :class:`Material` sub-class objects belonging to the Part."""
        return self._materials

    @property
    def sections(self):
        """dict : Dictionary with the :class:`Section` sub-class objects belonging to the ``Part``."""
        return self._sections

    @property
    def elements(self):
        """dict : Sorted list (by `Element key`) with the :class:`Element` sub-class objects belonging to the ``Part``."""
        return self._elements

    @property
    def groups(self):
        """list : List with the :class:`NodesGroup` or :class:`ElementsGroup` sub-class objects belonging to the ``Part``."""
        return self._groups

    @property
    def releases(self):
        """The releases property."""
        return self._releases

    # =========================================================================
    #                       Constructor methods
    # =========================================================================

    # def from_network(self, network):
    #     raise NotImplementedError()

    # def from_obj(self, obj):
    #     raise NotImplementedError()

    @classmethod
    def frame_from_mesh(cls, name, mesh, beam_section):
        """Creates a ``Part`` object from a compas Mesh object [WIP]. The edges of
        the mesh become the BeamElements of the frame. Currently, the same section
        is applied to all the elements.

        Parameters
        ----------
        name : str
            name of the new part.
        mesh : obj
            Mesh to convert to import as a Model.
        beam_section : obj
            compas_fea2 BeamSection object to to apply to the frame elements.

        """
        m = importlib.import_module('.'.join(cls.__module__.split('.')[:-1]))
        part = cls(name)
        part.add_section(beam_section)

        for v in mesh.vertices():
            part.add_node(m.Node(mesh.vertex_coordinates(v)))

        # Generate elements between nodes
        key_index = mesh.key_index()
        # vertices = list(mesh.vertices())
        edges = [(key_index[u], key_index[v]) for u, v in mesh.edges()]

        for e in edges:
            # get elements orientation
            v = normalize_vector(mesh.edge_vector(e[0], e[1]))
            v.append(v.pop(0))
            # add element to the model
            part.add_element(m.BeamElement(connectivity=[e[0], e[1]], section=beam_section, orientation=v))

        return part

    @classmethod
    def shell_from_mesh(cls, name, mesh, shell_section):
        """Creates a Part object from a compas Mesh object [WIP]. The faces of
        the mesh become ShellElement objects. Currently, the same section
        is applied to all the elements.

        Parameters
        ----------
        name : str
            name of the new part.
        mesh : obj
            Mesh to convert to import as a Model.
        shell_section : obj
            compas_fea2 ShellSection object to to apply to the shell elements.

        """
        m = importlib.import_module('.'.join(cls.__module__.split('.')[:-1]))
        part = cls(name)
        part.add_section(shell_section)

        for v in mesh.vertices():
            part.add_node(m.Node(mesh.vertex_coordinates(v)), 'part-1')

        # Generate elements between nodes
        key_index = mesh.key_index()
        faces = [[key_index[key]
                  for key in mesh.face_vertices(face)] for face in mesh.faces()]

        for face in faces:
            part.add_element(m.ShellElement(connectivity=face, section=shell_section))

        return part

    @classmethod
    def from_gmsh(cls, name, gmshModel, section, split=False, verbose=False, check=False):
        """Create a Part object from a gmshModel object. According to the `section`
        type provided, SolidElement or ShellElement elements are cretated.
        The same section is applied to all the elements.

        Note
        ----
        The gmshModel must have the right dimension corresponding to the section
        provided.

        Parameters
        ----------
        name : str
            name of the new part.
        gmshModel : obj
            gmsh Model to convert. See [1]_
        section : obj
            `compas_fea2` :class:`SolidSection` or :class:`ShellSection` sub-class
            object to to apply to the elements.
        split : bool, optional
            if ``True`` create an additional node in the middle of the edges of the
            elements to implement more refined element types. Check for example [2]_.
        verbose : bool, optional
            if ``True`` print a log, by default False
        check : bool, optional
            if ``True`` performs sanity checks, by default False. This is a quite
            resource-intense operation! Set to ``False`` for large models (>10000
            nodes).

        Returns
        -------
        obj
            compas_fea2 `Part` object.

        References
        ----------
        .. [1] https://gitlab.onelab.info/gmsh/gmsh/blob/gmsh_4_9_1/api/gmsh.py
        .. [2] https://web.mit.edu/calculix_v2.7/CalculiX/ccx_2.7/doc/ccx/node33.html

        Examples
        --------
        >>> gmshModel = gmsh.mode.generate(3)
        >>> mat = ElasticIsotropic(name='mat', E=29000, v=0.17, p=2.5e-9)
        >>> sec = SolidSection('mysec', mat)
        >>> part = Part.from_gmsh('part_gmsh', gmshModel, sec)

        """
        part = cls(name)
        m = importlib.import_module('.'.join(part.__module__.split('.')[:-1]))
        part.add_section(section)
        # add nodes
        nodes = gmshModel.mesh.get_nodes()
        node_coords = nodes[1].reshape((-1, 3), order='C')
        for coords in node_coords:
            k = part.add_node(m.Node(coords.tolist()), check)
            if verbose:
                print(f'node {k} added')
        # add elements
        elements = gmshModel.mesh.get_elements()
        if isinstance(section, SolidSection):
            ntags_per_element = np.split(elements[2][2]-1, len(elements[1][2]))  # gmsh keys start from 1
            for ntags in ntags_per_element:
                # if split:
                # iteritools combinations
                # for comb in combs:
                # midpoint a b
                # k = add node
                k = part.add_element(m.SolidElement(ntags, section), check)
                if verbose:
                    print(f'element {k} added')
        if isinstance(section, ShellSection):
            ntags_per_element = np.split(elements[2][1]-1, len(elements[1][1]))  # gmsh keys start from 1
            for ntags in ntags_per_element:
                k = part.add_element(m.ShellElement(ntags, section), check)
                if verbose:
                    print(f'element {k} added')
        print('\ncompas_fea2 model generated!\n')
        return part

    @classmethod
    def from_compas_part(cls, name, part):
        raise NotImplementedError()

    @classmethod
    def from_volmesh(self, name, volmesh):
        raise NotImplementedError()

    # =========================================================================
    #                           Nodes methods
    # =========================================================================

    # TODO check if this is still useful
    def _reorder_nodes(self):
        """Reorders the nodes to have consecutive keys. If the node label is an
        auto-generated label, it updates the label as well, otherwise leaves the
        user-generated label.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """

        k = 0
        for node in self.nodes:
            node.key = k
            k += 1
            if node.label[:2] == 'n-':
                node.label = 'n-{}'.format(node.key)

    def check_node_in_part(self, node):
        """Checks if a node already exists in the Part in the same location.

        Parameters
        ----------
        node : obj
            compas_fea2 Node object.

        Returns
        -------
        indices : list
            List of the indices of all the instances of the node already in the
            Part.
        """

        if node.gkey in self._nodes_gkeys:
            indices = [i for i, x in enumerate(self._nodes_gkeys) if x == node.gkey]
            return indices

    def add_node(self, node, check=False):
        """Add a :class:`Node` object to the ``Part``.
        If the node object has no label, one is automatically assigned.
        Duplicate nodes are automatically excluded.

        Parameters
        ----------
        node : obj
            :class:`Node` object.
        check : bool, optional
            If ``True``, checks if the node is already present. This is a quite
            resource-intense operation! Set to ``False`` for large parts (>10000
            nodes). By default ``False``

        Return
        ------
        int
            node key

        Examples
        --------
        >>> part = Part('mypart')
        >>> node = Node(1.0, 2.0, 3.0)
        >>> part.add_node(node)
        """
        if check and self.check_node_in_part(node):
            print('WARNING: duplicate node at {} skipped!'.format(node._gkey))
        else:
            k = len(self._nodes)
            node._key = k
            if not node._name:
                node._name = 'n-{}'.format(k)
            self._nodes.append(node)
            self._nodes_gkeys.append(node._gkey)
        return node._key

    def add_nodes(self, nodes, check=False):
        """Add multiple :class:`Node` objects to the ``Part``.

        Parameters
        ----------
        nodes : list
            List of :class:`Node` objects.
        check : bool, optional
            If ``True``, checks if the node is already present. This is a quite
            resource-intense operation! Set to ``False`` for large parts (>10000
            nodes). By default ``False``

        Return
        ------
        list of int
            list with the keys of the added nodes.

        Examples
        --------
        >>> part = Part('mypart')
        >>> node1 = Node([1.0, 2.0, 3.0])
        >>> node2 = Node([3.0, 4.0, 5.0])
        >>> node3 = Node([3.0, 4.0, 5.0]) # Duplicate node
        >>> part.add_nodes([node1, node2, node3], check=True)
        [0, 1, None]
        """
        return [self.add_node(node, check) for node in nodes]

    def remove_node(self, node_key):
        """Remove the node from the Part. If there are duplicate nodes, it
        removes also all the duplicates.

        Parameters
        ----------
        node_key : int
            Key number of the node to be removed.

        Returns
        -------
        None
        """
        raise NotImplementedError()
        # del self.nodes[node_key]
        # del self.nodes_gkeys[node_key]
        # self._reorder_nodes()

    def remove_nodes(self, nodes):
        """Remove the nodes from the Part. If there are duplicate nodes, it
        removes also all the duplicates.

        Parameters
        ----------
        node : list
            List with the key numbers of the nodes to be removed..

        Returns
        -------
        None
        """
        raise NotImplementedError()
        # for node in nodes:
        #     self.remove_node(node)

    def get_node_from_coordinates(self, xyz, tol):
        """Finds (if any) the nodes in the model at specified coordinates.
        A tollerance factor can be specified.

        Parameters
        ----------
        xyz : list
            List with the [x, y, z] coordinates.
        tol : int
            multiple to which round the coordinates.

        Returns
        -------
        list
            list with the keys of the maching nodes.
            key =  Part name
            value = Node object with the specified coordinates.
        """
        matches = []
        a = [tol * round(i/tol) for i in xyz]
        for node in self.nodes:
            b = [tol * round(i/tol) for i in node.xyz]
            if a == b:
                matches.append(node.key)
        return matches

    # =========================================================================
    #                           Materials methods
    # =========================================================================

    def add_material(self, material):
        """Add a :class:`Material` subclass object to the Part so that
        it can be later refernced and used in the Section and Element definitions.

        Parameters
        ----------
        material : obj
            :class:`Material` object to be added.

        Returns
        -------
        None
        """
        if material.name not in self._materials:
            self._materials[material.name] = material
        else:
            print('NOTE: {} already added to the model. skipped!'.format(material))

    def add_materials(self, materials):
        """Add multiple :class:`Material` subclass objects to the Part so
        that they can be later refernced and used in section and element definitions.

        Parameters
        ----------
        material : list
            List of :class:`Material` objects.

        Returns
        -------
        None
        """
        for material in materials:
            self.add_material(material)

    # =========================================================================
    #                        Sections methods
    # =========================================================================

    def add_section(self, section):
        """Add a :class:`Section` subclass object to the Part o that it can
        be later refernced and used in an element definition.

        Parameters
        ----------
        section : obj
            :class:`Section` subclass object to be added.

        Returns
        -------
        None

        Raises
        ------
        ValueError
            if the material associated to the section is a string and it has not
            been defined previously in the model
        """
        if section.name not in self._sections:
            self._sections[section.name] = section
            if isinstance(section.material, Material):
                if section.material.name not in self.materials:
                    self.add_material(section.material)
            elif isinstance(section.material, str):
                if section.material in self.materials:
                    section._material = self.materials[section.material]
                else:
                    raise ValueError(f'Material {section.material.__repr__()} not found in {self.__repr__}')
            else:
                raise TypeError('Provide a valid Section subclass object')

    def add_sections(self, sections):
        """Add multiple :class:`Section`subclass  objects to the Model.

        Parameters
        ----------
        sections : list
            list of :class:`Section` subclass objects.

        Returns
        -------
        None
        """
        for section in sections:
            self.add_section(section)

    # =========================================================================
    #                           Elements methods
    # =========================================================================

    # def _check_element_in_part(self, element):
    #     """Check if the element is already in the model and in case add it.
    #     If `element` is of type `str`, check if the element is already defined.
    #     If `element` is of type `Element`, add the element to the Part if not
    #     already defined.

    #     Warning
    #     -------
    #     the function does not check the elements connectivity. This could generate
    #     duplicate elements.

    #     Parameters
    #     ----------
    #     element : str or obj
    #         Name of the Part or Part object to check.

    #     Returns
    #     -------
    #     obj
    #         Part object

    #     Raises
    #     ------
    #     ValueError
    #         if `element` is a string and the element is not defined in the Part
    #     TypeError
    #         `element` must be either an instance of a `compas_fea2` Part class or the
    #         name of a Part already defined in the Problem.
    #     """
    #     if isinstance(element, str):
    #         if element not in self.elements:
    #             raise ValueError(f'{element} not found in the Part')
    #         element_name = element
    #     elif isinstance(element, Part):
    #         if element.name not in self.elements:
    #             self.add_element(element)
    #             print(f'{element.__repr__()} added to the Part')
    #         element_name = element.name
    #     else:
    #         raise TypeError(
    #             f'{element} is either not an instance of a `compas_fea2` Element class or not found in the Model')

    #     return self.elements[element_name]

    def _reorder_elements(self):
        """Reorders the elements to have consecutive keys.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """

        k = 0
        for element in self._elements:
            element.key = k
            k += 1

    def add_element(self, element, check=False):
        """Add a :class:`Element` subclass object to the Part.

        Parameters
        ----------
        element : obj
            :class:`Element` subclass object.
        check : bool
            If True, checks if the element keys are in the model. This is a quite
            resource-intense operation! Set to `False` for large models (>10000
            nodes)
        check : bool, optional
            If ``True``, checks if the node connected by the element are present.
            This is a quite resource-intense operation! Set to ``False`` for large parts (>10000
            nodes). By default ``False``

        Returns
        -------
        int
            element key
        """
        element._key = len(self.elements)
        if check:
            for c in element.connectivity:
                if c not in [node.key for node in self.nodes]:
                    raise ValueError(
                        f'ERROR CREATING ELEMENT: node {c} not found. Check the connectivity indices of element: \n {element.__repr__()}!')
        self._elements[element._key] = element

        if isinstance(element.section, str):
            if element.section in self._sections:
                element._section = self._sections[element.section]
            else:
                raise ValueError(f'{element.section.__repr__()} not found in {self.__repr__()}')
        elif isinstance(element.section, Section):
            self.add_section(element.section)
        else:
            raise TypeError('You must provide a Section object or the name of a previously added section')
        return element._key

    def add_elements(self, elements, check):
        """Adds multiple :class:`Element` subclass objects to the ``Part``.

        Parameters
        ----------
        elements : list
            List of :class:`Element` subclass objects.
        check : bool
            If True, checks if the element keys are in the model. This is a quite
            resource-intense operation! Set to `False` for large models (>10000
            nodes)

        Return
        ------
        list of int
            list with the keys of the added nodes.
        """
        return [self.add_element(element, check) for element in elements]

    def remove_element(self, element_key):
        """Removes the element from the Part.

        Parameters
        ----------
        element_key : int
            Key number of the element to be removed.

        Returns
        -------
        None
        """
        raise NotImplementedError()
        # # TODO check if element key exists
        # del self.elements[element_key]
        # self._reorder_elements()

    def remove_elements(self, elements):
        """Removes the elements from the Part.

        Parameters
        ----------
        elements : list
            List with the key numbers of the element to be removed.

        Returns
        -------
        None
        """
        raise NotImplementedError()

        # for element in elements:
        #     self.remove_element(element)

    # =========================================================================
    #                           Releases methods
    # =========================================================================

    # TODO: check the release definition
    def add_release(self, release):
        self.releases.append(release)

    def add_releases(self, releases):
        for release in releases:
            self.add_release(release)

    # =========================================================================
    #                           Groups methods
    # =========================================================================

    def add_group(self, group):
        if isinstance(group, (NodesGroup, ElementsGroup)):
            if group.name not in self.groups:
                self._groups[group.name] = group
        else:
            raise ValueError('You must provide either a NodesGroup or an ElementsGroup object')

    def add_groups(self, groups):
        for group in groups:
            self.add_group(group)

    def add_nodes_group(self, name, nodes_keys):
        """Add a NodeGroup object to the the part .

        Parameters
        ----------
        name : str
            name of the group.
        nodes : list
            list of nodes keys to group
        """
        m = importlib.import_module('.'.join(self.__module__.split('.')[:-1]))
        group = m.NodesGroup(name, nodes_keys)
        self._groups[name] = group

    def add_elements_group(self, name, elements_keys):
        """Add a ElementGroup object to the the part.

        Parameters
        ----------
        name : str
            name of the group.
        part : str
            name of the part
        elements : list
            list of elements keys to group
        """
        m = importlib.import_module('.'.join(self.__module__.split('.')[:-1]))
        group = m.ElementsGroup(name, elements_keys)
        self._groups[name] = group

    def add_elements_to_group(self, group_name, element_keys):
        raise NotADirectoryError()

    def remove_element_group(self, group_name):
        raise NotImplementedError()

    def remove_element_from_group(self, group_name, element):
        raise NotImplementedError()
