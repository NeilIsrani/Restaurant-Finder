class Activity:
    """Represents a possible activity that might be suggested to users."""

    def __init__(
        self,
        name: str,
        coordinates: tuple[float, float],
        activity_type: str,
        rating: float,
        price_category: float,
        time_needed: float
    ):
        self.name = name
        self.coordinates = coordinates
        self.activity_type = activity_type
        self.rating = rating
        self.price_category = price_category
        self.time_needed = time_needed

    def __repr__(self):
        return f"Activity({self.name})"

