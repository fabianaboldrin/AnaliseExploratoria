
# coding: utf-8

# # Primeiramente começamos com uma analise exploratoria dos dados

# In[7]:



import pandas as pd
import numpy

#Ferramentas de visualização

import plotly
from plotly.offline import iplot, init_notebook_mode
init_notebook_mode()
import plotly.plotly as py
import plotly.graph_objs as go


# In[85]:


# Lemos o data frame de registro de viajantes
trips_df = pd.read_csv('/Users/FabianaBoldrin/Documents/Udacity/ndfdsi-bikeshareanalysis/201402_trip_data.csv')

# Lemos o data frame de registro climático
weather_df = pd.read_csv('/Users/FabianaBoldrin/Documents/Udacity/ndfdsi-bikeshareanalysis/201402_weather_data.csv')

# Lemos o data frame de registro de estações
stations_df = pd.read_csv('/Users/FabianaBoldrin/Documents/Udacity/ndfdsi-bikeshareanalysis/201402_station_data.csv')

print(trips_df[['Duration']])


# Para dar início à analise, faremos a limpeza dos dados, mudando o formato de algumas colunas para facilitar a análise propriamente dita.

# In[9]:


# Começa-se a limpeza pelos dados de viagem

#Transforma-se a variável "date" de string para date
trips_df['Start Date'] = pd.to_datetime(trips_df['Start Date'])

# Tira-se as viagens que durem mais que 1 dia (86400 segundos)
trips_df = trips_df[trips_df['Duration'] < 86400]

#Agregamos 3 colunas para uma unica com os seguintes dados: data, hora, ano e dia da semana

trips_df['start_date_only'] = trips_df['Start Date'].dt.date
trips_df['start_hour'] = trips_df['Start Date'].dt.hour
trips_df['start_year'] = trips_df['Start Date'].dt.year
trips_df['start_weekday'] = trips_df['Start Date'].dt.dayofweek


# Fazemos agora o tratamento de dados com o csv de registro climático

# In[13]:


#Transforma-se a variável "date" de string para date
weather_df['Date'] = pd.to_datetime(weather_df['Date']).dt.date


# Convertemos "precipitacion_inches" para um float
weather_df['Precipitation_In '] = weather_df['Precipitation_In '].astype(float)


# Análise inicial

# In[14]:


# Quantidade de viajantes 
len(trips_df)


# In[15]:


# Exemplo de viagem
trips_df.sample()


# In[16]:


# Tipo de dados nas variáveis de trips_df
trips_df.dtypes


# In[17]:


# Agregamos com a coluna em trips com o nome do dia da semana que começou a viagem
dias_da_semana = {
    0: 'Segunda-feira',
    1: 'Terça-feira',
    2: 'Quarta-feira',
    3: 'Quinta-feira',
    4: 'Sexta-feira',
    5: 'Sábado',
    6: 'Domingo'
}

trips_df['start_weekday_name'] = trips_df['start_weekday'].apply(lambda numero: dias_da_semana[numero])
trips_counts_by_day = trips_df['start_weekday_name'].value_counts(sort=False)
trips_counts_by_day = trips_counts_by_day.reindex(['Segunda-feira', 'Terça-feira', 'Quarta-feira', 'Quinta-feira', 'Sexta-feira', 'Sábado', 'Domingo'])


# In[20]:


# Gráfico da quantidade de alugueis de bicicleta por dia da semana
trace = go.Bar(
    x=trips_counts_by_day.index,
    y=trips_counts_by_day.values,
    marker=dict(
        color='#c61136',
        ),
    opacity=0.7
)

data = [trace]
layout = go.Layout(
    title='Quantidade de Bicicletas Alugadas por dia da semana',
    titlefont=dict(
        family='Raleway',
        size=25
    ),
    xaxis=dict(
        title='Dia da semana',
        titlefont=dict(
            family='Raleway',
            size=16
        ),
        tickmode='array',
        tickvals=['Segunda-feira', 'Terça-feira', 'Quarta-feira', 'Quinta-feira', 'Sexta-feira', 'Sábado', 'Domingo']
    ),
    yaxis=dict(
        title='Quantidade de bicicletas alugadas',
        titlefont=dict(
            family='Raleway',
            size=16
        ),
    )
)

figure = go.Figure(data=data, layout=layout)
plotly.offline.iplot(figure)


# Pela análise do grafico, é possivel identificar uma maior quantidade de alugueis nos dias de semana e uma pequena variaçao entre os dias da semana. 

# In[19]:


# Gráfico da quantidade de alugueis de bicicleta por ano
trace = go.Bar(
    x=trips_df['start_year'].value_counts().index,
    y=trips_df['start_year'].value_counts().values,
    marker=dict(
        color='#25823e',
        ),
    opacity=0.7
)

data = [trace]
layout = go.Layout(
    title='Quantidade de Bicicletas Alugadas por Ano',
    titlefont=dict(
        family='Raleway',
        size=25
    ),
    xaxis=dict(
        title='Ano',
        titlefont=dict(
            family='Raleway',
            size=16
        ),
        tickmode='array',
        tickvals=[2013, 2014, 2015]
    ),
    yaxis=dict(
        title='Quantiade de Bicicletas Alugadas',
        titlefont=dict(
            family='Raleway',
            size=16
        ),
    )
)

figure = go.Figure(data=data, layout=layout)
plotly.offline.iplot(figure, filename='Quantidade de Bicicletas Alugadas por Ano')


