from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String

# Inicializa la base de datos
db = SQLAlchemy()

class Usuario(db.Model):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    picture = Column(String(200))

    def __repr__(self):
        return f'<Usuario {self.nombre}>'

# Función para inicializar la base de datos
def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()  # Crea las tablas en la base de datos
