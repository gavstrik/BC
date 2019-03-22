import pandas as pd

datafile_AMT = pd.read_csv('../../../Experiments/data/GoR/all_data_anonymous_gor.csv')
df_AMT = pd.DataFrame(datafile_AMT)
df = df_AMT[(df_AMT.split == 1) & (df_AMT.high == 1)]
df = df.drop(['Unnamed: 0', 'split', 'high'], 1)
df = df.reset_index(drop=True)
df.to_csv('../data/amt.csv')
