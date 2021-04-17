#pip install plotly


#Load the required libraries 
import plotly as py
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
from plotly.subplots import make_subplots

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# %matplotlib inline
import seaborn as sns
import math
import random

# color pallette
cnf = '#393e46' # confirmed - grey
dth = '#ff2e63' # death - red
rec = '#21bf73' # recovered - cyan
act = '#fe9801' # active case - yellow

#to hide warnings
import warnings
warnings.filterwarnings('ignore')

corona_confirmed_df = pd.read_csv("  . ./csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv")
corona_deaths_df = pd.read_csv("  . ./CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv")
corona_recovered_df =pd.read_csv("  . ./CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv")

corona_confirmed_df.head()

corona_confirmed_df = corona_confirmed_df.melt(id_vars=['Province/State','Country/Region','Lat','Long'])

corona_confirmed_df = corona_confirmed_df.rename({'variable':'Date','value':'Confirmed'}, axis ='columns')

corona_confirmed_df.head()

corona_deaths_df.head()

corona_deaths_df = corona_deaths_df.melt(id_vars=['Province/State','Country/Region','Lat','Long'])

corona_deaths_df = corona_deaths_df.rename({'variable':'Date','value':'Deaths'}, axis ='columns')

corona_deaths_df.head()

corona_recovered_df.head()

corona_recovered_df = corona_recovered_df.melt(id_vars=['Province/State','Country/Region','Lat','Long'])

corona_recovered_df = corona_recovered_df.rename({'variable':'Date','value':'Recovered'}, axis ='columns')

corona_recovered_df.head()

combined_df = [corona_confirmed_df,corona_deaths_df,corona_recovered_df]
combined_df = [df.set_index(['Province/State','Country/Region','Lat','Long', 'Date'])for df in combined_df]
combined_df = combined_df[0].join(combined_df[1:])

combined_df = combined_df.reset_index()

combined_df.head()

combined_df.count()

combined_df['Recovered'] = combined_df['Recovered'].fillna(0)
combined_df['Deaths'] = combined_df['Deaths'].fillna(0)

#active = confirmed — deaths — recovered
combined_df['Active'] = combined_df['Confirmed'] - combined_df['Deaths'] - combined_df['Recovered']

combined_df = combined_df.rename({'Country/Region':'Country'}, axis ='columns')
combined_df = combined_df.rename({'Province/State':'State'}, axis ='columns')

combined_df['State'] = combined_df['State'].fillna("Unknown")

#combined_df = combined_df.drop('Province/State', 1)

combined_df[['Lat','Long', 'Confirmed','Deaths', 'Recovered', 'Active']] = combined_df[['Lat','Long', 'Confirmed','Deaths', 'Recovered', 'Active']].apply(pd.to_numeric)

combined_df[['Date']] = combined_df[['Date']].apply(pd.to_datetime)

combined_df.head()

"""#Plotting worldwide confirmed, deaths and recovered cases"""

Cases_perday_till_date  = combined_df.groupby('Date')['Confirmed','Deaths', 'Recovered'].max()
Cases_perday_till_date =Cases_perday_till_date.reset_index()
pd.set_option('float_format', '{:f}'.format)
Cases_perday_till_date.describe()

confirmed_cases = combined_df.groupby('Date').sum()['Confirmed'].reset_index()
deaths_cases = combined_df.groupby('Date').sum()['Deaths'].reset_index()
recovered_cases = combined_df.groupby('Date').sum()['Recovered'].reset_index()

fig = go.Figure()
fig.add_trace(go.Scatter(x= confirmed_cases['Date'], y =confirmed_cases['Confirmed'], 
                         mode = 'lines+markers', name = 'Confirmed', line= dict(color= "Orange", width=2)))

fig.add_trace(go.Scatter(x= recovered_cases['Date'], y =recovered_cases['Recovered'], 
                         mode = 'lines+markers', name = 'Recovered', line= dict(color= "Green", width=2)))

fig.add_trace(go.Scatter(x= deaths_cases['Date'], y = deaths_cases['Deaths'],
                         mode = 'lines+markers', name = 'Deaths', line= dict(color= "Red", width=2)))

