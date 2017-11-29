import pandas as pd
from scipy.stats import ttest_1samp, wilcoxon, ttest_ind, mannwhitneyu
import numpy as np

pre = pd.read_csv("pre_score.csv", encoding = "ISO-8859-1", engine='python')
post = pd.read_csv("post_score.csv", encoding = "ISO-8859-1", engine='python')

pre_names = ['Pre_PSS_sum', 'Pre_CSSEC_Sum', 'Pre_ISEL_Sum', 'Pre_SCS_SF_Mean', 'Pre_LS_Sum', 'Pre_NBS_Sum', 'Pre_BRS_Sum']
post_names = ['Post_PSS_sum', 'Post_CSSEC_Sum', 'Post_ISEL_sum', 'Post_SF_CMU_Sum', 'Post_LS_Sum', 'Post_NBS_Sum', 'Post_BRS_sum']

dfs = [pre, post]
names = [pre_names, post_names]

count = 0

for df, name in zip(dfs, names):
    resilience = pd.DataFrame()
    neg = [0]*len(df)
    zero = [0]*len(df)
    pos = [0]*len(df)
    for i in range(0, len(df)):
        score = 0
        for n in name:
            x = df[n][i]
            if (x == -1):
                neg[i]+=1
            elif (x == 0):
                zero[i]+=1
            elif (x == 1):
                pos[i]+=1

    resilience['-1'] = pd.Series(neg, index=df.index)
    resilience['0'] = pd.Series(zero, index=df.index)
    resilience['1'] = pd.Series(pos, index=df.index)

    if (count == 0):
        resilience.to_csv('pre_score_distr.csv', index=False)
    else:
        resilience.to_csv('post_score_distr.csv', index=False)
        
    count+=1


