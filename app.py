from flask import Flask, request, render_template
import pandas as pd
import os

app = Flask(__name__)

# Load data
stations_df = pd.read_csv('stations.csv')  # Sheet 1
details_df = pd.read_csv('details.csv')    # Sheet 2

@app.route('/')
def home():
    query = request.args.get('search', '').lower()
    filtered = stations_df.copy()
    
    if query:
        filtered = filtered[filtered['Station'].str.lower().str.contains(query)]
    
    return render_template('home.html', stations=filtered.to_dict(orient='records'), query=query)

@app.route('/details/<int:station_id>')
def details(station_id):
    projects = details_df[details_df['ID'] == station_id]
    
    if projects.empty:
        return f"No details found for Station ID {station_id}", 404
    
    return render_template('details.html', projects=projects.to_dict(orient='records'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # default to 5000 if not set
    app.run(host='0.0.0.0', port=port, debug=True)
