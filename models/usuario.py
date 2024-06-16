from sql_alchemy import banco
from flask import request, url_for
from requests import post

MAILGUN_DOMAIN = 'sandboxbbdc01ddda4d426cad23c623f557af18.mailgun.org'
MAILGUN_API_KEY = '153f7547043e8e5ed15aae1be12a34c8-51356527-639b356a'
FROM_TITLE = 'No reply'
FROM_EMAIL = 'no-reply@restapi.com'

class UserModel(banco.Model):
    __tablename__ = 'usuarios'

    user_id = banco.Column(banco.Integer, primary_key=True)
    login = banco.Column(banco.String(40), nullable=False, unique=True)
    senha = banco.Column(banco.String(40), nullable=False)
    email = banco.Column(banco.String(80), nullable=False, unique=True)
    ativado = banco.Column(banco.Boolean, default=False)

    def __init__(self, login, senha, email, ativado):

        self.login = login
        self.senha = senha
        self.email = email
        self.ativado = ativado
        
    def send_confirmation_email(self):
        # http://127.0.0.1:5000/confirmacao/(user_id)
        link = request.url_root[:-1] + url_for('userconfirm', user_id=self.user_id)
        return post(f'https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages', auth=('api', MAILGUN_API_KEY),
                    data={'from': f'{FROM_TITLE} <{FROM_EMAIL}>', 
                          'to': self.email,
                          'subject':'Confirmação de Cadastro',
                          'text': f'Confirme seu cadastro clicando no link a seguir: {link}',
                          'html': f'<html><p>\
                            Confirme seu cadastro clicando no link a seguir: <a href="{link}">CONFIRMAR EMAIL</a>\
                                </p></html>'})
        
        

    def json(self):
        return {
            'user_id': self.user_id,
            'login': self.login,
            'email': self.email,
            'ativado': self.ativado
        }


    @classmethod
    def find_user(cls, user_id):
        user = cls.query.filter_by(user_id=user_id).first() # SELECT * FROM hoteis WHERE user_id = $user_id LIMIT 1;
        if user:
            return user
        return None
    
    @classmethod
    def find_by_login(cls, login):
        user = cls.query.filter_by(login=login).first() # SELECT * FROM hoteis WHERE user_id = $user_id LIMIT 1;
        if user:
            return user
        return None
    
    @classmethod
    def find_by_email(cls, email):
        user = cls.query.filter_by(email=email).first() # SELECT * FROM hoteis WHERE user_id = $user_id LIMIT 1;
        if user:
            return user
        return None
    
    def save_user(self):
        banco.session.add(self)
        banco.session.commit()

    def delete_user(self):
        banco.session.delete(self)
        banco.session.commit()