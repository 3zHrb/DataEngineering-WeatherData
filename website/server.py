from flask import Flask, request, render_template, url_for
import subprocess

app = Flask(__name__, template_folder="templates", static_folder="statics")


@app.route("/", methods=["GET"])
def home():
    return render_template("home.html")


@app.route("/userSubmitCities", methods=["POST"])
def userSubmitCities():
    # cities = request.form['tez']
    # subprocess.Popen(["python", "ETL/WeatherKafkaProducer.py"])
    # subprocess.Popen(["python", "ETL/WeatherKafkaConsumer.py"])
    # fileName = "Running"
    print("we are inside userSubmitCities()")
    submitedCities = request.form["citiesInput"]
    print(submitedCities)

    return render_template("home.html", submitedCities=submitedCities)


# def fileReciver(s3FileName):


if __name__ == "__main__":
    print("Server is running ...")
    app.run(debug=True)
