class Pets:
    def __init__(self, nome_tutor: str, tipo_pet: str, nome_pet: str, raca_pet: str, porte_pet: str, qtd_dias: int):
        self.nome_tutor = nome_tutor
        self.tipo_pet = tipo_pet
        self.nome_pet = nome_pet
        self.raca_pet = raca_pet
        self.porte_pet = porte_pet
        self.qtd_dias = qtd_dias

    def __str__(self):
        return f'Nome do tutor: {self.nome_tutor}, Tipo: {self.tipo_pet}, Nome do pet: {self.nome_pet}, Raça: {self.raca_pet}, Porte: {self.porte.pet}, Quantidade de dias hospedado: {self.qtd_dias}.'
    