import jieba
import wordcloud
import pandas as pd

df = pd.read_csv("data.csv")
title_data = df['title'].tolist()
title_data = [str(title) for title in title_data] 
title_text = ' '.join(title_data) 
list_s = jieba.lcut(title_text)
text = ' '.join(list_s)
stopwords = ["是", "的", "了", "啊",'*',"和",'与','在','都','再','已经','将','又','还','就','还','还有','还是','于','吗','也','不','已']
wc = wordcloud.WordCloud(font_path = "/System/Library/Fonts/Supplemental/Songti.ttc",
                         width=1000,
                         height=700,
                         background_color='white',
                         max_words=100,
                         stopwords=stopwords)
wc.generate(text)   
wc.to_file("wordcloud.png")