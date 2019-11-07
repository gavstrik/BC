import os
import numpy as np
import pandas as pd
from scipy.stats import mode, ks_2samp, mannwhitneyu, shapiro, pearsonr, kstest
import matplotlib.pyplot as plt
from matplotlib import style
import matplotlib.mlab as mlab
from statsmodels.graphics.gofplots import qqplot
from tabulate import tabulate
import random
from collections import Counter
plt.rcParams["font.family"] = "sans-serif"
PLOTS_DIR = '../plots'

"""
Comparing Nagel data with ours. Only one round data.
"""

datafile_AMT = pd.read_csv('../data/amt.csv')
datafile_1995 = pd.read_csv('../data/Nagel95.csv')
datafile_2002 = pd.read_csv('../data/Nagel02.csv')


def KS_test(new, control):
    return ks_2samp(new, control)[1]


def three_most_common_numbers(array):
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


def plot_comparisons(df_1995, df_2002, df_AMT):
    fig, axes = plt.subplots(nrows=4, ncols=2, sharex=True, sharey=True)
    axes = axes.flatten()
    bins = np.linspace(-0.5, 100.5, 102)
    control = df_AMT.guess.values

    # 1. Lab Experiments (1-5)
    df_1 = df_2002[(df_2002['session'] == 1) |
                 (df_2002['session'] == 2) |
                 (df_2002['session'] == 3) |
                 (df_2002['session'] == 4) |
                 (df_2002['session'] == 5)]
    data = df_1.guess.values.astype(int)
    ax0 = axes[0].hist(data, bins=bins, density=True)
    axes[0].set_title('1. Lab Experiments (1-5)', fontsize='smaller')
    print('\t Lab Experiments (1-5) Shapiro_Wilk normality test, p-value:', shapiro(df_1.guess.values)[1])
    avg = np.around(np.mean(df_1.guess.values),2)
    first, second, third, fourth, fifth = three_most_common_numbers(data)
    # print('\nmodes:', first, second, third, fourth, fifth)
    # print('df1', Counter(data))
    N = len(df_1.guess.values)
    axes[0].annotate("mean = "+str(avg)+'\nmode = '+str(first)+'\nN = '+str(N),
                     xy=(0.7, 0.9), xycoords='axes fraction', fontsize=7,
                     horizontalalignment='left', verticalalignment='top')
    # plt.sca(axes[0])
    # plt.xticks([0, second, third, 100], [0, int(second), int(third), 100], fontsize='x-small')
    # plt.yticks([0,.05,.1,.15], [0,.05,.1,.15], fontsize='x-small')


    # 2. Classroom Experiments (6,7)
    df_2 = df_2002[(df_2002['session'] == 6) |
                 (df_2002['session'] == 7)]
    data = df_2.guess.values.astype(int)
    # weights=np.ones(len(df_2.guess.values))/len(df_2.guess.values)
    ax1 = axes[1].hist(data, bins=bins, density=True) # weights=weights
    axes[1].set_title('2. Classroom Experiments (6,7)', fontsize='smaller')
    avg = np.around(np.mean(df_2.guess.values),2)
    first, second, third, fourth, fifth = three_most_common_numbers(data)
    N = len(df_2.guess.values)
    axes[1].annotate("mean = "+str(avg)+'\nmode = '+str(first)+', '+str(second)+'\nN = '+str(N),
                     xy=(0.7, 0.9), xycoords='axes fraction', fontsize=7,
                     horizontalalignment='left', verticalalignment='top')

    # 3. Take Home Experiments (8,9)
    df_3 = df_2002[(df_2002['session'] == 8) |
                 (df_2002['session'] == 9)]
    data = df_3.guess.values.astype(int)
    # weights = np.ones(len(df_3.guess.values))/len(df_3.guess.values)
    ax2 = axes[2].hist(data, bins=bins, density=True)
    axes[2].set_title('3. Take Home Experiments (8,9)', fontsize='smaller')
    avg = np.around(np.mean(df_3.guess.values),2)
    first, second, third, fourth, fifth = three_most_common_numbers(data)
    N = len(df_3.guess.values)
    axes[2].annotate("mean = "+str(avg)+'\nmode = '+str(first)+'\nN = '+str(N),
                     xy=(0.7, 0.9), xycoords='axes fraction', fontsize=7,
                     horizontalalignment='left', verticalalignment='top')

    # 4. Theorists Experiments (10-13)
    df_4 = df_2002[(df_2002['session'] == 10) |
                 (df_2002['session'] == 11) |
                 (df_2002['session'] == 12) |
                 (df_2002['session'] == 13)]
    data = df_4.guess.values.astype(int)
    ax3 = axes[3].hist(data, bins=bins, density=True)
    axes[3].set_title('4. Theorists Experiments (10-13)', fontsize='smaller')
    avg = np.around(np.mean(df_4.guess.values),2)
    first, second, third, fourth, fifth = three_most_common_numbers(data)
    N = len(data)
    axes[3].annotate("mean = "+str(avg)+'\nmode = '+str(first)+'\nN = '+str(N),
                     xy=(0.7, 0.9), xycoords='axes fraction', fontsize=7,
                     horizontalalignment='left', verticalalignment='top')

    # 5. Internet Newsgroup Experiment (14)
    df_5 = df_2002[df_2002['session'] == 14]
    data = df_5.guess.values.astype(int)
    ax4 = axes[4].hist(data, bins=bins, density=True)
    axes[4].set_title('5. Internet Newsgroup Experiment (14)', fontsize='smaller')
    avg = np.around(np.mean(df_5.guess.values),2)
    first, second, third, fourth, fifth = three_most_common_numbers(data)
    N = len(data)
    axes[4].annotate("mean = "+str(avg)+'\nmode = '+str(first)+'\nN = '+str(N),
                     xy=(0.7, 0.9), xycoords='axes fraction', fontsize=7,
                     horizontalalignment='left', verticalalignment='top')

    # 6. Newspaper Experiments (15-17)
    df_6 = df_2002[(df_2002['session'] == 15) |
                 (df_2002['session'] == 16) |
                 (df_2002['session'] == 17)]
    df_15 = df_6[df_6['session'] == 15]
    print('Spektrum der Wissenschaft:', np.mean(df_15.guess.values), np.mean(df_15.guess.values)*2/3)
    df_16 = df_6[df_6['session'] == 16]
    print('Expansion:', np.mean(df_16.guess.values), np.mean(df_16.guess.values)*2/3)
    df_17 = df_6[df_6['session'] == 17]
    print('Financial Times:', np.mean(df_17.guess.values), np.mean(df_17.guess.values)*2/3)
    data = df_6.guess.values.astype(int)
    ax5 = axes[5].hist(data, bins=bins, density=True)
    axes[5].set_title('6. Newspaper Experiments (15-17)', fontsize='smaller')
    avg = np.around(np.mean(df_6.guess.values),2)
    first, second, third, fourth, fifth = three_most_common_numbers(data)
    N = len(data)
    axes[5].annotate("mean = "+str(avg)+'\nmode = '+str(first)+'\nN = '+str(N),
                     xy=(0.7, 0.9), xycoords='axes fraction', fontsize=7,
                     horizontalalignment='left', verticalalignment='top')

    # 7. Nagel 1995 Experiments (18-22)
    df_7 = df_1995
    data = df_7.guess.values.astype(int)
    ax6 = axes[6].hist(data, bins=bins, density=True)
    axes[6].set_title('7. Nagel 1995 Experiments (18-22)', fontsize='smaller')
    avg = np.around(np.mean(df_7.guess.values),2)
    # print(avg)
    first, second, third, fourth, fifth = three_most_common_numbers(data)
    N = len(data)
    axes[6].annotate("mean = "+str(avg)+'\nmode = '+str(first)+'\nN = '+str(N),
                     xy=(0.7, 0.9), xycoords='axes fraction', fontsize=7,
                     horizontalalignment='left', verticalalignment='top')

    # 8. AMT Experiments (23-109)
    df_8 = df_AMT
    print('\t AMT Experiments (23-109) Shapiro_Wilk normality test, p-value:', shapiro(df_8.guess.values)[1])
    print('\t AMT Experiments (23-109) KS-test onesided:', kstest(df_8.guess.values,'norm', alternative = 'less'))
    print('\t AMT Experiments (23-109) KS-test onesided:', kstest(df_8.guess.values,'norm', alternative = 'greater'))
    print('\t AMT Experiments (23-109) KS-test onesided:', kstest(df_8.guess.values,'norm', mode='asymp'))
    data = df_8.guess.values.astype(int)
    ax7 = axes[7].hist(data, bins=bins, density=True)
    axes[7].set_title('8. AMT Experiments (23-109)', fontsize='smaller')
    avg = np.around(np.mean(df_8.guess.values),2)
    first, second, third, fourth, fifth = three_most_common_numbers(data)
    N = len(data)
    axes[7].annotate("mean = "+str(avg)+'\nmode = '+str(first)+'\nN = '+str(N),
                     xy=(0.7, 0.9), xycoords='axes fraction', fontsize=7,
                     horizontalalignment='left', verticalalignment='top')

    # plotting paraphernalia
    # Set the ticks and ticklabels for all axes
    plt.setp(axes, xticks=[0, 22, 33, 50, 100], xticklabels=[0, 22, 33, 50, 100],
                   yticks=[0,0.1,0.2])
    for ax in axes:
        ax.set_xticklabels([0, 22, 33, 50, 100], fontsize='x-small')
        ax.set_yticklabels([0,0.1,0.2], fontsize='x-small')
    fig.tight_layout()

    # Remember: save as pdf and transparent=True for Adobe Illustrator
    if not os.path.exists(PLOTS_DIR):
        os.makedirs(PLOTS_DIR)

    plt.savefig(os.path.join(PLOTS_DIR, 'fig1.png'), transparent=True, dpi=300)
    plt.savefig(os.path.join(PLOTS_DIR, 'fig1.pdf'), transparent=True, dpi=300)

    plt.show()

    # print(df_7.guess.values)
    # print(random.sample(list(df_7.guess.values), 67))
    corr, _ = pearsonr(random.sample(list(df_7.guess.values), 67), df_7.guess.values)
    # print('Pearsons correlation btw 1 and 7: %.3f' % corr)

    return df_1.guess.values, df_2.guess.values, df_3.guess.values, df_4.guess.values, df_5.guess.values, df_6.guess.values, df_7.guess.values, df_8.guess.values


