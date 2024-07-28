from flask import Flask, render_template, request
import json
import numpy as np
import pandas as pd
import plotly
import plotly.express as px
import plotly.graph_objects as go

# Configure application
app = Flask(__name__)

# Import data
contestants = pd.read_csv('data/contestants.csv')

@app.route("/")
def overview_of_wins():
    
    # Create copy of 'contestants'
    contestants_copy = contestants
    
    # Get the index (the name of the row) in which Switzerland participated in 1956
    switz_1956_index = contestants_copy['place_final'] \
        .where(contestants_copy['to_country'] == 'Switzerland') \
        .where(contestants_copy['year'] == 1956) \
        .dropna() \
        .index[0]
        
    # Switzerland won Eurovision in 1956 - therefore, impute place_final as 1.0
    contestants_copy.loc[switz_1956_index, 'place_final'] = 1.0
    
    # Get the number of times each country won Eurovision
    winners = contestants_copy['to_country'] \
        .where(contestants_copy['place_final'] == 1.0) \
        .dropna() \
        .sort_values()
    
    # Plot barplot of winners (with x-axis labeled as "Country")
    winners_barplot = px.histogram(winners,
                                x='to_country',
                                labels = {
                                    'to_country': "Country",
                                },
                                title="Eurovision Wins by Country")
    
    # Centre the title
    winners_barplot.update_layout(title_x = 0.5)
    
    # Label y-axis as "Number of wins"
    winners_barplot.update_layout(yaxis_title="Number of Wins")
    
    # Change hover labels
    winners_barplot.update_traces(hovertemplate = "<b>Country: </b> %{x} <br>" +
                                                  "<b>Number of wins: </b> %{y}")
    
    # Increase the height of the barplot
    winners_barplot.update_layout(height=700)
    
    # Display the barplot in the Flask app
    winnersJSON = json.dumps(winners_barplot, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template("overview_of_wins.html", winnersJSON=winnersJSON)


@app.route("/results_by_country", methods=["GET", "POST"])
def results_by_country():
    
    # Create 2nd copy of 'contestants'
    contestants_copy2 = contestants
    
    # Get the index (the name of the row) in which Switzerland participated in 1956
    switz_1956_index = contestants_copy2['place_final'] \
        .where(contestants_copy2['to_country'] == 'Switzerland') \
        .where(contestants_copy2['year'] == 1956) \
        .dropna() \
        .index[0]
        
    # Switzerland won Eurovision in 1956 - therefore, impute place_final as 1.0
    contestants_copy2.loc[switz_1956_index, 'place_final'] = 1.0
    
    # Get the list of all the countries that have participated in Eurovision
    list_of_countries = contestants_copy2['to_country'].unique()
    
    # Sort the list of countries
    list_of_countries.sort()
    
    # Display Albania's results by default.
    # The country shown changes depending on user selection
    if request.method == "POST":
        selected_country = request.form.get("countries")
    else:
        selected_country = 'Albania'
        
    # Get the country's years of participation in Eurovision finals, along with their contest places
    country_finals = contestants_copy2[['year', 'place_final']] \
        .where(contestants_copy2['to_country'] == selected_country) \
        .dropna()

    # Andorra has never competed in a final
    if (selected_country == 'Andorra'):
        country_finals = pd.DataFrame([{'year': np.nan, 'place_final': np.nan}])
    
    # Set the index (row name) of the dataframes as the 'year' column
    country_finals = country_finals.set_index('year')
    
    # Belgium, France, Germany, Italy and the Netherlands submitted two songs in 1956 (the first Eurovision contest).
    # This means that the first 2 rows of country_finals contain the 1956 contest results
    # In addition, every country other than Switzerland received 2nd place
    # Therefore, if the country is Belgium, France, Germany, Italy or Netherlands, drop the first row of country_finals
    if ((selected_country == 'Belgium') or \
        (selected_country == 'France') or \
        (selected_country == 'Germany') or \
        (selected_country == 'Italy') or \
        (selected_country == 'Netherlands')):
        country_finals = country_finals.iloc[1:]
    
    # 'North MacedoniaN.Macedonia' is actually 'North Macedonia'
    contestants_copy2 = contestants_copy2.replace('North MacedoniaN.Macedonia', 'North Macedonia')
    
    # Accordingly, remove 'North MacedoniaN.Macedonia' from the list of countries
    north_macedonia_index = np.where(list_of_countries == 'North MacedoniaN.Macedonia')
    list_of_countries = np.delete(list_of_countries, north_macedonia_index)
    
    # Invert the country's results for visual purposes
    # Formula taken from Atanas Atanasov:
    # https://stackoverflow.com/a/74458979
    country_finals['place_final_inverted'] = abs(country_finals['place_final'] - country_finals['place_final'].max()) + 1
    
    # Calculate country's average placement (unless country is Andorra)
    if (selected_country != 'Andorra'):
        place_final_avg = country_finals['place_final'].mean().round(1)
        place_final_avg_inverted = country_finals['place_final_inverted'].mean()
    else:
        place_final_avg = np.nan
    
    # Plot barplot of results by country
    country_barplot = px.bar(country_finals,
                          x = country_finals.index,
                          y = 'place_final_inverted',
                          labels = {
                              'year': "Year",
                              'place_final_inverted': "Place",
                          },
                          title = "Grand Final Results Over the Years")
    
    # Centre the title
    country_barplot.update_layout(title_x = 0.5)
    
    # Change hover labels
    country_barplot.update_traces(customdata = country_finals['place_final'],
                                  hovertemplate = "<b>Year: </b> %{x} <br>" +
                                                  "<b>Place: </b> %{customdata}")

    # If country is not Andorra:
    # Get the lowest and highest places a country received
    if (selected_country != 'Andorra'):
        lowest_place = int(country_finals['place_final'].max())
        highest_place = int(country_finals['place_final'].min())

        # Change y-axis ticks
        # Set tick intervals to:
        # 1 if the difference between the highest and lowest places is less than 5
        # 2 if the difference between the highest and lowest places is less than 13
        # Otherwise, set tick intervals to 5
        tick_intervals = 1 if (highest_place - lowest_place >= -5) else 2 if (highest_place - lowest_place >= -13) else 5
        country_barplot.update_yaxes(tickvals = list(range(lowest_place, 0, -tick_intervals)),
                                  ticktext = list(range(1, lowest_place + 1, tick_intervals)))
    
        # Change x-axis ticks
        earliest_year = int(country_finals.index.min())
        most_recent_year = int(country_finals.index.max())
        if (most_recent_year - earliest_year <= 5):
            country_barplot.update_xaxes(tickvals = list(range(earliest_year, most_recent_year + 1, 1)))
            
        # Increase the length of the average line (its beginning and endpoint)
        # If the country is San Marino or Slovakia, increase that length by a greater amount
        if (selected_country == 'San Marino') or (selected_country == 'Slovakia'):
            x0 = country_finals.index.min() - 1
            x1 = country_finals.index.max() + 1
        else:
            x0 = country_finals.index.min() - 0.5
            x1 = country_finals.index.max() + 0.5
            
        # Add average line
        country_barplot.add_trace(
            go.Scatter(
                x = [x0, x1],
                y = [place_final_avg_inverted, place_final_avg_inverted],
                customdata = [place_final_avg, place_final_avg],
                mode = 'lines',
                name = 'Average<br>Placement',
                line = dict(dash='dash', color='red'),
                hoveron = "fills",
                hovertemplate = "%{customdata}"     # Hover should not show any text at all; however, custom hovertemplate serves as an extra cautionary measure
            )
        )
        
        # Add legend title
        country_barplot.update_layout(legend_title='<b>Legend</b>')
        
        # Do not show the country's placement (the blue bar) within the legend
        for trace in country_barplot['data']:
            if (trace['name'] == ''): trace['showlegend'] = False

    # Increase the height of the barplot
    country_barplot.update_layout(height=650)
    
    # Display the barplot in the Flask app
    countryJSON = json.dumps(country_barplot, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template("results_by_country.html", countryJSON=countryJSON, countries=list_of_countries, selection=selected_country, place_final_avg=place_final_avg)


@app.route("/about_me")
def about_me():
    
    # Simply return the "About Me" page
    return render_template("about_me.html")
