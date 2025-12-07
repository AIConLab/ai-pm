"""
Main script to generate research figures at 300 DPI
"""
import os

# Set matplotlib config directory BEFORE importing matplotlib to avoid permission issues
os.environ['MPLCONFIGDIR'] = '/tmp/matplotlib'
os.makedirs('/tmp/matplotlib', exist_ok=True)

import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np
from data import (
    avg_round_ratings,
    completion_times,
    planning_efficiency_scores,
    execution_efficiency_scores
)

# ============================================================================
# CONFIGURATION - All styling variables in one place
# ============================================================================

# Font settings
FONT_FAMILY = 'DejaVu Serif'  # Times New Roman alternative (widely available)
TITLE_SIZE = 20
AXIS_LABEL_SIZE = 18
TICK_LABEL_SIZE = 16
LEGEND_SIZE = 16
DATA_LABEL_SIZE = 16

# Colors
COLOR_BLACK = '#000000'           # Main labels
COLOR_DARK_GREY = '#2C2C2C'       # Axis labels (more distinct)
COLOR_LIGHT_GREY = '#808080'      # Inner chart numbers
COLOR_UTSA_BLUE = '#0C2340'       # UTSA Dark Blue
COLOR_UTSA_ORANGE = '#F15A22'     # UTSA Orange
COLOR_YELLOW = '#FFC107'          # For No PM condition

# Condition colors mapping
CONDITION_COLORS = {
    'AI PM': COLOR_UTSA_BLUE,
    'Human PM': COLOR_UTSA_ORANGE,
    'No PM': COLOR_YELLOW
}

# Figure settings
DPI = 300
FIGURE_WIDTH = 10
FIGURE_HEIGHT = 6

# Grid and styling
GRID_ALPHA = 0.3
GRID_LINESTYLE = '--'
GRID_LINEWIDTH = 0.5

# ============================================================================
# HELPER FUNCTIONS
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
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir, 'output')
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    output_path = os.path.join(output_dir, filename)
    fig.savefig(output_path, dpi=DPI, bbox_inches='tight', facecolor='white')
    print(f"Saved: {output_path}")

# ============================================================================
# FIGURE 1: Execution Efficiency Score Distribution
# ============================================================================

def create_execution_efficiency_plot():
    """Create scatter plot showing execution efficiency scores by condition"""
    setup_plot_style()
    
    fig, ax = plt.subplots(figsize=(FIGURE_WIDTH, FIGURE_HEIGHT))
    
    # Organize data by condition
    conditions = {}
    for item in execution_efficiency_scores:
        cond = item['classification']
        if cond not in conditions:
            conditions[cond] = {'rounds': [], 'scores': []}
        conditions[cond]['rounds'].append(item['round'])
        conditions[cond]['scores'].append(item['efficiency_score'])
    
    # Calculate means for each condition
    means = {cond: np.mean(data['scores']) for cond, data in conditions.items()}
    
    # Plot each condition
    x_positions = {'AI PM': 0, 'Human PM': 1, 'No PM': 2}
    
    for cond in ['AI PM', 'Human PM', 'No PM']:
        if cond in conditions:
            x_pos = x_positions[cond]
            scores = conditions[cond]['scores']
            rounds = conditions[cond]['rounds']
            
            # Plot individual points - solid color without text inside
            for i, (score, round_num) in enumerate(zip(scores, rounds)):
                ax.scatter(x_pos, score, 
                          color=CONDITION_COLORS[cond], 
                          s=200,
                          alpha=0.8,
                          edgecolors=COLOR_DARK_GREY,
                          linewidths=2,
                          zorder=3)
                
                # Add round number to LEFT in parentheses: (round#)
                ax.text(x_pos - 0.15, score, f'({round_num})', 
                       fontsize=DATA_LABEL_SIZE-2, 
                       color=COLOR_BLACK,
                       va='center',
                       ha='right',
                       fontweight='bold')
                
                # Add score value to RIGHT
                ax.text(x_pos + 0.15, score, f'{score:.0f}', 
                       fontsize=DATA_LABEL_SIZE-2, 
                       color=COLOR_BLACK,
                       va='center',
                       ha='left')
            
            # Plot mean as triangle
            ax.scatter(x_pos, means[cond], 
                      marker='^', 
                      s=200, 
                      color='#2E7D32',
                      edgecolors=COLOR_BLACK,
                      linewidths=2,
                      zorder=4,
                      label='Mean' if cond == 'AI PM' else '')
            
            # Add mean value label to Right
            ax.text(x_pos + 0.15, means[cond], f'{means[cond]:.0f}', 
                   fontsize=DATA_LABEL_SIZE-2, 
                   color=COLOR_BLACK,
                   va='center',
                   ha='left')
    
    # Formatting
    ax.set_xticks([0, 1, 2])
    ax.set_xticklabels(['AI PM', 'Human PM', 'No PM'], fontsize=AXIS_LABEL_SIZE, color=COLOR_DARK_GREY)
    ax.set_ylabel('Execution Efficiency Score', fontsize=AXIS_LABEL_SIZE, color=COLOR_DARK_GREY, fontweight='bold')
    ax.set_title('Execution Efficiency Score Distribution', 
                fontsize=TITLE_SIZE, 
                color=COLOR_BLACK, 
                fontweight='bold',
                pad=20)
    
    ax.grid(True, alpha=GRID_ALPHA, linestyle=GRID_LINESTYLE, linewidth=GRID_LINEWIDTH)
    ax.axhline(y=0, color=COLOR_DARK_GREY, linestyle='-', linewidth=1)
    
    # Set y-axis limits with more padding for labels
    ax.set_yticks(np.arange(-250, 250, 50))
    ax.set_xlim(-0.6, 2.6)
    
    # Style tick labels
    ax.tick_params(colors=COLOR_DARK_GREY)
    for label in ax.get_yticklabels():
        label.set_color(COLOR_DARK_GREY)
    
    # Create custom legend showing the format: (round#) point value
    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0], [0], marker='^', color='w', markerfacecolor='#2E7D32', 
               markersize=12, label='Mean', markeredgecolor=COLOR_BLACK, markeredgewidth=1.5),
        Line2D([0], [0], marker='o', color='w', markerfacecolor=COLOR_UTSA_BLUE, 
               markersize=12, label='(round#), score', markeredgecolor=COLOR_DARK_GREY, markeredgewidth=1.5)
    ]
    ax.legend(handles=legend_elements, loc='upper right', framealpha=0.9)
    
    plt.tight_layout()
    save_figure(fig, 'Execution_Efficiency_Score_Distribution.png')
    plt.close()

