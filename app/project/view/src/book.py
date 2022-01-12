import matplotlib
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from matplotlib import font_manager, rc
matplotlib.use('Agg')
from io import BytesIO
import base64

def book():
    img = BytesIO()
    kyobo_df = pd.read_csv('static/csv/book.csv')
    kyobo_df['price'] = kyobo_df['price'].str.replace(',','').astype('int64')
    kyobo_vis = pd.DataFrame({'price':kyobo_df['price'],'page':kyobo_df['page']})

    kyobo_vis['onepage_price'] = round(kyobo_vis['price']/kyobo_vis['page'])
    kyobo_vis = kyobo_vis.drop(index = kyobo_vis.loc[kyobo_vis.onepage_price >= 10000].index)
    kyobo_vis['onepage_price_class'] = pd.cut(kyobo_vis['onepage_price'], 10, labels=[1,2,3,4,5,6,7,8,9,10])
    sns.set(rc={'axes.facecolor':'#e8edec', 'figure.facecolor':'#e8edec'})
    sns.displot(kyobo_vis, x='onepage_price', hue='onepage_price_class', element='step')
    plt.savefig(img, format='png')
    plt.close()
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')
    return plot_url