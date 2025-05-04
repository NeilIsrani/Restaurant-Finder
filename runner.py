from eta_calculator import ETACalculator
from suggestion import suggest_midpoint_activity, suggest_group_activity, rough_distance, get_heur
from midpoint_utils import load_metro_graph, load_user_requests, load_group_requests, load_activities
from activity import Activity
from user_request import UserRequest, GroupRequest

def filter_activities(activities: list[Activity], request: UserRequest | GroupRequest) -> list[Activity]:
    """
    Filter activities based on user preferences. If no activities meet all criteria,
    fall back to only filtering by activity type.
    """
    # First try to filter by all criteria
    filtered_activities = [
        activity for activity in activities
        if (activity.activity_type == request.activity_type and
            activity.rating >= request.rating and
            activity.price_category <= request.price_category and
            activity.time_needed <= request.time_needed)
    ]
    
    # If no activities meet all criteria, fall back to only filtering by activity type
    if not filtered_activities:
        filtered_activities = [
            activity for activity in activities
            if activity.activity_type == request.activity_type
        ]
    
    return filtered_activities

class Runner:
    def run(self):
        eta_calculator = ETACalculator(load_metro_graph())
        user_requests = load_user_requests()
        group_requests = load_group_requests()
        activities = load_activities()

        print("\n=== Task 1: Activity Filtering ===")
        print("Processing user requests...\n")

        # Task 1: Track suggestions generated
        suggestions_generated = 0
        total_requests = len(user_requests)

        # Task 2: Track fairness statistics
        fair_suggestions = 0
        total_suggestions = 0
        heuristic_used = 0
        # Process individual requests
        for request in user_requests:
            filtered_activities = filter_activities(activities, request)
            suggestion = suggest_midpoint_activity(request.user1_location, request.user2_location, filtered_activities, eta_calculator)
            if suggestion is not None:
                suggestions_generated += 1
                total_suggestions += 1
                # Check if suggestion is fair (ratio <= 1.5)
                time_ratio = max(suggestion.user_etas) / min(suggestion.user_etas)
                if time_ratio <= 1.5:
                    fair_suggestions += 1
                if get_heur():
                    print("ping")
                    heuristic_used += 1    
                # suggestion.print_details()

        # Process group requests
        print("\n=== Task 3: Group Activity Suggestions ===")
        print("Processing group requests...\n")
        
        group_suggestions = 0
        total_group_requests = len(group_requests)
        fair_group_suggestions = 0
        total_group_suggestions = 0

        for request in group_requests:
            filtered_activities = filter_activities(activities, request)
            suggestion = suggest_group_activity(request.user_locations, filtered_activities, eta_calculator)
            if suggestion is not None:
                group_suggestions += 1
                total_group_suggestions += 1
                # Check if suggestion is fair (ratio <= 1.5)
                time_ratio = max(suggestion.user_etas) / min(suggestion.user_etas)
                if time_ratio <= 1.5:
                    fair_group_suggestions += 1
                # suggestion.print_details()

        # Print Task 1 summary
        print(f"\nTask 1 Tests")
        print(f"Total user requests: {total_requests}")
        print(f"Suggestions generated: {suggestions_generated}")
        print(f"Success rate: {(suggestions_generated/total_requests*100):.1f}%")

        # Print Task 2 summary
        print(f"\nTask 2 Tests ")
        print(f"Total suggestions analyzed: {total_suggestions}")
        print(f"Fair suggestions (≤50% time difference): {fair_suggestions}")
        print(f"Percentage of fair suggestions: {(fair_suggestions/total_suggestions*100):.1f}%")
        print(f"Number of times heuristic was used: {heuristic_used}")
        print(f"Percentage of requests using heuristic: {(heuristic_used/total_requests*100):.1f}%")

        # Print Task 3 summary
        print(f"\nTask 3 Summary:")
        print(f"Total group requests: {total_group_requests}")
        print(f"Group suggestions generated: {group_suggestions}")
        print(f"Group success rate: {(group_suggestions/total_group_requests*100):.1f}%")
        print(f"Fair group suggestions: {fair_group_suggestions}")
        if total_group_suggestions > 0:
            print(f"Percentage of fair group suggestions: {(fair_group_suggestions/total_group_suggestions*100):.1f}%")
        else:
            print("Percentage of fair group suggestions: N/A (no suggestions generated)")

if __name__ == "__main__":
    Runner().run()
