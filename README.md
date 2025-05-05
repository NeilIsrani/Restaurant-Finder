# Activity Suggestion System

This system helps find midpoint activities between users, taking into account commute times and fairness. It supports both pairs of users and larger groups.

## Features

- Suggests activities that minimize total commute time while ensuring fairness (no user has to travel more than 50% longer than others)
- Supports both pairs of users and groups of any size
- Optimizes ETA calculations using a rough distance heuristic
- Filters activities based on user preferences (activity type, rating, price, time needed)

## Requirements

- Python 3.x
- Required Python packages (install via `pip install -r requirements.txt`):
  - csv
  - dataclasses
  - typing

## Data Files

The system uses the following CSV files in the `data` directory:
- `metro_stations.csv`: Metro station locations
- `metro_timetable.csv`: Travel times between stations
- `activities.csv`: Available activities with their details
- `user_requests.csv`: Requests from pairs of users
- `user_group_requests.csv`: Requests from groups of users

## Running the System

1. Ensure all data files are in the `data` directory
2. Run the system:
```bash
python runner.py
```

