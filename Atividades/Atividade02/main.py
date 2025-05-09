from fastapi import FastAPI, HTTPException
from models import Livro, Leitor, Emprestimo
from typing import List
from datetime import date, timedelta

app = FastAPI()

livros:List[Livro]=[]
leitores:List[Leitor]=[]
emprestimos:List[Emprestimo]=[]

@app.get("/livros/", response_model=List[Livro])
def listar_livros():
    return livros

@app.get("/livros/{titulo}", response_model=Livro)
def listar_livro(titulo:str):
    for livro in livros:
        if livro.titulo == titulo:
            return livro
    raise HTTPException(status_code=404, detail="Não Localizado")


@app.post("/livros/", response_model=Livro)
def adicionar_livro(livro:Livro):
    livros.append(livro)
    return livro

@app.post("/leitores/", response_model=Leitor)
def adicionar_leitor(leitor:Leitor):
    leitores.append(leitor)
    return leitor

@app.get("/livros_emprestados/{leitor_uuid}", response_model=List[Livro])
def listar_livros_emprestados_por_leitor(leitor_uuid: int):
    for leitor in leitores:
        if leitor.uuid == leitor_uuid:
            livros_emprestados = []
            for livro in livros:
                if livro.uuid in leitor.livros_emprestados:
                    livros_emprestados.append(livro)
            return livros_emprestados
    raise HTTPException(status_code=404, detail="Não Localizado")

@app.get("/emprestimos/{leitor_uuid}", response_model=Emprestimo)
def listar_emprestimo(leitor_uuid:int):
    for emprestimo in emprestimos:
        if emprestimo.leitor_id == leitor_uuid:
            return emprestimo
    raise HTTPException(status_code=404, detail="Não Localizado")
    

@app.post("/emprestimos/", response_model=Emprestimo)
def adicionar_emprestimo(leitor_uuid:int, livro_uuid:int, data_de_emprestimo:str):
    Novoemprestimo = Emprestimo(
        uuid=len(emprestimos) + 1,
        leitor_id=leitor_uuid,
        livro_id=livro_uuid,
        data_emprestimo=data_de_emprestimo,
        data_devolucao=""
    )
    emprestimos.append(Novoemprestimo)
    return Novoemprestimo

@app.post("/devolucao/", response_model=Emprestimo)
def registrar_devolucao(leitor_uuid:int, livro_uuid:int, data_de_devolucao:str):
    for emprestimo in emprestimos:
        if emprestimo.livro_id == livro_uuid and emprestimo.leitor_id == leitor_uuid:
            emprestimo.data_devolucao = data_de_devolucao
            return emprestimo
        
