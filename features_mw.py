from sqlalchemy import (create_engine)
from sqlalchemy import (MetaData, Table, inspect)
import pandas as pd
from datetime import datetime, timedelta
from scipy.stats import ttest_1samp, wilcoxon, ttest_ind, mannwhitneyu

def add_group_col():
    #engine = create_engine('mysql+mysqlconnector://{0}:{1}@{2}:{3}'.format(USER, PASSWORD, HOST, DBNAME))
    engine = create_engine('mysql+mysqlconnector://root:23802380@127.0.0.1:3306/resilience', echo=False)
    conn = engine.connect()
    info = Table(DIRI_table, MetaData(), autoload = True, autoload_with = conn)
    cols = info.c
    if not ('group' in cols):
        addCol = "alter table `%s` add column `group_name` varchar(255)" % DIRI_table
        conn.execute(addCol)
    get_DIRI = "select device_id, Pre_Res, Post_Res from `%s`" % DIRI_table
    DIRI = pd.read_sql(get_DIRI, conn)
    for row in DIRI.iterrows():
        device_id = row[1]["device_id"]
        pre = row[1]["Pre_Res"]
        post = row[1]["Post_Res"]
        pre = str(pre)
        post = str(post)
        #if not pre.isdigit() or not post.isdigit():
         #   continue
        if pre == "0" and post == "0":
            group = "pNpN"
        elif pre == "0" and post == "1":
            group = "pNpH"
        elif pre == "0" and post == "-1":
            group = "pNpL"
        elif pre =="1" and post == "0":
            group = "pHpN"
        elif pre =="1" and post == "-1":
            group = "pHpL"
        elif pre =="-1" and post == "0":
            group = "pLpN"
        elif pre =="-1" and post == "1":
            group = "pLpH"
        elif pre =="1" and post == "1":
            group = "pHpH"
        elif pre =="-1" and post == "-1":
            group = "pLpL"

        update = "update `%s` set `group_name` = '%s' where `device_id` = '%s'" % (DIRI_table, group, device_id)
        conn.execute(update)
    conn.close()

def get_data_group_day(group, sensor, table_names, date, conn):
    group_day = pd.DataFrame()
    for device_id in group["device_id"]:
        table = "_" + device_id + "_" + sensor + "_day"
        #table = "_" + device_id + "_" + sensor
        if not table in table_names: continue
        select_device_day = "select * from `%s` where datetime_EST = '%s'" % (table, date)
        df = pd.read_sql(select_device_day, conn)
        group_day = group_day.append(df)
    return group_day

def test(groups, groups_names, date, sensor):
    result = []
    pNpN = groups[0]
    features = list(pNpN)
    for feature in features:
        for i in range (0, 4):
            for j in range (i + 1, 4):
                row_title = sensor + "_" + feature + ("(%s, %s)" % (groups_names[i], groups_names[j]))
                try:
                    a = groups[i][feature].dropna().tolist()
                    b = groups[j][feature].dropna().tolist()
                    u, p = mannwhitneyu(a, b, alternative = 'two-sided')
                except ValueError as e:
                    print(e, date, row_title)
                    p = None
                d = {"item" : row_title, date : p}
                result.append(d)
    result_df = pd.DataFrame(result)
    return result_df.set_index("item")