#     Nosso data set conta com análises feitas do mês 08/2013 a 02/2014, é normal que haja diferença na quantidade de bicicletas alugadas nos dois anos. Porém, podemos fazer uma análise proporcional pela quantidade de meses e tentar predizer se o ano de 2014 superará o ano de 2013 em alugueis (desconsiderando a variável de temporadas). 
#     
#     Arredondaremos o ano de 2013 como contendo 4 meses completos e o ano de 2014 como contendo 2 meses completos. Dessa forma os dados de 2014 deveriam conter pelo menos a metade do valor dos dados de 2013, ja que condizem a metade do tempo aproximadamente.
#     
#     Como os dados de 2014 não correspondem a metade do valor do ano de 2013, podemos esperar que o ano de 2014 tenha uma quantidade menor de alugueis de bicicletas.

# In[22]:


# Quantidade de registros climáticos
len(weather_df)


# In[23]:


#Exemplo de registro climático
weather_df.sample()


# In[24]:


# Tipo de dados nas variáveis de weather_df
weather_df.dtypes


# In[26]:


# Tipos de eventos climáticos possíveis
weather_df.Events.unique()


# In[29]:


# Normalizamos os eventos climáticos
weather_df['Events'] = weather_df['Events'].replace(['rain'],'Rain')
weather_df.Events.unique()


# In[34]:


# Quantidde de estações
stations_df['station_id'].unique()


# In[35]:


# Exemplo de registo de estações
stations_df.sample()


# In[36]:


# Tipos de dados nas vairáveis de stations_df
stations_df.dtypes


# # Aqui começa nossa análise em questao de estações com o objetivo de responder a pergunta de: quais as estaçoes mais populares?

# In[43]:


#Estação mais popular de origem
trips_df['Start Terminal'].value_counts().index[0]


# In[44]:


# Quantidade de viagens iniciadas por terminal
trace = go.Bar(
    x=trips_df['Start Terminal'].value_counts().index,
    y=trips_df['Start Terminal'].value_counts().values,
    marker=dict(
        color='#addd8e',
        ),
    opacity=0.8
)

data = [trace]
layout = go.Layout(
    title='Quantidade de Viagens Iniciadas por Estação',
    titlefont=dict(
        family='Raleway',
        size=25
    ),
    xaxis=dict(
        title='Estações',
        titlefont=dict(
            family='Raleway',
            size=16
        ),
        tickmode='array',
        tickvals=stations_df['station_id'].unique(),
        type="category"
    ),
    yaxis=dict(
        title='Quantidade de Viagens Iniciadas',
        titlefont=dict(
            family='Raleway',
            size=16
        ),
    )
)

figure = go.Figure(data=data, layout=layout)
plotly.offline.iplot(figure, filename='Quantidade de Viagens Iniciadas por Estação')


# In[45]:


# Estação mais popular de destino
trips_df['End Terminal'].value_counts().index[0]


# In[96]:


# Quantidade de viagens finalizadas por estação
trace = go.Bar(
    x=trips_df['End Terminal'].value_counts().index,
    y=trips_df['End Terminal'].value_counts().values,
    marker=dict(
        color='#42f495',
        ),
    opacity=0.8
)

data = [trace]
layout = go.Layout(
    title='Quantidade de Viagens Finalizadas por Estação',
    titlefont=dict(
        family='Raleway',
        size=25
    ),
    xaxis=dict(
        title='Estações',
        titlefont=dict(
            family='Raleway',
            size=16
        ),
        tickmode='array',
        tickvals=stations_df['station_id'].unique(),
        type="category"
    ),
    yaxis=dict(
        title='Quantidade de Viagens Finalizadas',
        titlefont=dict(
            family='Raleway',
            size=16
        ),
    )
)

figure = go.Figure(data=data, layout=layout)
plotly.offline.iplot(figure, filename='Quantidade de Viagens Finalizadas por Estação')


# In[92]:


# Definimos o conceito de popularidade de uma estação como:
# Viagens iniciadas na estação + Viagens finalizadas na estação / total de viagens * 2

total_trips = trips_df.shape[0]
def popularity(started_trips, ended_trips):
    popularity_percentage = (float(started_trips + ended_trips) / float(total_trips * 2)) * 100
    return round(popularity_percentage, 1)

stations = stations_df['station_id'].unique()
popularity_by_station = {}
for station_id in stations:
    started_trips = trips_df[trips_df['Start Terminal']== station_id].shape[0]
    ended_trips = trips_df[trips_df['End Terminal']== station_id].shape[0]
    popularity_by_station[station_id] = popularity(started_trips, ended_trips)

stations_df['popularity'] = stations_df['station_id'].map(popularity_by_station)


# In[95]:


# Porcentagem de popularidade
trace = go.Bar(
    x=stations_df['station_id'].unique(),
    y=stations_df['popularity'].values,
    marker=dict(
        color='#d3c23d',
        ),
    opacity=0.8
)

data = [trace]
layout = go.Layout(
    title='Porcentagem de Popularidade por Estação',
    titlefont=dict(
        family='Raleway',
        size=25
    ),
    xaxis=dict(
        title='Estações',
        titlefont=dict(
            family='Raleway',
            size=16
        ),
        tickmode='array',
        tickvals=stations_df['station_id'].unique(),
        type='category'
    ),
    yaxis=dict(
        title='Porcentagem de Popularidade',
        titlefont=dict(
            family='Raleway',
            size=16
        ),
    )
)

figure = go.Figure(data=data, layout=layout)
plotly.offline.iplot(figure, filename='Porcentagem de Popularidade por Estação')


# In[ ]:




