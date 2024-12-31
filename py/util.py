from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from pets import Pets
from tipo import Tipo
from porte import Porte
from hospedado import Hospedado
from resposta import Resposta

engine = create_engine('mysql+mysqlconnector://root:root@localhost/hotel-pet')

def adicionar_pet():
	
	print('')
	print('Adicionar Pet: ')
	print('')
	
	nome_tutor_input = input('    Nome do tutor: ')
	if nome_tutor_input == '':
		raise ValueError('O nome do tutor não pode estar vazio.')

	with Session(engine) as sessao:
		
		pesquisa_tutor = sessao.execute(text("SELECT nome_tutor FROM pets WHERE nome_tutor = :nome_tutor"), {'nome_tutor': nome_tutor_input}).first()
		
		if pesquisa_tutor is not None:
			print('')
			raise ValueError(f'Tutor {nome_tutor_input} já cadastrado!')

	aux_tipo = input('    Tipo do pet (Gato ou Cachorro): ')
	
	tipo_verificado = None
	
	if aux_tipo in ['Gato', 'GATO', 'gato', 'g', 'G']:
		tipo_verificado = Tipo.GATO
	elif aux_tipo in ['Cachorro', 'cachorro', 'CACHORRO', 'c', 'C']:
		tipo_verificado = Tipo.CACHORRO
	elif aux_tipo == '':
		raise ValueError('O tipo do pet não pode estar vazio.')
	else:
		raise ValueError('Tipo inválido.')

	tipo_input = Tipo(tipo_verificado)

	nome_pet_input = input('    Nome do pet: ')

	if nome_pet_input == '':
		raise ValueError('O nome do pet não pode estar vazio.')

	raca_pet_input = input('    Raça do pet: ')

	if raca_pet_input == '':
		raise ValueError('A raça do pet não pode estar vazia.')

	aux_porte = input('    Porte do pet (Pequeno, Médio ou Grande): ')
	
	porte_verificado = None
	if aux_porte in ['Pequeno', 'PEQUENO', 'pequeno', 'p', 'P']:
		porte_verificado = Porte.PEQUENO
	elif aux_porte in ['Médio', 'MÉDIO', 'médio', 'Medio', 'MEDIO', 'medio', 'm', 'M']:
		porte_verificado = Porte.MEDIO
	elif aux_porte in ['Grande', 'GRANDE', 'grande', 'g', 'G']:
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
			print(f'❌ Ocorreu um erro de rede ao cadastrar o pet. ❌')
			print('')

