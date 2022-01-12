import matplotlib
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from matplotlib import font_manager, rc
matplotlib.use('Agg')
from io import BytesIO
import base64


def art():
    img = BytesIO()
    #0-price, 1-year, 2-date
    art_df = pd.read_csv('static/csv/art.csv') # 천경자 데이터

    #각 년도별 최고 금액
    maxs = art_df['0'].max()
    art_df_group = art_df.groupby('1')
    art_df_group = art_df_group['0'].max()
    art_df_group = art_df_group.reset_index()

    # 천경자 시각화1
    art_df['2'] = pd.to_datetime(art_df['2'])
    maxs = art_df["0"].max()
    plt.figure(facecolor='#ecf1f1')
    ax = plt.axes()
    ax.set_facecolor = ('white')
    plt.scatter(art_df['2'],art_df['0'])
    plt.style.use(['tableau-colorblind10'])
    plt.yticks(np.arange(0,maxs, step=maxs // 10))
    plt.savefig(img, format='png')
    plt.close()
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')

    img = BytesIO()
    # 천경자 시각화2;
    plt.figure(facecolor='#ecf1f1')
    ax = plt.axes()
    ax.set_facecolor = ('white')
    plt.plot(art_df_group['1'],art_df_group['0'])
    plt.style.use(['tableau-colorblind10'])
    plt.yticks(np.arange(0,maxs, step=maxs // 10))
    plt.text(2015,100000000,'X',fontdict={'size':30,'color':'#E27689','weight':'bold'})
    plt.savefig(img, format='png')
    plt.close()
    img.seek(0)
    plot_url2 = base64.b64encode(img.getvalue()).decode('utf8')

    line = []
    line.append(plot_url)
    line.append(plot_url2)
    return line
