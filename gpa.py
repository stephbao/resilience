import pandas as pd
from scipy.stats import ttest_1samp, wilcoxon, ttest_ind, mannwhitneyu
import numpy as np

df = pd.read_csv("device_id_resilience_ideation.csv", encoding = "ISO-8859-1", engine='python')
pre_df = pd.read_csv("pre_baseline.csv", encoding = "ISO-8859-1", engine='python')
post = pd.read_csv("post_baseline.csv", encoding = "ISO-8859-1", engine='python')
gpa = pd.DataFrame()
pre0post0 = pd.DataFrame()
pre0post1 = pd.DataFrame()
pre0post_1 = pd.DataFrame()
pre1post0 = pd.DataFrame()
pre_1post0 = pd.DataFrame()
pre1post1 = pd.DataFrame() 
pre_1post_1 = pd.DataFrame()
pre_1post1 = pd.DataFrame()
pre1post_1 = pd.DataFrame()
results = pd.DataFrame()

pre = pd.concat([pre_df, df], axis=1)

gpa['subjectID'] = pre['subjectID']
gpa['Pre_Res'] = pre['Pre_Res']
gpa['Post_Res'] = pre['Post_Res']
gpa['Pre_f16_cum_GPA'] = pre['Pre_f16_cum_GPA']
gpa['Post_S17_cum_gpa'] = post['Post_S17_cum_gpa']
gpa['Post_S17_change_in_cum_gpa'] = post['Post_S17_change_in_cum_gpa']
gpa['Post_S17_term_gpa'] = post['Post_S17_term_gpa']

ignore = ['Pre_Res',
'Post_Res',
'subjectID']

for col in gpa:
    if (col not in ignore):
        pre0post0[col] = (gpa[(gpa['Pre_Res'] == 0) & (gpa['Post_Res'] == 0)])[col]
        pre0post1[col] = (gpa[(gpa['Pre_Res'] == 0) & (gpa['Post_Res'] == 1)])[col]
        pre0post_1[col] = (gpa[(gpa['Pre_Res'] == 0) & (gpa['Post_Res'] == -1)])[col]
        pre1post0[col] = (gpa[(gpa['Pre_Res'] == 1) & (gpa['Post_Res'] == 0)])[col]
        pre_1post0[col] = (gpa[(gpa['Pre_Res'] == -1) & (gpa['Post_Res'] == 0)])[col]
        pre1post1[col] = (gpa[(gpa['Pre_Res'] == 1) & (gpa['Post_Res'] == 1)])[col]
        pre_1post_1[col] = (gpa[(gpa['Pre_Res'] == -1) & (gpa['Post_Res'] == -1)])[col]
        pre_1post1[col] = (gpa[(gpa['Pre_Res'] == -1) & (gpa['Post_Res'] == 1)])[col]
        pre1post_1[col] = (gpa[(gpa['Pre_Res'] == 1) & (gpa['Post_Res'] == -1)])[col]

categories = [pre0post0, pre0post1, pre0post_1, pre1post0, pre_1post0, pre1post1, pre_1post_1,
                    pre_1post1, pre1post_1]
c_n = ['pre_Norm_post_Norm', 'pre_Norm_post_High', 'pre_Norm_post_Low', 'pre_High_post_Norm', 'pre_Low_post_Norm', 
    'pre_High_post_High', 'pre_Low_post_Low', 'pre_Low_post_High', 'pre_High_post_Low']

names = []
surveys = []
p_list = []
u_list = []

for i in range(0, len(categories)):
    for j in range(i+1, len(categories)):
        a = categories[i]
        b = categories[j]
        for ai, bi in zip(a, b):
            try:
                u,p = mannwhitneyu(a[ai], b[bi], alternative = 'two-sided')
            except ValueError as e:
                u = None
                p = None
            p_list.append(p)
            u_list.append(u)
            surveys.append(ai + ' : ' + bi)
            names.append(c_n[i] + ' : ' + c_n[j])

results['PrePost'] = pd.Series(names)
results['Surveys'] = pd.Series(surveys)
results['u'] = pd.Series(u_list)
results['p'] = pd.Series(p_list)
results.to_csv('GPA_mannwhitney.csv', index=False)