def editar_pet():

	print('')
	print('Editar Pet: ')
	print('')

	nome_tutor_input = input('   Nome do tutor: ')
	print('')
	if nome_tutor_input == '':
		raise ValueError('O nome do tutor não pode estar vazio.')

	with Session(engine) as sessao:

		parametros = {
			'nome_tutor': nome_tutor_input
		}

		try:
			pesquisa_tutor = sessao.execute(text("SELECT nome_tutor, tipo_pet, nome_pet, raca_pet, porte_pet FROM pets WHERE nome_tutor = :nome_tutor"), parametros).first()

		except IntegrityError as ex:
			print('')
			print(f'❌ Ocorreu um erro de rede ao editar o pet. ❌')
			print('')
				
		if pesquisa_tutor is None:
			print('')
			raise ValueError(f'Tutor {nome_tutor_input} não encontrado, efetue o cadastro primeiro.')

	nome_tutor_original_sql = pesquisa_tutor[0]

	aux_nome_tutor_input = input(f'   O nome do tutor é "{pesquisa_tutor[0]}". \n   Alterar informação? (Sim ou Não). ')
	
	nome_tutor_verificado = None
	if aux_nome_tutor_input in ['Sim', 'SIM', 'sim', 's', 'S']:
		nome_tutor_verificado = Resposta.SIM
	elif aux_nome_tutor_input in ['Não', 'NÃO', 'não', 'Nao', 'NAO', 'nao', 'n', 'N']:
		nome_tutor_verificado = Resposta.NAO
	elif aux_nome_tutor_input == '':
		print('')
		raise ValueError('A resposta do nome do tutor não pode estar vazia.')
	else:
		print('')
		raise ValueError('Resposta inválida.')
	
	nome_tutor_input = Resposta(nome_tutor_verificado)

	if nome_tutor_input.value == 'Sim':
		nome_tutor_editado = input('      Novo nome do tutor: ')
		if nome_tutor_editado == '':
			raise ValueError('A resposta do nome do tutor não pode estar vazia.')
	else:
		nome_tutor_editado = pesquisa_tutor[0]

	print('')
	aux_tipo_pet_input = input(f'   O tipo do pet é "{pesquisa_tutor[1]}". \n   Alterar informação? (Sim ou Não). ')
	
	tipo_pet_verificado = None
	if aux_tipo_pet_input in ['Sim', 'SIM', 'sim', 's', 'S']:
		tipo_pet_verificado = Resposta.SIM
	elif aux_tipo_pet_input in ['Não', 'NÃO', 'não', 'Nao', 'NAO', 'nao', 'n', 'N']:
		tipo_pet_verificado = Resposta.NAO
	elif aux_tipo_pet_input == '':
		print('')
		raise ValueError('A resposta do tipo do pet não pode estar vazia.')
	else:
		print('')
		raise ValueError('Resposta inválida.')
	
	tipo_pet_input = Resposta(tipo_pet_verificado)

	if tipo_pet_input.value == 'Sim':
		aux_tipo_pet = input('      Novo tipo (Gato ou Cachorro): ')
		tipo_verificado = None

		if aux_tipo_pet in ['Gato', 'GATO', 'gato', 'g', 'G']:
			tipo_verificado = Tipo.GATO
		elif aux_tipo_pet in ['Cachorro', 'cachorro', 'CACHORRO', 'c', 'C']:
			tipo_verificado = Tipo.CACHORRO
		elif aux_tipo_pet == '':
			raise ValueError('O tipo do pet não pode estar vazio.')
		else:
			raise ValueError('Tipo inválido.')

		tipo_pet_editado = Tipo(tipo_verificado)
	else:
		tipo_pet_editado = Tipo(pesquisa_tutor[1])

	print('')
	aux_nome_pet_input = input(f'   O nome do pet é "{pesquisa_tutor[2]}". \n   Alterar informação? (Sim ou Não). ')
	
	nome_pet_verificado = None
	if aux_nome_pet_input in ['Sim', 'SIM', 'sim', 's', 'S']:
		nome_pet_verificado = Resposta.SIM
	elif aux_nome_pet_input in ['Não', 'NÃO', 'não', 'Nao', 'NAO', 'nao', 'n', 'N']:
		nome_pet_verificado = Resposta.NAO
	elif aux_nome_pet_input == '':
		print('')
		raise ValueError('A resposta do nome do pet não pode estar vazia.')
	else:
		print('')
		raise ValueError('Resposta inválida.')
	
	nome_pet_input = Resposta(nome_pet_verificado)

	if nome_pet_input.value == 'Sim':
		nome_pet_editado = input('      Novo nome do pet: ')
		if nome_pet_editado == '':
			raise ValueError('A resposta do nome do pet não pode estar vazia.')
	else:
		nome_pet_editado = pesquisa_tutor[2]

	print('')
	aux_raca_pet_input = input(f'   A raça é "{pesquisa_tutor[3]}". \n   Alterar informação? (Sim ou Não). ')
	
	raca_pet_verificado = None
	if aux_raca_pet_input in ['Sim', 'SIM', 'sim', 's', 'S']:
		raca_pet_verificado = Resposta.SIM
	elif aux_raca_pet_input in ['Não', 'NÃO', 'não', 'Nao', 'NAO', 'nao', 'n', 'N']:
		raca_pet_verificado = Resposta.NAO
	elif aux_raca_pet_input == '':
		print('')
		raise ValueError('A resposta da raça não pode estar vazia.')
	else:
		print('')
		raise ValueError('Resposta inválida.')
	
	raca_pet_input = Resposta(raca_pet_verificado)

	if raca_pet_input.value == 'Sim':
		raca_pet_editado = input('      Nova raça: ')
		if raca_pet_editado == '':
			raise ValueError('A resposta da raça não pode estar vazia.')
	else:
		raca_pet_editado = pesquisa_tutor[3]

	print('')
	aux_porte_pet_input = input(f'   O porte é "{pesquisa_tutor[4]}". \n   Alterar informação? (Sim ou Não). ')
	
	porte_pet_verificado = None
	if aux_porte_pet_input in ['Sim', 'SIM', 'sim', 's', 'S']:
		porte_pet_verificado = Resposta.SIM
	elif aux_porte_pet_input in ['Não', 'NÃO', 'não', 'Nao', 'NAO', 'nao', 'n', 'N']:
		porte_pet_verificado = Resposta.NAO
	elif aux_porte_pet_input == '':
		print('')
		raise ValueError('A resposta do tipo do pet não pode estar vazia.')
	else:
		print('')
		raise ValueError('Resposta inválida.')
	
	porte_pet_input = Resposta(porte_pet_verificado)

	if porte_pet_input.value == 'Sim':
		aux_porte_pet = input('      Novo porte (Pequeno, Médio ou Grande): ')
		porte_verificado = None

		if aux_porte_pet in ['Pequeno', 'PEQUENO', 'pequeno', 'p', 'P']:
			porte_verificado = Porte.PEQUENO
		elif aux_porte_pet in ['Médio', 'MÉDIO', 'médio', 'Medio', 'MEDIO', 'medio', 'm', 'M']:
			porte_verificado = Porte.MEDIO
		elif aux_porte_pet in ['Grande', 'GRANDE', 'grande', 'g', 'G']:
			porte_verificado = Porte.GRANDE
		elif aux_porte_pet == '':
			raise ValueError('O porte do pet não pode estar vazio.')
		else:
			raise ValueError('Porte inválido.')

		porte_pet_editado = Porte(porte_verificado)
	else:
		porte_pet_editado = Porte(pesquisa_tutor[4])

	with Session(engine) as sessao, sessao.begin():
		parametros = {
			'nome_tutor': nome_tutor_editado,
			'tipo_pet': tipo_pet_editado.value,
			'nome_pet': nome_pet_editado,
			'raca_pet': raca_pet_editado,
			'porte_pet': porte_pet_editado.value,
			'nome_tutor_original_sql': nome_tutor_original_sql
		}

		try:
			sessao.execute(text("UPDATE pets SET nome_tutor = :nome_tutor, tipo_pet = :tipo_pet, nome_pet = :nome_pet, raca_pet = :raca_pet, porte_pet = :porte_pet WHERE nome_tutor = :nome_tutor_original_sql"), parametros)
			print('')
			print(f'✅ Informações editadas com sucesso! ✅')
			print('')

		except IntegrityError as ex:
			print('')
			print(f'❌ Ocorreu um erro de rede ao editar o pet. ❌')
			print('')

