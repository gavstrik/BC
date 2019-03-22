import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
plt.rcParams["font.family"] = "sans-serif"
PLOTS_DIR = '../plots'

"""
plotting the fraction of players making guesses above 2/3rds of the
previous mean.
"""

AMTdata = pd.read_csv('../data/amt.csv')
Nagel95 = pd.read_csv('../data/Nagel95.csv')

bonus = 13  # this is the bonus in $ payed by Nagel for the winner(s)


def reformat_Nagel95_data(df):
    df_1 = df[['session', 'id', 'round 1']]
    df_2 = df[['session', 'id', 'round 2']]
    df_3 = df[['session', 'id', 'round 3']]
    df_4 = df[['session', 'id', 'round 4']]
    df_1.columns = ['group', 'id_in_group', 'guess']
    df_2.columns = ['group', 'id_in_group', 'guess']
    df_3.columns = ['group', 'id_in_group', 'guess']
    df_4.columns = ['group', 'id_in_group', 'guess']
    df_1['round'] = [1 for i in range(len(df_1.index))]
    df_2['round'] = [2 for i in range(len(df_2.index))]
    df_3['round'] = [3 for i in range(len(df_3.index))]
    df_4['round'] = [4 for i in range(len(df_4.index))]
    df_new = pd.DataFrame()
    df_new = df_new.append(df_1)
    df_new = df_new.append(df_2)
    df_new = df_new.append(df_3)
    df_new = df_new.append(df_4)
    return df_new


def find_payoff(df_group, id):
    payoff = []
    ids = df_group['id_in_group'].unique()
    for r in range(1,5):
        guesses = df_group[df_group['round'] == r]['guess'].values
        tt = (2/3) * np.mean(guesses)
        best_guess = find_nearest(guesses, tt)
        winners = [p for pos, p in enumerate(ids)
                   if abs(guesses[pos] - tt) == abs(best_guess - tt)]
        if id in winners:
            payoff.append(bonus/len(winners))
    return np.sum(payoff)


def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]


def make_barplot(strategies_AMT, strategies_95):
    fig, axes = plt.subplots(nrows=1, ncols=2, sharex=True, sharey=True, figsize=(6,4))
    at_AMT, payoff_AMT = zip(*strategies_AMT)
    at_95, payoff_95 = zip(*strategies_95)
    colors = ['#4575b4', '#e74c3c']

    # calculate the average bonus for each "strategy"-bin
    avg_payoff_AMT = []
    avg_payoff_95 = []
    for l in range(8):
        if l in at_AMT:
            avg_payoff_AMT.append(np.mean([p for pos, p in enumerate(payoff_AMT) if at_AMT[pos] == l]))
        else:
            avg_payoff_AMT.append(0)
        if l in at_95:
            avg_payoff_95.append(np.mean([p for pos, p in enumerate(payoff_95) if at_95[pos] == l]))
        else:
            avg_payoff_95.append(0)
    print(avg_payoff_95)

    # find fraction of players above twothirds of the previous mean (among ALL)
    above_AMT = [0 for i in range(8)]
    above_95 = [0 for i in range(8)]
    for pos, i in enumerate(at_AMT):
        above_AMT[i] += 1  # fraction of guesses above twothirds
    ab_AMT = above_AMT/np.sum(above_AMT)
    for pos, i in enumerate(at_95):
        above_95[i] += 1
    ab_95 = above_95/np.sum(above_95)

    # plot
    axes[0].bar([i for i in range(8)], ab_95, align='center', color=colors[1], label='above 2/3')
    axes[1].bar([i for i in range(8)], ab_AMT, align='center', color=colors[1], label='above 2/3')
    axes[0].set_ylabel('fraction of players')
    print('ab_95', ab_95)
    print('amt', ab_AMT )
    # plot the average payoff on another y-axis
    ax0 = axes[0].twinx()
    ax1 = axes[1].twinx()
    ax1.get_shared_y_axes().join(ax0, ax1)  # magic for sharing the second y-axis
    ax0.plot(avg_payoff_95, marker='o', linestyle='-', c=colors[0], label='payoff')
    ax1.plot(avg_payoff_AMT, marker='o', linestyle='-', c=colors[0], label='payoff')
    ax1.set_yticks([0,1,2,3,4,5], [])
    ax0.set_yticks([])

    # control position of labels by sorting both labels and handles by labels
    handles_95, labels_95 = axes[0].get_legend_handles_labels()
    handles_line, labels_line = ax0.get_legend_handles_labels()
    handles_95.append(handles_line[0])
    labels_95.append(labels_line[0])
    legend_95 = axes[0].legend(handles_95, labels_95)
    legend_95.set_title('Nagel95 (N='+str(len(at_95))+')')
    # ax0.grid(False)

    handles_AMT, labels_AMT = axes[1].get_legend_handles_labels()
    handles_line, labels_line = ax1.get_legend_handles_labels()
    handles_AMT.append(handles_line[0])
    labels_AMT.append(labels_line[0])
    legend_AMT = axes[1].legend(handles_AMT, labels_AMT)
    legend_AMT.set_title('AMT (N='+str(len(at_AMT))+')')
    plt.ylabel('average payoff ($)')
    # ax1.grid(False)

    # paraphernalia
    txtv = fig.text(0.51, .0, '# times a player guesses > 2/3 of previous mean',
                    fontsize='large', ha='center')
    plt.tight_layout()

    # Remember: save as pdf and transparent=True for Adobe Illustrator
    if not os.path.exists(PLOTS_DIR):
        os.makedirs(PLOTS_DIR)

    plt.savefig(os.path.join(PLOTS_DIR, 'fig4.png'), bbox_extra_artists=(txtv,),
                bbox_inches='tight', transparent=True, dpi=300)
    plt.savefig(os.path.join(PLOTS_DIR, 'fig4.pdf'), bbox_extra_artists=(txtv,),
                bbox_inches='tight', transparent=True, dpi=300)

    # plt.savefig('../plots/dynamic_above_twothirds.png', bbox_extra_artists=(txtv,),
    #            bbox_inches='tight', dpi=300)
    plt.show()


