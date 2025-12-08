# file: friedman_analysis.py
"""
Friedman test analysis for PM comparison study
"""
"""

FRIEDMAN TEST ANALYSIS (alpha = 0.05)
============================================================

Total Completion Time (seconds)
------------------------------------------------------------
n per condition = 3
Chi-square = 2.6667
p-value = 0.2636
Kendall's W = 0.4444

Planning Efficiency Score
------------------------------------------------------------
n per condition = 3
Chi-square = 0.0000
p-value = 1.0000
Kendall's W = 0.0000

Execution Efficiency Score
------------------------------------------------------------
n per condition = 3
Chi-square = 2.0000
p-value = 0.3679
Kendall's W = 0.3333

============================================================
"""

import numpy as np
from scipy import stats
from data import completion_times, planning_efficiency_scores, execution_efficiency_scores


def organize_data_by_condition(data_list, value_key):
    """Extract values by classification into separate arrays"""
    ai_pm = [item[value_key] for item in data_list if item['classification'] == 'AI PM']
    human_pm = [item[value_key] for item in data_list if item['classification'] == 'Human PM']
    no_pm = [item[value_key] for item in data_list if item['classification'] == 'No PM']
    
    return np.array(ai_pm), np.array(human_pm), np.array(no_pm)


def verify_equal_n(ai_pm, human_pm, no_pm):
    """Verify all conditions have equal sample size"""
    n_ai = len(ai_pm)
    n_human = len(human_pm)
    n_no = len(no_pm)
    
    if not (n_ai == n_human == n_no):
        raise ValueError(f"Unequal sample sizes: AI PM (n={n_ai}), Human PM (n={n_human}), No PM (n={n_no})")
    
    return n_ai


def calculate_kendalls_w(chi_square, n, k):
    """Calculate Kendall's W concordance coefficient"""
    return chi_square / (n * (k - 1))


def run_friedman_test(data_list, value_key, label):
    """Run Friedman test on data"""
    print(f"\n{label}")
    print("-" * 60)
    
    # Organize data
    ai_pm, human_pm, no_pm = organize_data_by_condition(data_list, value_key)
    
    # Verify equal sample sizes
    n = verify_equal_n(ai_pm, human_pm, no_pm)
    
    # Friedman test
    chi_square, p_value = stats.friedmanchisquare(ai_pm, human_pm, no_pm)
    
    # Kendall's W
    k = 3  # number of conditions
    kendalls_w = calculate_kendalls_w(chi_square, n, k)
    
    print(f"n per condition = {n}")
    print(f"Chi-square = {chi_square:.4f}")
    print(f"p-value = {p_value:.4f}")
    print(f"Kendall's W = {kendalls_w:.4f}")
    
    return chi_square, p_value, kendalls_w


def main():
    print("FRIEDMAN TEST ANALYSIS (alpha = 0.05)")
    print("=" * 60)
    
    # Test 1: Completion time
    run_friedman_test(completion_times, 'total_completion_time_sec', 
                     "Total Completion Time (seconds)")
    
    # Test 2: Planning efficiency
    run_friedman_test(planning_efficiency_scores, 'efficiency_score',
                     "Planning Efficiency Score")
    
    # Test 3: Execution efficiency
    run_friedman_test(execution_efficiency_scores, 'efficiency_score',
                     "Execution Efficiency Score")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
