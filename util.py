from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from pets import Pets
from tipo import Tipo
from porte import Porte
from hospedado import Hospedado
from resposta import Resposta

engine = create_engine('mysql+mysqlconnector://root:root@localhost/hotel-pet')

contatosPorEmail = { }

def adicionar_pet():
	
	print('')
	print('Adicionar Pet: ')
	print('')
	
	nome_tutor_input = input('    Nome do tutor: ')
	print('')

	with Session(engine) as sessao:
		if nome_tutor_input == '':
			raise ValueError('O nome do tutor não pode estar vazio.')
		
		pesquisa_tutor = sessao.execute(text("SELECT nome_tutor FROM pets WHERE nome_tutor = :nome_tutor"), {'nome_tutor': nome_tutor_input}).first()

		if pesquisa_tutor is not None:
			print('')
			raise ValueError(f'Tutor {nome_tutor_input} já cadastrado!')

	aux_tipo = input('    Tipo do pet (Gato ou Cachorro): ')
	print('')
	
	tipo_verificado = None
	
	if aux_tipo in ['Gato', 'GATO', 'gato']:
		tipo_verificado = Tipo.GATO
	elif aux_tipo in ['Cachorro', 'cachorro', 'CACHORRO']:
		tipo_verificado = Tipo.CACHORRO
	elif aux_tipo == '':
		raise ValueError('O tipo do pet não pode estar vazio.')
	else:
		raise ValueError('Tipo inválido.')

	tipo_input = Tipo(tipo_verificado)

	nome_pet_input = input('    Nome do pet: ')
	print('')
	if nome_pet_input == '':
		raise ValueError('O nome do pet não pode estar vazio.')

	raca_pet_input = input('    Raça do pet: ')
	print('')
	if raca_pet_input == '':
		raise ValueError('A raça do pet não pode estar vazia.')

	aux_porte = input('    Porte do pet (Pequeno, Médio ou Grande): ')
	print('')
	
	porte_verificado = None
	if aux_porte in ['Pequeno', 'PEQUENO', 'pequeno']:
		porte_verificado = Porte.PEQUENO
	elif aux_porte in ['Médio', 'MÉDIO', 'médio', 'Medio', 'MEDIO', 'medio']:
		porte_verificado = Porte.MEDIO
	elif aux_porte in ['Grande', 'GRANDE', 'grande']:
		porte_verificado = Porte.GRANDE
	elif aux_porte == '':
		raise ValueError('O porte do pet não pode estar vazio.')
	else:
		raise ValueError('Porte inválido.')
	
	porte_input = Porte(porte_verificado)

	hospedado_input = Hospedado.NAO
	qtd_dias_input = 0
	historico_qtd_hospedagem_input = 0
	observacoes_input = 'Sem observações de histórico de hospedagem.'

	pet = Pets(nome_tutor_input, tipo_input, nome_pet_input, raca_pet_input, porte_input, hospedado_input, qtd_dias_input, historico_qtd_hospedagem_input, observacoes_input)

	with Session(engine) as sessao, sessao.begin():
		
		pets = {
			'nome_tutor': pet.nome_tutor,
			'tipo_pet': pet.tipo_pet.value,
			'nome_pet': pet.nome_pet,
			'raca_pet': pet.raca_pet,
			'porte_pet': pet.porte_pet.value,
			'hospedado': pet.hospedado.value,
			'qtd_dias': pet.qtd_dias,
			'historico_qtd_hospedagem': pet.historico_qtd_hospedagem,
			'observacoes': pet.observacoes
		}

		try:
			sessao.execute(
				text("INSERT INTO pets (nome_tutor, tipo_pet, nome_pet, raca_pet, porte_pet, hospedado, qtd_dias, historico_qtd_hospedagem, observacoes) VALUES (:nome_tutor, :tipo_pet, :nome_pet, :raca_pet, :porte_pet, :hospedado, :qtd_dias, :historico_qtd_hospedagem, :observacoes)"), pets)
			print('')
			print('✅ Cadastro de pet feito com sucesso! ✅')
			print('')

		except IntegrityError as ex:
			print('')
			print(f'❌ Ocorreu um erro ao cadastrar o pet. ❌')
			print('')

