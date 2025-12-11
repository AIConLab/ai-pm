"""
Script to validate linear model assumption for efficiency score metric
Creates scatterplot of difficulty vs completion time with regression line
"""
import os

# Set matplotlib config directory BEFORE importing matplotlib to avoid permission issues
os.environ['MPLCONFIGDIR'] = '/tmp/matplotlib'
os.makedirs('/tmp/matplotlib', exist_ok=True)

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
from data import avg_round_ratings, completion_times

# ============================================================================
# CONFIGURATION - Match existing style
# ============================================================================

# Font settings
FONT_FAMILY = 'DejaVu Serif'
TITLE_SIZE = 20
AXIS_LABEL_SIZE = 18
TICK_LABEL_SIZE = 16
LEGEND_SIZE = 14
DATA_LABEL_SIZE = 14

# Colors
COLOR_BLACK = '#000000'
COLOR_DARK_GREY = '#2C2C2C'
COLOR_LIGHT_GREY = '#808080'
COLOR_UTSA_BLUE = '#0C2340'
COLOR_UTSA_ORANGE = '#F15A22'
COLOR_YELLOW = '#FFC107'

# Condition colors mapping
CONDITION_COLORS = {
    'AI PM': COLOR_UTSA_BLUE,
    'Human PM': COLOR_UTSA_ORANGE,
    'No PM': COLOR_YELLOW
}

# Figure settings
DPI = 300
FIGURE_WIDTH = 10
FIGURE_HEIGHT = 7

# Grid and styling
GRID_ALPHA = 0.3
GRID_LINESTYLE = '--'
GRID_LINEWIDTH = 0.5

# ============================================================================
# SETUP
# ============================================================================

def setup_plot_style():
    """Configure matplotlib to use specified fonts and styling"""
    plt.rcParams['font.family'] = FONT_FAMILY
    plt.rcParams['font.size'] = TICK_LABEL_SIZE
    plt.rcParams['axes.labelsize'] = AXIS_LABEL_SIZE
    plt.rcParams['axes.titlesize'] = TITLE_SIZE
    plt.rcParams['xtick.labelsize'] = TICK_LABEL_SIZE
    plt.rcParams['ytick.labelsize'] = TICK_LABEL_SIZE
    plt.rcParams['legend.fontsize'] = LEGEND_SIZE
    plt.rcParams['figure.dpi'] = DPI

