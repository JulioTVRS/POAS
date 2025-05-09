from pydantic import BaseModel

class Livro(BaseModel):
    uuid:int
    titulo:str
    autor:str
    ano_publicacao:int
    disponibilidade:bool

class Leitor(BaseModel):
    uuid:int
    nome:str
    livros_emprestados:list

class Emprestimo(BaseModel):
    uuid:int
    leitor_id:int
    livro_id:int
    data_emprestimo:str
    data_devolucao:str