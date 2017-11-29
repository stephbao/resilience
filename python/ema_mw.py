import pandas as pd
from scipy.stats import ttest_1samp, wilcoxon, ttest_ind, mannwhitneyu
import numpy as np

ema = pd.read_csv("ema_data.csv", encoding = "ISO-8859-1", engine='python')
df = pd.read_csv("post_res.csv", encoding = "ISO-8859-1", engine='python')
types = pd.read_csv("user_resil.csv", encoding = "ISO-8859-1", engine='python')
ema_mw = pd.DataFrame()

df_keys = list()
for i in df.keys():
    df_keys.append(i)

ema_keys = list()
for j in ema.keys():
    ema_keys.append(j)

sorted_df = df.sort_values(by=df_keys)
sorted_ema = ema.sort_values(by=ema_keys)

emaIDs = list(ema['SubjectID'])
dfIDs = list(df['subjectID'])

x = 0
indices = list()
for i in range(0,len(ema)):
    indices.append(x)
    x+=1

remove = list()

for user, index in zip(emaIDs, indices):
    user = int(user)
    if (user not in dfIDs):
        remove.append(index)

sorted_ema = sorted_ema.drop(ema.index[remove])

data = pd.concat([types, sorted_ema], axis=1)

specialTreats = ['WEEK1_HrsBed_Avg', 'WEEK1_HrsAsleep_Avg', 'WEEK1_HrsBed_Weekday_Avg',
'WEEK1_HrsAsleep_Weekday_Avg', 'WEEK1_HrsBed_Weekend_Avg', 'WEEK1_HrsAsleep_Weekend_Avg',
'WEEK2_HrsBed_Avg', 'WEEK2_HrsAsleep_Avg', 'WEEK2_HrsBed_Weekday_avg',
'WEEK2_HrsAsleep_Weekday_avg', 'WEEK2_HrsBed_Weekend_avg', 'WEEK2_HrsAsleep_Weekend_avg',
'WEEK3_HrsBed_avg', 'WEEK3_HrsAsleep_avg', 'WEEK3_HrsBed_Weekday_avg',
'WEEK3_HrsAsleep_Weekday_avg', 'WEEK3_HrsBed_Weekend_avg', 'WEEK3_HrsAsleep_Weekend_avg']

ignore = ['Pre_Res',
'Post_Res',
'SubjectID']

def specialTreatHelper(s):
    if (s != ' '):
        time = s.split(":")
        hour = time[0]
        minute = time[1]
        new_time = hour + "." + minute
        return float(new_time)

data = data.fillna(999)

pre0post0 = pd.DataFrame()
pre0post1 = pd.DataFrame()
pre0post_1 = pd.DataFrame()
pre1post0 = pd.DataFrame()
pre_1post0 = pd.DataFrame()
pre1post1 = pd.DataFrame() 
pre_1post_1 = pd.DataFrame()
pre_1post1 = pd.DataFrame()
pre1post_1 = pd.DataFrame()


for col in data:
    if (col not in ignore):
        if (col in specialTreats):
            notNull = (data["Post_Res"] != 999) & (data["Pre_Res"] != 999) & (data[col] != 999)
            pre0post0[col] = data[(data['Pre_Res'] == 0) & (data['Post_Res'] == 0) & notNull][col].apply(specialTreatHelper)
            pre0post1[col] = data[(data['Pre_Res'] == 0) & (data['Post_Res'] == 1) & notNull][col].apply(specialTreatHelper)
            pre0post_1[col] = data[(data['Pre_Res'] == 0) & (data['Post_Res'] == -1) & notNull][col].apply(specialTreatHelper)
            pre1post0[col] = data[(data['Pre_Res'] == 1) & (data['Post_Res'] == 0) & notNull][col].apply(specialTreatHelper)
            pre_1post0[col] = data[(data['Pre_Res'] == -1) & (data['Post_Res'] == 0) & notNull][col].apply(specialTreatHelper)
            pre1post1[col] = data[(data['Pre_Res'] == 1) & (data['Post_Res'] == 1) & notNull][col].apply(specialTreatHelper)
            pre_1post_1[col] = data[(data['Pre_Res'] == -1) & (data['Post_Res'] == -1) & notNull][col].apply(specialTreatHelper)
            pre_1post1[col] = data[(data['Pre_Res'] == -1) & (data['Post_Res'] == 1) & notNull][col].apply(specialTreatHelper)
            pre1post_1[col] = data[(data['Pre_Res'] == 1) & (data['Post_Res'] == -1) & notNull][col].apply(specialTreatHelper)

        else:
            notNull = (data["Post_Res"] != 999) & (data["Pre_Res"] != 999) & (data[col] != 999)
            pre0post0[col] = data[(data['Pre_Res'] == 0) & (data['Post_Res'] == 0) & notNull][col]
            pre0post1[col] = data[(data['Pre_Res'] == 0) & (data['Post_Res'] == 1) & notNull][col]
            pre0post_1[col] = data[(data['Pre_Res'] == 0) & (data['Post_Res'] == -1) & notNull][col]
            pre1post0[col] = data[(data['Pre_Res'] == 1) & (data['Post_Res'] == 0) & notNull][col]
            pre_1post0[col] = data[(data['Pre_Res'] == -1) & (data['Post_Res'] == 0) & notNull][col]
            pre1post1[col] = data[(data['Pre_Res'] == 1) & (data['Post_Res'] == 1) & notNull][col]
            pre_1post_1[col] = data[(data['Pre_Res'] == -1) & (data['Post_Res'] == -1) & notNull][col]
            pre_1post1[col] = data[(data['Pre_Res'] == -1) & (data['Post_Res'] == 1) & notNull][col]
            pre1post_1[col] = data[(data['Pre_Res'] == 1) & (data['Post_Res'] == -1) & notNull][col]

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

ema_mw['PrePost'] = pd.Series(names)
ema_mw['Type'] = pd.Series(surveys)
ema_mw['u'] = pd.Series(u_list)
ema_mw['p'] = pd.Series(p_list)
ema_mw.to_csv('ema_mannwhitney.csv', index=False)