def consultar_pet():

	print('')
	print('Consultar Pet: ')
	print('')

	nome_tutor_input = input('Nome do tutor: ')
	print('')

	with Session(engine) as sessao:
		parametros = {
			'nome_tutor': nome_tutor_input
		}

		try:
			pet = sessao.execute(text("SELECT id, nome_tutor, tipo_pet, nome_pet, raca_pet, porte_pet FROM pets WHERE nome_tutor = :nome_tutor"), parametros).first()

		except IntegrityError as ex:
			print('')
			print(f'❌ Ocorreu um erro de rede ao consultar o pet. ❌')
			print('')

		if pet is None:
			raise ValueError(f'Nome do tutor {pet} não encontrado!')
		else:
			print(f'   Id: {pet.id}')
			print(f'   Nome do tutor: {pet.nome_tutor}')
			print(f'   Tipo: {pet.tipo_pet}')
			print(f'   Nome do pet: {pet.nome_pet}')
			print(f'   Raça: {pet.raca_pet}')
			print(f'   Porte: {pet.porte_pet}')
			print('')

def listar_pets():
		
	print('')
	print('Listar Pets: ')
	print('')

	with Session(engine) as sessao:

		try:
			pets = sessao.execute(text("SELECT id, nome_tutor, tipo_pet, nome_pet, raca_pet, porte_pet FROM pets ORDER BY nome_tutor"))

		except IntegrityError as ex:
			print('')
			print(f'❌ Ocorreu um erro de rede ao listar os pets. ❌')
			print('')
		if pets.rowcount == 0:
			raise ValueError(f'Não há pets cadastrados.')
		else:
			for pet in pets:
				print(f'   Id: {pet.id}')
				print(f'   Nome do tutor: {pet.nome_tutor}')
				print(f'   Tipo: {pet.tipo_pet}')
				print(f'   Nome do pet: {pet.nome_pet}')
				print(f'   Raça: {pet.raca_pet}')
				print(f'   Porte: {pet.porte_pet}')
				print('')

		print('')

