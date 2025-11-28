import flet as ft
import requests

def main(page: ft.Page):
    page.title = "Lista de Alunos (Vindo do Django)"
    page.scroll = "adaptive"

    API_URL = "http://127.0.0.1:8000/pessoa/api/alunos/"

    lista_alunos = ft.Column()

    def carregar_dados():
        lista_alunos.controls.clear()
        
        try:
            response = requests.get(API_URL)
            
            if response.status_code == 200:
                dados = response.json() 
                
                for aluno in dados:
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

    btn_atualizar = ft.ElevatedButton("Buscar Alunos do Banco", on_click=lambda _: carregar_dados())

    page.add(
        ft.Text("Integração Flet + Django", size=25),
        btn_atualizar,
        lista_alunos
    )
    
    carregar_dados()

ft.app(target=main)