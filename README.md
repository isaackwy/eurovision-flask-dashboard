# Eurovision Flask Dashboard

### CS50 Final Project
For Harvard [CS50x](https://cs50.harvard.edu/x/2024/)'s final project, I have set up a [Flask](https://palletsprojects.com/p/flask/) dashboard that displays Eurovision Song Contest results. I wanted to learn how to set up [Plotly](https://plotly.com/python/) charts inside a Flask web application. Udacity's data scientist [nanodegree](https://www.udacity.com/course/data-scientist-nanodegree--nd025) program - particularly its web development lesson module - inspired the development of this project.

This dashboard displays the number of times each country has won Eurovision, as well as Eurovision Grand Final contest placements by country. However, the dashboard does not display semi-final contest results. I also have not displayed voting results by jury and televote.

## Libraries Used
1. Flask
2. Numpy
3. Pandas
4. Plotly

This list of libraries is also available in the `requirements.txt` file.

## Instructions (How to Run)
Clone the repo, then run the Flask app.
```
$ git clone https://github.com/isaackwy/eurovision-flask-dashboard.git
$ cd eurovision-flask-dashboard
$ flask run
```

## Project Dataset
[Spijkervet](https://github.com/Spijkervet/) had already prepared a contestants.csv file within her [eurovision-dataset](https://github.com/Spijkervet/eurovision-dataset/) repository. However, since that file only displays contest results up to 2023, I have manually added in results from the 2024 Grand Final.
