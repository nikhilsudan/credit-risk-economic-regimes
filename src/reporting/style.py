import matplotlib.pyplot as plt
import seaborn as sns


def set_plot_style():
    """
    Set consistent, publication-quality plotting style.
    """
    sns.set_theme(style="whitegrid")
    plt.rcParams.update({
        "figure.figsize": (8, 5),
        "figure.dpi": 120,
        "font.size": 12,
        "axes.titlesize": 14,
        "axes.labelsize": 12,
        "legend.fontsize": 11,
        "xtick.labelsize": 11,
        "ytick.labelsize": 11,
        "axes.spines.top": False,
        "axes.spines.right": False,
    })