def editar_pet():

	print('')
	print('Editar Pet: ')
	print('')

	nome_tutor_input = input('   Nome do tutor que deseja editar as informações: ')
	if nome_tutor_input == '':
		raise ValueError('O nome do tutor não pode estar vazio.')

	with Session(engine) as sessao:
		if nome_tutor_input == '':
			raise ValueError('O nome do tutor não pode estar vazio.')
		
		pesquisa_tutor = sessao.execute(text("SELECT nome_tutor, tipo_pet, nome_pet, raca_pet, porte_pet FROM pets WHERE nome_tutor = :nome_tutor"), {'nome_tutor': nome_tutor_input}).first()

		if pesquisa_tutor is None:
			print('')
			raise ValueError(f'Tutor {nome_tutor_input} não encontrado, efetue o cadastro!')
	
	#

	print('')
	aux_nome_tutor_input = input(f'O nome do tutor é "{pesquisa_tutor[0]}". Alterar informação? (Sim ou Não).')
	print('')
	
	nome_tutor_verificado = None
	if aux_nome_tutor_input in ['Sim', 'SIM', 'sim']:
		nome_tutor_verificado = Resposta.SIM
	elif aux_nome_tutor_input in ['Não', 'NÃO', 'não', 'Nao', 'NAO', 'nao']:
		nome_tutor_verificado = Resposta.NAO
	elif aux_nome_tutor_input == '':
		raise ValueError('A resposta do nome do tutor não pode estar vazia.')
	else:
		raise ValueError('Resposta inválida.')
	
	nome_tutor_input = Resposta(nome_tutor_verificado)

	if nome_tutor_input.value == 'Sim':
		nome_tutor_editado = input('   Novo nome do tutor: ')
		if nome_tutor_editado == '':
			raise ValueError('A resposta do nome do tutor não pode estar vazia.')
	else:
		nome_tutor_editado = pesquisa_tutor[0]

	#

	print('')
	aux_tipo_pet_input = input(f'O tipo do pet é "{pesquisa_tutor[1]}". Alterar informação? (Sim ou Não).')
	print('')
	
	tipo_pet_verificado = None
	if aux_tipo_pet_input in ['Sim', 'SIM', 'sim']:
		tipo_pet_verificado = Resposta.SIM
	elif aux_tipo_pet_input in ['Não', 'NÃO', 'não', 'Nao', 'NAO', 'nao']:
		tipo_pet_verificado = Resposta.NAO
	elif aux_tipo_pet_input == '':
		raise ValueError('A resposta do tipo do pet não pode estar vazia.')
	else:
		raise ValueError('Resposta inválida.')
	
	tipo_pet_input = Resposta(tipo_pet_verificado)

	if tipo_pet_input.value == 'Sim':
		aux_tipo_pet = input('   Novo tipo (Gato ou Cachorro): ')
		tipo_verificado = None

		if aux_tipo_pet in ['Gato', 'GATO', 'gato']:
			tipo_verificado = Tipo.GATO
		elif aux_tipo_pet in ['Cachorro', 'cachorro', 'CACHORRO']:
			tipo_verificado = Tipo.CACHORRO
		elif aux_tipo_pet == '':
			raise ValueError('O tipo do pet não pode estar vazio.')
		else:
			raise ValueError('Tipo inválido.')

		tipo_pet_editado = Tipo(tipo_verificado)
	else:
		tipo_pet_editado = pesquisa_tutor[1]

	#

	print('')
	aux_nome_pet_input = input(f'O nome do pet é "{pesquisa_tutor[2]}". Alterar informação? (Sim ou Não).')
	print('')
	
	nome_pet_verificado = None
	if aux_nome_pet_input in ['Sim', 'SIM', 'sim']:
		nome_pet_verificado = Resposta.SIM
	elif aux_nome_pet_input in ['Não', 'NÃO', 'não', 'Nao', 'NAO', 'nao']:
		nome_pet_verificado = Resposta.NAO
	elif aux_nome_pet_input == '':
		raise ValueError('A resposta do nome do pet não pode estar vazia.')
	else:
		raise ValueError('Resposta inválida.')
	
	nome_pet_input = Resposta(nome_pet_verificado)

	if nome_pet_input.value == 'Sim':
		nome_pet_editado = input('   Novo nome do pet: ')
		if nome_pet_editado == '':
			raise ValueError('A resposta do nome do pet não pode estar vazia.')
	else:
		nome_pet_editado = pesquisa_tutor[2]

	#

	print('')
	aux_raca_pet_input = input(f'A raça é "{pesquisa_tutor[3]}". Alterar informação? (Sim ou Não).')
	print('')
	
	raca_pet_verificado = None
	if aux_raca_pet_input in ['Sim', 'SIM', 'sim']:
		raca_pet_verificado = Resposta.SIM
	elif aux_raca_pet_input in ['Não', 'NÃO', 'não', 'Nao', 'NAO', 'nao']:
		raca_pet_verificado = Resposta.NAO
	elif aux_raca_pet_input == '':
		raise ValueError('A resposta da raça não pode estar vazia.')
	else:
		raise ValueError('Resposta inválida.')
	
	raca_pet_input = Resposta(raca_pet_verificado)

	if raca_pet_input.value == 'Sim':
		raca_pet_editado = input('   Nova raça: ')
		if raca_pet_editado == '':
			raise ValueError('A resposta da raça não pode estar vazia.')
	else:
		raca_pet_editado = pesquisa_tutor[3]

	#

	print('')
	aux_porte_pet_input = input(f'O porte é "{pesquisa_tutor[4]}". Alterar informação? (Sim ou Não).')
	print('')
	
	porte_pet_verificado = None
	if aux_porte_pet_input in ['Sim', 'SIM', 'sim']:
		porte_pet_verificado = Resposta.SIM
	elif aux_porte_pet_input in ['Não', 'NÃO', 'não', 'Nao', 'NAO', 'nao']:
		porte_pet_verificado = Resposta.NAO
	elif aux_porte_pet_input == '':
		raise ValueError('A resposta do tipo do pet não pode estar vazia.')
	else:
		raise ValueError('Resposta inválida.')
	
	porte_pet_input = Resposta(porte_pet_verificado)

	if porte_pet_input.value == 'Sim':
		aux_porte_pet = input('   Novo porte (Pequeno, Médio ou Grande): ')
		porte_verificado = None

		if aux_porte_pet in ['Pequeno', 'PEQUENO', 'pequeno']:
			porte_verificado = Porte.PEQUENO
		elif aux_porte_pet in ['Médio', 'MÉDIO', 'médio', 'Medio', 'MEDIO', 'medio']:
			porte_verificado = Porte.MEDIO
		elif aux_porte_pet in ['Grande', 'GRANDE', 'grande']:
			porte_verificado = Porte.GRANDE
		elif aux_porte_pet == '':
			raise ValueError('O porte do pet não pode estar vazio.')
		else:
			raise ValueError('Porte inválido.')

		porte_pet_editado = Porte(porte_verificado)
	else:
		porte_pet_editado = pesquisa_tutor[4]

	with Session(engine) as sessao, sessao.begin():
		parametros = {
			'nome_tutor': nome_tutor_editado,
			'tipo_pet': tipo_pet_editado.value,
			'nome_pet': nome_pet_editado,
			'raca_pet': raca_pet_editado,
			'porte_pet': porte_pet_editado.value
		}

		# Mais informações sobre o método execute e sobre o resultado que ele retorna:
		# https://docs.sqlalchemy.org/en/14/orm/session_api.html#sqlalchemy.orm.Session.execute
		# https://docs.sqlalchemy.org/en/14/core/connections.html#sqlalchemy.engine.Result
		resultado = sessao.execute(text("UPDATE pets SET nome_tutor = :nome_tutor, tipo_pet = :tipo_pet, nome_pet = :nome_pet, raca_pet = :raca_pet, porte_pet = :porte_pet WHERE nome_tutor = :nome_tutor"), parametros)

		if resultado.rowcount == 0:
			print('')
			print(f'❌ Nome de tutor {nome_tutor_input} não estava cadastrado. ❌')
			print('')
		else:
			print('')
			print(f'✅ Informações editadas com sucesso! ✅')
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

def menu():
	opcao = 1

	while opcao > 0:
		print('''Escolha uma opção:
	0 - Sair
	1 - Adicionar Pet
	2 - Editar Pet
	3 - Excluir Pet
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
			try:
				editar_pet()
			except ValueError as e:
				print(f'❌ Erro: {e} ❌')
				print('Retornando ao menu principal...')
				print('')

		elif opcao == 3:
			email = input("E-mail: ")
			nome = input("Nome: ")
			telefone = input("Telefone: ")
			excluir_contato(email, nome, telefone)
		elif opcao == 4:
			email = input("E-mail: ")
			consultar_contato(email)
		elif opcao == 5:
			listar_contatos()
