import pandas as pd
import numpy as np
import mysql.connector
from sqlalchemy import (create_engine)
from sqlalchemy import (insert, MetaData, Table, inspect)

def testData(col, conn, result):
    getData = "select * from `%s`" % (table)
    data = pd.read_sql(getData, conn)
    print(data)
    notNull = (data["Pre_Res"] != "") & (data["Post_Res"] != "") & (data[col] != "")
    pre0post0[col] = data[(data['Pre_Res'] == 0) & (data['Post_Res'] == 0) & notNull][col]
    pre0post1[col] = data[(data['Pre_Res'] == 0) & (data['Post_Res'] == 1) & notNull][col]
    pre0post_1[col] = data[(data['Pre_Res'] == 0) & (data['Post_Res'] == -1) & notNull][col]
    pre1post0[col] = data[(data['Pre_Res'] == 1) & (data['Post_Res'] == 0) & notNull][col]
    pre_1post0[col] = data[(data['Pre_Res'] == -1) & (data['Post_Res'] == 0) & notNull][col]
    pre1post1[col] = data[(data['Pre_Res'] == 1) & (data['Post_Res'] == 1) & notNull][col]
    pre_1post_1[col] = data[(data['Pre_Res'] == -1) & (data['Post_Res'] == -1) & notNull][col]
    pre_1post1[col] = data[(data['Pre_Res'] == -1) & (data['Post_Res'] == 1) & notNull][col]
    pre1post_1[col] = data[(data['Pre_Res'] == 1) & (data['Post_Res'] == -1) & notNull][col]
    pre_categories = [pre_pre0post0, pre_pre0post1, pre_pre0post_1, pre_pre1post0, pre_pre_1post0, pre_pre1post1, pre_pre_1post_1,
                    pre_pre_1post1, pre_pre1post_1]
    post_categories = [post_pre0post0, post_pre0post1, post_pre0post_1, post_pre1post0, post_pre_1post0, post_pre1post1, post_pre_1post_1,
                    post_pre_1post1, post_pre1post_1]

    categories = pre_categories + post_categories

    c_n = ['preNpostN', 'preNpostH', 'preNpostL', 'preHpostN', 'preLpostN', 
    'preHpostH', 'preLpostL', 'preLpostH', 'preHpostL']
    c_n = c_n * 2

    for i in range(0, len(categories)):
        for j in range (i + 1, len(categories)):
            row_title = col + ("(%s, %s)" % (c_n[i], c_n[j]))
            try:
                a = categories[i].tolist()
                b = categories[j].tolist()
                z, p = mannwhitneyu(a, b, alternative = 'two-sided')
            except ValueError as e:
                print(e, row_title)
                z = None
                p = None
            d = {"item" : row_title, "z":z,"p":p}
            result.append(d)
    return result

def main():
    engine = create_engine('mysql+mysqlconnector://root:23802380@127.0.0.1:3306/resilience', echo=False)
    conn = engine.connect()
    ema = Table(table, MetaData(), autoload = True, autoload_with = conn)
    cols = ema.c.keys()
    result = []
    for col in cols:
        print(col)
        if col in ignore: continue
        else: result = testData(col, conn, result)
    result_df = pd.DataFrame(result)
    result_df.to_sql("post_baseline_WILXON_test", con=conn, if_exists="append",
                     index=False)
    conn.close()


ignore = ['Pre_Res', 'Post_Res', 'subjectID', 'device_id', 'Pre_Suicidal', 'Post_Suicidal', 'group_name']

USER = ""
PASSWORD = ""
HOST = ""
DBNAME = ""
table = "res"
main()