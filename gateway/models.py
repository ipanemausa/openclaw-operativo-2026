from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSONB

db = SQLAlchemy()

class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(100), index=True)
    agent = db.Column(db.String(100))
    role = db.Column(db.String(50))
    content = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Sale(db.Model):
    __tablename__ = 'sales'
    id = db.Column(db.Integer, primary_key=True)
    producto = db.Column(db.String(200))
    cantidad = db.Column(db.Integer, default=1)
    precio_unitario = db.Column(db.Numeric(10, 2), default=0)
    total = db.Column(db.Numeric(10, 2), default=0)
    cliente = db.Column(db.String(200))
    canal_venta = db.Column(db.String(100))
    notas = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200))
    categoria = db.Column(db.String(100))
    material = db.Column(db.String(100))
    precio = db.Column(db.Numeric(10, 2), default=0)
    inventario = db.Column(db.Integer, default=0)
    descripcion = db.Column(db.Text)
    canal = db.Column(db.String(100))
    activo = db.Column(db.Boolean, default=True)

class Cotizacion(db.Model):
    __tablename__ = 'cotizaciones'
    id = db.Column(db.Integer, primary_key=True)
    cliente_nombre = db.Column(db.String(255))
    cliente_email = db.Column(db.String(255))
    tipo_pieza = db.Column(db.String(100))
    material = db.Column(db.String(100))
    ocasion = db.Column(db.String(100))
    presupuesto = db.Column(db.String(50))
    descripcion = db.Column(db.Text)
    referencias = db.Column(db.Text)
    clasificacion = db.Column(JSONB)
    propuesta = db.Column(db.Text)
    estado = db.Column(db.String(50), default='recibida')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
