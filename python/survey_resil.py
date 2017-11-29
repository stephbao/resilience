import pandas as pd
from scipy.stats import ttest_1samp, wilcoxon, ttest_ind, mannwhitneyu
import numpy as np

pre = pd.read_csv("pre_res.csv", encoding = "ISO-8859-1", engine='python')
post = pd.read_csv("post_res.csv", encoding = "ISO-8859-1", engine='python')
resilience = pd.DataFrame()

pre_names = ['Pre_PSS_sum', 'Pre_CSSEC_Sum', 'Pre_ISEL_Sum', 
            'Pre_SCS_SF_Mean', 'Pre_LS_Sum', 'Pre_NBS_Sum', 'Pre_BRS_Sum']
post_names = ['Post_PSS_sum', 'Post_CSSEC_Sum', 'Post_ISEL_sum',
            'Post_SF_CMU_Sum', 'Post_LS_Sum', 'Post_NBS_Sum', 'Post_BRS_sum']

scoring = ['PSS, CSSEC', 'ISEL', 'SF', 'LS', 'NBS', 'BRS']

dfs = [pre, post]
names = [pre_names, post_names]

count = 0

for df, name in zip(dfs, names):
    resilience = pd.DataFrame()
    for survey in name:
        values = []
        if ('PSS' in survey):
            for score in df[survey]:
                if (score >= 20):
                    values.append(-1)
                elif (score >= 10 and score < 20):
                    values.append(0)
                else:
                    values.append(1)

        elif ('CSSEC' in survey):
            for score in df[survey]:
                if (score >= 300):
                    values.append(-1)
                elif (score >= 150 and score < 300):
                    values.append(0)
                else:
                    values.append(1)

        elif ('ISEL' in survey):
            for score in df[survey]:
                if (score < 12):
                    values.append(-1)
                elif (score >= 12 and score < 24):
                    values.append(0)
                else:
                    values.append(1)   

        elif ('SF' in survey):
            for score in df[survey]:
                if (score < 5/3):
                    values.append(-1)
                elif (score >= 5/3 and score < 10/3):
                    values.append(0)
                else:
                    values.append(1)    

        elif ('LS' in survey):
            for score in df[survey]:
                if (score < 80/3):
                    values.append(-1)
                elif (score >= 80/3 and score < 160/3):
                    values.append(0)
                else:
                    values.append(1)

        elif ('NBS' in survey):
            for score in df[survey]:
                if (score >= 100/3):
                    values.append(-1)
                elif (score >= 50/3 and score < 100/3):
                    values.append(0)
                else:
                    values.append(1)

        elif ('BRS' in survey):
            for score in df[survey]:
                score = score / 5
                if (score < 3):
                    values.append(-1)
                elif (score >= 3 and score < 4.31):
                    values.append(0)
                else:
                    values.append(1)


        resilience[survey] = pd.Series(values, index=df.index)

    if (count == 0):
        resilience.to_csv('pre_score.csv', index=False)
    else:
        resilience.to_csv('post_score.csv', index=False)
        
    count+=1


