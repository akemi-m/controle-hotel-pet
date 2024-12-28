from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from pets import Pets
from tipo import Tipo
from porte import Porte

# CREATE TABLE hospedagempets (
#   id int NOT NULL PRIMARY KEY AUTO_INCREMENT,
#   nome_tutor varchar(50) NOT NULL,
#   tipo_pet varchar(50) NOT NULL,
#   nome_pet varchar(50) NOT NULL,
#   raca_pet varchar(50) NOT NULL,
#   porte_pet varchar(50) NOT NULL,
#   qtd_dias INT NOT NULL,
#   UNIQUE KEY nome_UN (nome_tutor)
# );

engine = create_engine('mysql+mysqlconnector://root:root@localhost/hospedagempets')

contatosPorEmail = { }

print('🐱 Bem-vindo ao Hotel Pet! 🐶')
print('')

def adicionar_pet():
	
	print('Adicionar Pet: ')
	print('')
	
	nome_tutor_input = input('Digite o nome do tutor: ')
	print('')
	if nome_tutor_input == '':
		raise ValueError('O nome do tutor não pode estar vazio.')

	with Session(engine) as sessao:
		tutor = {
			'nome_tutor': nome_tutor_input
		}

		pesquisa_tutor = sessao.execute(text("SELECT nome_tutor FROM pets WHERE nome_tutor = :nome_tutor"), {'nome_tutor': nome_tutor_input}).first()

		if pesquisa_tutor is not None:
			print('')
			raise ValueError(f'Tutor {nome_tutor_input} já cadastrado!')

	aux_tipo = input('Digite o tipo (Gato ou Cachorro): ')
	print('')
	
	tipo_verificado = None
	
	if aux_tipo in ['Gato', 'GATO', 'gato']:
		tipo_verificado = Tipo.GATO
	elif aux_tipo in ['Cachorro', 'cachorro', 'CACHORRO']:
		tipo_verificado = Tipo.CACHORRO
	else:
		raise ValueError('Tipo inválido.')

	tipo_input = Tipo(tipo_verificado)

	nome_pet_input = input('Digite o nome do pet: ')
	print('')
	if nome_pet_input == '':
		raise ValueError('O nome do pet não pode estar vazio.')

	raca_pet_input = input('Digite a raça do pet: ')
	print('')
	if raca_pet_input == '':
		raise ValueError('A raça do pet não pode estar vazia.')

	aux_porte = input('Digite o porte (Pequeno, Médio ou Grande): ')
	print('')
	
	porte_verificado = None
	if aux_porte in ['Pequeno', 'PEQUENO', 'pequeno']:
		porte_verificado = Porte.PEQUENO
	elif aux_porte in ['Médio', 'MÉDIO', 'médio', 'Medio', 'MEDIO', 'medio']:
		porte_verificado = Porte.MEDIO
	elif aux_porte in ['Grande', 'GRANDE', 'grande']:
		porte_verificado = Porte.GRANDE
	else:
		raise ValueError('Porte inválido.')
	
	porte_input = Porte(porte_verificado)

	qtd_dias_input = int(input('Digite a quantidade de dias: '))
	print('')
	if qtd_dias_input == '':
		raise ValueError('A quantidade de dias não pode estar vazia.')

	pet = Pets(nome_tutor_input, tipo_input, nome_pet_input, raca_pet_input, porte_input, qtd_dias_input)

	with Session(engine) as sessao, sessao.begin():
		
		pets = {
			'nome_tutor': pet.nome_tutor,
			'tipo_pet': pet.tipo_pet.value,
			'nome_pet': pet.nome_pet,
			'raca_pet': pet.raca_pet,
			'porte_pet': pet.porte_pet.value,
			'qtd_dias': pet.qtd_dias
		}

		try:
			sessao.execute(
				text("INSERT INTO pets (nome_tutor, tipo_pet, nome_pet, raca_pet, porte_pet, qtd_dias) VALUES (:nome_tutor, :tipo_pet, :nome_pet, :raca_pet, :porte_pet, :qtd_dias)"), pets)
			print('')
			print('✅ Novo cadastro de pet criado com sucesso! ✅')
			print('')

		except IntegrityError as ex:
			print('')
			print(f'❌ O tutor {pet.nome_tutor} já está cadastrado. ❌')
			print('')