# ============================================================================
# FIGURE 2: Planning Efficiency Score Distribution
# ============================================================================

def create_planning_efficiency_plot():
    """Create scatter plot showing planning efficiency scores by condition"""
    setup_plot_style()
    
    fig, ax = plt.subplots(figsize=(FIGURE_WIDTH, FIGURE_HEIGHT))
    
    # Organize data by condition
    conditions = {}
    for item in planning_efficiency_scores:
        cond = item['classification']
        if cond not in conditions:
            conditions[cond] = {'rounds': [], 'scores': []}
        conditions[cond]['rounds'].append(item['round'])
        conditions[cond]['scores'].append(item['efficiency_score'])
    
    # Calculate means for each condition
    means = {cond: np.mean(data['scores']) for cond, data in conditions.items()}
    
    # Plot each condition
    x_positions = {'AI PM': 0, 'Human PM': 1, 'No PM': 2}
    
    for cond in ['AI PM', 'Human PM', 'No PM']:
        if cond in conditions:
            x_pos = x_positions[cond]
            scores = conditions[cond]['scores']
            rounds = conditions[cond]['rounds']
            
            # Plot individual points - solid color without text inside
            for i, (score, round_num) in enumerate(zip(scores, rounds)):
                ax.scatter(x_pos, score, 
                          color=CONDITION_COLORS[cond], 
                          s=200,
                          alpha=0.8,
                          edgecolors=COLOR_DARK_GREY,
                          linewidths=2,
                          zorder=3)
                
                # Add round number to LEFT in parentheses: (round#)
                ax.text(x_pos - 0.15, score, f'({round_num})', 
                       fontsize=DATA_LABEL_SIZE-2, 
                       color=COLOR_BLACK,
                       va='center',
                       ha='right',
                       fontweight='bold')
                
                # Add score value to RIGHT
                ax.text(x_pos + 0.15, score, f'{score:.0f}', 
                       fontsize=DATA_LABEL_SIZE-2, 
                       color=COLOR_BLACK,
                       va='center',
                       ha='left')
            
            # Plot mean as triangle
            ax.scatter(x_pos, means[cond], 
                      marker='^', 
                      s=200, 
                      color='#2E7D32',
                      edgecolors=COLOR_BLACK,
                      linewidths=2,
                      zorder=4,
                      label='Mean' if cond == 'AI PM' else '')
            
            ax.text(x_pos + 0.15, means[cond], f'{means[cond]:.0f}', 
                   fontsize=DATA_LABEL_SIZE-2, 
                   color=COLOR_BLACK,
                   va='center',
                   ha='left')
    
    # Formatting
    ax.set_xticks([0, 1, 2])
    ax.set_xticklabels(['AI PM', 'Human PM', 'No PM'], fontsize=AXIS_LABEL_SIZE, color=COLOR_DARK_GREY)
    ax.set_ylabel('Planning Efficiency Score', fontsize=AXIS_LABEL_SIZE, color=COLOR_DARK_GREY, fontweight='bold')
    ax.set_title('Planning Efficiency Score Distribution', 
                fontsize=TITLE_SIZE, 
                color=COLOR_BLACK, 
                fontweight='bold',
                pad=20)
    
    ax.grid(True, alpha=GRID_ALPHA, linestyle=GRID_LINESTYLE, linewidth=GRID_LINEWIDTH)
    ax.axhline(y=0, color=COLOR_DARK_GREY, linestyle='-', linewidth=1)
    
    # Set y-axis limits with more padding for labels
    ax.set_ylim(-100, 50)
    ax.set_xlim(-0.6, 2.6)
    
    # Style tick labels
    ax.tick_params(colors=COLOR_DARK_GREY)
    for label in ax.get_yticklabels():
        label.set_color(COLOR_DARK_GREY)
    
    # Create custom legend showing the format: (round#) point value
    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0], [0], marker='^', color='w', markerfacecolor='#2E7D32', 
               markersize=12, label='Mean', markeredgecolor=COLOR_BLACK, markeredgewidth=1.5),
        Line2D([0], [0], marker='o', color='w', markerfacecolor=COLOR_UTSA_BLUE, 
               markersize=12, label='(round#), score', markeredgecolor=COLOR_DARK_GREY, markeredgewidth=1.5)
    ]
    # Legend in bottom right where there's whitespace
    ax.legend(handles=legend_elements, loc='lower right', framealpha=0.9)
    
    plt.tight_layout()
    save_figure(fig, 'Planning_Efficiency_Score_Distribution.png')
    plt.close()

