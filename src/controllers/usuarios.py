import psycopg2
from flask import jsonify, request
from flask_restx import Resource
from src.server.instance import server
from src.server.models.usuarios import usuario, Usuario, cpf

# Conexão à instância RDS na AWS
url = 'postgres://postgres:postgres@api-deborah.c6u7sarwqno4.us-east-1.rds.amazonaws.com/postgres'
connection = psycopg2.connect(url)

# Manipulação do banco de dados
CREATE_USUARIOS_TABLE = ('''CREATE SCHEMA IF NOT EXISTS api;
                         CREATE TABLE IF NOT EXISTS api.usuarios (cpf INT,
                                                                  nome VARCHAR,
                                                                  data_nascimento DATE,
                                                                  CONSTRAINT pk_cpf PRIMARY KEY (cpf));''')
POST_USUARIO = 'INSERT INTO api.usuarios (cpf, nome, data_nascimento) VALUES (%s, %s, %s)'
GET_USUARIO = 'SELECT * FROM api.usuarios WHERE cpf = %s'

app, api = server.app, server.api

@api.route('/post')
class Post(Resource):
    @api.expect(usuario, validate=True)
    def post(self):
        dados = request.get_json()
        cpf = dados.get('cpf')
        nome = dados.get('nome')
        data_nascimento = dados.get('data_nascimento')
        try:
            with connection:
                with connection.cursor() as cursor:
                    cursor.execute(CREATE_USUARIOS_TABLE)
                    cursor.execute(POST_USUARIO, (cpf, nome, data_nascimento))
            return f'Usuário cadastrado'
        except psycopg2.IntegrityError as e:
            return f'Erro de integridade: {e}'
        except psycopg2.Error as e:
            return f'Erro no banco de dados: {e}'
        except Exception as e:
            return f'Erro de inesperado: {e}'

@api.route('/get')
class Get(Resource):
    @api.expect(cpf, validate=True)
    @api.doc(model=usuario, body=Usuario)
    def get(self):
        dados = request.get_json()
        cpf = dados.get('cpf')
        try:
            with connection:
                with connection.cursor() as cursor:
                    cursor.execute(GET_USUARIO, (cpf,))
                    usuario = cursor.fetchone()
            if usuario == None:
                return f'Usuario {cpf} não encontrado'
            else:
                return jsonify(usuario)
        except psycopg2.IntegrityError as e:
            return f'Erro de integridade: {e}'
        except psycopg2.Error as e:
            return f'Erro no banco de dados: {e}'
        except Exception as e:
            return f'Erro de inesperado: {e}'
       
