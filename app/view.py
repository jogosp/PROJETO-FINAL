from wtforms import ValidationError
from app import app, db
from flask import render_template, url_for, request, redirect, flash, make_response
from app.forms import UserForm, LoginForm, MaterialRecebidoForm, EstoqueDetailForm
from app.models import Contato, User, MaterialRecebido, MaterialMovimentacao
from flask_login import login_user, logout_user, current_user, login_required
from datetime import datetime
from io import BytesIO
from reportlab.lib.pagesizes import letter, landscape
from reportlab.pdfgen import canvas
from reportlab.lib import colors

@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/cadastro/', methods=['GET', 'POST'])
def cadastro():
    form = UserForm()
    if form.validate_on_submit():
        try:
            user = form.save()
            login_user(user, remember=True)
            
            return redirect(url_for('homepage'))
        except Exception as e: 
            flash(str(e), 'error')
    return render_template('cadastro.html', form=form)

@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        try:
            user = form.login()
            login_user(user, remember=True)

            return redirect(url_for('homepage'))
        except Exception as e:
            flash(str(e), 'error')
    return render_template('login.html', form=form)

@app.route('/home_estoque/')
@login_required
def home_estoque():
    return render_template('home_estoque.html')

@app.route('/estoque_limpeza/')
@login_required
def estoquelimpeza():
    estoque = MaterialRecebido.query.filter_by(tipo_produto='Limpeza').all()
    return render_template('limpeza.html', estoque= estoque)

@app.route('/estoque_alimentos/')
@login_required
def estoquealimentos():
    estoque = MaterialRecebido.query.filter_by(tipo_produto='Alimentos').all()
    return render_template('alimentos.html', estoque=estoque)

@app.route('/estoque_materiais/')
@login_required
def estoquemateriais():
    estoque = MaterialRecebido.query.filter_by(tipo_produto='Materiais').all()
    return render_template('materiais.html', estoque=estoque)

@app.route('/estoque_mobilia/')
@login_required
def estoquemobilia():
    estoque = MaterialRecebido.query.filter_by(tipo_produto='Mobília').all()
    return render_template('mobilia.html', estoque=estoque)

@app.route('/recebidos/', methods=['GET', 'POST'])
@login_required
def recebidos():
    form = MaterialRecebidoForm()
    if form.validate_on_submit():
        try:
            form.save(current_user)
            return redirect(url_for('recebidos'))
        except ValueError as e:
            return render_template('Erro.html')

    return render_template('recebidos.html', form=form)

@app.route('/estoque/<int:id>', methods=['GET', 'POST'])
@login_required
def estoqueDetail(id):
    obj = MaterialRecebido.query.get(id)
    form = EstoqueDetailForm()
    if form.validate_on_submit():
        if form.processar_movimentacao(id):
            return redirect(url_for('sucesso'))

        else:
            flash('Quantidade insuficiente no estoque!', 'danger')
    return render_template('estoque_detail.html', obj=obj, form=form)

@app.route('/sucesso/')
@login_required
def sucesso():
    return render_template('sucesso.html')

@app.route('/historico_movimentacoes/', methods=['GET', 'POST'])
@login_required
def historico_movimentacoes():
    query = request.args.get('query')
    filter_by = request.args.get('filter_by')

    if query:
        if filter_by == 'nome_produto':
            movimentacoes = MaterialMovimentacao.query.filter(MaterialMovimentacao.nome_produto.ilike(f'%{query}%')).order_by(MaterialMovimentacao.data_movimentacao.desc()).all()
        elif filter_by == 'tipo_produto':
            movimentacoes = MaterialMovimentacao.query.filter(MaterialMovimentacao.tipo_produto.ilike(f'%{query}%')).order_by(MaterialMovimentacao.data_movimentacao.desc()).all()
        elif filter_by == 'destino':
            movimentacoes = MaterialMovimentacao.query.filter(MaterialMovimentacao.destino.ilike(f'%{query}%')).order_by(MaterialMovimentacao.data_movimentacao.desc()).all()
        elif filter_by == 'movimentado_por':
            movimentacoes = MaterialMovimentacao.query.filter(MaterialMovimentacao.movimentado_por.ilike(f'%{query}%')).order_by(MaterialMovimentacao.data_movimentacao.desc()).all()
        elif filter_by == 'data_movimentacao':
            try:
                date_obj = datetime.strptime(query, '%d/%m/%Y')
                movimentacoes = MaterialMovimentacao.query.filter(db.func.date(MaterialMovimentacao.data_movimentacao) == date_obj.date()).order_by(MaterialMovimentacao.data_movimentacao.desc()).all()
            except ValueError:
                movimentacoes = []  
        else:
            movimentacoes = MaterialMovimentacao.query.order_by(MaterialMovimentacao.data_movimentacao.desc()).all()
    else:
        movimentacoes = MaterialMovimentacao.query.order_by(MaterialMovimentacao.data_movimentacao.desc()).all()

    return render_template('historico_movimentacoes.html', movimentacoes=movimentacoes)

