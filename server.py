from flask import Flask, render_template, request
import requests

# creates a Flask application, named app
app = Flask(__name__)

@app.route("/")
def initial_route():
    return render_template('index.html')

@app.route("/state-insights")
def state_insights():
    result = {}
    state = str(request.args.get('state'))
    timeseries = requests.get('https://api.covidactnow.org/v2/state/'+state+'.timeseries.json?apiKey=7c46a86300384a39899b7aa0d60be10f').json()['metricsTimeseries']
    result['timeseries'] = timeseries
    counties = requests.get('https://api.covidactnow.org/v2/county/'+state+'.json?apiKey=7c46a86300384a39899b7aa0d60be10f').json()
    result['counties'] = sorted(counties, key= lambda x: x['metrics']['caseDensity'], reverse=True)
    result['vaccinatedLastWeek'] = abs(timeseries[len(timeseries) - 2]['vaccinationsCompletedRatio'] - timeseries[len(timeseries) - 9]['vaccinationsCompletedRatio'])
    result['vaccinatedLastLastWeek'] = abs(timeseries[len(timeseries) - 16]['vaccinationsCompletedRatio'] - timeseries[len(timeseries) - 9]['vaccinationsCompletedRatio'])
    result['vaccinatedInitiatedLastWeek'] = abs(timeseries[len(timeseries) - 2]['vaccinationsCompletedRatio'] - timeseries[len(timeseries) - 9]['vaccinationsInitiatedRatio'])
    result['vaccinatedInitiatedLastLastWeek'] = abs(timeseries[len(timeseries) - 16]['vaccinationsCompletedRatio'] - timeseries[len(timeseries) - 9]['vaccinationsInitiatedRatio'])
    result['totalVaccinated'] = timeseries[len(timeseries) - 2]['vaccinationsCompletedRatio']
    weeks_to_finish = 1
    while True:
        if result['totalVaccinated'] + (weeks_to_finish * result['vaccinatedLastWeek']) >= .70:
            break
        weeks_to_finish += 1
    result['weeksToFinish'] = weeks_to_finish
    return result
# run the application
if __name__ == "__main__":
    app.run(debug=True)