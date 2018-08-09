from flask_sqlalchemy import SQLAlchemy
import app.app

db = SQLAlchemy()
db.init_app(app)