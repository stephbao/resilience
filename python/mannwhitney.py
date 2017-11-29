import pandas as pd
from scipy.stats import ttest_1samp, wilcoxon, ttest_ind, mannwhitneyu
import numpy as np

pre = pd.read_csv("pre_res.csv", encoding = "ISO-8859-1", engine='python')
post = pd.read_csv("post_res.csv", encoding = "ISO-8859-1", engine='python')

new_df = pd.DataFrame()

dfs = [pre, post]
count = 0

for data in dfs:
    data["Post_Suicidal"] = data["Post_Suicidal"].fillna(999)
    data["Post_Suicidal"].astype(int)
    if (count == 0):
        notNull = (data["Post_Suicidal"] != 999) & (data["Pre_Suicidal"] != 999)
        pre_preNpostN = data[(data["Post_Suicidal"] == 0) & (data["Pre_Suicidal"] == 0)]
        pre_preSpostN = data[(data["Post_Suicidal"] == 0) & (data["Pre_Suicidal"] != 0)]
        pre_preNpostS = data[(data["Post_Suicidal"] != 0) & (data["Pre_Suicidal"] == 0)]
        pre_preSpostS = data[(data["Post_Suicidal"] != 0) & (data["Pre_Suicidal"] != 0)]

    elif (count == 1):
        notNull = (data["Post_Suicidal"] != 999) & (data["Pre_Suicidal"] != 999)
        post_preNpostN = data[(data["Post_Suicidal"] == 0) & (data["Pre_Suicidal"] == 0)]
        post_preSpostN = data[(data["Post_Suicidal"] == 0) & (data["Pre_Suicidal"] != 0)]
        post_preNpostS = data[(data["Post_Suicidal"] != 0) & (data["Pre_Suicidal"] == 0)]
        post_preSpostS = data[(data["Post_Suicidal"] != 0) & (data["Pre_Suicidal"] != 0)]

    count+=1 

    pre_categories = [pre_preNpostN, pre_preSpostN, pre_preNpostS, pre_preSpostS]
    pre_cat_names = ['pre_preNpostN', 'pre_preSpostN', 'pre_preNpostS', 'pre_preSpostS']
    post_categories = [post_preNpostN, post_preSpostN, post_preNpostS, post_preSpostS]
    post_cat_names = ['post_preNpostN', 'post_preSpostN', 'post_preNpostS', 'post_preSpostS']

    ignore = ['subjectID', 'device_id', 'Pre_Suicidal', 'Post_Suicidal', 'group_name']
    for df in categories:
        for j in ignore:
            #df.drop(j, axis=1, inplace=True)
            del df[j]

    for i in range(0, 4):
        for j in range(i+1, 4):
            print('\n=============== ' + cat_names[i] + ' : ' + cat_names[j] + ' ===============\n')
            a = categories[i].dropna()
            b = categories[j].dropna()
            for ai, bi in zip(a, b):
                print(ai, bi)
                z, u = mannwhitneyu(a[ai], b[bi], alternative = 'two-sided')
                print(z, u)
            