fig.update_layout(title = 'Worldwide COVID-19 cases status', xaxis_tickfont_size = 13, yaxis = dict(title = 'Number of cases'))
fig.update_layout(height=400, width=900)
fig.show()

"""#Plot cases over the time with area plot"""

temp = combined_df.groupby('Date')['Confirmed','Deaths', 'Recovered', 'Active'].sum().reset_index()
temp = temp[temp['Date']==max(temp['Date'])].reset_index(drop = True)
tm = temp.melt(id_vars = 'Date', value_vars = ['Confirmed','Deaths', 'Recovered', 'Active'])

labels = tm['variable']
values = tm['value']
fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.5)])
fig.update_layout(autosize=False,width=800,height=500,margin=dict(l=50,r=50,b=100,t=100,pad=4))
fig.update_layout(title = 'COVID-19 cases pie chart')
fig.show()

temp = combined_df.groupby('Date')['Confirmed','Deaths', 'Recovered', 'Active'].sum().reset_index()
tm = temp.melt(id_vars = 'Date', value_vars = ['Confirmed','Deaths', 'Recovered', 'Active'], 
               var_name = 'Cases', value_name = 'Count')
fig = px.area(tm, x = 'Date', y = 'Count', color= 'Cases', 
              title="COVID-19 cases over time", color_discrete_sequence= [cnf,dth,rec,act])
fig.update_layout(xaxis_rangeslider_visible=True)
fig.update_layout(height=500, width=900)
fig.show()

"""#Plotting the worst-hit countries"""

country_df = combined_df.groupby("Country")['Confirmed','Deaths','Recovered'].sum().reset_index()
country_df.head()

#Worst hit countries
top_10_Confirmed_cases = country_df.sort_values(by=['Confirmed'],ascending=False).head(10)
fig = px.scatter(top_10_Confirmed_cases, x= "Country", y = "Confirmed", size = "Confirmed",
                  color = "Country", hover_name = "Country", size_max = 60)
fig.update_layout(title = 'Top 10 worst hit countries')
fig.update_layout(height=400, width=1000)
fig.show()

#worst affected countries 
top_10_deaths_cases = country_df .sort_values(by=['Deaths'],ascending=False).head(10)
fig = px.bar(top_10_deaths_cases , x= "Country", y = "Deaths", color = "Country")
fig.update_layout(title = 'Top 10 affected countries')
fig.update_layout(height=400, width=1000)
fig.show()

"""#Line plot of Confirmed, deaths and recovered cases"""

country_daywise_df = combined_df.groupby(["Country", "Date"])['Confirmed','Deaths','Recovered'].sum().reset_index()
country_daywise_df.head()

fig = px.line(country_daywise_df, x = 'Date', y= 'Confirmed', color ='Country', 
              title= 'confirmed', color_discrete_sequence=px.colors.cyclical.mygbm)
fig.update_layout(height=800, width=1000)
fig.show()

"""#Cases density animation on world map"""

figure = px.choropleth(combined_df,locations='Country', locationmode='country names', color='Confirmed', hover_name='Country', 
                       color_continuous_scale=px.colors.sequential.Plasma, range_color=[1,1000000],title='Countries with Confirmed cases')
figure.update_layout(height=600, width=1000)
figure.show()

#Date is to be organized by week.
combined_df = combined_df[combined_df.Date.dt.weekday == 6].copy()
combined_df['Week'] = combined_df['Date'].dt.isocalendar()['week']

fig = px.density_mapbox( combined_df, lat = 'Lat', lon = 'Long', hover_name = 'Country',
                        hover_data = ['Confirmed', 'Recovered', 'Deaths'],
                        animation_frame = 'Week',color_continuous_scale='Portland',radius=5, zoom = 0)
fig.update_layout(title = 'Worldwide COVID-19 evolution with time laps')
fig.update_layout(mapbox_style = 'open-street-map',mapbox_center_lon = 0)
fig.update_layout(height=800, width=1000)
fig.show()
