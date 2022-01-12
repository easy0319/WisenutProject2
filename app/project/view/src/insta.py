import matplotlib
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from matplotlib import font_manager, rc
matplotlib.use('Agg')
from io import BytesIO
import base64

def insta():
    font_path = '/System/Library/Fonts/AppleSDGothicNeo.ttc'
    fontprop = font_manager.FontProperties(fname=font_path).get_name()
    rc('font',family = fontprop)
    insta_df = pd.read_csv('static/csv/insta.csv')
    insta_df_anal = insta_df.dropna(axis=0)
    insta_grouped = insta_df_anal.groupby('place').count()
    insta_grouped = insta_grouped.reset_index()
    insta_grouped.columns = ['place', 'count']
    insta_top10 = insta_grouped.sort_values('count', ascending=False).head(10)

    insta_top10 = insta_top10.sort_values('place')
    insta_top10['place'][1:2].replace(' ','')
    insta_top10['place'][1:2].replace('-','\n')
    img = BytesIO()
    for i in insta_top10['place']:
      insta_top10.loc[(insta_top10.place == i),'place'] = i.replace(' ','\n')
    explodes =(0, 0.1, 0, 0, 0, 0, 0, 0, 0, 0)
    plt.figure(facecolor='#ecf1f1')
    ax = plt.axes()
    ax.set_facecolor = ('white')
    plt.pie(
        insta_top10['count'],
        startangle=90,
        counterclock=False,
        labels=insta_top10['place'],
        autopct = lambda p : '{:.1f}%'.format(p),
        colors = sns.color_palette('Set2'),
        radius=1.2,
        explode=explodes)
    plt.savefig(img, format='png')
    plt.close()
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')

    return plot_url
