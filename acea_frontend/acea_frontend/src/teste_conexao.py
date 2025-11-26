import flet as ft
import requests

def main(page: ft.Page):
    page.title = "Lista de Alunos (Vindo do Django)"
    page.scroll = "adaptive"

    # URL da sua API (Exatamente a que funcionou no navegador)
    API_URL = "http://127.0.0.1:8000/pessoa/api/alunos/"

    # Container onde vamos colocar os alunos
    lista_alunos = ft.Column()

    def carregar_dados():
        lista_alunos.controls.clear()
        
        try:
            # 1. O Flet "liga" para o Django
            response = requests.get(API_URL)
            
            # 2. Verifica se o Django atendeu (Status 200)
            if response.status_code == 200:
                dados = response.json() # Transforma o texto em Lista Python
                
                # 3. Para cada aluno na lista, cria um visual
                for aluno in dados:
                    # Montando um Card simples para cada aluno
                    card = ft.Card(
                        content=ft.Container(
                            padding=10,
                            content=ft.Column([
                                ft.Text(f"Nome: {aluno['nome']}", size=16, weight="bold"),
                                ft.Text(f"Email: {aluno['email']}"),
                                ft.Text(f"CPF: {aluno['cpf']}"),
                            ])
                        )
                    )
                    lista_alunos.controls.append(card)
                
                print("Dados carregados com sucesso!")
            else:
                lista_alunos.controls.append(ft.Text(f"Erro: {response.status_code}"))
                
        except Exception as e:
            lista_alunos.controls.append(ft.Text(f"Erro de conexão: {e}"))
            print(e)
        
        page.update()

    # Botão para atualizar
    btn_atualizar = ft.ElevatedButton("Buscar Alunos do Banco", on_click=lambda _: carregar_dados())

    page.add(
        ft.Text("Integração Flet + Django", size=25),
        btn_atualizar,
        lista_alunos
    )
    
    # Chama a função assim que abre o app
    carregar_dados()

ft.app(target=main)