class UniqueInstancesClass(type):
    """A metaclass to provide class instances with a unique identifier."""

    _instances = dict()
    _id = None

    def __call__(cls, *args, **kwargs):
        """Implements a factory pattern to return a new instance if there is no
        existing instance with the same _id, otherwise returns the existing
        instance with that _id.

        Notes:
            Skips __init__ methods in all derived classes if returning an
            existing instance.

            It is assumed that either the SECOND or FIRST positional argument
            or the FIRST keyword argument provides a unique identifier for a
            particular child type (cls.__name__). The child type (cls.__name__)
            is combined with this identifier to create an identifier that is
            unique across all child types that inherit from this class.

            Order preference for the unique identifier:
                1st: SECOND position argument.
                2nd: FIRST position argument.
                3rd: FIRST keyword argument.
        """

        if args:
            if len(args) >= 2:
                unique_identifier = args[1]
            else:
                unique_identifier = args[0]
        elif kwargs:
            unique_identifier = kwargs[list(kwargs.keys())[0]]
        else:
            return

        cls._id = "{0}:{1}".format(cls.__name__, unique_identifier)

        if cls._id not in cls._instances.keys():
            self = cls.__new__(cls, *args, **kwargs)
            cls._instances[cls._id] = self
            cls.__init__(self, *args, **kwargs)
        return cls._instances[cls._id]

    def __init__(cls, *args, **kwargs):
        """Initialize the child class instance.
        """
        super(UniqueInstancesClass, cls).__init__(cls)

    @classmethod
    def get_instances(mcs):
        return mcs._instances

    @classmethod
    def get_instance_ids(mcs):
        return list(mcs._instances.keys())