def excluir_pet():

	print('')
	print('Excluir Pet: ')
	print('')

	nome_tutor_input = input('Nome do tutor: ')
	if nome_tutor_input == '':
		raise ValueError('O nome do tutor não pode estar vazio.')

	with Session(engine) as sessao, sessao.begin():
		parametros = {
			'nome_tutor': nome_tutor_input
		}

		try:
			resultado = sessao.execute(text("DELETE FROM pets WHERE nome_tutor = :nome_tutor"), parametros)

		except IntegrityError as ex:
			print('')
			print(f'❌ Ocorreu um erro de rede ao excluir o pet. ❌')
			print('')

		if resultado.rowcount == 0:
			print('')
			print(f'❌ Não é possível excluir um contato não cadastrado. ❌')
			print('')
		else:
			print('')
			print(f'✅ Pet excluído com sucesso! ✅')
			print('')

def entrada_hotel_pet():

	print('')
	print('Entrada Hotel Pet: ')
	print('')

	nome_tutor_input = input('Nome do tutor: ')
	print('')
	if nome_tutor_input == '':
		raise ValueError('O nome do tutor não pode estar vazio.')

	with Session(engine) as sessao:

		try:
			pet = sessao.execute(text("SELECT nome_tutor, tipo_pet, nome_pet, porte_pet, hospedado FROM pets WHERE nome_tutor = :nome_tutor"), {'nome_tutor': nome_tutor_input}).first()

		except IntegrityError as ex:
			print('')
			print(f'❌ Ocorreu um erro de rede ao efetuar a entrada no hotel pet. ❌')
			print('')

		if pet.hospedado == 'Sim':
			print('')
			raise ValueError(f'O pet já está no Hotel Pet')

		if pet is None:
			print('')
			raise ValueError(f'Tutor {nome_tutor_input} não encontrado, efetue o cadastro primeiro.')
		
		else:
			print(f'   Nome do tutor: {pet.nome_tutor}')
			print(f'   Tipo: {pet.tipo_pet}')
			print(f'   Nome do pet: {pet.nome_pet}')
			print(f'   Porte: {pet.porte_pet}')
			print('')
		
	aux_dados_resposta = input('As informações estão corretas? (Sim ou Não). ')
	print('')

	dados_resposta_verificado = None
	if aux_dados_resposta in ['Sim', 'SIM', 'sim', 's', 'S']:
		dados_resposta_verificado = Resposta.SIM
	elif aux_dados_resposta in ['Não', 'NÃO', 'não', 'Nao', 'NAO', 'nao', 'n', 'N']:
		dados_resposta_verificado = Resposta.NAO
	elif aux_dados_resposta == '':
		print('')
		raise ValueError('A resposta não pode estar vazia.')
	else:
		print('')
		raise ValueError('Resposta inválida.')
	
	dados_resposta_input = Resposta(dados_resposta_verificado)

	if dados_resposta_input.value == 'Sim':
		hospedado = Resposta.SIM

		try:
			qtd_dias = int(input('Quantidade de diárias no Hotel Pet: '))
			print('')
		except:
			print('')
			raise ValueError('Digite um número inteiro válido.')

		with Session(engine) as sessao:

			parametros = {
				'nome_tutor': nome_tutor_input
			}

			try:
				pesquisa_tutor = sessao.execute(text("SELECT observacoes FROM pets WHERE nome_tutor = :nome_tutor"), parametros).first()

			except IntegrityError as ex:
				print('')
				print(f'❌ Ocorreu um erro de rede ao efetuar a entrada no hotel pet. ❌')
				print('')
					
		aux_observacoes = input(f'A observação é "{pesquisa_tutor[0]}". \n   Alterar informação? (Sim ou Não). ')

		observacoes_verificado = None
		if aux_observacoes in ['Sim', 'SIM', 'sim', 's', 'S']:
			observacoes_verificado = Resposta.SIM
		elif aux_observacoes in ['Não', 'NÃO', 'não', 'Nao', 'NAO', 'nao', 'n', 'N']:
			observacoes_verificado = Resposta.NAO
		elif aux_observacoes == '':
			print('')
			raise ValueError('A resposta não pode estar vazia.')
		else:
			print('')
			raise ValueError('Resposta inválida.')
		
		observacoes_resposta = Resposta(observacoes_verificado)

		if observacoes_resposta.value == 'Sim':
			observacoes = input('Nova observação: ')

			if observacoes == '':
				raise ValueError('A resposta não pode estar vazia.')
		else:
			observacoes = pesquisa_tutor[0]

		with Session(engine) as sessao, sessao.begin():
			parametros = {
				'nome_tutor': nome_tutor_input,
				'hospedado': hospedado.value,
				'qtd_dias': qtd_dias,
				'observacoes': observacoes
			}

			try:
				sessao.execute(text("UPDATE pets SET hospedado = :hospedado, qtd_dias = :qtd_dias, observacoes = :observacoes WHERE nome_tutor = :nome_tutor"), parametros)
				print('')
				print(f'✅ Entrada no Hotel Pet confirmada! ✅')
				print('')

			except IntegrityError as ex:
				print('')
				print(f'❌ Ocorreu um erro de rede ao efetuar a entrada no Hotel Pet. ❌')
				print('')

	if dados_resposta_input.value == 'Não':
		print('Retornando ao menu principal...')
		print('')

