import pandas as pd
from dash import Dash, html
from sqlalchemy import create_engine
import time

# Create a Dash app
app = Dash(__name__)

# Load the data from the database
db_string = "postgresql://postgres:123@db:5432/postgres"
engine = create_engine(db_string)

while True:
    try:
        df = pd.read_sql_table('winmag', engine)
        break
    except:
        time.sleep(60)


# Take the first 10 rows of the dataset
first_10_rows = df.head(10)

# Create a DataTable to display the raw data
app.layout = html.Div([
    html.H1("Data Visualization", style={'text-align': 'center'}),
    html.Table(
        [html.Tr([html.Th(col) for col in first_10_rows.columns])] +

        [html.Tr([html.Td(str(first_10_rows.iloc[i][col])) for col in first_10_rows.columns]) for i in range(len(first_10_rows))]
    )
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0')