def save_figure(fig, filename):
    """Save figure at 300 DPI as PNG"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir, 'output')
    os.makedirs(output_dir, exist_ok=True)
    
    output_path = os.path.join(output_dir, filename)
    fig.savefig(output_path, dpi=DPI, bbox_inches='tight', facecolor='white')
    print(f"Saved: {output_path}")

# ============================================================================
# MAIN PLOT: Difficulty vs Completion Time with Regression
# ============================================================================

def create_validation_scatterplot():
    """Create scatterplot showing relationship between difficulty and completion time"""
    setup_plot_style()
    
    # Prepare data - merge difficulty ratings with completion times
    data = []
    for rating_item in avg_round_ratings:
        round_num = rating_item['round']
        difficulty = rating_item['avg_structure_difficulty']
        classification = rating_item['classification']
        
        # Find matching completion time
        for time_item in completion_times:
            if time_item['round'] == round_num:
                data.append({
                    'round': round_num,
                    'difficulty': difficulty,
                    'time': time_item['total_completion_time_sec'],
                    'classification': classification
                })
                break
    
    # Extract arrays for regression
    difficulties = np.array([d['difficulty'] for d in data])
    times = np.array([d['time'] for d in data])
    rounds = [d['round'] for d in data]
    classifications = [d['classification'] for d in data]
    
    # Perform linear regression
    slope, intercept, r_value, p_value, std_err = stats.linregress(difficulties, times)
    r_squared = r_value ** 2
    
    # Create figure
    fig, ax = plt.subplots(figsize=(FIGURE_WIDTH, FIGURE_HEIGHT))
    
    # Plot data points colored by condition
    for i, (diff, time, round_num, cond) in enumerate(zip(difficulties, times, rounds, classifications)):
        ax.scatter(diff, time, 
                  color=CONDITION_COLORS[cond],
                  s=250,
                  alpha=0.8,
                  edgecolors=COLOR_DARK_GREY,
                  linewidths=2,
                  zorder=3,
                  label=cond if cond not in [c for c in classifications[:i]] else '')
        
        # Add round number next to point
        ax.text(diff + 0.15, time, f'R{round_num}',
               fontsize=DATA_LABEL_SIZE-2,
               color=COLOR_BLACK,
               va='center',
               ha='left',
               fontweight='bold')
    
    # Plot regression line
    x_line = np.array([difficulties.min() - 0.5, difficulties.max() + 0.5])
    y_line = slope * x_line + intercept
    ax.plot(x_line, y_line, 
            color='#D32F2F',
            linewidth=3,
            linestyle='-',
            label=f'Linear Fit',
            zorder=2)
    
    # Add regression equation and statistics
    equation_text = f'y = {slope:.1f}x + {intercept:.1f}\nR² = {r_squared:.3f}\np = {p_value:.4f}'
    ax.text(0.05, 0.95, equation_text,
           transform=ax.transAxes,
           fontsize=LEGEND_SIZE,
           verticalalignment='top',
           bbox=dict(boxstyle='round', facecolor='white', alpha=0.8, edgecolor=COLOR_DARK_GREY),
           color=COLOR_BLACK,
           fontfamily=FONT_FAMILY)
    
    # Formatting
    ax.set_xlabel('Structure Difficulty Rating (1-7 scale)', 
                 fontsize=AXIS_LABEL_SIZE, 
                 color=COLOR_DARK_GREY, 
                 fontweight='bold')
    ax.set_ylabel('Total Completion Time (seconds)', 
                 fontsize=AXIS_LABEL_SIZE, 
                 color=COLOR_DARK_GREY, 
                 fontweight='bold')
    ax.set_title('Validation of Linear Model: Difficulty vs Completion Time', 
                fontsize=TITLE_SIZE, 
                color=COLOR_BLACK, 
                fontweight='bold',
                pad=20)
    
    # Grid
    ax.grid(True, alpha=GRID_ALPHA, linestyle=GRID_LINESTYLE, linewidth=GRID_LINEWIDTH)
    ax.set_axisbelow(True)
    
    # Style tick labels
    ax.tick_params(colors=COLOR_DARK_GREY)
    for label in ax.get_xticklabels():
        label.set_color(COLOR_DARK_GREY)
    for label in ax.get_yticklabels():
        label.set_color(COLOR_DARK_GREY)
    
    # Set reasonable axis limits
    ax.set_xlim(0, 7)
    ax.set_ylim(0, max(times) * 1.1)
    
    # Legend
    handles, labels = ax.get_legend_handles_labels()
    # Reorder to show conditions first, then regression line
    condition_order = ['AI PM', 'Human PM', 'No PM', 'Linear Fit']
    ordered_handles = []
    ordered_labels = []
    for label in condition_order:
        if label in labels:
            idx = labels.index(label)
            ordered_handles.append(handles[idx])
            ordered_labels.append(labels[idx])
    
    ax.legend(ordered_handles, ordered_labels, 
             loc='upper left', 
             framealpha=0.9, 
             fontsize=LEGEND_SIZE)
    
    plt.tight_layout()
    save_figure(fig, 'Linear_Model_Validation_Scatterplot.png')
    
    # Print statistics to console
    print("\n" + "="*60)
    print("LINEAR REGRESSION STATISTICS")
    print("="*60)
    print(f"Slope (β₁):           {slope:.2f} seconds/difficulty point")
    print(f"Intercept (β₀):       {intercept:.2f} seconds")
    print(f"R-squared (R²):       {r_squared:.4f}")
    print(f"Correlation (r):      {r_value:.4f}")
    print(f"P-value:              {p_value:.4f}")
    print(f"Standard Error:       {std_err:.2f}")
    print(f"Sample Size (n):      {len(difficulties)}")
    print("="*60)
    
    if p_value < 0.05:
        print("✓ The relationship is statistically significant (p < 0.05)")
    else:
        print("✗ The relationship is NOT statistically significant (p ≥ 0.05)")
    
    if r_squared > 0.5:
        print(f"✓ The model explains {r_squared*100:.1f}% of variance (R² > 0.5)")
    else:
        print(f"⚠ The model explains only {r_squared*100:.1f}% of variance (R² ≤ 0.5)")
    
    print("="*60 + "\n")
    
    plt.close()

# ============================================================================
# RESIDUAL PLOT
# ============================================================================

def create_residual_plot():
    """Create residual plot to check for linearity and homoscedasticity"""
    setup_plot_style()
    
    # Prepare data
    data = []
    for rating_item in avg_round_ratings:
        round_num = rating_item['round']
        difficulty = rating_item['avg_structure_difficulty']
        classification = rating_item['classification']
        
        for time_item in completion_times:
            if time_item['round'] == round_num:
                data.append({
                    'round': round_num,
                    'difficulty': difficulty,
                    'time': time_item['total_completion_time_sec'],
                    'classification': classification
                })
                break
    
    difficulties = np.array([d['difficulty'] for d in data])
    times = np.array([d['time'] for d in data])
    rounds = [d['round'] for d in data]
    classifications = [d['classification'] for d in data]
    
    # Perform linear regression
    slope, intercept, r_value, p_value, std_err = stats.linregress(difficulties, times)
    
    # Calculate fitted values and residuals
    fitted_values = slope * difficulties + intercept
    residuals = times - fitted_values
    
    # Create figure
    fig, ax = plt.subplots(figsize=(FIGURE_WIDTH, FIGURE_HEIGHT))
    
    # Plot residuals
    for i, (fitted, residual, round_num, cond) in enumerate(zip(fitted_values, residuals, rounds, classifications)):
        ax.scatter(fitted, residual,
                  color=CONDITION_COLORS[cond],
                  s=250,
                  alpha=0.8,
                  edgecolors=COLOR_DARK_GREY,
                  linewidths=2,
                  zorder=3,
                  label=cond if cond not in [c for c in classifications[:i]] else '')
        
        # Add round number next to point
        ax.text(fitted + 15, residual, f'R{round_num}',
               fontsize=DATA_LABEL_SIZE-2,
               color=COLOR_BLACK,
               va='center',
               ha='left',
               fontweight='bold')
    
    # Add horizontal line at y=0
    ax.axhline(y=0, color=COLOR_DARK_GREY, linestyle='-', linewidth=2, zorder=2)
    
    # Formatting
    ax.set_xlabel('Fitted Values (seconds)', 
                 fontsize=AXIS_LABEL_SIZE, 
                 color=COLOR_DARK_GREY, 
                 fontweight='bold')
    ax.set_ylabel('Residuals (seconds)', 
                 fontsize=AXIS_LABEL_SIZE, 
                 color=COLOR_DARK_GREY, 
                 fontweight='bold')
    ax.set_title('Residual Plot: Checking Linear Model Assumptions', 
                fontsize=TITLE_SIZE, 
                color=COLOR_BLACK, 
                fontweight='bold',
                pad=20)
    
    # Grid
    ax.grid(True, alpha=GRID_ALPHA, linestyle=GRID_LINESTYLE, linewidth=GRID_LINEWIDTH)
    ax.set_axisbelow(True)
    
    # Style tick labels
    ax.tick_params(colors=COLOR_DARK_GREY)
    for label in ax.get_xticklabels():
        label.set_color(COLOR_DARK_GREY)
    for label in ax.get_yticklabels():
        label.set_color(COLOR_DARK_GREY)
    
    # Legend
    ax.legend(loc='best', framealpha=0.9, fontsize=LEGEND_SIZE)
    
    # Add interpretation text
    interpretation = "Good fit: residuals randomly scattered around zero\nPoor fit: residuals show pattern or increasing spread"
    ax.text(0.98, 0.02, interpretation,
           transform=ax.transAxes,
           fontsize=LEGEND_SIZE-2,
           verticalalignment='bottom',
           horizontalalignment='right',
           bbox=dict(boxstyle='round', facecolor='white', alpha=0.8, edgecolor=COLOR_DARK_GREY),
           color=COLOR_BLACK,
           fontfamily=FONT_FAMILY)
    
    plt.tight_layout()
    save_figure(fig, 'Residual_Plot.png')
    
    # Print residual statistics
    print("\n" + "="*60)
    print("RESIDUAL ANALYSIS")
    print("="*60)
    print(f"Mean of residuals:     {np.mean(residuals):.2f} (should be ≈ 0)")
    print(f"Std dev of residuals:  {np.std(residuals, ddof=2):.2f}")
    print(f"Min residual:          {np.min(residuals):.2f}")
    print(f"Max residual:          {np.max(residuals):.2f}")
    print("="*60)
    print("\nResiduals by round:")
    for i, (round_num, residual) in enumerate(zip(rounds, residuals)):
        print(f"  Round {round_num}: {residual:7.2f}s")
    print("="*60 + "\n")
    
    plt.close()

# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    print("="*60)
    print("VALIDATING LINEAR MODEL FOR EFFICIENCY SCORE METRIC")
    print("="*60)
    
    create_validation_scatterplot()
    create_residual_plot()
    
    print("="*60)
    print("VALIDATION PLOTS GENERATED SUCCESSFULLY!")
    print("="*60)
    print("\nInterpretation Guide:")
    print("---------------------")
    print("1. Check scatterplot for linear trend")
    print("2. Examine R² value (>0.5 is generally acceptable for exploratory)")
    print("3. Look at p-value (<0.05 indicates significant relationship)")
    print("4. Check residual plot for:")
    print("   - Random scatter (not curved pattern)")
    print("   - Constant spread (homoscedasticity)")
    print("   - No obvious outliers")
    print("="*60)