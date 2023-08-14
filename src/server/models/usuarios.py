from flask_restx import fields
from src.server.instance import server

cpf = server.api.model('CPF', {
    'cpf': fields.Integer(description='CPF do usuario', required=True),
})

usuario = server.api.model('Usuario', {
    'cpf': fields.Integer(description='CPF do usuario', required=True),
    'nome': fields.String(description='Nome do usuario', required=True),
    'data_nascimento': fields.DateTime(description='Data de nascimento do usuario', required=True, dt_format='iso8601'),
})

class Usuario(fields.Raw):
    def format(self, value):
        return {'cpf': value.cpf, 'nome': value.nome, 'data_nascimento': value.data_nascimento}