def main():
    engine = create_engine('mysql+mysqlconnector://root:23802380@127.0.0.1:3306/resilience', echo=False)
    conn = engine.connect()
    inspector = inspect(engine)
    table_names = inspector.get_table_names()
    date = start_date
    get_DIRI = "select device_id, group_name from `%s`" % DIRI_table
    DIRI = pd.read_sql(get_DIRI, conn)
    pNpN = DIRI[DIRI["group_name"] == "pNpN"]
    pNpH = DIRI[DIRI["group_name"] == "pNpH"]
    pNpL = DIRI[DIRI["group_name"] == "pNpL"]
    pHpN = DIRI[DIRI["group_name"] == "pHpN"]
    pHpL = DIRI[DIRI["group_name"] == "pHpL"]
    pHpH = DIRI[DIRI["group_name"] == "pHpH"]
    pLpN = DIRI[DIRI["group_name"] == "pLpN"]
    pLpH = DIRI[DIRI["group_name"] == "pLpH"]
    pLpL = DIRI[DIRI["group_name"] == "pLpL"]

    groups_names = ["pNpN", "pNpH", "pNpL", "pHpN",
                    "pHpL", "pHpH", "pLpN", "pLpH", "pLpL"]
    for sensor in sensors:
        result = pd.DataFrame()
        while date < end_date:
            pNpN_day = get_data_group_day(pNpN, sensor, table_names, date, conn)
            pNpH_day = get_data_group_day(pNpH, sensor, table_names, date, conn)
            pNpL_day = get_data_group_day(pNpL, sensor, table_names, date, conn)
            pHpN_day = get_data_group_day(pHpN, sensor, table_names, date, conn)
            pHpL_day = get_data_group_day(pHpL, sensor, table_names, date, conn)
            pHpH_day = get_data_group_day(pHpH, sensor, table_names, date, conn)
            pLpN_day = get_data_group_day(pLpN, sensor, table_names, date, conn)
            pLpH_day = get_data_group_day(pLpH, sensor, table_names, date, conn)
            pLpL_day = get_data_group_day(pLpL, sensor, table_names, date, conn)
            
            #pNpN_day.to_sql(sensor + "_pNpN", con = conn, if_exists="append", index=False)
            #pNpS_day.to_sql(sensor + "_pNpS", con = conn, if_exists="append", index=False)
            #pSpN_day.to_sql(sensor + "_pSpN", con = conn, if_exists="append", index=False)
            #pSpS_day.to_sql(sensor + "_pSpS", con = conn, if_exists="append", index=False)
            groups = [pNpN_day, pNpH_day, pNpL_day, pHpN_day, pHpL_day, pHpH_day, pLpN_day, pLpH_day, pLpL_day]
            date_string = str(date)[:-9]
            result_day = test(groups, groups_names, date_string, sensor)
            result = pd.concat([result, result_day],axis = 1)
            print(date)
            date = date + timedelta(days = 1)
        result = result.reset_index()
        result.to_sql("_features_WILCOXON_test_resilience2", con = conn, if_exists="append", index = False)
    
    conn.close()
    
def alter_column_date():
    engine = create_engine('mysql+mysqlconnector://root:23802380@127.0.0.1:3306/resilience', echo=False)
    conn = engine.connect()
    inspector = inspect(engine)
    table_names = inspector.get_table_names()
    for table in table_names:
        if "steps_day" in table:
            info = Table(table, MetaData(), autoload = True, autoload_with = conn)
            cols = info.c
            if "date" in cols:
                print (table)
                alter = "ALTER TABLE `%s` CHANGE `date` `datetime_EST` DATETIME" % table
                conn.execute(alter)
    conn.close()

def add_col_datetime_EST_sleep():
    engine = create_engine('mysql+mysqlconnector://root:23802380@127.0.0.1:3306/resilience', echo=False)
    conn = engine.connect()
    inspector = inspect(engine)
    table_names = inspector.get_table_names()
    for table in table_names:
        if "sleep_day" in table:
            info = Table(table, MetaData(), autoload = True, autoload_with = conn)
            cols = info.c
            if not ('datetime_EST' in cols):
                addCol = "alter table `%s` add column `datetime_EST` DATETIME" % table
                conn.execute(addCol)
                
                read_col_end = "select end from `%s`" % table
                df = pd.read_sql(read_col_end, conn)
                for row in df.iterrows():
                    time = row[1]["end"]
                    date = datetime.strptime(str(time)[:-9], '%Y-%m-%d')
                    update = "update `%s` set `datetime_EST` = '%s' where `end` = '%s'" % (table, date, time)
                    conn.execute(update)

    conn.close()

