import os
import numpy as np
import pandas as pd
from scipy.stats import ks_2samp, mannwhitneyu
import matplotlib.pyplot as plt
plt.rcParams["font.family"] = "sans-serif"
PLOTS_DIR = '../plots'

"""
plot means over all rounds.
"""

AMTdata = pd.read_csv('../data/amt.csv')
Nagel95 = pd.read_csv('../data/Nagel95.csv')

def plot_round_by_round_means(df_all, Nagel_avgs):
    colors = ['#74add1', '#4575b4', '#313695', '#fc9272', '#fb6a4a', '#ef3b2c', '#cb181d', '#a50f15', '#67000d']
    treatments = [[1,1]]
    for position, treat in enumerate(treatments):
        group_sizes = [2, 4, 8]
        df_means = pd.DataFrame()
        m = []
        lg = []
        control = []
        for g in group_sizes:
            number_of_players = len(df[df.name == 'GoR_'+str(g)]['group'].unique())*g
            RoD = 0
            for r in range(1,9):
                if g == 2:
                    control = df[(df.name == 'GoR_'+str(g)) & (df['round'] == r)]['guess'].values
                new = df[(df.name == 'GoR_'+str(g)) & (df['round'] == r)]['guess'].values
                # print(g, r, 'Kolmogorov-Smirnov test:', ks_2samp(new, control)[1])
                # print(g, r, 'Man_Whitney U test:', mannwhitneyu(new, control)[1])
                # print('number of players chosing zero = ', len([1 for i in new if i == 0]), 'out of', len(new))
                if r > 1 and r < 5:
                    RoD += (df[(df.name == 'GoR_'+str(g)) & (df['round'] == r-1)]['guess'].mean()
                            - df[(df.name == 'GoR_'+str(g)) & (df['round'] == r)]['guess'].mean())/df[(df.name == 'GoR_'+str(g)) & (df['round'] == r-1)]['guess'].mean()
                m.append(df[(df.name == 'GoR_'+str(g)) & (df['round'] == r)]['guess'].mean())
            print('Average rate of decrease per round for AMT (only counting the first 4 rounds),', g, 'player groups:', RoD/3)
            print('Rate of decrease for AMT from round 1 to round 4,', g, 'player groups:', (df[(df.name == 'GoR_'+str(g)) & (df['round'] == 1)]['guess'].mean()
                    - df[(df.name == 'GoR_'+str(g)) & (df['round'] == 4)]['guess'].mean())/df[(df.name == 'GoR_'+str(g)) & (df['round'] == 1)]['guess'].mean())
            df_means[g] = m
            m[:] = []
            lg.append('AMT (n=' + str(g) + ', N=' + str(number_of_players) + ')')
        df_means['round'] = [1,2,3,4,5,6,7,8]
        df_means.set_index('round', inplace=True)
        df_means.plot(marker='o', kind='line', color=colors, fontsize=9) # , legend=False)
        print('AMT means:', df_means)

    # plot the data from Nagel 1995
    RoD = 0
    for pos, n in enumerate(Nagel_avgs):
        if pos > 0:
            RoD += (Nagel_avgs[pos-1] - Nagel_avgs[pos])/Nagel_avgs[pos-1]
    print('Nagel average rate of decrease per round:', RoD/3)
    print('Nagel rate of decrease from round 1 to round 4:', (Nagel_avgs[0] - Nagel_avgs[3])/Nagel_avgs[0])
    plt.plot([1,2,3,4], Nagel_avgs, marker='s', linestyle='-', color=colors[3])
    lg.append('N95 (students, n=15, N=64)')

    # plot the data from Kamm & Dahinden, 2008, taken from Diekmann 2009, table 1
    # using only the experiments with "full information":
    plt.plot([1,2,3,4,5],[35.3, 21.5, 17.1, 14.0, 13.4], 'x', linestyle='-', color=colors[4])
    lg.append('KD08 (students, N=14)')
    plt.plot([1,2,3,4,5],[35.7, 25.1, 15.9, 12.2, 12.9], 'x', linestyle='-', color=colors[5])
    lg.append('KD08 (students, N=50)')
    plt.plot([1,2,3,4,5],[30.0, 21.9, 15.7, 13.6, 10.8], 'x', linestyle='-', color=colors[6])
    lg.append('KD08 (students, N=188)')
    print('KD rate of decrease from round 1 to round 4:', (35.3-14)/35.3, (35.7-12.2)/35.7, (30-13.6)/30)

    # plot the data from Grosskopf & Nagel 2008
    #plt.plot(1,35.57,'^', color=colors[7])
    #lg.append('GN08 (students, n=2, N=132)')
    #plt.plot(1,21.73,'v', color=colors[7])
    #lg.append('GN08 (professionals, n=2, N=130)')

    # plot the data from Rubinstein 2007, page 1250
    #plt.plot(1,36.2,'<', color=colors[8])
    #lg.append('R07 (students, n=40-90, N=2423)')

    # plot the data from Bühren & Frank 2010:
    plt.plot([1, 2] ,[32.15, 25.7],'<', linestyle='-', color=colors[8])
    lg.append('BF10 (chess players, n=13-897, N=2481)')

    # plot the data from Weber (2003):
    plt.plot([1,2,3,4,5,6,7,8,9,10] ,[24.6, 16.4, 6.7, 6.2, 12.1, 5.4, 9.6, 11.2, 8.4, 6.5],'<', linestyle='-', color=colors[7])
    lg.append('W03 (students, n=8-10, N=26)')
    print('W03 rate of decrease from round 1 to round 4:', (24.6-6.2)/24.6)

    # general plot paraphernalia
    plt.xlim(.7, 10.3)
    plt.ylim(-2, 59)
    plt.legend(lg, loc='upper right', ncol=2, fancybox=True, fontsize=7)
    plt.ylabel('average')
    plt.tight_layout()

    # Remember: save as pdf and transparent=True for Adobe Illustrator
    if not os.path.exists(PLOTS_DIR):
        os.makedirs(PLOTS_DIR)

    plt.savefig(os.path.join(PLOTS_DIR, 'fig3.png'), transparent=True, dpi=300)
    plt.savefig(os.path.join(PLOTS_DIR, 'fig3.pdf'), transparent=True, dpi=300)

    plt.show()


# main code
df = pd.DataFrame(AMTdata)
df_95 = pd.DataFrame(Nagel95)
Nagel_avgs = [df_95['round 1'].mean(), df_95['round 2'].mean(), df_95['round 3'].mean(), df_95['round 4'].mean()]
print(Nagel_avgs)
plot_round_by_round_means(df, Nagel_avgs)
