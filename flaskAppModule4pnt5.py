# -*- coding: utf-8 -*-
"""
Created on Sun Nov  4 14:42:27 2018

@author: Swigo
"""

from flask import Flask, jsonify
import pandas as pd


app = Flask(__name__)

@app.route('/trees/<string:spc_common>/<string:boroname>')
def return_trees_data(spc_common,boroname):
        soql_url_health = ('https://data.cityofnewyork.us/resource/nwxe-4ae8.json?' +\
        '$select=health,count(tree_id)' +\
        '&$where=spc_common=\'' + spc_common + '\' AND boroname=\'' + boroname + '\''+\
        '&$group=health').replace(' ', '%20')    
        soql_trees_health = pd.read_json(soql_url_health)
        filtered_data_json = {
 
                'health': soql_trees_health['health'].tolist(),
                'count_tree_id' : soql_trees_health['count_tree_id'].tolist()
    }
        
        return jsonify(filtered_data_json)

if __name__ == '__main__':
    app.run(debug=True)