def add_col_datetime_EST_screen_overnight():
    engine = create_engine('mysql+mysqlconnector://root:23802380@127.0.0.1:3306/resilience', echo=False)
    conn = engine.connect()
    inspector = inspect(engine)
    table_names = inspector.get_table_names()
    for table in table_names:
        if "screen_overnight" in table:
            info = Table(table, MetaData(), autoload = True, autoload_with = conn)
            cols = info.c
            if not ('datetime_EST' in cols):
                addCol = "alter table `%s` add column `datetime_EST` DATETIME" % table
                conn.execute(addCol)
                
                read_col_end = "select use_end_time, unuse_end_time from `%s`" % table
                df = pd.read_sql(read_col_end, conn)
                for row in df.iterrows():
                    if row[1].isnull()["use_end_time"] == False: 
                        time = row[1]["use_end_time"]
                        col = "use_end_time"
                    elif row[1].isnull()["unuse_end_time"] == False: 
                        time = row[1]["unuse_end_time"]
                        col = "unuse_end_time"
                    else: continue
                    date = datetime.strptime(str(time)[:-9], '%Y-%m-%d')
                    update = "update `%s` set `datetime_EST` = '%s' where `%s` = '%s'" % (table, date, col, time)
                    conn.execute(update)

    conn.close()

def add_col_datetime_EST_screen_night():
    engine = create_engine('mysql+mysqlconnector://root:23802380@127.0.0.1:3306/resilience', echo=False)
    conn = engine.connect()
    inspector = inspect(engine)
    table_names = inspector.get_table_names()
    for table in table_names:
        if "screen_night" in table:
            info = Table(table, MetaData(), autoload = True, autoload_with = conn)
            cols = info.c
            if not ('datetime_EST' in cols):
                addCol = "alter table `%s` add column `datetime_EST` DATETIME" % table
                conn.execute(addCol)
                
                read_col_end = "select EndTime from `%s`" % table
                df = pd.read_sql(read_col_end, conn)
                for row in df.iterrows():
                    time = row[1]["EndTime"]
                    try:
                        date = datetime.strptime(str(time)[:-9], '%Y-%m-%d')
                        update = "update `%s` set `datetime_EST` = '%s' where `EndTime` = '%s'" % (table, date, time)
                        conn.execute(update)
                    except:
                        print(row)
                    
                    

    conn.close()

def count_significant_days():
    engine = create_engine('mysql+mysqlconnector://root:23802380@127.0.0.1:3306/resilience', echo=False)
    conn = engine.connect()
    get_data = "select * from `features_WILCOXON_test`"
    df = pd.read_sql(get_data, conn)
    result = []
    for row in df.itertuples():
        item = row[1]
        data = list(row[2:])
        count = 0
        for n in data:
            if n != None and n < 0.05 and n != 0.0 :
                count += 1
        d = {"item" : item, "number_significant_days": count}
        result.append(d)
    result_df = pd.DataFrame(result)
    result_df.to_sql("_count_significant_days", con=conn, if_exists="append",
            index=None)
    conn.close()

#STARTDATE : 1/4/2017
#start_date = datetime.strptime("2017-01-04 00:00:00", '%Y-%m-%d %H:%M:%S')
#end_date = datetime.strptime("2017-07-01 00:00:00", '%Y-%m-%d %H:%M:%S')
start_date = datetime.strptime("2017-01-04", '%Y-%m-%d')
end_date = datetime.strptime("2017-07-01", '%Y-%m-%d')

USER = "root"
PASSWORD = "23802380"
HOST = "127.0.0.1"
DBNAME = "resilience"
sensors = ["wifi"]
#the table that has device id and Res ideation group
DIRI_table = "device_id_resilience_ideation"
#add_group_col()
main()
#alter_column_date()
#add_col_datetime_EST_sleep()
#add_col_datetime_EST_screen_overnight()
#add_col_datetime_EST_screen_night()
#count_significant_days()