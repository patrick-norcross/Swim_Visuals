import pandas as pd

import dash
from dash import dcc, Input, Output, html
import plotly.graph_objects as go

#https://docs.google.com/spreadsheets/d/1EbwSzErok2FeK3elyr9y9igBYiQlkQoNWjgUtCB01y4/edit#gid=2117964050

sheet_id = "1EbwSzErok2FeK3elyr9y9igBYiQlkQoNWjgUtCB01y4"

df = pd.read_csv(f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv")


col_rename = ['timestamp','Email','yards_actual','time_zone5','time_zone4','time_zone3','kickyards_comp','pullyards_comp','percieved_effort','avg_sleep',
              'SA_participationdifficulty','SA_reducedtraining','SA_effect_on_perf','SA_extentpain_overusual',
              'NB_participationdifficulty','NB_reducedtraining','NB_effect_on_perf','NB_extentpain_overusual',
              'LB_participationdifficulty','LB_reducedtraining','LB_effect_on_perf','LB_extentpain_overusual',
              'HP_participationdifficulty','HP_reducedtraining','HP_effect_on_perf','HP_extentpain_overusual',
              'TK_participationdifficulty','TK_reducedtraining','TK_effect_on_perf','TK_extentpain_overusual',
              'date','Double'] #new column names

colids = []
for i in (list(range(32))):
    colids.append(df.columns[i])

map = {}
for key in colids:
    for value in col_rename:
        map[key] = value
        col_rename.remove(value)
        break

df.rename(columns=map,inplace=True)
df['date']= pd.to_datetime(df['date']).dt.date
df.dropna(subset=['date'], inplace=True)

df['date'] = pd.to_datetime(df['date']).dt.strftime('%m/%d/%y %H')
df.loc[df['Double'] == 'Second', 'date'] = pd.to_datetime(df['date']) + pd.Timedelta(hours=6)
df.loc[df['Double'] == 'First', 'date'] = pd.to_datetime(df['date']) + pd.Timedelta(hours=0)

df_san = df[df['Email'] == df.Email.unique()[0]]
df_knighte = df[df['Email'] == df.Email.unique()[1]] 


df_san = df_san.copy()
df_san['change_z5'] = df_san['time_zone5'] - df_san['time_zone5'].shift(1)
df_san['change_z4'] = df_san['time_zone4'] - df_san['time_zone4'].shift(1) #2 different ways to do the same thing (changez3 compared to z4/z5)
df_san.loc[:,'change_z3'] = (df_san['time_zone3'] - df_san['time_zone3'].shift(1))
df_san['change_z3'].fillna(0,inplace=True)
df_san['change_z4'].fillna(0,inplace=True)
df_san['change_z5'].fillna(0,inplace=True)

df_knighte = df_knighte.copy()
df_knighte['change_z5'] = df_knighte['time_zone5'] - df_knighte['time_zone5'].shift(1)
df_knighte['change_z4'] = df_knighte['time_zone4'] - df_knighte['time_zone4'].shift(1) #2 different ways to do the same thing (changez3 compared to z4/z5)
df_knighte.loc[:,'change_z3'] = (df_knighte['time_zone3'] - df_knighte['time_zone3'].shift(1))
df_knighte['change_z3'].fillna(0,inplace=True)
df_knighte['change_z4'].fillna(0,inplace=True)
df_knighte['change_z5'].fillna(0,inplace=True)


####
####
####
#APP WITH TABS (THINK OF MORE VISUALS TO ADD TO EACH TAB FOR EACH PERSON)

app = dash.Dash(__name__)   #initialising dash app
server = app.server

def zonetime1():
    fig1 = go.Figure([go.Scatter(x = df_san['date'], y = df_san.iloc[:,3], name = 5),
                     go.Scatter(x = df_san['date'], y = df_san.iloc[:,4], name = 4),
                     go.Scatter(x = df_san['date'], y = df_san.iloc[:,5], name = 3)
                     ])
    fig1.update_layout(title = 'Time in Different Zones - san',
                      xaxis_title = 'Date',
                      yaxis_title = 'Time',
                      legend_title_text='Zone Level'
                      )
    return fig1

def zonechange1():
    fig1 = go.Figure([go.Scatter(x = df_san['date'], y = df_san.iloc[:,32], name = 5),
                     go.Scatter(x = df_san['date'], y = df_san.iloc[:,33], name = 4),
                     go.Scatter(x = df_san['date'], y = df_san.iloc[:,34], name = 3)
                     ])
    fig1.add_hline(y=0, line_width = 0.5, line_dash='dash')
    fig1.update_layout(title = 'Change in time in Different Zones - san',
                      xaxis_title = 'Date',
                      yaxis_title = 'change',
                      legend_title_text='Zone Level'
                      )
    return fig1

    
def zonetime2():
    fig2 = go.Figure([go.Scatter(x = df_knighte['date'], y = df_knighte.iloc[:,3], name = 5),
                     go.Scatter(x = df_knighte['date'], y = df_knighte.iloc[:,4], name = 4),
                     go.Scatter(x = df_knighte['date'], y = df_knighte.iloc[:,5], name = 3)
                     ])
    fig2.update_layout(title = 'Time in Different Zones - knighte',
                      xaxis_title = 'Date',
                      yaxis_title = 'Time',
                      legend_title_text='Zone Level'
                      )


    return fig2 


def zonechange2():
    fig2 = go.Figure([go.Scatter(x = df_knighte['date'], y = df_knighte.iloc[:,32], name = 5),
                     go.Scatter(x = df_knighte['date'], y = df_knighte.iloc[:,33], name = 4),
                     go.Scatter(x = df_knighte['date'], y = df_knighte.iloc[:,34], name = 3)
                     ])
    fig2.add_hline(y=0, line_width = 0.5, line_dash='dash')
    fig2.update_layout(title = 'Change in time in Different Zones - knighte',
                      xaxis_title = 'Date',
                      yaxis_title = 'change',
                      legend_title_text='Zone Level'
                      )
    return fig2


app.layout = html.Div([
    dcc.Tabs(id='tabs', value='tabs1',children=[
        dcc.Tab(label='Sa, N',value='san'),
        dcc.Tab(label='Knight, E',value='knighte')
    ]),
    html.Div(id='tab-content')
])



@app.callback(
    Output('tab-content','children'),
    [Input('tabs','value')]
)

def render_content(tab):
    if tab == 'san':
        return html.Div([
            html.H1(children='Swim Team Visuals'),

            dcc.Graph(
                id='san1',
                figure= zonetime1()
            ), 
            dcc.Graph(
                id='san2',
                figure = zonechange1()
            )
        ], className='san')
    elif tab == 'knighte':
        return html.Div([
            html.H1(children='Swim Team Visuals'),

            dcc.Graph(
                id='knighte1',
                figure= zonetime2()
            ), 
            dcc.Graph(
                id='kngihte2',
                figure = zonechange2()
            )
        ], className='knighte')
    else:
        return html.Div([
            html.H1(children='Swim Team Visuals'),
            html.H2(children='Select Swimmer')
])

if __name__ == '__main__': 
    app.run_server(port=8051) 
