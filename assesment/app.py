from flask import Flask
from expenses.routes import exp_bp
from auth.routes import auth_bp
from flask_jwt_extended import JWTManager
from datetime import timedelta
app = Flask(__name__)
app.register_blueprint(exp_bp)
app.register_blueprint(auth_bp)


app.config["JWT_SECRET_KEY"] = "SUPER_SECRET_KEY"

app.config["JWT_TOKEN_LOCATION"] = ["cookies"]

app.config["JWT_COOKIE_CSRF_PROTECT"] = False

app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=120) 

jwt = JWTManager(app)



if __name__ == '__main__':
    app.run(debug=True)
