#flask
from flask import Flask
from view.mainAPI import mainAPI

app = Flask(__name__)

#route
app.register_blueprint(mainAPI)


if __name__ == '__main__':
	app.run(host = '0.0.0.0', port = 5000);
