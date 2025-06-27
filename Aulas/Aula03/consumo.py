import requests

URL = "http://127.0.0.1:8000"

def listar_livros():
    r = requests.get(f"{URL}/livros")
    if r.status_code == 200:
        print(r.text)

def listar_livro():
    titulo = input("Digite o titulo do livro: ")
    r = requests.get(f"{URL}/livros/{titulo}")
    if r.status_code == 200:
        print(r.text)

def listar_usuarios():
    pass

def cadastrar_livro():
    titulo = input("Digite o titulo do livro: ")
    ano = input("Digite o ano do livro: ")
    edicao = input("Digite a ediçao do livro: ")
    livro = {
        "titulo":titulo,
        "edicao":edicao,
        "ano":ano
    }
    r = requests.post(f"{URL}/livros", json=livro)

def excluir_livro():
    titulo = input("Digite o titulo do livro: ")
    r = requests.delete(f"{URL}/livros/{titulo}")
    if r.status_code == 200:
        print( "Excluido com sucesso")
    else:
        print(r.text)

def menu():
    print("1 - Listar Livros")
    print("2 - Listar Livros pelo título")
    print("3 - Cadastrar Livro")
    print("4 - Deletar Livro")
    print("5 - Sair")
    return int(input("Digite sua opção: "))

opcao=menu()
while opcao != 5:
    if opcao == 1:
        listar_livros()
    elif opcao == 2:
        listar_livro()
    elif opcao == 3:
        cadastrar_livro()
    elif opcao == 4:
        excluir_livro()
    opcao = menu()