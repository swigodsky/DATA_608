# -*- coding: utf-8 -*-
"""
Created on Sat Oct  6 21:20:23 2018

@author: Swigo
"""
import pandas as pd
import numpy as np
import dash
import dash_core_components as dcc
import dash_html_components as html
import matplotlib.pyplot as plt

#soql_url_health = ('https://data.cityofnewyork.us/resource/nwxe-4ae8.json?' +\
 #       '$select=health,count(tree_id)' +\
  #      '&$where=spc_common=\'holly\'' +\
   #     '&$group=health').replace(' ', '%20')

#soql_url_health = ('https://data.cityofnewyork.us/resource/nwxe-4ae8.json?').replace(' ', '%20')


#soql_trees_health = pd.read_json(soql_url_health)

#tot = sum(soql_trees_health['count_tree_id'])
#soql_trees_health['proportion_tree'] = soql_trees_health['count_tree_id']/tot

#soql_trees_health
#plt.figure(figsize=(6, 4))
#plt.bar(soql_trees_health['health'], soql_trees_health['proportion_tree'])
#plt.xlabel="Health"
#plt.tight_layout()
#plt.show(block=True)

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
    dcc.Graph(id='Tree_Health')
     
    ]) 
                              
@app.callback(
    dash.dependencies.Output('Tree_Health', 'figure'),
    [dash.dependencies.Input('species-dropdown', 'value'),
    dash.dependencies.Input('borough-dropdown', 'value')])


def update_figure(species_dropdown, borough_dropdown):
  #  filtered_df = soql_trees_health[soql_trees_health.spc_common == selected_species]
   # filtered_df = soql_trees_health[soql_trees_health.borough == boroname]
    
    soql_url_health = ('https://data.cityofnewyork.us/resource/nwxe-4ae8.json?' +\
        '$select=health,count(tree_id)' +\
        '&$where=spc_common=\'' + species_dropdown + '\' AND boroname=\'' + borough_dropdown + '\''+\
        '&$group=health').replace(' ', '%20')
    

  #  soql_url_health = ('https://data.cityofnewyork.us/resource/nwxe-4ae8.json?').replace(' ', '%20')
    soql_trees_health = pd.read_json(soql_url_health)

#    soql_trees_health=soql_trees_health[soql_trees_health.spc_common == species_dropdown]
 #   soql_trees_health=soql_trees_health[soql_trees_health.boroname == borough_dropdown]
  #  soql_trees_health.groupby(['health']) 
   # soql_trees_health=soql_trees_health['health',]

    tot = sum(soql_trees_health['count_tree_id'])
    soql_trees_health['proportion_tree'] = soql_trees_health['count_tree_id']/tot
  
    return { 
            'data': [{'x':soql_trees_health['health'], 'y':soql_trees_health['proportion_tree'], 'type':'bar'}],
            'layout':[{
                    'title':('tree health')
                    }]    
    
    }



if __name__=='__main__':
    app.run_server(debug=True)