import requests

if __name__ == "__main__":
    url = "http://127.0.0.1:8000"

    def listar_livros():
        r = requests.get(f"{url}/livros")
        if r.status_code == 200:
            print(r.text)

    def listar_livro():
        titulo = input("Digite o titulo do livro: ")
        r = requests.get(f"{url}/livros/{titulo}")
        if r.status_code == 200:
            print(r.text)
        else:
            print(r.text)

    def cadastrar_livro():
        titulo = input("Digite o titulo do livro: ")
        ano = input("Digite o ano do livro: ")
        edicao = input("Digite a ediçao do livro: ")
        livro = {
            "titulo":titulo,
            "edicao":edicao,
            "ano":ano
        }
        r = requests.post(f"{url}/livros", json=livro)

    def excluir_livro():
        titulo = input("Digite o titulo do livro: ")
        r = requests.delete(f"{url}/livros/{titulo}")
        if r.status_code == 200:
            print("Excluido com sucesso")
        else:
            print(r.text)

    def editar_livro():
        titulo = input("Digite o titulo do livro: ")
        novoTitulo = input("Digite o NOVO titulo do livro: ")
        novoAno = int(input("Digite o NOVO ano do livro: "))
        novoEdicao = int(input("Digite a NOVA ediçao do livro: "))
        livroEditado = {
            "titulo":novoTitulo,
            "ano":novoAno,
            "edicao":novoEdicao
        }

        r = requests.put(f"{url}/livros/{titulo}", json=livroEditado)
        if r.status_code == 200:
            print("Editado com sucesso")
        else:
            print(r.text)


    def menu():
        print("1 - Listar Livros")
        print("2 - Listar Livros pelo título")
        print("3 - Cadastrar Livro")
        print("4 - Deletar Livro")
        print("5 - Editar Livro")
        print("6 - Sair")
        return int(input("Digite sua opção: "))

    opcao=menu()
    while opcao != 6:
        if opcao == 1:
            listar_livros()
        elif opcao == 2:
            listar_livro()
        elif opcao == 3:
            cadastrar_livro()
        elif opcao == 4:
            excluir_livro()
        elif opcao == 5:
            editar_livro()
        opcao = menu()