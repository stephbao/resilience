import pandas as pd
from scipy.stats import ttest_1samp, wilcoxon, ttest_ind, mannwhitneyu
import numpy as np

pre = pd.read_csv("pre_score_distr.csv", encoding = "ISO-8859-1", engine='python')
post = pd.read_csv("post_score_distr.csv", encoding = "ISO-8859-1", engine='python')
resilience = pd.DataFrame()

names = ['-1', '0', '1']

dfs = [pre, post]
df_name = ['Pre_Res', 'Post_Res']
count = 0

for df, name in zip(dfs, df_name):
    scores = []
    for i in range(0, len(df)):
        if (df['-1'][i] >= 4):
            scores.append('-1')
        elif (df['1'][i]>=4):
            scores.append('1')
        else:
            scores.append('0')
    resilience[name] = pd.Series(scores, index=df.index)

resilience.to_csv('user_resil.csv', index=False)