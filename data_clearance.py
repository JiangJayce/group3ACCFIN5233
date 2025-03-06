import pandas as pd
df = pd.read_csv("data.csv")

title_data = df["title"].str.replace("_财富号_东方财富网", "", regex=False)
title_data = df["title"].str.replace("股吧_东方财富网股吧", "", regex=False)
title_data = df["title"].str.replace("_上证指数(zssh000001)", "", regex=False)

date_data=df['date']
date_list = date_data.tolist()
for i in range(len(date_list)):
    date_list[i] = date_list[i].split(" ")[0]
    if date_list[i][:2] =='01'or date_list[i][:2] =='02'or date_list[i][:2] =='03':
        date_list[i] = '2025-'+date_list[i][2:]
    else:
        date_list[i] = '2024-'+date_list[i][2:]

like_data = df["like_count"]
like_list = like_data.tolist()
for i in range(len(like_list)):
    if like_list[i]=='点赞':
        like_list[i]='0'

df["like_count"] = like_list
df["title"] = title_data
df["date"] = date_list
df['date'] = pd.to_datetime(df['date'], errors='coerce')
df = df.sort_values(by='date', ascending=True)
df.to_csv("data.csv", index=False)
    