def saida_hotel_pet():
	print('')
	print('Saída Hotel Pet: ')
	print('')

	nome_tutor_input = input('Nome do tutor: ')
	print('')
	if nome_tutor_input == '':
		raise ValueError('O nome do tutor não pode estar vazio.')

	with Session(engine) as sessao:

		parametros = {
			'nome_tutor': nome_tutor_input
		}

		try:
			pet = sessao.execute(text("SELECT nome_tutor, tipo_pet, nome_pet, porte_pet, hospedado, qtd_dias, historico_qtd_hospedagem FROM pets WHERE nome_tutor = :nome_tutor"), parametros).first()

		except IntegrityError as ex:
			print('')
			print(f'❌ Ocorreu um erro de rede ao efetuar a saída no hotel pet. ❌')
			print('')

		if pet is None:
			print('')
			raise ValueError(f'Tutor {nome_tutor_input} não encontrado, efetue o cadastro primeiro.')
		if pet.hospedado == 'Não':
			print('')
			raise ValueError(f'O pet não está no Hotel Pet. Efetue a entrada primeiro.')
		else:
			print(f'   Nome do tutor: {pet.nome_tutor}')
			print(f'   Tipo: {pet.tipo_pet}')
			print(f'   Nome do pet: {pet.nome_pet}')
			print(f'   Porte: {pet.porte_pet}')
			print(f'   Hospedado: {pet.hospedado}')
			print(f'   Diárias: {pet.qtd_dias}')
			print('')
		
	aux_dados_resposta = input('As informações estão corretas? (Sim ou Não). ')
	print('')

	dados_resposta_verificado = None
	if aux_dados_resposta in ['Sim', 'SIM', 'sim', 's', 'S']:
		dados_resposta_verificado = Resposta.SIM
	elif aux_dados_resposta in ['Não', 'NÃO', 'não', 'Nao', 'NAO', 'nao', 'n', 'N']:
		dados_resposta_verificado = Resposta.NAO
	elif aux_dados_resposta == '':
		print('')
		raise ValueError('A resposta não pode estar vazia.')
	else:
		print('')
		raise ValueError('Resposta inválida.')
	
	dados_resposta_input = Resposta(dados_resposta_verificado)

	if dados_resposta_input.value == 'Sim':
		porte_pet = pet.porte_pet
		qtd_dias = pet.qtd_dias

		if porte_pet == 'Pequeno':
			diaria = 90
			total_a_pagar = diaria * qtd_dias

			print(f'Total a pagar: R$ {total_a_pagar:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.'))

		if porte_pet == 'Médio':
			diaria = 120
			total_a_pagar = diaria * qtd_dias

			print(f'Total a pagar: R$ {total_a_pagar:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.'))

		if porte_pet == 'Grande':
			diaria = 150
			total_a_pagar = diaria * qtd_dias

			print(f'Total a pagar: R$ {total_a_pagar:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.'))

		aux_dados_resposta = input('Pagamento efetuado? (Sim ou Não). ')

		dados_resposta_verificado = None
		if aux_dados_resposta in ['Sim', 'SIM', 'sim', 's', 'S']:
			dados_resposta_verificado = Resposta.SIM
		elif aux_dados_resposta in ['Não', 'NÃO', 'não', 'Nao', 'NAO', 'nao', 'n', 'N']:
			dados_resposta_verificado = Resposta.NAO
		elif aux_dados_resposta == '':
			print('')
			raise ValueError('A resposta não pode estar vazia.')
		else:
			print('')
			raise ValueError('Resposta inválida.')
		
		dados_resposta_input = Resposta(dados_resposta_verificado)

		if dados_resposta_input.value == 'Sim':
			hospedado = Resposta.NAO
			qtd_dias = 0
			historico_qtd_hospedagem = pet.historico_qtd_hospedagem
			historico_qtd_hospedagem += 1

			with Session(engine) as sessao, sessao.begin():
				parametros = {
					'hospedado': hospedado.value,
					'qtd_dias': qtd_dias,
					'historico_qtd_hospedagem': historico_qtd_hospedagem,
					'nome_tutor':nome_tutor_input
				}

				try:
					sessao.execute(text("UPDATE pets SET hospedado = :hospedado, qtd_dias = :qtd_dias, historico_qtd_hospedagem = :historico_qtd_hospedagem WHERE nome_tutor = :nome_tutor"), parametros)
					print('')
					print(f'✅ Saída no Hotel Pet confirmada! ✅')
					print('')

				except IntegrityError as ex:
					print('')
					print(f'❌ Ocorreu um erro de rede ao efetuar a saída no Hotel Pet. ❌')
					print('')

		if dados_resposta_input.value == 'Não':
			print('Retornando ao menu principal...')
			print('')

	if dados_resposta_input.value == 'Não':
		print('Retornando ao menu principal...')
		print('')


