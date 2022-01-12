import matplotlib
import pandas as pd
import matplotlib.pyplot as plt
from pandas.io.parsers import read_csv
import seaborn as sns
import numpy as np
from matplotlib import font_manager, rc
matplotlib.use('Agg')
from io import BytesIO
import base64
from wordcloud import WordCloud
from konlpy.tag import Okt
from collections import Counter
import csv


def dance():
  with open('static/csv/dance1.csv', mode='r') as inp:
    reader = csv.reader(inp)
    dict_from_csv = {rows[0]:int(rows[1]) for rows in reader}
  
  img = BytesIO()
  word_cloud = WordCloud(font_path = '/System/Library/Fonts/AppleSDGothicNeo.ttc', colormap = 'OrRd', background_color = 'white')
  wc = word_cloud.generate_from_frequencies(dict_from_csv)
  plt.figure(facecolor='#f5fafa')
  plt.imshow(wc)
  plt.imshow(wc, interpolation = 'bilinear')
  plt.axis('off')
  plt.savefig(img, format='png')
  plt.close()
  img.seek(0)
  plot_url1 = base64.b64encode(img.getvalue()).decode('utf8')


  dance_df = pd.read_csv('static/csv/dance2.csv')
  img = BytesIO()
  dance_df['month'] = dance_df['month']
  plt.figure(facecolor='#f5fafa')
  plt.plot(dance_df.index+1, dance_df['month'], marker = 'o', markersize = 5 ,linestyle = 'dashed', color = 'grey', label = 'Total')
  plt.plot(dance_df.index+1, dance_df['keyword'], marker = 'o', markersize = 5 ,linestyle = 'solid', color = 'red', label = 'Keyword')
  plt.text(7.6,530,'O',fontdict={'size':30,'color':'#45aba6','weight':'bold'})
  plt.text(9.6,690,'O',fontdict={'size':30,'color':'#45aba6','weight':'bold'})
  plt.legend()
  plt.savefig(img, format='png')
  plt.close()
  img.seek(0)
  plot_url2 = base64.b64encode(img.getvalue()).decode('utf8')

  line = []
  line.append(plot_url1)
  line.append(plot_url2)
  
  return line