import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import math


def plot_grouped_distances(mean_distances, median_distances):

    # men_means = (20, 35, 30, 35, 27)
    # women_means = (25, 32, 34, 20, 25)

    men_means = mean_distances
    women_means = median_distances

    below_threshold = min(mean_distances + median_distances)

    ind = np.arange(len(men_means))  # the x locations for the groups
    width = 0.35  # the width of the bars

    fig, ax = plt.subplots()
    ax.bar(ind - width / 2, men_means, width,
                    label='Mean digits')

    ax.bar(ind + width / 2, women_means, width,
                    label='Median Digits')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Distances')
    ax.set_xlabel('Digits')
    ax.set_title('Distance between drawn digit and meta digits')
    ax.set_xticks(ind)
    ax.set_xticklabels(get_x_ticks_label())

    axes = plt.gca()
    axes.set_ylim([below_threshold-math.sqrt(below_threshold), None])

    ax.legend()
    ax.plot([-0.5, 9.5], [below_threshold, below_threshold], "k--")
    fig.tight_layout()

    plt.show()


def get_x_ticks_label():
    labels = list()
    for i in range(10):
        labels.append(i)
    return labels

if __name__ == '__main__':
    plot_grouped_distances([20, 35, 30, 35, 27], [25, 32, 34, 20, 25])