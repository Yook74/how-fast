import flask
import maintain_json

maintain_json.start_maintence()

application = flask.Flask(__name__)

@application.route('/')
def graph():
    return flask.render_template("speed_graph.html")

@application.route('/speed-data')
def speed_data():
    with open('speed_data.json', 'r') as speed_file:
        speed_data_str = speed_file.read()

    return flask.Response(speed_data_str, mimetype='application/json') 

if __name__ == '__main__':
    application.run("0.0.0.0", port=80)
