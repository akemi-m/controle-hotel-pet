from tipo import Tipo
from porte import Porte
from hospedado import Hospedado

class Pets:
    def __init__(self, nome_tutor: str, tipo_pet: Tipo, nome_pet: str, raca_pet: str, porte_pet: Porte, hospedado: Hospedado, qtd_dias: int, historico_qtd_hospedagem: int, observacoes: str):
        self.nome_tutor = nome_tutor
        self.tipo_pet = tipo_pet
        self.nome_pet = nome_pet
        self.raca_pet = raca_pet
        self.porte_pet = porte_pet
        self.hospedado = hospedado
        self.qtd_dias = qtd_dias
        self.historico_qtd_hospedagem = historico_qtd_hospedagem
        self.observacoes = observacoes

    def __str__(self):
        return f'\nNome do tutor: {self.nome_tutor}, \nTipo: {self.tipo_pet}, \nNome do pet: {self.nome_pet}, \nRaça: {self.raca_pet}, \nPorte: {self.porte_pet}.\nEstá hospedado? {self.hospedado} \nHá quantos dias? {self.qtd_dias} \nHistórico de hospedagem: {self.historico_qtd_hospedagem} \nObservações: {self.observacoes}'
    