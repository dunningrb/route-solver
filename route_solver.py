from node import Node
from queue import PriorityQueue
from math import atan, cos, radians, sin, sqrt
from unique_instances import UniqueInstancesClass
from city_data import CityData
from road_data import RoadData
import config


class RouteSolver:
    """
    A class to find the best route between two cities.
    """

    def __init__(self, *, start, end, opt):
        """Initialize an instance of this class.

        Parameters:
            start: Name of the starting city or location.
            end: Name of the ending city or location.
            opt: Optimization method.
        """

        self.start_city_name = start
        self.end_city_name = end
        self.cost_function = opt

        self.city_data = dict()  # Initialized by self.build_city_data().
        self.road_data = dict()  # Initialized by self.build_road_data().

        self.build_city_data()
        self.build_road_data()

        start_city_data = self.city_data[start]
        end_city_data = self.city_data[end]

        self.start_city = Node(start, data=start_city_data, gofs=0.00,
                               path=[start])
        
        self.end_city = Node(end, hofs=0.00, data=end_city_data)

        self.fringe = PriorityQueue()
        self.closed = list()

    @classmethod
    def distance(cls, city1, city2):
        """
        Return the distance in miles between the given cities.
        :param city1: type Node.
        :param city2: type Node.
        :return: the distance in miles.
        """

        earth_radius = 3958.8  # miles

        lat1 = radians(city1.data.lat)
        lng1 = radians(city1.data.lng)
        lat2 = radians(city2.data.lat)
        lng2 = radians(city2.data.lng)
        delta_lng = abs(lng2 - lng1)
        cos_delta_lng = cos(delta_lng)
        cos_lat1 = cos(lat1)
        cos_lat2 = cos(lat2)
        sin_delta_lng = sin(delta_lng)
        sin_lat1 = sin(lat1)
        sin_lat2 = sin(lat2)

        term_a = (cos_lat2 * sin_delta_lng) ** 2
        term_b = (cos_lat1 * sin_lat2 - sin_lat1 * cos_lat2 * cos_delta_lng) ** 2
        term_c = sin_lat1 * sin_lat2 + cos_lat1 * cos_lat2 * cos_delta_lng

        try:
            central_angle = atan(sqrt(term_a + term_b) / term_c)
        except ZeroDivisionError:
            return 0

        return earth_radius * central_angle

    def build_city_data(self):
        """
        Initialize self.city_data.
        :return:
        """
        if len(self.city_data) > 0:
            return self.city_data

        with open(config.CITY_GPS_PATH, 'r') as f:
            city_gps_lines = f.readlines()

        for line in city_gps_lines:
            tokens = line.split()
            name = tokens[0]
            lat = float(tokens[1])
            lng = float(tokens[2])
            self.city_data[tokens[0]] = CityData(name, lat=lat, lng=lng)

    def build_road_data(self):
        """
        Initialize self.road_data.
        :return:
        """
        if len(self.road_data) > 0:
            return self.road_data

        with open(config.ROAD_SEGMENTS_PATH, 'r') as f:
            road_segments_lines = f.readlines()

        for line in road_segments_lines:
            tokens = line.split()
            city1 = tokens[0]
            city2 = tokens[1]
            dist = int(tokens[2])
            speed = int(tokens[3])
            name = tokens[4]
            key = (city1, city2)
            self.road_data[key] = RoadData(name, city1=city1, city2=city2,
                                           dist=dist, speed=speed)

    def is_goal(self, city):
        """
        Return true if the given city (type Node) is the goal city.
        :param city: type Node.
        :return: bool
        """
        return self.distance(city, self.end_city) == 0

    def solve(self):
        """
        Find the best route between the start city and end city or fail.
        :return:
        """

        # Are we there yet?
        if self.is_goal(self.start_city):
            return self.start_city

        if self.cost_function in ['segments']:
            self.fringe.put((0.00, 0, self.start_city))
        else:
            self.fringe.put((0.00, self.start_city))

        counter = 0
        while not self.fringe.empty():
            if self.cost_function in ['segments']:
                fofs, _, next_city = self.fringe.get()
            else:
                fofs, next_city = self.fringe.get()

            # How much longer??
            if self.is_goal(next_city):
                return next_city

            self.closed.append(next_city.name)

            # Can we stop for ice cream???
            for successor in self.successors(next_city):
                if self.cost_function in ['segments']:
                    if (successor.fofs, 0, successor) not in self.fringe.queue:
                        counter += 1
                        self.fringe.put((successor.fofs, counter, successor))
                else:
                    if (successor.fofs, successor) not in self.fringe.queue:
                        self.fringe.put((successor.fofs, successor))

        # You can't get there from here.
        return

    def successors(self, city):
        """
        :param city: type Node.
        :return:
        """
        successors = list()
        road_data = self.road_data

        for pair in road_data.keys():
            if city.name in pair:
                index = {0: 1, 1: 0}[pair.index(city.name)]
                succ_city_name = pair[index]
                if succ_city_name in self.closed:
                    continue
                try:
                    succ_data = self.city_data[succ_city_name]
                except KeyError:
                    continue
                segments = city.data.segments + 1
                distance = city.data.distance + road_data[pair].dist
                hours = city.data.hours + road_data[pair].hours
                hours_bike = city.data.hours_bike + road_data[pair].hours_bike
                accidents = city.data.accidents + road_data[pair].accidents
                path = city.path + [succ_city_name]
                succ_data.starting_city = self.start_city
                succ_data.segments = segments
                succ_data.distance = distance
                succ_data.hours = hours
                succ_data.hours_bike = hours_bike
                succ_data.accidents = accidents

                # Is the goal city? Check by name. (This is not an exit
                # condition.)

                if succ_city_name == self.end_city.name:

                    # This is the goal city!

                    self.end_city.segments = segments
                    self.end_city.distance = distance
                    self.end_city.hours = hours
                    self.end_city.hours_bike = hours_bike
                    self.end_city.accidents = accidents
                    self.end_city.path = path

                    successors.append(self.end_city)

                    continue

                # The successor may already exist in the fringe. First we check
                # if an instance has been created at all. Note that an instance
                # of Node HAS been created for the goal city: self.end_city, but
                # we already check for this.

                existing_city_nodes = UniqueInstancesClass.get_instances()

                search_name = f'Node:{succ_city_name}'

                if search_name in existing_city_nodes.keys():

                    # The successor already exists as an instantiated Node. The
                    # hofs value cannot change, because it is calculated
                    # relative to the end city. But the gofs will be smaller if
                    # the search has (just now) discovered a shorter path to
                    # reach the successor.

                    city = existing_city_nodes[search_name]

                    # Now we must check if the successor, which already exists,
                    # is in the fringe. It should be, because we would not
                    # reach this point if the successor name was in self.closed
                    # or if the successor was the goal city, and there is
                    # nowhere else for it to be.

                    if (city.fofs, city) in self.fringe.queue:

                        # Now check if the distance just calculated is less than
                        # the current gofs.

                        if succ_data.distance + city.hofs > city.fofs:

                            # The new gofs is less, so remove the existing node
                            # from the fringe.

                            self.fringe.queue.remove((city.fofs, city))

                            # Overwrite the stored value of gofs, and overwrite
                            # the path (since it must be different).

                            city.gofs = succ_data.distance
                            city.path = path

                            # Add the existing node to the successors. After the
                            # return to the calling unit, the existing node will
                            # be put back on the fringe, but with new values
                            # for gofs and path.

                            successors.append(city)

                            continue

                        else:

                            # The new gofs is greater than the existing value.
                            # We can reject this city as a viable successor.

                            continue

                    # The successor exists as an instantiated node but it is not
                    # referenced by name in self.closed, is not on the fringe,
                    # and is not the goal city. So this is a stray node that is
                    # somehow lost, and indicates a logic error.

                    continue

                else:
                    # The successor has not been instantiated. Instantiate it,
                    # and add it to the list of successors.

                    # The choice of gofs and hofs depends on the cost function
                    # specified by the user.

                    gofs = {
                        'segments': succ_data.segments, 'distance': succ_data.distance,
                        'time': succ_data.hours, 'cycling': succ_data.accidents
                    }[self.cost_function]

                    successor = Node(succ_city_name, data=succ_data,
                                     gofs=gofs, path=path)

                    distance = self.distance(successor, self.end_city)

                    try:
                        hours = distance / (city.data.distance / city.data.hours)
                    except ZeroDivisionError:
                        hours = distance / self.road_data[pair].speed_limit

                    try:
                        accidents = 0.000001 * (city.data.distance / city.data.hours) * distance
                    except ZeroDivisionError:
                        accidents = 0.000001 * self.road_data[pair].speed_limit * distance

                    successor.hofs = {'segments': 1, 'distance': distance,
                                      'time': hours, 'cycling': accidents}[self.cost_function]

                    successors.append(successor)

        return successors
