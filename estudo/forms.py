from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, FileField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from estudo.models import User, Post, PostComentario
from estudo import bcrypt, db, app
from datetime import datetime
import os
from werkzeug.utils import secure_filename

class userform(FlaskForm):
    nome = StringField("Nome", validators=[DataRequired()])
    sobrenome = StringField("Sobrenome", validators=[DataRequired()])
    sexo = StringField("Sexo", validators=[DataRequired()])
    nascimento = StringField("Nascimento", validators=[DataRequired()], render_kw={"placeholder": "DD/MM/AAAA"})
    telefone = StringField("Telefone", validators=[DataRequired()])
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    senha = PasswordField("Senha", validators=[DataRequired()])
    confirma_senha = PasswordField("Confirma senha", validators=[DataRequired(), EqualTo('senha')])
    btnsubmit = SubmitField("Cadastrar")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first() #VERIFICA SE O EMAIL JA ESTA CADASTRADO
        if user and user.is_active:
            raise ValidationError('Email ja cadastrado!')

    def save(self):
        senha = bcrypt.generate_password_hash(self.senha.data.encode('utf-8'))
        novo_usuario = User(
            nome = self.nome.data,
            sobrenome = self.sobrenome.data,
            sexo=self.sexo.data,
            nascimento=self.nascimento.data,
            telefone=self.telefone.data, 
            email = self.email.data,
            senha = senha

            )

        db.session.add(novo_usuario)
        db.session.commit()
        return novo_usuario
    
class loginForm(FlaskForm):
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    senha = PasswordField("Senha", validators=[DataRequired()])
    btnsubmit = SubmitField("Entrar")

    def login(self):
        user = User.query.filter_by(email=self.email.data).first()
        if user:
            if bcrypt.check_password_hash(user.senha, self.senha.data):  
                return user
            else:
                raise Exception('Senha incorreta!')
        else:
            raise Exception('Usuario não encontrado!')
        
class PostForm(FlaskForm):
    mensagem = StringField("Mensagem", validators=[DataRequired()])
    imagem = FileField("Imagem", validators=[DataRequired()])
    botao = SubmitField("Enviar")

    def save(self, user_id):
        imagem = self.imagem.data
        nome_seguro = secure_filename(imagem.filename)
        post = Post(
            mensagem=self.mensagem.data,
            user_id=user_id,
            imagem=nome_seguro
        )
        caminho = os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            app.config['UPLOAD_FILES'],
            'post',
            nome_seguro
        )
        
        imagem.save(caminho)
        db.session.add(post)
        db.session.commit()
        return post


class PostComentarioForm(FlaskForm):
    comentario = StringField("Comentário", validators=[DataRequired()])
    botao = SubmitField("Enviar")

    def save(self, user_id, post_id):
        comentario = PostComentario(
            comentario=self.comentario.data,
            user_id=user_id,
            post_id=post_id
        )
        db.session.add(comentario)
        db.session.commit()
        return comentario
