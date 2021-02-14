from unique_instances import UniqueInstancesClass


class Node(metaclass=UniqueInstancesClass):
    """A class to represent a node on a graph.
    """

    def __init__(self, name, *, data, gofs=None, hofs=None, path=None):
        """Initialize an instance of this class.
        
        Parameters:
            data: The state value of the node. The state could itself be an
                         object or data structure.
            name: Unique identifier.
            gofs: The cost to reach this node along the given path.
            hofs: Estimated cost to reach a goal state from this node.
            path: Solution path of which this node is the last element.
                         An ordered list of references to other Node instances.
        """
        gofs = 0.000 if gofs is None else gofs      # gofs = g(s)
        hofs = 0.000 if hofs is None else hofs      # hofs = h(s)
        path = list() if path is None else path

        self.data = data
        self.name = name
        self.gofs = gofs
        self.hofs = hofs
        self.path = path

    @property
    def fofs(self):     # fofs = f(s)
        return self.gofs + self.hofs
