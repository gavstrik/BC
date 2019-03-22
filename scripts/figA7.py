import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
style.use('ggplot')
import seaborn as sns
sns.set()
from textwrap import fill
plt.rcParams["font.family"] = "sans-serif"
PLOTS_DIR = '../plots'

"""
Dynamics of guesses round by round.
"""

datafile = pd.read_csv('../data/amt.csv')

# specifying treatment and group size:
treatment = (1,1)
# players_in_group = 8
number_of_plots = 3

def player_comments(df, groups):
    fig, axes = plt.subplots(nrows=number_of_plots, ncols=1,
                             sharex=True, sharey=True, figsize=(7,10))
    axes = axes.flatten()
    fig.subplots_adjust(bottom = -1)  # removes error messages when using tigth_layout
    color_dots = sns.color_palette('Set1', 2)

    for i in range(number_of_plots):
        axes[i].grid(False)

    for position, g in enumerate(groups):
        df1 = df[(df['name'] == 'GoR_'+str(g[0])) & (df['group'] == g[1])]
        players_in_group = g[0]

        # plot a diagonal line
        axes[position].plot([0, 100], [0, 100], 'k-', linewidth=1)

        # scatter plot of all guess-pairs for round r and r+1:
        for round in range(1, 8):
            r = df1[df1['round'] == round]['guess'].values
            r_1 = df1[df1['round'] == round + 1]['guess'].values
            if position == 0:
                if round == 1:
                    axes[position].scatter(r, r_1, s=14, color=color_dots[0], label=str(round)+'.-'+str(round+1)+'. round')
                elif round == 2:
                    axes[position].scatter(r, r_1, s=14, color='black', label=str(round)+'.-'+str(round+5)+'. round')
                elif round == 7:
                    axes[position].scatter(r, r_1, s=14, color=color_dots[1], label=str(round)+'.-'+str(round+1)+'. round')
                else:
                    axes[position].scatter(r, r_1, s=14, color='black') #, label=str(round)+'.-'+str(round+1)+'. round')
            else:
                if round == 1:
                    axes[position].scatter(r, r_1, s=14, color=color_dots[0])
                elif round == 2:
                    axes[position].scatter(r, r_1, s=14, color='black')
                elif round == 7:
                    axes[position].scatter(r, r_1, s=14, color=color_dots[1])
                else:
                    axes[position].scatter(r, r_1, s=14, color='black')
        player = []
        p_tup = []
        comments = []
        payoff = []
        for play in range(players_in_group):
            colors = sns.color_palette('Set1', players_in_group)
            player.append(df1[df1['id_in_group'] == (play + 1)]['guess'].values)
            comments.append(df1[(df1['id_in_group'] == (play + 1)) & (df1['round'] == 8)]['strategy'].item())
            payoff.append(df1[(df1['id_in_group'] == (play + 1)) & (df1['round'] == 8)]['payoff'].item())
            p_tup.append([(g, player[play][pos+1]) for pos, g in enumerate(player[play][:len(player[play])-1])])
        for t in range(len(p_tup[0])-1):
            pl = ['"'+str(fill(comments[p], 45))+'" ($'+str(payoff[p])+')' for p in range(players_in_group)]
            for j in range(players_in_group):
                if t == 0:
                    axes[position].plot(p_tup[j][t], p_tup[j][t+1], linewidth=1, c=colors[j], label=pl[j])
                else:
                    axes[position].plot(p_tup[j][t], p_tup[j][t+1], linewidth=1, c=colors[j])

        # plotting paraphernalia
        lgd = axes[position].legend(title='Group '+str(g[1])+' ('+str(g[0])+' players)', fontsize='x-small', bbox_to_anchor=(1.1, 1.05))

    plt.tight_layout()

    # Remember: save as pdf and transparent=True for Adobe Illustrator
    if not os.path.exists(PLOTS_DIR):
        os.makedirs(PLOTS_DIR)

    plt.savefig(os.path.join(PLOTS_DIR, 'figA7.png'), bbox_extra_artists=(lgd,),
                bbox_inches='tight', transparent=True, dpi=300)
    plt.savefig(os.path.join(PLOTS_DIR, 'figA7.pdf'), bbox_extra_artists=(lgd,),
                bbox_inches='tight', transparent=True, dpi=300)

    plt.show()

# main
df = pd.DataFrame(datafile)
groups = [(2,351), (4,250), (8,67)]  # selected games
player_comments(df, groups)
