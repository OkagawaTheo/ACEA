import flet as ft
from login_view import create_login_view
from dashboard_view import create_dashboard_view, create_dashboard_content
from cronograma_professor_view import create_cronograma_professor_view
from atividades_aluno_view import create_atividades_aluno_view
from financeiro_view import create_financeiro_view
from gestao_alunos_curso_professor_view import create_gestao_alunos_curso_professor_view
from gestao_documentos_view import create_gestao_documentos_view
from gestao_professores import create_gestao_professor_view
from profile_view import get_profile_card

# Mapeamento para navegação interna
VIEW_MAPPING = {
    "Home": 0, 
    "Perfil": 1, 
    "Cronogramas": 2,
    "Gestão Alunos": 3,
    "Gestão Professores": 4,
    "Documentos": 5, 
    "Atividades": 6, 
    "Doações": 7,    
}

def main(page: ft.Page):
    # Configurações iniciais
    page.title = "Associação Cultural"
    page.padding = 0
    page.bgcolor = ft.Colors.BLUE_GREY_50
    page.update()

    # --- 1. Função de Navegação para o Conteúdo Dinâmico ---
    def switch_content(item_key, role):
        """Alterna a área de conteúdo principal do Dashboard com base na permissão."""
        
        # Localiza a coluna de conteúdo dinâmico no layout principal
        content_wrapper_row = page.controls[0].controls[2].content.controls[1]
        main_content_column = content_wrapper_row.controls[0]
        
        main_content_column.controls.clear()

        if item_key == "Home":
            main_content_column.controls.append(create_dashboard_content(page, role))
        
        elif item_key == "Cronogramas":
            # Permissão: Professor/Admin (Edição)
            if role in ["Professor", "Admin"]:
                main_content_column.controls.append(create_cronograma_professor_view(page))
            else:
                main_content_column.controls.append(ft.Container(ft.Text("Acesso Negado: Gerenciamento de Cronogramas.", color=ft.Colors.RED_700), padding=20))
        
        elif item_key == "Gestão Alunos":
            if role in ["Professor", "Admin"]:
                # Chama a tela de ALUNOS
                main_content_column.controls.append(create_gestao_alunos_curso_professor_view(page))
            else:
                main_content_column.controls.append(ft.Container(ft.Text("Acesso Negado.", color=ft.Colors.RED)))

        elif item_key == "Gestão Professores":
            if role == "Admin":
                # Chama a tela de PROFESSORES (Confira se o nome da função é este mesmo)
                # E lembre de passar o 'role' se o seu arquivo pedir
                main_content_column.controls.append(create_gestao_professor_view(page, role))
            else:
                main_content_column.controls.append(ft.Container(ft.Text("Acesso Negado: Apenas Admin.", color=ft.Colors.RED), padding=20))
                    
        elif item_key == "Documentos":
            if role in ["Professor", "Admin"]:
                main_content_column.controls.append(create_gestao_documentos_view(page, role))
            else:
                main_content_column.controls.append(ft.Container(ft.Text("Acesso Negado: Gestão de Documentos.", color=ft.Colors.RED_700), padding=20))
                
   

        elif item_key == "Atividades":
             # Permissão: Aluno (Visão de TAlunoAgenda)
             main_content_column.controls.append(create_atividades_aluno_view(page))

        elif item_key == "Doações": # Ou "Financeiro"
            # Lembre-se de importar create_financeiro_view no topo
            main_content_column.controls.append(create_financeiro_view(page, role))
        
        elif item_key == "Perfil":
            # Passamos 'page' para ele poder acessar o page.client_storage (Token)
            main_content_column.controls.append(get_profile_card(page))

        page.update()
        
    # --- 2. Função de Navegação (Dashboard) ---
    def switch_to_dashboard(role: str):
        page.clean()
        page.client_storage.set("user_role", role)
        
        page.vertical_alignment = ft.MainAxisAlignment.START
        page.horizontal_alignment = ft.CrossAxisAlignment.START
        
        dashboard_content = create_dashboard_view(page, switch_to_login, switch_content, role)
        page.add(dashboard_content)
        
        switch_content("Home", role)
        page.update()

    # --- 3. Função de Navegação (Login) ---
    def switch_to_login():
        page.clean()
        page.client_storage.remove("user_role")
        
        page.vertical_alignment = ft.MainAxisAlignment.CENTER
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        login_content = create_login_view(page, on_success=lambda role: switch_to_dashboard(role))
        page.add(login_content)
        page.update()
        
    # Inicia o aplicativo na tela de Login
    switch_to_login()


if __name__ == "__main__":
    ft.app(target=main)