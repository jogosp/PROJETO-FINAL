from app import db, login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class Contato(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data_envio = db.Column(db.DateTime, default=datetime.now())
    nome = db.Column(db.String, nullable=True)
    email = db.Column(db.String, nullable=True)
    assunto = db.Column(db.String, nullable=True)
    mensagem = db.Column(db.String, nullable=True)
    respondido = db.Column(db.Integer, default=0)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String, nullable=True)
    email = db.Column(db.String, nullable=True)
    cargo = db.Column(db.String, nullable=True)
    senha = db.Column(db.String, nullable=True)


class MaterialRecebido(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_produto = db.Column(db.String, nullable=False)
    quantidade = db.Column(db.Float, nullable=False)
    data_recebimento = db.Column(db.DateTime, default=datetime.now())
    descricao_produto = db.Column(db.String, nullable=True)
    tipo_produto = db.Column(db.String, nullable=False) 
    recebido_por = db.Column(db.String, nullable=False)
    registrado_por = db.Column(db.String, nullable=False)


class MaterialMovimentacao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    material_id = db.Column(db.Integer, db.ForeignKey('material_recebido.id'), nullable=False)
    quantidade = db.Column(db.Float, nullable=False)
    destino = db.Column(db.String(255), nullable=False)
    movimentado_por = db.Column(db.String(255), nullable=False)
    data_movimentacao = db.Column(db.DateTime, default=datetime.now())
    nome_produto = db.Column(db.String(255), nullable=False) 
    tipo_produto = db.Column(db.String(255), nullable=False) 