def listagem_hotel_pet():
	print('')
	print('Listagem de Pets no Hotel Pet:')
	print('')

	with Session(engine) as sessao:

		try:
			pets = sessao.execute(text("SELECT id, nome_tutor, tipo_pet, nome_pet, raca_pet, porte_pet, qtd_dias FROM pets WHERE hospedado = 'Sim' ORDER BY nome_tutor"))

		except IntegrityError as ex:
			print('')
			print(f'❌ Ocorreu um erro de rede ao listar os pets no Hotel Pet. ❌')
			print('')

		if pets.rowcount == 0:
			print(f'   Não há pets no Hotel Pet.')
		else:
			for pet in pets:
				print(f'   Id: {pet.id}')
				print(f'   Nome do tutor: {pet.nome_tutor}')
				print(f'   Tipo: {pet.tipo_pet}')
				print(f'   Nome do pet: {pet.nome_pet}')
				print(f'   Raça: {pet.raca_pet}')
				print(f'   Porte: {pet.porte_pet}')
				print(f'   Diárias: {pet.qtd_dias}')
				print('')

	print('')
	print('Listagem de Histórico do Hotel Pet')
	print('')

	with Session(engine) as sessao:

		try:
			pets = sessao.execute(text("SELECT id, nome_tutor, tipo_pet, nome_pet, raca_pet, porte_pet, historico_qtd_hospedagem FROM pets WHERE hospedado = 'Não' AND historico_qtd_hospedagem >= 1 ORDER BY nome_tutor"))

		except IntegrityError as ex:
			print('')
			print(f'❌ Ocorreu um erro de rede ao listar o histórico do Hotel Pet. ❌')
			print('')

		if pets.rowcount == 0:
			print(f'   Não há pets no histórico do Hotel Pet.')
		else:
			for pet in pets:
				print(f'   Id: {pet.id}')
				print(f'   Nome do tutor: {pet.nome_tutor}')
				print(f'   Tipo: {pet.tipo_pet}')
				print(f'   Nome do pet: {pet.nome_pet}')
				print(f'   Raça: {pet.raca_pet}')
				print(f'   Porte: {pet.porte_pet}')
				print(f'   Quantidade de hospedagens: {pet.historico_qtd_hospedagem}')
				print('')

