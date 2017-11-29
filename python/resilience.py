import pandas as pd
import numpy as np
import mysql.connector
from sqlalchemy import (create_engine)

'''def level(score, total):
    if (total == 0):
        if (score < 3):
            return 0
        elif (score >4.30):
            return 2
        else:
            return 1
    else:
        x = score / total
        if (x <= 1/3):
            return 0
        elif (x >= 2/3):
            return 2
        else:
            return 1'''

pre = pd.read_csv("pre_baseline.csv", encoding = "ISO-8859-1", engine='python')
#ema = pd.read_csv("ema_data.csv", encoding = "ISO-8859-1")
post = pd.read_csv("post_baseline.csv", encoding = "ISO-8859-1", engine='python')

names = pd.read_csv("_device_id_suicidal_ideation.csv", encoding = "ISO-8859-1", engine='python')

new_df = pd.DataFrame()

pre.fillna(0)
#ema.fillna(0)
post.fillna(0)
'''
pre_names = {'Pre_PSS_Stressed':1, 'Pre_PSS_sum':1, 'Pre_CSSEC_Sum':1, 'Pre_ISEL_Sum':36, 
			'Pre_SCS_SF_Mean':1, 'Pre_LS_Sum':80, 'Pre_NBS_Sum':50, 'Pre_BRS_Sum':6}

post_names = {'Post_PSS_Stressed':1, 'Post_PSS_sum':1, 'Post_CSSEC_Sum':1, 'Post_ISEL_sum':36,
			'Post_SF_CMU_Sum':130, 'Post_LS_Sum':80, 'Post_NBS_Sum':50, 'Post_BRS_sum':6}
'''
pre_names = ['Pre_PSS_sum', 'Pre_CSSEC_Sum', 'Pre_ISEL_Sum', 
            'Pre_SCS_SF_Mean', 'Pre_LS_Sum', 'Pre_NBS_Sum', 'Pre_BRS_Sum']

post_names = ['Post_PSS_sum', 'Post_CSSEC_Sum', 'Post_ISEL_sum',
            'Post_SF_CMU_Sum', 'Post_LS_Sum', 'Post_NBS_Sum', 'Post_BRS_sum']

df_list = [pre, post]
names_list = [pre_names, post_names]

count = 0

engine = create_engine('mysql+mysqlconnector://root:23802380@127.0.0.1:3306/resilience', echo=False)
conn = engine.connect()

for df, name in zip(df_list, names_list):
    for j in name:
        #total = name[j]
        empty = []
        for i in range(len(df)):
            score = df[j][i]
            empty.append(score)


        new_df[j] = pd.Series(empty, index=df.index)

    result = pd.concat([names, new_df], axis=1)

    if (count == 0):
        result.to_csv('pre_res.csv', index=False)
        #new_df.to_sql('pre_res.csv', con=conn, if_exists="append",
                    #index=False)
    elif (count ==1):
        result.to_csv('post_res.csv', index=False)
        #new_df.to_sql('post_res.csv', con=conn, if_exists="append",
                    #index=False)
    new_df = pd.DataFrame()
    count+=1

conn.close()


#Pre_BDI_II_Suicidal, subject id