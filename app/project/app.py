#flask
from flask import Flask
#views
from view.userAPI import userAPI

app = Flask(__name__)

#route
app.register_blueprint(userAPI)

if __name__ == '__main__':
	app.secret_key = 'super secret key'
	app.config['SESSION_TYPE'] = 'filesystem'
	app.run(host = '0.0.0.0', port = 80, debug = True);