# -*- coding: utf-8 -*-
"""
Created on Sat Dec  1 22:53:12 2018

@author: Swigo
"""
import pandas as pd
import plotly.plotly as py
import plotly.graph_objs as go
from plotly import tools
import dash
import dash_core_components as dcc
import dash_html_components as html
import folium
import plotly.tools as tls



rodent = pd.read_csv('Rodent_Inspection.csv')
#gives unique borough results
boro = rodent['BOROUGH'].unique()

#gives unique results of rodent inspections
results = rodent['RESULT'].unique()

folium_map = folium.Map(location=[40.738, -73.98],
                        zoom_start=10.5,
                        tiles="Stamen Toner")


app=dash.Dash()
app.layout = html.Div(children=[html.H1('Rodent Inspections'),
  #  html.Iframe(id='map',width='100%',height='600'), 
    dcc.Dropdown(
            id='borough-dropdown',
            options=[{'label': i, 'value': i} for i in boro],
            value='Bronx'           
            ),

    dcc.Graph(id='rats'), 

    dcc.Dropdown(
            id='result-dropdown',
            options=[{'label': i, 'value': i} for i in results],
            value='Bait applied'           
            ),
            
    dcc.Graph(id='mapnyc')
  # html.Div(id='mapnyc')
  #  html.Iframe(id='map',srcDoc=open('rodent_locations.html','r').read(),width='100%',height='600')
    ]) 

#app.layout = html.Iframe(srcDoc = open('test.html', 'r').read())



@app.callback(
    dash.dependencies.Output('rats', 'figure'),
    [dash.dependencies.Input('borough-dropdown', 'value')])  
  
def update_steward(borough_dropdown):  

    #gives number of each type of rodent sign
  ##  types = rodent.groupby(['RESULT']).size().reset_index(name='counts')
    
    #gives total number of counts
   ## total = rodent.groupby(['RESULT']).size().sum()
    
    #gives proportion of each type of inspection result
   ## types['proportion_result'] = types['counts']/total
    
    rodentboro = rodent.loc[rodent['BOROUGH'] == borough_dropdown]
    borotypes = rodentboro.groupby(['RESULT']).size().reset_index(name='counts')
    
    #gives total number of counts
    borototal = rodentboro.groupby(['RESULT']).size().sum()
    
    #gives proportion of each type of inspection result
    borotypes['proportion_result'] = borotypes['counts']/borototal
        

    return { 
            'data': [{'x':borotypes['RESULT'], 'y':borotypes['counts'], 'type':'bar'}],
             'layout':{
                    'title':'Number of Rodent Inspections By Type',
                    'xaxis':{
                            'title':'Result of Rodent Inspection'
                            },
                    'yaxis':{
                            'title':'Number of Rodent Inspections'
                            }  
                  
                    }
    }
@app.callback(
    dash.dependencies.Output('mapnyc', 'figure'),
    [dash.dependencies.Input('result-dropdown', 'value')]) 


#@app.route('/map')
#def map():
#    global map_obj
#    return map_obj.get_root().render()

def update_map(result_dropdown):  

    rodentresult = rodent.loc[rodent['RESULT'] == result_dropdown] 
    mapbox_access_token = 'pk.eyJ1Ijoic3dpZ29kc2t5IiwiYSI6ImNqcDd0Z3FvMjFzbXIza28xNzl3MTVucmQifQ.S4QVCVp8zHyiJD9meunLEQ'
    
    
   # for item in rodentresult:
   #     popup = folium.Popup([item['LATITUDE'],item['LONGITUDE']],parse_html=True)
   #     marker = folium.Marker(location=[item['LATITUDE'],item['LONGITUDE']],popup=popup)
   #     marker.add_to(folium_map)
   # folium_map.save("rodent_locations.html")
   # tls.get_embed(folium_map)
   # return(folium_map)
    return {'data': [go.Scattermapbox(                    
                    {'lat':rodentresult['LATITUDE'], 'lon':rodentresult['LONGITUDE'], 'mode':'markers'})],
             'layout':{
                     'autosize':True,
                     'hovermode':'closest',
                     'mapbox':dict(
                            accesstoken=mapbox_access_token,
                            bearing=0,
                            center=dict(
                                lat=40.7638,
                                lon=-73.9795
                            ),
                            pitch=0,
                            zoom=10)  
                  
                    }
}


#layout = go.Layout(
#    autosize=True,
#    hovermode='closest',
#    mapbox=dict(
#        accesstoken=mapbox_access_token,
#        bearing=0,
 #       center=dict(
  #          lat=40.7638,
  #          lon=-73.9795
  #      ),
  ##      pitch=0,
    #    zoom=10
   # ),
#)

#fig = dict(data=data, layout=layout)

#py.plot(fig, filename='NYC_map')                    
         #  FigureWidget()

            # two different ways to view f2
#            py.iplot(f2)
         #   f2         
  #  } 

 #   folium_map = folium.Map(location=[40.738, -73.98],
 #                       zoom_start=10.8,
 #                       tiles="CartoDB dark_matter")
 #   marker = folium.CircleMarker(location=[40.738, -73.98])
 #   marker.add_to(folium_map)
    #return{folium_map}
 #   return folium_map.get_root().render()


##try to add another visualizaton - data shader for map of NYC where what is shaded in filtered by 
#result of inspection

if __name__=='__main__':
    app.run_server(debug=True)