class RoadData:
    """A class to representing a connecting road between two cities.
    """

    def __init__(self, name, *, city1, city2, dist, speed):
        """Initialize an instance of this class.
        Either city1 or city2 can be starting city for this connection.
        
        Parameters:
            name: The name of the road connecting city1 and city2.
            city1: The name of one connecting city.
            city2: The name of the other connecting city.
            dist: The distance between the cities in miles.
            speed: The speed_limit of the road in mph.
        """
        self.name = name
        self.city1 = city1
        self.city2 = city2
        self.dist = dist
        self.speed_limit = speed

        # self.hours is the time in hours needed to travel on this road,
        # assuming a car that travels at 5 mph above the speed_limit limit.

        self.hours = self.dist / (self.speed_limit + 5)

        # self.hours_bike is the time in hours needed for a bicycle to travel on
        # this road, assuming an average speed_limit of 13.5 mph.

        self.hours_bike = self.dist / 13.5

        # self.accidents is the expected number of accidents for a bicycle
        # traveling on this road, per trip. If self.accidents = 0.25, it means
        # there is a virtual certainty that one in four bicyclists would be
        # involved in an accident on this road.

        self.accidents = 0.000001 * self.speed_limit * self.dist