@app.route('/gerar_relatorio/')
@login_required
def gerar_relatorio():
    query = request.args.get('query')
    filter_by = request.args.get('filter_by')

    if query:
        if filter_by == 'nome_produto':
            movimentacoes = MaterialMovimentacao.query.filter(MaterialMovimentacao.nome_produto.ilike(f'%{query}%')).order_by(MaterialMovimentacao.data_movimentacao.desc()).all()
        elif filter_by == 'tipo_produto':
            movimentacoes = MaterialMovimentacao.query.filter(MaterialMovimentacao.tipo_produto.ilike(f'%{query}%')).order_by(MaterialMovimentacao.data_movimentacao.desc()).all()
        elif filter_by == 'destino':
            movimentacoes = MaterialMovimentacao.query.filter(MaterialMovimentacao.destino.ilike(f'%{query}%')).order_by(MaterialMovimentacao.data_movimentacao.desc()).all()
        elif filter_by == 'movimentado_por':
            movimentacoes = MaterialMovimentacao.query.filter(MaterialMovimentacao.movimentado_por.ilike(f'%{query}%')).order_by(MaterialMovimentacao.data_movimentacao.desc()).all()
        elif filter_by == 'data_movimentacao':
            try:
                date_obj = datetime.strptime(query, '%d/%m/%Y')
                movimentacoes = MaterialMovimentacao.query.filter(db.func.date(MaterialMovimentacao.data_movimentacao) == date_obj.date()).order_by(MaterialMovimentacao.data_movimentacao.desc()).all()
            except ValueError:
                movimentacoes = []
        else:
            movimentacoes = MaterialMovimentacao.query.order_by(MaterialMovimentacao.data_movimentacao.desc()).all()
    else:
        movimentacoes = MaterialMovimentacao.query.order_by(MaterialMovimentacao.data_movimentacao.desc()).all()

    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=landscape(letter))

    left_margin = 50
    top_margin = 550
    max_line_length = 120  
    line_height = 20  

    pdf.drawString(left_margin, top_margin, "Relatório de Movimentações")

    y = top_margin - 50

    def split_text(text, max_length):

        lines = []
        while len(text) > max_length:
            space_index = text.rfind(' ', 0, max_length)
            if space_index == -1:
                space_index = max_length
            lines.append(text[:space_index])
            text = text[space_index:].lstrip()
        lines.append(text)
        return lines

    for movimentacao in movimentacoes:
        texto = f"PRODUTO: {movimentacao.nome_produto}. TIPO: {movimentacao.tipo_produto}. QNTD: {movimentacao.quantidade}. DESTINO: {movimentacao.destino}. RETIRADO POR: {movimentacao.movimentado_por}. DATA: {movimentacao.data_movimentacao.strftime('%d/%m/%Y %H:%M')}"
        
        lines = split_text(texto, max_line_length)
        for line in lines:
            pdf.drawString(left_margin, y, line)
            y -= line_height
        
        y -= 10 

    pdf.showPage()
    pdf.save()

    buffer.seek(0)
    return make_response(buffer.read(), {'Content-Type': 'application/pdf', 'Content-Disposition': 'inline; filename=relatorio_movimentacoes.pdf'})




@app.route('/sair/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('homepage'))

