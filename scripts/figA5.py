import os
import numpy as np
import pandas as pd
from scipy.stats import mode, ks_2samp, mannwhitneyu, shapiro, pearsonr
import matplotlib.pyplot as plt
plt.rcParams["font.family"] = "sans-serif"
PLOTS_DIR = '../plots'

"""
histograms of guess distributions partitioned into groups and rounds.
"""

datafile_AMT = pd.read_csv('../data/amt.csv')


def most_common_numbers(array):
    first = mode(array)[0][0]
    array = array[array != first]
    second = mode(array)[0][0]
    array = array[array != second]
    third = mode(array)[0][0]
    array = array[array != third]
    fourth = mode(array)[0][0]
    array = array[array != fourth]
    fifth = mode(array)[0][0]
    return first, second, third, fourth, fifth


def plot_histograms(df_AMT):
    fig, axes = plt.subplots(nrows=4, ncols=2, sharex=True, sharey=True,
                             figsize=(8,8))
    axes = axes.flatten()
    bins = np.linspace(-0.5, 100.5, 102)
    colors = ['#4575b4', 'orange', 'red']
    df_2 = df_AMT[df_AMT['name'] == 'GoR_'+str(2)]
    df_4 = df_AMT[df_AMT['name'] == 'GoR_'+str(4)]
    df_8 = df_AMT[df_AMT['name'] == 'GoR_'+str(8)]

    for i in range(1,len(axes)+1):
        data = df_AMT[df_AMT['round'] == i].guess.values.astype(int)
        data_2 = df_2[df_2['round'] == i].guess.values.astype(int)
        data_4 = df_4[df_4['round'] == i].guess.values.astype(int)
        data_8 = df_8[df_8['round'] == i].guess.values.astype(int)
        axes[i-1].hist([data_2, data_4, data_8],
                 stacked=True, density=True, color=colors, bins=bins,
                 label=['2 players', '4 players', '8 players'])
        # axes[i-1].hist(data, bins=bins, density=True, color=colors[0])
        axes[i-1].set_title('round '+str(i), fontsize='smaller')
        avg = np.around(np.mean(data),2)
        first, second, third, fourth, fifth = most_common_numbers(data)
        N = len(data)
        axes[i-1].annotate("mean = "+str(avg)+'\nmode = '+str(first),
                     xy=(0.7, 0.9), xycoords='axes fraction', fontsize=7,
                     horizontalalignment='left', verticalalignment='top')

    # plotting paraphernalia
    # Set the ticks and ticklabels for all axes
    plt.setp(axes, xticks=[0, 22, 33, 50, 100], xticklabels=[0, 22, 33, 50, 100])
    for ax in axes:
        ax.set_xticklabels([0, 22, 33, 50, 100], fontsize='x-small')
        ax.set_yticklabels([0,0.1,0.2], fontsize='x-small')
        ax.legend(fontsize='x-small', loc='upper left')
    fig.tight_layout()

    # Remember: save as pdf and transparent=True for Adobe Illustrator
    if not os.path.exists(PLOTS_DIR):
        os.makedirs(PLOTS_DIR)

    plt.savefig(os.path.join(PLOTS_DIR, 'figA5.png'), transparent=True, dpi=300)
    plt.savefig(os.path.join(PLOTS_DIR, 'figA5.pdf'), transparent=True, dpi=300)

    plt.show()


# main code
df_AMT = pd.DataFrame(datafile_AMT)

plot_histograms(df_AMT)