def plot_QQplots(guess_arrays):
    fig, axes = plt.subplots(nrows=4, ncols=2)
    axes = axes.flatten()
    for pos, i in enumerate(guess_arrays):
        qqplot(i, fit=True, line='s', ax=axes[pos])
        # axes[pos].legend([i+1 for i in range(8)])
    plt.legend()
    plt.show()


def plot_cdfs(guess_arrays):
    labls = ['Lab Experiments (1-5)', 'Classroom (6,7)', 'Take Home (8,9)',
             'Theorists (10-13)', 'Newsgroup (14)', 'Newspapers (15-17)',
             'Nagel 1995 (18-22)', 'AMT (23-109)']
    for pos, i in enumerate(guess_arrays):
        sortedguesses = np.sort(i)
        p = 1. * np.arange(len(i))/(len(i) - 1)
        plt.plot(sortedguesses, p, label=labls[pos])
    plt.legend()
    plt.tight_layout()

    # Remember: save as pdf and transparent=True for Adobe Illustrator
    if not os.path.exists(PLOTS_DIR):
        os.makedirs(PLOTS_DIR)

    plt.savefig(os.path.join(PLOTS_DIR, 'fig2.png'), transparent=True, dpi=300)
    plt.savefig(os.path.join(PLOTS_DIR, 'fig2.pdf'), transparent=True, dpi=300)
    plt.show()


