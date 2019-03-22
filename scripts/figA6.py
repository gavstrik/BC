import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams["font.family"] = "sans-serif"
PLOTS_DIR = '../plots'

"""
Guess dynamics of player guesses from randomly selected
groups.
"""

datafile_AMT = pd.read_csv('../data/amt.csv')
np.random.seed(0)

def plot_trajectories(df_AMT):
    fig, axes = plt.subplots(nrows=4, ncols=3, sharex=True, sharey=True,
                             figsize=(10,10))
    axes = axes.flatten()
    bins = np.linspace(-0.5, 100.5, 102)
    colors = ['#4575b4', 'orange', 'red']
    df_2 = df_AMT[df_AMT['name'] == 'GoR_'+str(2)]
    df_4 = df_AMT[df_AMT['name'] == 'GoR_'+str(4)]
    df_8 = df_AMT[df_AMT['name'] == 'GoR_'+str(8)]
    example_groups_2 = np.random.choice(df_2.group.unique(),4, replace=False)
    example_groups_4 = np.random.choice(df_4.group.unique(),4, replace=False)
    example_groups_8 = np.random.choice(df_8.group.unique(),4, replace=False)
    example_groups = []
    for i in range(4):
        example_groups.append(example_groups_2[i])
        example_groups.append(example_groups_4[i])
        example_groups.append(example_groups_8[i])

    for i, group in enumerate(example_groups):
        df = df_AMT[df_AMT.group == group]
        players = len(df.id_in_group.unique())
        for player in range(1,players+1):
            data = df[df.id_in_group == player].guess.values
            axes[i].plot(data, label='group '+str(group))
            # axes[i].annotate("group "+str(group),
            #              xy=(0.2, 0.92), xycoords='axes fraction', fontsize=11,
            #              horizontalalignment='left', verticalalignment='top')

    # plotting paraphernalia
    axes[0].set_title('2 players', fontsize='large')
    axes[1].set_title('4 players', fontsize='large')
    axes[2].set_title('8 players', fontsize='large')
    plt.setp(axes, xticks=[i for i in range(8)], xticklabels=[i+1 for i in range(8)])
    axes[9].set_xlabel('round'), axes[10].set_xlabel('round'), axes[11].set_xlabel('round')
    fig.tight_layout()

    # Remember: save as pdf and transparent=True for Adobe Illustrator
    if not os.path.exists(PLOTS_DIR):
        os.makedirs(PLOTS_DIR)

    plt.savefig(os.path.join(PLOTS_DIR, 'figA6.png'), transparent=True, dpi=300)
    plt.savefig(os.path.join(PLOTS_DIR, 'figA6.pdf'), transparent=True, dpi=300)

    plt.show()


# main code
df_AMT = pd.DataFrame(datafile_AMT)
plot_trajectories(df_AMT)
