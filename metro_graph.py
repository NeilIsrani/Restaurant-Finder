from typing import Optional


class Station:
    def __init__(self, name: str, coordinates: tuple[float, float]):
        self.name = name
        self.coordinates = coordinates

    def __eq__(self, other):
        if not isinstance(other, Station):
            return NotImplemented
        return self.name == other.name

    def __repr__(self):
        return f"Station({self.name})"

class MetroGraph:
    # Mapping from station name -> station name -> travel time
    graph: dict[str, dict[str, float]]

    # Mapping from station name to stations
    stations: dict[str, Station]

    def __init__(self):
        self.graph = {}
        self.stations = {}

    def add_station(self, station: Station):
        """Add station to the graph."""
        if station.name not in self.stations:
            self.stations[station.name] = station
            self.graph[station.name] = {}

    def add_connection(self, start_station: str, end_station: str, time: float):
        """Add connection time between two station names."""
        if start_station in self.graph and end_station in self.graph:
            # Assume bidirectional connections
            self.graph[start_station][end_station] = time
            self.graph[end_station][start_station] = time
        else:
            raise Exception("Invalid connection: One or more stations not in graph.")

    def shortest_path(self, start_station: str, end_station: str) -> tuple[float, Optional[list[str]]]:
        """Returns the distance and shortest path between stations."""
        # Initialize distances dictionary with infinity for all stations except start_station
        distances: dict[str, float] = {station: float("inf") for station in self.graph}
        distances[start_station] = 0

        # Initialize dictionary to store previous station in shortest path
        previous: dict[str, Optional[str]] = {station: None for station in self.graph}

        # Priority queue implemented as a list to store tuples of (distance, station)
        priority_queue: list[tuple[float, str]] = [(0, start_station)]

        while priority_queue:
            # Manually find the smallest item in priority queue and remove it from queue
            current_distance, current_station = min(priority_queue, key=lambda x: x[0])
            priority_queue.remove((current_distance, current_station))

            # If we reach the end station, reconstruct and return the shortest path
            if current_station == end_station:
                path = []
                while current_station is not None:
                    path.append(current_station)
                    current_station = previous[current_station]
                path.reverse()
                return distances[end_station], path

            # Iterate through neighboring stations
            for neighbor, travel_time in self.graph[current_station].items():
                distance = current_distance + travel_time

                # If found shorter path to neighbor, update distances, previous station, and queue
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous[neighbor] = current_station

                    # Update the queue: Remove old entry if it exists and add new
                    priority_queue = [
                        (distance, station) for distance, station in priority_queue
                        if station != neighbor
                    ]
                    priority_queue.append((distance, neighbor))

        # End station is not reachable from start
        return float("inf"), None

