#! python3

from sqlalchemy import (create_engine)
from sqlalchemy import (MetaData, Table, inspect)
import pandas as pd
import plotly.plotly as py
import plotly.graph_objs as go

def main_one():
    engine = create_engine('mysql+mysqlconnector://root:23802380@127.0.0.1:3306/resilience', echo=False)
    conn = engine.connect()
    get_data = "select * from `for_heatmap`"
    df = pd.read_sql(get_data, conn)
    row_names = df["item"].tolist()
    
    df = df.drop('item', axis = 1).fillna(value = 0)
    
    col_names = list(df.columns.values)
    
    trace = go.Heatmap(z=df.as_matrix(),
                    x=col_names,
                    y=row_names,
                    colorscale = 'Viridis')
    data=[trace]
    py.plot(data, filename='heatmap_2')
    conn.close()

def main_two():
    engine = create_engine('mysql+mysqlconnector://root:23802380@127.0.0.1:3306/resilience', echo=False)
    conn = engine.connect()
    get_data = "select * from `features_WILCOXON_test_resilience2`"
    df = pd.read_sql(get_data, conn)
    row_names = df["item"].tolist()
    
    df = df.drop('item', axis = 1).fillna(value = 1)
    df = df.replace(to_replace = 0, value = 1)
    
    col_names = list(df.columns.values)
    
    trace = go.Heatmap(z=df.as_matrix(),
                    x=col_names,
                    y=row_names,
                    colorscale = 'Viridis')
    data=[trace]
    py.plot(data, filename='heatmap_3')
    conn.close()
    
def getsensor(s):
    return s.split("_")[0]

def shorten(s):
    L = s.split("(")
    left = "".join(L[0].split("_")[1:])
    right = L[1]
    if "pre_norm_post_norm, pre_sui_post_non" in right: right = "(pNpN,pSpN)"
    elif "pre_non_post_non, pre_non_post_sui" in right: right = "(pNpN,pNpS)"
    elif "pre_non_post_non, pre_sui_post_sui" in right: right = "(pNpN,pSpS)"
    elif "pre_non_post_sui, pre_sui_post_non" in right: right = "(pNpS,pSpN)"
    elif "pre_non_post_sui, pre_sui_post_sui" in right: right = "(pNpS,pSpS)"
    elif "pre_sui_post_non, pre_sui_post_sui" in right: right = "(pSpN,pSpS)"
    return left + right

def significant(a):
    if a > 0.06: return None
    else: return a

def make_graph(df):
    df["item"] = df.index
    row_names = df["item"].tolist()
    sensor = row_names[0].split("_")[0]
    row_names = df["item"].tolist()
    df = df.drop('item', axis = 1).fillna(value = 1)
    df = df.replace(to_replace = 0, value = 1)
    df = df.applymap(significant)
    col_names = list(df.columns.values)
    trace = go.Heatmap(z=df.as_matrix(),
                    x=col_names,
                    y=row_names,
                    colorscale = 'Viridis')
    data=[trace]
    layout = go.Layout(
        title = 'heatmap_week_' + sensor,
        margin = go.Margin(l = 300)
    )
    fig = go.Figure(data=data, layout=layout)
    py.plot(fig, filename='heatmap_week_' + sensor)

def main():
    engine = create_engine('mysql+mysqlconnector://root:23802380@127.0.0.1:3306/resilience', echo=False)
    conn = engine.connect()
    get_data = "select * from `_features_WILCOXON_test_resilience2`"
    df = pd.read_sql(get_data, conn)
    df = df.set_index("item")
    grouped = df.groupby(getsensor)
    
    grouped.apply(make_graph)
    
    conn.close()
    

USER = "root"
PASSWORD = ""
HOST = "127.0.0.1"
DBNAME = ""
main()