# ============================================================================
# FIGURE 3: Completion Time per Round
# ============================================================================

def create_completion_time_plot():
    """Create bar chart showing completion times by round and condition"""
    setup_plot_style()
    
    fig, ax = plt.subplots(figsize=(FIGURE_WIDTH, FIGURE_HEIGHT))
    
    # Organize data by round
    rounds = list(range(1, 10))
    data_by_condition = {cond: [None] * 9 for cond in ['AI PM', 'Human PM', 'No PM']}
    
    for item in completion_times:
        cond = item['classification']
        round_idx = item['round'] - 1
        data_by_condition[cond][round_idx] = item['total_completion_time_sec']
    
    # Create bar positions
    bar_width = 0.8
    x = np.arange(len(rounds))
    
    # Plot bars for each round
    for i, round_num in enumerate(rounds):
        for cond in ['AI PM', 'Human PM', 'No PM']:
            value = data_by_condition[cond][i]
            if value is not None:
                bar = ax.bar(x[i], value, bar_width, 
                           color=CONDITION_COLORS[cond],
                           edgecolor=COLOR_DARK_GREY,
                           linewidth=1)
                
                # Add value labels on top of bars
                ax.text(x[i], value + 20, str(value),
                       ha='center', va='bottom',
                       fontsize=DATA_LABEL_SIZE,
                       color=COLOR_LIGHT_GREY,
                       fontweight='bold')
    
    # Formatting
    ax.set_xlabel('Round Number', fontsize=AXIS_LABEL_SIZE, color=COLOR_DARK_GREY, fontweight='bold')
    ax.set_ylabel('Round Completion Times (s)', fontsize=AXIS_LABEL_SIZE, color=COLOR_DARK_GREY, fontweight='bold')
    ax.set_title('Completion Time per Round', 
                fontsize=TITLE_SIZE, 
                color=COLOR_BLACK,
                fontweight='bold',
                pad=20)
    
    ax.set_xticks(x)
    ax.set_xticklabels(rounds, fontsize=TICK_LABEL_SIZE, color=COLOR_DARK_GREY)
    ax.set_ylim(0, 1100)
    
    # Grid
    ax.grid(True, axis='y', alpha=GRID_ALPHA, linestyle=GRID_LINESTYLE, linewidth=GRID_LINEWIDTH)
    ax.set_axisbelow(True)
    
    # Style tick labels
    ax.tick_params(colors=COLOR_DARK_GREY)
    for label in ax.get_yticklabels():
        label.set_color(COLOR_DARK_GREY)
    
    # Create custom legend
    from matplotlib.patches import Rectangle
    legend_elements = [
        Rectangle((0, 0), 1, 1, fc=COLOR_YELLOW, edgecolor=COLOR_DARK_GREY, label='No PM'),
        Rectangle((0, 0), 1, 1, fc=COLOR_UTSA_ORANGE, edgecolor=COLOR_DARK_GREY, label='Human PM'),
        Rectangle((0, 0), 1, 1, fc=COLOR_UTSA_BLUE, edgecolor=COLOR_DARK_GREY, label='AI PM')
    ]
    ax.legend(handles=legend_elements, loc='upper right', framealpha=0.9, fontsize=LEGEND_SIZE)
    
    plt.tight_layout()
    save_figure(fig, 'Completion_Time_per_Round.png')
    plt.close()

