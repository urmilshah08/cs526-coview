from flask import Flask, render_template

# creates a Flask application, named app
app = Flask(__name__)

@app.route("/")
def initial_route():
    return render_template('index.html')

# run the application
if __name__ == "__main__":
    app.run(debug=True)