def count_movements(df_AMT, df_95):
    # find players in AMT experiment:
    players_AMT = df_AMT.id.unique()
    print('number of players (AMT):', len(players_AMT))

    # find players in Nagel95:
    players_95 = []
    groups = df_95.group.unique()
    for g in groups:
        dfg = df_95[df_95.group == g]
        id_group = dfg.id_in_group.unique()
        for id in id_group:
            players_95.append((g,id))
    print('number of players (95):', len(players_95))

    # find and append strategies in AMT-experiments:
    above_twothirds_AMT  = 0
    not_above_twothirds_AMT =  0
    strategies_AMT = []
    for player in players_AMT:
        dfp = df_AMT[df_AMT.id == player]
        payoff = df_AMT[df_AMT.id == player]['payoff'].unique().item()
        guesses = dfp.guess.values
        twothirds = dfp.twothirds.values

        at = 0
        for i in range(1, 8):
            if guesses[i] > twothirds[i-1]:
                above_twothirds_AMT += 1
                at += 1
            else:
                not_above_twothirds_AMT += 1
        strategies_AMT.append((at, payoff))
    print('Percentage of guesses above 2/3rds of previous mean:',
          100*above_twothirds_AMT/(len(players_AMT)*7), '%.')
    print('Percentage of guesses below (or same as) 2/3 of previous mean:',
          100*not_above_twothirds_AMT/(len(players_AMT)*7), '%.\n')

    # find and append strategies in Nagel95-experiments:
    above_twothirds_95  = 0
    not_above_twothirds_95 =  0
    strategies_95 = []
    for player in players_95:
        group = player[0]
        df_group = df_95[df_95.group == player[0]]
        df_player = df_group[df_group.id_in_group == player[1]]
        guesses = df_player.guess.values
        twothirds = []
        for r in range(1,5):
            tt = (2/3) * np.mean(df_group[df_group['round'] == r]['guess'].values)
            twothirds.append(tt)
        payoff = find_payoff(df_group, player[1])

        at = 0
        for i in range(1, 4):
            if guesses[i] > twothirds[i-1]:
                above_twothirds_95 += 1
                at += 1
            else:
                not_above_twothirds_95 += 1
        strategies_95.append((at, payoff))
    print('Percentage of guesses above 2/3rds of previous mean:',
          100*above_twothirds_95/(len(players_95)*7), '%.')
    print('Percentage of guesses below (or same as) 2/3rds of previous mean:',
          100*not_above_twothirds_95/(len(players_95)*7), '%.\n')

    # plot strategies:
    make_barplot(strategies_AMT, strategies_95)


# main
df_AMT = pd.DataFrame(AMTdata)
df = pd.DataFrame(Nagel95)
df_95 = reformat_Nagel95_data(df)

count_movements(df_AMT, df_95)
