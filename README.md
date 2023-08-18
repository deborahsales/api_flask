# API Usuários

### Atividade para a disciplina de Banco de Dados I

##### API criada utilizando a linguagem python e o framework web Flask.
##### Conexão com uma instância RDS do SGBD Postgresql utilizando a biblioteca psycopg2.
##### Documentação Swagger está disponível na rota "/docs"

- Método POST, na rota "/post", insere uma nova linha na tabela usuários, sendo necessário informar: cpf:int, nome:String, data_nascimento:Date.
- Método GET, na roa "/get", realiza uma operação select na tabela usuários e retorna o resultado, sendo necessário informar: cpf:int


