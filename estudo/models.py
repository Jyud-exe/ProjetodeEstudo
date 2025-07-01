from estudo import db, login_manager
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):       #DECORADOR
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String, nullable=True)
    sobrenome = db.Column(db.String, nullable=True)
    sexo = db.Column(db.String, nullable=True)
    nascimento = db.Column(db.Integer, nullable=True)
    telefone = db.Column(db.Integer, nullable=True)
    email = db.Column(db.String, unique=True, nullable=True)
    senha = db.Column(db.String, nullable=True)
    posts = db.relationship('Post', backref='user', lazy=True)
    post_comentario = db.relationship('PostComentario', backref='user', lazy=True)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow())
    mensagem = db.Column(db.Integer, nullable=True)
    imagem = db.Column(db.Integer, nullable=True, default='default.png')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    comentario = db.relationship('PostComentario', backref='post', lazy=True)

    def resumo_mensagem(self):
        return f"{self.mensagem[:10]}..."
    

class PostComentario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow())
    comentario = db.Column(db.Integer, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=True)
