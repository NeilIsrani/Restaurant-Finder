from math import radians, sin, cos, sqrt, atan2

from metro_graph import MetroGraph


class ETACalculator:
    """
    Simple estimator for ETA between two locations based on travel by metro.

    Eventually, the goal for this project is to switch to using an external API
    that will also take into account other modes of transport, traffic, metro
    delays, and other factors that influence transportation time.

    Therefore, where possible, we'd like to aim to minimize calls to `calculate_eta`
    to minimize future API costs.
    """

    def __init__(self, metro_graph: MetroGraph):
        self.metro_graph = metro_graph

    @staticmethod
    def haversine(location1: tuple[float, float], location2: tuple[float, float]) -> float:
        """Computes distance between two latitude/logitude coordinates in kilometers."""
        lat1, lon1, lat2, lon2 = map(radians, [location1[0], location1[1], location2[0], location2[1]])
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1-a))
        R = 6371.0
        distance = R * c
        return distance

    def nearest_station(self, coordinates: tuple[float, float]) -> tuple[str, float]:
        """Returns the station name and distance to the nearest metro station."""
        station_name = None
        min_distance = float("inf")

        for station in self.metro_graph.stations.values():
            distance = ETACalculator.haversine(coordinates, station.coordinates)

            if distance < min_distance:
                min_distance = distance
                station_name = station.name

        return station_name, min_distance

    def calculate_eta(self, location1: tuple[float, float], location2: tuple[float, float]) -> float:
        """Computes travel time between two locations, either by walking or via metro if it's faster."""
        nearest_station1, additional_distance1 = self.nearest_station(location1)
        nearest_station2, additional_distance2 = self.nearest_station(location2)

        if nearest_station1 is None or nearest_station2 is None:
            raise Exception("Could not find nearest metro station.")

        # Assume an average walking pace
        total_time_walking = (ETACalculator.haversine(location1, location2) / 5) * 60

        total_time_metro, shortest_path_metro = self.metro_graph.shortest_path(nearest_station1, nearest_station2)
        if shortest_path_metro:
            walking_time = (additional_distance1 / 5 * 60) + (additional_distance2 / 5 * 60)
            return total_time_metro + walking_time if total_time_metro < total_time_walking else total_time_walking
        else:
            # No metro route found, just return the walking time
            return total_time_walking
