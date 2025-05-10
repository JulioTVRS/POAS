from fastapi import FastAPI, HTTPException
from models import Livro, Leitor, Emprestimo
from typing import List

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
    raise HTTPException(status_code=404, detail="Não Localizado.")

@app.post("/livros/", response_model=Livro)
def adicionar_livro(livro:Livro):
    livros.append(livro)
    return livro

@app.post("/leitores/", response_model=Leitor)
def adicionar_leitor(leitor:Leitor):
    leitores.append(leitor)
    return leitor

@app.get("/livros_emprestados/{leitor_uuid}", response_model=List)
def listar_livros_emprestados_por_leitor(leitor_uuid: int):
    for leitor in leitores:
        if leitor.uuid == leitor_uuid:
            return leitor.livros_emprestados
    raise HTTPException(status_code=404, detail="Não Localizado.")

@app.get("/emprestimos/{leitor_uuid}", response_model=List[Emprestimo])
def listar_emprestimo(leitor_uuid:int):
    all_emprestimos = []
    for emprestimo in emprestimos:
        if emprestimo.leitor_id == leitor_uuid:
            all_emprestimos.append(emprestimo)

    if all_emprestimos == []: 
        raise HTTPException(status_code=404, detail="Não Localizado.")
    return all_emprestimos
    

@app.post("/emprestimos/", response_model=Emprestimo)
def adicionar_emprestimo(leitor_uuid:int, livro_uuid:int, data_de_emprestimo:str):

    livro_encontrado = False
    for livro in livros:
        if livro.uuid == livro_uuid:
            livro_encontrado = True
            if livro.disponibilidade == False:
                raise HTTPException(status_code=404, detail="Livro indisponível.")
            livro.disponibilidade = False

    if not livro_encontrado:
        raise HTTPException(status_code=404, detail="Livro não encontrado.")
            
    for leitor in leitores:
        if leitor.uuid == leitor_uuid:
            break
    else:
        raise HTTPException(status_code=404, detail="Leitor inexistente.")

    emprestimo = Emprestimo(
        uuid=len(emprestimos) + 1,
        leitor_id=leitor_uuid,
        livro_id=livro_uuid,
        data_emprestimo=data_de_emprestimo,
        data_devolucao=""
    )
    leitor.livros_emprestados.append([livro.uuid, livro.titulo])
    emprestimos.append(emprestimo)
    return emprestimo

@app.post("/devolucao/", response_model=Emprestimo)
def registrar_devolucao(leitor_uuid:int, livro_uuid:int, data_de_devolucao:str):
    for emprestimo in emprestimos:
        if emprestimo.livro_id == livro_uuid and emprestimo.leitor_id == leitor_uuid:
            emprestimo.data_devolucao = data_de_devolucao

            for leitor in leitores:
                if leitor.uuid == leitor_uuid:
                    for livro_emprestado in leitor.livros_emprestados:
                        if isinstance(livro_emprestado, list) and len(livro_emprestado) > 0:
                            if livro_emprestado[0] == livro_uuid:
                                leitor.livros_emprestados.remove(livro_emprestado)
                                break
                    break


            for livro in livros:
                if livro.uuid == livro_uuid:
                    livro.disponibilidade = True
                    break

            return emprestimo
    raise HTTPException(status_code=404, detail="Empréstimo não encontrado.")
