class CityData:
    """A class to encapsulate data for a city.
    """

    def __init__(self, name, *, lat=None, lng=None, starting_city=None,
                 segments=0, distance=0.00, hours=0.00, hours_bike=0.00,
                 accidents=0.00):
        """Initialize an instance of this class.
        The values for attributes segments, distance, hours, accidents, and
        route are all relative to the starting city of the overall search.
        
        Parameters: 
            name: Name of the city (may not be an actual city).
            lat: Latitude, if known, or None.
            lng: Longitude, if known, or None.
            starting_city: Name of the starting city.
            segments: Number of road segments to reach this city.
            distance: Distance to reach this city.
            hours: Time to reach this city by car.
            hours_bike: Time to reach this city by bicycle.
            accidents: Expected number of accidents reaching this city by bicycle.
        """
        self.name = name
        self.lat = lat
        self.lng = lng
        self.starting_city = starting_city
        self.segments = segments
        self.distance = distance
        self.hours = hours
        self.hours_bike = hours_bike
        self.accidents = accidents
