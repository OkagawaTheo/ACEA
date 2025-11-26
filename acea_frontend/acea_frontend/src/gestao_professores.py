import flet as ft
import requests

def create_gestao_professor_view(page: ft.Page, role: str): # <--- Adicionei 'role' aqui
    
    API_URL_PROFESSORES = "http://127.0.0.1:8000/pessoa/api/professores/"
    API_URL_CURSOS = "http://127.0.0.1:8000/curso/api/cursos/"

    snack_bar = ft.SnackBar(ft.Text(""))
    page.overlay.append(snack_bar)

    def mostrar_msg(msg, cor=ft.Colors.WHITE):
        snack_bar.content.value = msg
        snack_bar.content.color = cor
        snack_bar.open = True
        page.update()

    def get_headers():
        token = page.client_storage.get("auth_token")
        return {'Authorization': f'Token {token}'} if token else None

    # --- Campos ---
    nome_professor = ft.TextField(label="Nome Completo", width=300)
    email_professor = ft.TextField(label="E-mail", width=300)
    cpf_professor = ft.TextField(label="CPF", width=140)
    especialidade_professor = ft.TextField(label="Especialidade", width=300)

    dropdown_cursos = ft.Dropdown(
        label="Vincular ao Curso (Opcional)",
        width=300,
        options=[],
        color=ft.Colors.BLACK, 
        border_color=ft.Colors.RED_ACCENT_100
    )

    # --- Tabela ---
    professor_data_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID", color=ft.Colors.BLACK)),
            ft.DataColumn(ft.Text("Nome", color=ft.Colors.BLACK)),
            ft.DataColumn(ft.Text("Especialidade", color=ft.Colors.BLACK)),
            ft.DataColumn(ft.Text("E-mail", color=ft.Colors.BLACK)),
            ft.DataColumn(ft.Text("Ações", color=ft.Colors.BLACK)),
        ],
        rows=[], 
        border=ft.border.all(1, ft.Colors.BLACK12),
        vertical_lines=ft.border.BorderSide(0.5, ft.Colors.BLACK12),
        horizontal_lines=ft.border.BorderSide(0.5, ft.Colors.BLACK12),
    )

    # --- Carregar Dados ---
    def carregar_cursos_dropdown():
        headers = get_headers()
        if not headers: return
        try:
            response = requests.get(API_URL_CURSOS, headers=headers)
            if response.status_code == 200:
                lista_cursos = response.json()
                dropdown_cursos.options.clear()
                for curso in lista_cursos:
                    dropdown_cursos.options.append(ft.dropdown.Option(key=str(curso['id_curso']), text=curso['nome']))
                if dropdown_cursos.page: dropdown_cursos.update()
        except Exception: pass

    def carregar_professores():
        headers = get_headers()
        if not headers: return
        try:
            response = requests.get(API_URL_PROFESSORES, headers=headers)
            if response.status_code == 200:
                lista_profs = response.json()
                professor_data_table.rows.clear()

                for prof in lista_profs:
                    # Botões de ação (Só Admin vê)
                    acoes = ft.Text("-", color=ft.Colors.BLACK)
                    if role == "Admin":
                        acoes = ft.Row([
                            ft.IconButton(ft.Icons.EDIT, icon_color=ft.Colors.TEAL_700), 
                            ft.IconButton(ft.Icons.DELETE, icon_color=ft.Colors.RED_ACCENT_700)
                        ])

                    linha = ft.DataRow(cells=[
                        ft.DataCell(ft.Text(str(prof.get('id_professor')), color=ft.Colors.BLACK)),
                        ft.DataCell(ft.Text(prof.get('nome'), color=ft.Colors.BLACK)),
                        ft.DataCell(ft.Text(prof.get('especialidade'), color=ft.Colors.BLACK)),
                        ft.DataCell(ft.Text(prof.get('email'), color=ft.Colors.BLACK)),
                        ft.DataCell(acoes)
                    ])
                    professor_data_table.rows.append(linha)
            elif response.status_code == 403:
                mostrar_msg("Acesso restrito.", ft.Colors.RED)
        except Exception: pass
        
        if professor_data_table.page: page.update()

    def btn_adicionar_click(e):
        headers = get_headers()
        dados_novo_prof = {
            "nome": nome_professor.value,
            "email": email_professor.value,
            "cpf": cpf_professor.value,
            "especialidade": especialidade_professor.value
        }
        try:
            if requests.post(API_URL_PROFESSORES, json=dados_novo_prof, headers=headers).status_code == 201:
                mostrar_msg("Sucesso!", ft.Colors.GREEN)
                carregar_professores()
        except Exception: pass
        page.update()

    # --- Layout Inteligente ---
    
    # 1. Seção de Adicionar (Só aparece se for Admin)
    secao_adicionar = ft.Container()
    if role == "Admin":
        secao_adicionar = ft.Container(
            content=ft.Column([
                ft.Text("Adicionar Novo Professor", size=18, weight=ft.FontWeight.W_600, color=ft.Colors.BLACK),
                ft.Container(
                    content=ft.Column([
                        ft.Text("Atribuir Curso (Visual):", color=ft.Colors.BLACK),
                        dropdown_cursos,
                        ft.Row([nome_professor, email_professor]),
                        ft.Row([cpf_professor, especialidade_professor]),
                        ft.ElevatedButton("Adicionar Professor", icon=ft.Icons.ADD, bgcolor=ft.Colors.RED_700, color=ft.Colors.WHITE, on_click=btn_adicionar_click)
                    ], spacing=10),
                    padding=20, bgcolor=ft.Colors.WHITE, border_radius=10, shadow=ft.BoxShadow(blur_radius=5, color=ft.Colors.BLACK12)
                ),
                ft.Container(height=30),
            ])
        )

    # 2. Montagem Final
    main_column = ft.Column(
        [ 
            ft.Text("Gestão de Professores", size=30, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK),
            ft.Container(height=20),
            
            secao_adicionar, # <--- Aqui está o segredo: só adiciona se for Admin
            
            ft.Row([
                ft.Text("Professores cadastrados", size=18, weight=ft.FontWeight.W_600, color=ft.Colors.BLACK),
                ft.IconButton(ft.Icons.REFRESH, icon_color=ft.Colors.BLUE, on_click=lambda _: carregar_professores())
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),

            ft.Container(
                content=ft.Column([professor_data_table], scroll=ft.ScrollMode.ALWAYS),
                padding=20, bgcolor=ft.Colors.WHITE, border_radius=10, shadow=ft.BoxShadow(blur_radius=5, color=ft.Colors.BLACK12),
                expand=True
            )
        ],
        scroll=ft.ScrollMode.ADAPTIVE,
        expand=True
    )
    
    def inicializar_dados():
        if role == "Admin": carregar_cursos_dropdown()
        carregar_professores()

    main_column.did_mount = inicializar_dados
    return main_column