def precos_diarias():
	print('')
	print("+-------------------+------------------------+")
	print("| Porte do Pet      | Preço da Diária (R$)   |")
	print("+-------------------+------------------------+")
	print("| Pequeno           | 90,00                  |")
	print("| Médio             | 120,00                 |")
	print("| Grande            | 150,00                 |")
	print("+-------------------+------------------------+")
	print('')

def menu():
	opcao = 1

	while opcao > 0:
		print('''Escolha uma opção:\n
	0 - Sair
	1 - Adicionar Pet
	2 - Editar Pet
	3 - Consultar Pet
	4 - Listar Pets
	5 - Excluir Pet
	6 - Entrada Hotel Pet
	7 - Saída Hotel Pet
	8 - Listagem Hotel Pet
	9 - Preços das Diárias
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
			try:
				consultar_pet()
			except ValueError as e:
				print(f'❌ Erro: {e} ❌')
				print('Retornando ao menu principal...')
				print('')

		elif opcao == 4:
			try:
				listar_pets()
			except ValueError as e:
				print(f'❌ Erro: {e} ❌')
				print('Retornando ao menu principal...')
				print('')

		elif opcao == 5:
			try:
				excluir_pet()
			except ValueError as e:
				print(f'❌ Erro: {e} ❌')
				print('Retornando ao menu principal...')
				print('')

		elif opcao == 6:
			try:
				entrada_hotel_pet()
			except ValueError as e:
				print(f'❌ Erro: {e} ❌')
				print('Retornando ao menu principal...')
				print('')

		elif opcao == 7:
			try:
				saida_hotel_pet()
			except ValueError as e:
				print(f'❌ Erro: {e} ❌')
				print('Retornando ao menu principal...')
				print('')

		elif opcao == 8:
			try:
				listagem_hotel_pet()
			except ValueError as e:
				print(f'❌ Erro: {e} ❌')
				print('Retornando ao menu principal...')
				print('')

		elif opcao == 9:
			try:
				precos_diarias()
			except ValueError as e:
				print(f'❌ Erro: {e} ❌')
				print('Retornando ao menu principal...')
				print('')

		elif opcao == 0:
			print('')
			print('Encerrando o sistema...')

		else:
			print('')
			print('Opção inválida, tente novamente.')
			print('')