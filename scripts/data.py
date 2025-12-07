# file: data.py
"""
Data file containing experimental results for PM comparison study
"""

# Average Round Ratings
avg_round_ratings = [
    {"round": 1, "classification": "AI PM", "avg_structure_difficulty": 1.00, "avg_plan_rating": 3.67},
    {"round": 2, "classification": "Human PM", "avg_structure_difficulty": 4.33, "avg_plan_rating": 3.00},
    {"round": 3, "classification": "No PM", "avg_structure_difficulty": 3.33, "avg_plan_rating": 5.67},
    {"round": 4, "classification": "AI PM", "avg_structure_difficulty": 3.67, "avg_plan_rating": 3.33},
    {"round": 5, "classification": "Human PM", "avg_structure_difficulty": 5.67, "avg_plan_rating": 5.00},
    {"round": 6, "classification": "No PM", "avg_structure_difficulty": 5.00, "avg_plan_rating": 5.00},
    {"round": 7, "classification": "AI PM", "avg_structure_difficulty": 6.33, "avg_plan_rating": 4.00},
    {"round": 8, "classification": "Human PM", "avg_structure_difficulty": 5.33, "avg_plan_rating": 3.00},
    {"round": 9, "classification": "No PM", "avg_structure_difficulty": 2.67, "avg_plan_rating": 6.00},
]

# Completion Times
completion_times = [
    {"round": 1, "classification": "AI PM", "total_completion_time_sec": 244},
    {"round": 2, "classification": "Human PM", "total_completion_time_sec": 943},
    {"round": 3, "classification": "No PM", "total_completion_time_sec": 352},
    {"round": 4, "classification": "AI PM", "total_completion_time_sec": 692},
    {"round": 5, "classification": "Human PM", "total_completion_time_sec": 987},
    {"round": 6, "classification": "No PM", "total_completion_time_sec": 529},
    {"round": 7, "classification": "AI PM", "total_completion_time_sec": 882},
    {"round": 8, "classification": "Human PM", "total_completion_time_sec": 561},
    {"round": 9, "classification": "No PM", "total_completion_time_sec": 413},
]

# Planning Efficiency Scores
planning_efficiency_scores = [
    {"round": 1, "classification": "AI PM", "efficiency_score": 20.62},
    {"round": 2, "classification": "Human PM", "efficiency_score": -81.51},
    {"round": 3, "classification": "No PM", "efficiency_score": 29.43},
    {"round": 4, "classification": "AI PM", "efficiency_score": -6.88},
    {"round": 5, "classification": "Human PM", "efficiency_score": 24.24},
    {"round": 6, "classification": "No PM", "efficiency_score": 0.87},
    {"round": 7, "classification": "AI PM", "efficiency_score": 15.61},
    {"round": 8, "classification": "Human PM", "efficiency_score": 9.55},
    {"round": 9, "classification": "No PM", "efficiency_score": -11.94},
]

# Execution Efficiency Scores
execution_efficiency_scores = [
    {"round": 1, "classification": "AI PM", "efficiency_score": 26.44},
    {"round": 2, "classification": "Human PM", "efficiency_score": 216.33},
    {"round": 3, "classification": "No PM", "efficiency_score": -141.64},
    {"round": 4, "classification": "AI PM", "efficiency_score": 121.35},
    {"round": 5, "classification": "Human PM", "efficiency_score": 203.28},
    {"round": 6, "classification": "No PM", "efficiency_score": -196.70},
    {"round": 7, "classification": "AI PM", "efficiency_score": 8.26},
    {"round": 8, "classification": "Human PM", "efficiency_score": -196.71},
    {"round": 9, "classification": "No PM", "efficiency_score": -40.61},
]