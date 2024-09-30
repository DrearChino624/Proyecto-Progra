from flask import Flask
from utils.database import db 
from models import Usuario
import os

app = Flask(__name__)  # Corregido __name__

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', 'a_default_secret_key_for_development')

db.init_app(app)

with app.app_context():
    db.create_all()

# Importar el controlador después de que se haya inicializado la app
from controllers.user_controller import user_blueprint
app.register_blueprint(user_blueprint)

if __name__ == "__main__":  # Corregido __name__
    app.run(debug=True)