def make_table(dfs):
    df_table = pd.DataFrame()

    row1 = []
    row2 = []
    row3 = []
    row4 = []
    row5 = []
    row6 = []
    row7 = []
    row8 = []
    for y in dfs:
        row1.append(ks_2samp(dfs[0], y)[1])
        row2.append(ks_2samp(dfs[1], y)[1])
        row3.append(ks_2samp(dfs[2], y)[1])
        row4.append(ks_2samp(dfs[3], y)[1])
        row5.append(ks_2samp(dfs[4], y)[1])
        row6.append(ks_2samp(dfs[5], y)[1])
        row7.append(ks_2samp(dfs[6], y)[1])
        row8.append(ks_2samp(dfs[7], y)[1])
    df_table['1'] = row1
    df_table['2'] = row2
    df_table['3'] = row3
    df_table['4'] = row4
    df_table['5'] = row5
    df_table['6'] = row6
    df_table['7'] = row7
    df_table['8'] = row8

    print('Kolmogorov-Smirnov tests:')
    print(tabulate(df_table, tablefmt="pipe", headers="keys", showindex=False))


# main code
df_1995 = pd.DataFrame(datafile_1995)
df_2002 = pd.DataFrame(datafile_2002)
df_AMT = pd.DataFrame(datafile_AMT)

# formate dataframes:
df_1995 = df_1995[['session', 'round 1']]
df_1995.columns = ['session', 'guess']
df_2002 = df_2002.dropna()
df_AMT = df_AMT[df_AMT['round'] == 1]
df_AMT = df_AMT[['group', 'guess']]
df_AMT.columns = ['session', 'guess']

# make a new dataframe for all:
df_all = pd.DataFrame()
df_all = df_all.append(df_1995, sort=True)
df_all = df_all.append(df_2002, sort=True)
df_all = df_all.append(df_AMT, sort=True)

dfs = plot_comparisons(df_1995, df_2002, df_AMT)
make_table(dfs)
plot_cdfs(dfs)
# plot_QQplots(dfs)
