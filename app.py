# -*- coding: utf-8 -*-
"""
Created on Sat Oct  6 21:20:23 2018

@author: Swigo
"""
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html


soql_url = ('https://data.cityofnewyork.us/resource/nwxe-4ae8.json?').replace(' ', '%20')
soql_trees = pd.read_json(soql_url)
species = soql_trees['spc_common'].unique()
borough = soql_trees['boroname'].unique()

app=dash.Dash()
app.layout = html.Div(children=[html.H1('Tree Health'),
    
    dcc.Dropdown(
            id='species-dropdown',
            options=[{'label': i, 'value': i} for i in species],
            value='mulberry'           
            ),
    dcc.Dropdown(
            id='borough-dropdown',
            options=[{'label': x, 'value': x} for x in borough],
            value='Bronx'           
            ),
    dcc.Graph(id='Tree_Health'),
    dcc.Graph(id='Steward') 
    ]) 
                              
@app.callback(
    dash.dependencies.Output('Tree_Health', 'figure'),
    [dash.dependencies.Input('species-dropdown', 'value'),
    dash.dependencies.Input('borough-dropdown', 'value')])



def update_figure(species_dropdown, borough_dropdown):
    
    soql_url_health = ('https://data.cityofnewyork.us/resource/nwxe-4ae8.json?' +\
        '$select=health,count(tree_id)' +\
        '&$where=spc_common=\'' + species_dropdown + '\' AND boroname=\'' + borough_dropdown + '\''+\
        '&$group=health').replace(' ', '%20')

    soql_trees_health = pd.read_json(soql_url_health)

    tot = sum(soql_trees_health['count_tree_id'])
    soql_trees_health['proportion_tree'] = soql_trees_health['count_tree_id']/tot
  
    return { 
            'data': [{'x':soql_trees_health['health'], 'y':soql_trees_health['proportion_tree'], 'type':'bar'}],
             'layout':{
                    'title':'Proportion of Trees By Health',
                    'xaxis':{
                            'title':'Tree Health'
                            },
                    'yaxis':{
                            'title':'Proportion'
                            }  
                  
                    }
    }
@app.callback(
    dash.dependencies.Output('Steward', 'figure'),
    [dash.dependencies.Input('species-dropdown', 'value'),
    dash.dependencies.Input('borough-dropdown', 'value')])
    
def update_steward(species_dropdown, borough_dropdown):  

    soql_url_health = ('https://data.cityofnewyork.us/resource/nwxe-4ae8.json?' +\
        '$select=health,steward,count(tree_id)' +\
        '&$where=spc_common=\'' + species_dropdown + '\' AND boroname=\'' + borough_dropdown + '\''+\
        '&$group=steward,health').replace(' ', '%20')    

    soql_trees_health = pd.read_json(soql_url_health)      

    tot = sum(soql_trees_health['count_tree_id'])
    soql_trees_health['proportion_tree'] = soql_trees_health['count_tree_id']/tot

    soql_trees_health['steward'] = soql_trees_health['steward'].map({'None': 0,'1or2':1,'2':2,'3or4':3,'4orMore':4})    
  
    poor=soql_trees_health.loc[lambda soql_trees_health: soql_trees_health.health =='Poor', :]
    fair=soql_trees_health.loc[lambda soql_trees_health: soql_trees_health.health =='Fair', :]
    good=soql_trees_health.loc[lambda soql_trees_health: soql_trees_health.health =='Good', :]

    return{
           'data': [{'x':poor['steward'], 
                     'y':poor['proportion_tree'],
                     'type':'bar',
                     'name':'Poor Health'
                     },
                    {'x':fair['steward'], 
                     'y':fair['proportion_tree'],
                     'type':'bar',
                     'name':'Fair Health'
                     },
                     {'x':good['steward'], 
                     'y':good['proportion_tree'],
                     'type':'bar',
                     'name':'Good Health'
                     }],
             'layout':{
                    'title':'Relationship Between Stewards and Tree Health',
                    'xaxis':{
                            'title':'Number of Stewards'
                            },
                    'yaxis':{
                            'title':'Proportion'
                            }  
                  
                    }
    
    }

 


if __name__=='__main__':
    app.run_server(debug=True)