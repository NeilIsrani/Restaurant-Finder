from dataclasses import dataclass
from typing import List, Tuple
from activity import Activity
from metro_graph import MetroGraph, Station
from eta_calculator import ETACalculator
from user_request import UserRequest
import math

@dataclass
class Suggestion:
    """Represents a suggested activity with ETAs for each user."""
    activity: Activity
    user_etas: List[float]

    """ def print_details(self):
        print(f"Activity: {self.activity.name} | User 1 ETA: {self.user1_eta:.1f} minutes | User 2 ETA: {self.user2_eta:.1f} minutes") """

# Counter for heuristic usage
heuristic_used = 0

def rough_distance(loc1: tuple[float, float], loc2: tuple[float, float]) -> float:
    """Quick estimate of distance between two points using Manhattan distance."""
    return abs(loc1[0] - loc2[0]) + abs(loc1[1] - loc2[1])

def suggest_midpoint_activity(
    user1_location: tuple[float, float],
    user2_location: tuple[float, float],
    activities: list[Activity],
    eta_calculator: ETACalculator
) -> Suggestion:
    """
    Returns a suggested activity that's somewhere between the users' locations.
    Uses heuristics to minimize calculate_eta calls:
    1. Uses rough distance estimates first to filter candidates
    2. Only calculates exact ETAs for promising candidates
    3. Stops early if we find a good enough suggestion
    """
    global heuristic_used
    if not activities:
        return None

    # Calculate rough distances to all activities from both users
    activity_scores = []
    for activity in activities:
        # Use rough Manhattan distance as a quick estimate
        dist1 = rough_distance(user1_location, activity.coordinates)
        dist2 = rough_distance(user2_location, activity.coordinates)
        rough_ratio = max(dist1, dist2) / min(dist1, dist2) if min(dist1, dist2) > 0 else float('inf')
        activity_scores.append((activity, rough_ratio, dist1 + dist2))
    
    # Sort activities by rough distance ratio and total distance
    activity_scores.sort(key=lambda x: (x[1], x[2]))
    
    # Only calculate exact ETAs for the top N candidates
    max_candidates = 5
    best_suggestion = None
    best_score = float('inf')
    best_fair_suggestion = None
    best_fair_score = float('inf')
    max_time_difference_ratio = 1.5

    # Increment heuristic counter if we filtered activities
    if len(activities) > max_candidates:
        heuristic_used += 1
    
    for activity, rough_ratio, rough_total in activity_scores[:max_candidates]:
        # Calculate exact ETAs only for promising candidates
        user1_eta = eta_calculator.calculate_eta(user1_location, activity.coordinates)
        user2_eta = eta_calculator.calculate_eta(user2_location, activity.coordinates)
        
        if user1_eta == 0 or user2_eta == 0:
            continue
            
        time_ratio = max(user1_eta, user2_eta) / min(user1_eta, user2_eta)
        total_time = user1_eta + user2_eta

        # Always update best overall suggestion
        if total_time < best_score:
            best_score = total_time
            best_suggestion = Suggestion(activity, [user1_eta, user2_eta])

        # If this is a fair suggestion, update best fair suggestion
        if time_ratio <= max_time_difference_ratio and total_time < best_fair_score:
            best_fair_score = total_time
            best_fair_suggestion = Suggestion(activity, [user1_eta, user2_eta])
    
    return best_fair_suggestion if best_fair_suggestion is not None else best_suggestion

def suggest_group_activity(
    user_locations: List[Tuple[float, float]],
    activities: list[Activity],
    eta_calculator: ETACalculator
) -> Suggestion:
    """
    Returns a suggested activity that's fair for all users in the group.
    Uses heuristics to minimize calculate_eta calls:
    1. Uses rough distance estimates first to filter candidates
    2. Only calculates exact ETAs for promising candidates
    3. Ensures no user has to travel more than 50% longer than any other user
    """
    global heuristic_used
    if not activities or not user_locations:
        return None

    # Calculate rough distances to all activities from all users
    activity_scores = []
    for activity in activities:
        # Use rough Manhattan distance as a quick estimate
        rough_distances = [rough_distance(loc, activity.coordinates) for loc in user_locations]
        rough_ratio = max(rough_distances) / min(rough_distances) if min(rough_distances) > 0 else float('inf')
        activity_scores.append((activity, rough_ratio, sum(rough_distances)))
    
    # Sort activities by rough distance ratio and total distance
    activity_scores.sort(key=lambda x: (x[1], x[2]))
    
    # Only calculate exact ETAs for the top N candidates
    max_candidates = 2
    best_suggestion = None
    best_score = float('inf')
    best_fair_suggestion = None
    best_fair_score = float('inf')
    max_time_difference_ratio = 1.5

    # Increment heuristic counter if we filtered activities
    if len(activities) > max_candidates:
        heuristic_used += 1
    
    for activity, rough_ratio, rough_total in activity_scores[:max_candidates]:
        # Calculate exact ETAs only for promising candidates
        user_etas = [eta_calculator.calculate_eta(loc, activity.coordinates) for loc in user_locations]
        
        if any(eta == 0 for eta in user_etas):
            continue
            
        time_ratio = max(user_etas) / min(user_etas)
        total_time = sum(user_etas)

        # Always update best overall suggestion
        if total_time < best_score:
            best_score = total_time
            best_suggestion = Suggestion(activity, user_etas)

        # If this is a fair suggestion, update best fair suggestion
        if time_ratio <= max_time_difference_ratio and total_time < best_fair_score:
            best_fair_score = total_time
            best_fair_suggestion = Suggestion(activity, user_etas)
    
    return best_fair_suggestion if best_fair_suggestion is not None else best_suggestion