def excluir_contato(email):
	with Session(engine) as sessao, sessao.begin():
		parametros = {
			'email1': email
		}

		# Mais informações sobre o método execute e sobre o resultado que ele retorna:
		# https://docs.sqlalchemy.org/en/14/orm/session_api.html#sqlalchemy.orm.Session.execute
		# https://docs.sqlalchemy.org/en/14/core/connections.html#sqlalchemy.engine.Result
		resultado = sessao.execute(text("DELETE FROM pessoa WHERE email = :email1"), parametros)

		if resultado.rowcount == 0:
			print('')
			print(f'E-mail {email} não estava cadastrado.')
			print('')
		else:
			print('')
			print(f'Contato excluído com sucesso!')
			print('')

def editar_contato(email, nome, telefone):
	with Session(engine) as sessao, sessao.begin():
		parametros = {
			'email1': email,
			'nome': nome, 
			'telefone': telefone
		}

		# Mais informações sobre o método execute e sobre o resultado que ele retorna:
		# https://docs.sqlalchemy.org/en/14/orm/session_api.html#sqlalchemy.orm.Session.execute
		# https://docs.sqlalchemy.org/en/14/core/connections.html#sqlalchemy.engine.Result
		resultado = sessao.execute(text("UPDATE pessoa SET nome = :nome, telefone = :telefone WHERE email = :email1"), parametros)

		if resultado.rowcount == 0:
			print('')
			print(f'E-mail {email} não estava cadastrado.')
			print('')
		else:
			print('')
			print(f'Contato editado com sucesso!')
			print('')

def consultar_contato(email):
	with Session(engine) as sessao:
		parametros = {
			'email1': email
		}

		# Mais informações sobre o método execute e sobre o resultado que ele retorna:
		# https://docs.sqlalchemy.org/en/14/orm/session_api.html#sqlalchemy.orm.Session.execute
		# https://docs.sqlalchemy.org/en/14/core/connections.html#sqlalchemy.engine.Result
		pessoa = sessao.execute(text("SELECT id, nome, email, telefone FROM pessoa WHERE email = :email1"), parametros).first()

		if pessoa == None:
			print('')
			print(f'E-mail {email} não encontrada!')
			print('')
		else:
			print('')
			print(f'\nid: {pessoa.id} / nome: {pessoa.nome} / email: {pessoa.email} / telefone: {pessoa.telefone}')
			print('')

def listar_contatos():
	# O with do Python é similar ao using do C#, ou o try with resources do Java.
	# Ele serve para limitar o escopo/vida do objeto automaticamente, garantindo
	# que recursos, como uma conexão com o banco, não sejam desperdiçados!
	with Session(engine) as sessao:
		pessoas = sessao.execute(text("SELECT id, email, nome, telefone FROM pessoa ORDER BY nome"))

		# Como cada registro retornado é uma tupla ordenada, é possível
		# utilizar a forma de enumeração de tuplas:
		for (id, email, nome, telefone) in pessoas:
			print(f'\nid: {id} / email: {email} / nome: {nome} / telefone: {telefone}')

		# Ou, se preferir, é possível retornar cada tupla, o que fica mais parecido
		# com outras linguagens de programação:
		#for pessoa in pessoas:
		#	print(f'\nid: {pessoa.id} / nome: {pessoa.nome} / email: {pessoa.email} / telefone: {pessoa.telefone}')

opcao = 1

while opcao > 0:
	print('''Escolha uma opção:
0 - Sair
1 - Adicionar Pet
2 - Excluir Pet
3 - Editar Pet
4 - Consultar Pet
5 - Listar Pets
''')
	opcao = int(input("Opção: "))

	if opcao == 1:
		try:
			adicionar_pet()
		except ValueError as e:
			print(f'❌ Erro: {e} ❌')
			print('Retornando ao menu principal...')
			print('')

	elif opcao == 2:
		email = input("E-mail: ")
		excluir_contato(email)
	elif opcao == 3:
		email = input("E-mail: ")
		nome = input("Nome: ")
		telefone = input("Telefone: ")
		editar_contato(email, nome, telefone)
	elif opcao == 4:
		email = input("E-mail: ")
		consultar_contato(email)
	elif opcao == 5:
		listar_contatos()
