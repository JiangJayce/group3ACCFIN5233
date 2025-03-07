from snownlp import SnowNLP
import pandas as pd
import math
import datetime,traceback

def quantilizeSentiments(data):
    try:
        nlp = SnowNLP(data)
        sentimentScore = nlp.sentiments
    except:
        print(traceback.format_exc())
        sentimentScore = None
    return sentimentScore

df = pd.read_csv("data.csv")
sentimentScore_data=[]
title_data=df['title'].tolist()
for i in range(len(title_data)):
    sentimentScore_data.append(quantilizeSentiments(str(title_data[i])))
df['sentimentScore']=sentimentScore_data
df.to_csv("data.csv", index=False)

date_list=df['date'].tolist()
sentimentScore_list=df['sentimentScore'].tolist()
read_list=df['read'].tolist()
reply_list=df['reply'].tolist()
like_list=df['like_count'].tolist()
fans_list=df['fan'].tolist()
date_set=set(date_list)
score_list=[]
for i in date_set:
    pos=neg=num=0
    for j in range(len(date_list)):
        if i==date_list[j]:
            num+=1
            if(sentimentScore_list[j]>0.6):
                pos+=1+math.log(like_list[j]+fans_list[j]+reply_list[j]+1,2)
            if(sentimentScore_list[j]<0.4):
                neg+=1+math.log(like_list[j]+fans_list[j]+reply_list[j]+1,2)
    score=(pos/(pos+neg+0.0001)-0.5)*math.log(num+1,2)
    score_list.append(score)
Score_data={'date':list(date_set),'score':score_list}
df_score=pd.DataFrame(Score_data)
df_score = df_score.sort_values(by='date', ascending=True)
df_score.to_csv("score.csv", index=False)



            

    

