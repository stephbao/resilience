import pandas as pd
from scipy.stats import ttest_1samp, wilcoxon, ttest_ind, mannwhitneyu
import numpy as np

df = pd.read_csv("user_resil.csv", encoding = "ISO-8859-1", engine='python')
pre_df = pd.read_csv("pre_res.csv", encoding = "ISO-8859-1", engine='python')
post_df = pd.read_csv("post_res.csv", encoding = "ISO-8859-1", engine='python')
pre_post_mannwhitney = pd.DataFrame()

pre = pd.concat([df, pre_df], axis=1)
post = pd.concat([df, post_df], axis = 1)
dfs = [pre, post]
count = 0

for data in dfs:
    if (count == 0):
        print(data.keys())
        pre_pre0post0 = data[(data['Pre_Res'] == 0) & (data['Post_Res'] == 0)]
        pre_pre0post1 = data[(data['Pre_Res'] == 0) & (data['Post_Res'] == 1)]
        pre_pre0post_1 = data[(data['Pre_Res'] == 0) & (data['Post_Res'] == -1)]
        pre_pre1post0 = data[(data['Pre_Res'] == 1) & (data['Post_Res'] == 0)]
        pre_pre_1post0 = data[(data['Pre_Res'] == -1) & (data['Post_Res'] == 0)]
        pre_pre1post1 = data[(data['Pre_Res'] == 1) & (data['Post_Res'] == 1)]
        pre_pre_1post_1 = data[(data['Pre_Res'] == -1) & (data['Post_Res'] == -1)]
        pre_pre_1post1 = data[(data['Pre_Res'] == -1) & (data['Post_Res'] == 1)]
        pre_pre1post_1 = data[(data['Pre_Res'] == 1) & (data['Post_Res'] == -1)]

    elif (count == 1):
        post_pre0post0 = data[(data['Pre_Res'] == 0) & (data['Post_Res'] == 0)]
        post_pre0post1 = data[(data['Pre_Res'] == 0) & (data['Post_Res'] == 1)]
        post_pre0post_1 = data[(data['Pre_Res'] == 0) & (data['Post_Res'] == -1)]
        post_pre1post0 = data[(data['Pre_Res'] == 1) & (data['Post_Res'] == 0)]
        post_pre_1post0 = data[(data['Pre_Res'] == -1) & (data['Post_Res'] == 0)]
        post_pre1post1 = data[(data['Pre_Res'] == 1) & (data['Post_Res'] == 1)]
        post_pre_1post_1 = data[(data['Pre_Res'] == -1) & (data['Post_Res'] == -1)]
        post_pre_1post1 = data[(data['Pre_Res'] == -1) & (data['Post_Res'] == 1)]
        post_pre1post_1 = data[(data['Pre_Res'] == 1) & (data['Post_Res'] == -1)]

    count +=1

pre_categories = [pre_pre0post0, pre_pre0post1, pre_pre0post_1, pre_pre1post0, pre_pre_1post0, pre_pre1post1, pre_pre_1post_1,
                    pre_pre_1post1, pre_pre1post_1]
post_categories = [post_pre0post0, post_pre0post1, post_pre0post_1, post_pre1post0, post_pre_1post0, post_pre1post1, post_pre_1post_1,
                    post_pre_1post1, post_pre1post_1]

categories = pre_categories + post_categories

c_n = ['preNpostN', 'preNpostH', 'preNpostL', 'preHpostN', 'preLpostN', 
    'preHpostH', 'preLpostL', 'preLpostH', 'preHpostL']
c_n = c_n * 2

ignore = ['Pre_Res', 'Post_Res', 'subjectID', 'device_id', 'Pre_Suicidal', 'Post_Suicidal', 'group_name']
for df, df2 in zip(pre_categories, post_categories):
    for j in ignore:
        #df.drop(j, axis=1, inplace=True)
        del df[j]
        del df2[j]

'''
for i in range(0, len(c_n)):
    a = pre_categories[i].dropna()
    b = post_categories[i].dropna()
    for ai, bi in zip(a, b):
        print(ai, bi)
        z, u = mannwhitneyu(a[ai], b[bi], alternative = 'two-sided')
        print(z, u)
'''
names = []
surveys = []
p_list = []
u_list = []

for i in range(0, len(categories)):
    for j in range(i+1, len(categories)):
        a = categories[i].dropna()
        b = categories[j].dropna()
        for ai, bi in zip(a, b):
            u,p = mannwhitneyu(a[ai], b[bi], alternative = 'two-sided')
            p_list.append(p)
            u_list.append(u)
            surveys.append(ai + ' : ' + bi)
            names.append(c_n[i] + ':' + c_n[j])

pre_post_mannwhitney['PrePost'] = pd.Series(names)
pre_post_mannwhitney['Surveys'] = pd.Series(surveys)
pre_post_mannwhitney['u'] = pd.Series(u_list)
pre_post_mannwhitney['p'] = pd.Series(p_list)
pre_post_mannwhitney.to_csv('pre_post_mannwhitney.csv', index=False)


            