# ============================================================================
# FIGURE 3: Post-Round Survey Results
# ============================================================================

def create_survey_results_plot():
    """Create horizontal bar chart showing survey ratings by round"""
    setup_plot_style()
    
    fig, ax = plt.subplots(figsize=(FIGURE_WIDTH, FIGURE_HEIGHT))
    
    # Organize data
    rounds = list(range(1, 10))
    structure_difficulty = []
    plan_rating = []
    conditions = []
    
    for item in avg_round_ratings:
        structure_difficulty.append(item['avg_structure_difficulty'])
        plan_rating.append(item['avg_plan_rating'])
        conditions.append(item['classification'])
    
    # Create bar positions
    y = np.arange(len(rounds))
    bar_height = 0.35
    
    # Plot horizontal bars using UTSA colors
    bars1 = ax.barh(y - bar_height/2, structure_difficulty, bar_height,
                    label='Avg Structure Difficulty Rating',
                    color=COLOR_UTSA_ORANGE,  # Changed to UTSA orange
                    edgecolor=COLOR_DARK_GREY,
                    linewidth=1)
    
    bars2 = ax.barh(y + bar_height/2, plan_rating, bar_height,
                    label='Avg Plan Rating',
                    color=COLOR_UTSA_BLUE,  # Changed to UTSA blue
                    edgecolor=COLOR_DARK_GREY,
                    linewidth=1)
    
    # Create y-axis labels with round number and classification
    y_labels = [f"{round_num} ({cond})" for round_num, cond in zip(rounds, conditions)]
    
    # Formatting
    ax.set_yticks(y)
    ax.set_yticklabels(y_labels, fontsize=TICK_LABEL_SIZE, color=COLOR_DARK_GREY)
    ax.set_ylabel('Round Number', fontsize=AXIS_LABEL_SIZE, color=COLOR_DARK_GREY, fontweight='bold')
    ax.set_xlabel('Rating', fontsize=AXIS_LABEL_SIZE, color=COLOR_DARK_GREY, fontweight='bold')
    ax.set_title('Post-Round Survey Results', 
                fontsize=TITLE_SIZE, 
                color=COLOR_BLACK,
                fontweight='bold',
                pad=20)
    
    ax.set_xlim(0, 7)
    
    # Grid
    ax.grid(True, axis='x', alpha=GRID_ALPHA, linestyle=GRID_LINESTYLE, linewidth=GRID_LINEWIDTH)
    ax.set_axisbelow(True)
    
    # Style tick labels
    ax.tick_params(colors=COLOR_DARK_GREY)
    for label in ax.get_xticklabels():
        label.set_color(COLOR_DARK_GREY)
    
    # Legend - moved to bottom right to avoid covering chart data
    ax.legend(loc='best', bbox_to_anchor=(0.5, 0., 0.5, 0.5), framealpha=0.5, fontsize=LEGEND_SIZE)
    
    plt.tight_layout()
    save_figure(fig, 'Post-Round_Survey_Results.png')
    plt.close()

# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    print("Generating figures at 300 DPI...")
    print(f"Using font: {FONT_FAMILY}")
    print("-" * 60)
    
    create_execution_efficiency_plot()
    create_planning_efficiency_plot()
    create_completion_time_plot()
    create_survey_results_plot()
    
    print("-" * 60)
    print("All figures generated successfully!")