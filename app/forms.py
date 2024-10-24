from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, FileField, FloatField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from datetime import datetime
from flask_login import current_user

from app import db, bcrypt, app
from app.models import Contato, User, MaterialRecebido, MaterialMovimentacao

import os
from werkzeug.utils import secure_filename


class UserForm(FlaskForm):
    usuario = StringField('', validators=[DataRequired()])
    email = StringField('', validators=[DataRequired(), Email()])
    cargo = StringField('', validators=[DataRequired()])
    senha = PasswordField('', validators=[DataRequired()])
    btnSubmit = SubmitField('CADASTRAR')

    def save(self):

        if User.query.filter_by(email=self.email.data).first():
            raise Exception('O usuário já está cadastrado com esse e-mail')

        if not self.email.data.endswith('@storage.com'):
            raise Exception('O e-mail não está liberado')

        senha = bcrypt.generate_password_hash(self.senha.data.encode('utf-8'))
        user = User(
            usuario=self.usuario.data,
            email=self.email.data,
            cargo=self.cargo.data,
            senha=senha
        )
        db.session.add(user)
        db.session.commit()
        return user




class LoginForm(FlaskForm):
    email = StringField('', validators=[DataRequired(),Email()])
    senha = PasswordField('', validators=[DataRequired()])
    btnSubmit = SubmitField('ENTRAR')

    def login(self):

        user= User.query.filter_by(email=self.email.data).first()

        if user:
            if bcrypt.check_password_hash(user.senha , self.senha.data.encode('utf-8')):
                return user
            else:
                 raise Exception('Senha Incorreta!!!!!!!')
        else:
            raise Exception('Usuário inexistente!!!!!!!!!')
        



class MaterialRecebidoForm(FlaskForm):
    nome_produto = StringField('Nome do Produto', validators=[DataRequired()])
    quantidade = FloatField('Quantidade', validators=[DataRequired()])
    data_recebimento = StringField('Data do Recebimento', validators=[DataRequired()])
    descricao_produto = StringField('Descrição do Produto', validators=[DataRequired()])
    tipo_produto = SelectField('Tipo de Produto', choices=[('', 'Selecione o tipo do produto'), ('Limpeza', 'Limpeza'), ('Alimentos', 'Alimentos'), ('Materiais', 'Materiais'), ('Mobília', 'Mobília')], validators=[DataRequired()])  # Novo campo com opção padrão
    recebido_por = StringField('Recebido por', validators=[DataRequired()])
    btnSubmit = SubmitField('Registrar')

    def save(self, user):
        material = MaterialRecebido.query.filter_by(nome_produto=self.nome_produto.data).first()
        if material:
            material.quantidade += self.quantidade.data  
        else:
            material = MaterialRecebido(
                nome_produto=self.nome_produto.data,
                quantidade=self.quantidade.data,
                data_recebimento=datetime.strptime(self.data_recebimento.data, '%d/%m/%Y'),
                descricao_produto=self.descricao_produto.data,
                tipo_produto=self.tipo_produto.data, 
                recebido_por=self.recebido_por.data,
                registrado_por=user.usuario
            )
            db.session.add(material)
        db.session.commit()


class EstoqueDetailForm(FlaskForm):
    destino = StringField('Destino', validators=[DataRequired()])
    quantidade = FloatField('Quantidade a Retirar', validators=[DataRequired()])
    btnSubmit = SubmitField('Enviar')

    def processar_movimentacao(self, material_id):
        obj = MaterialRecebido.query.get(material_id)
        if self.quantidade.data <= obj.quantidade:
            obj.quantidade -= self.quantidade.data
            movimentacao = MaterialMovimentacao(
                material_id=obj.id,
                quantidade=self.quantidade.data,
                destino=self.destino.data,
                movimentado_por=current_user.usuario,
                data_movimentacao=datetime.now(),
                nome_produto=obj.nome_produto,
                tipo_produto=obj.tipo_produto

            )
            db.session.add(movimentacao)
            db.session.commit()
            return True
        else:
            return False