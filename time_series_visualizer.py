from turtle import color
from matplotlib import dates
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv')
df.set_index('date', inplace = True)

# Clean data
df = df[(df['value'] > df['value'].quantile(0.025)) & (df['value'] < df['value'].quantile(0.975))]


def draw_line_plot():
    # Draw line plot
    fig = plt.figure(figsize=(10,5))

    plt.plot(df.index,df['value'], color='red')
    plt.title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    plt.xlabel('Date')
    plt.ylabel('Page Views')
    plt.gca().xaxis.set_major_locator(dates.MonthLocator(interval=6)) 
    plt.gcf().autofmt_xdate()

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    df_bar.reset_index(inplace=True)
    df_bar['date']=pd.to_datetime(df_bar['date'])
    df_bar['month']= df_bar['date'].dt.month
    df_bar['year']= df_bar['date'].dt.year
  
    # Draw bar plot
    fig = df_bar.groupby(['year', 'month']).mean().unstack().plot(kind='bar', y='value', figsize=(8,6)).figure
    plt.xlabel('Years')
    plt.ylabel('Average Page Views')
    plt.legend(
        ['January','February','March','April','May','June','July',
        'August','September','October','November','December'],title='Months')

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['date']=pd.to_datetime(df_box['date'])
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month']= df_box['date'].dt.month
    df_box.sort_values('month', inplace=True)
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)

    fig,a =  plt.subplots(1,2, figsize=(15,5))
    
    sns.boxplot(data = df_box, x='year', y='value', ax=a[0])
    a[0].set_title('Year-wise Box Plot (Trend)')
    a[0].set_xlabel('Year')
    a[0].set_ylabel('Page Views')

    sns.boxplot(data = df_box, x='month', y='value', ax=a[1])
    a[1].set_title('Month-wise Box Plot (Seasonality)')
    plt.xlabel('Month')
    plt.ylabel('Page Views')


    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig