from estudo.models import User, Post
from estudo import db
from estudo.forms import userform, loginForm, PostForm, PostComentarioForm
from estudo import app
from flask import render_template, url_for, request, redirect
from flask_login import login_user, logout_user, current_user, login_required


@app.route('/', methods=['GET', 'POST'])    
def home():
    form = loginForm()
    if form.validate_on_submit():
        user = form.login()
        login_user(user, remember=True)
    return render_template('index.html', form=form)


@app.route('/revisao')
@login_required
def revisao():
    return render_template('revisão.html')


@app.route('/sair')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/novo", methods=['GET', 'POST'])
@login_required
def PostNovo():
    form = PostForm()
    if form.validate_on_submit():
        form.save(current_user.id)
        return redirect(url_for('home'))
    return render_template('Post_Novo.html', form=form)


@app.route('/lista')
@login_required
def lista():
    pesquisa = request.args.get('pesquisa', '')
    if pesquisa != '':
        dados = User.query.filter_by(nome=pesquisa).all()
    else:
        dados = User.query.all()
    dados_filtrados = [x for x in dados if x.nome is not None]
    dados_ordenados = sorted(dados_filtrados, key=lambda x: x.nome.lower())
    context = {'dados': dados_ordenados}
    return render_template("lista.html", context=context)


@app.route('/contato/<int:id>/')
@login_required
def contatoDetail(id):
    obj = User.query.get(id)
    return render_template('contatodetail.html', obj=obj)


@app.route('/post/<int:id>', methods=['GET', 'POST'])
@login_required
def PostDetail(id):
    post = Post.query.get(id)
    form = PostComentarioForm()
    if form.validate_on_submit():
        form.save(current_user.id, id)
        return redirect(url_for('PostDetail', id=id))
    return render_template('Post.html', post=post, form=form)


@app.route('/cadastro/', methods=['GET', 'POST'])
def cadastro():
    form = userform()
    if form.validate_on_submit():
        user = form.save()
        login_user(user, remember=True)
        return redirect(url_for('home'))
    return render_template('cadastro.html', form=form)

@app.route('/ListaPost')
@login_required
def listaPost():
    posts = Post.query.all()
    return render_template('PostLista.html', posts=posts)
