import flet as ft

def create_gestao_alunos_curso_professor_view(page):
    
    # Simulação de dados (TCurso)
    cursos_disponiveis = ["Japonês Nível Básico", "Cerimônia do Chá", "Caligrafia Artística"]
    
    # Campos para Adicionar/Editar Aluno (TAluno)
    nome_aluno = ft.TextField(label="Nome Completo do Aluno", width=300)
    email_aluno = ft.TextField(label="E-mail", width=300)
    
    # Tabela para Visualizar Alunos
    alunos_data_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Nome (TAluno)")),
            ft.DataColumn(ft.Text("E-mail")),
            ft.DataColumn(ft.Text("Ações")),
        ],
        rows=[
            ft.DataRow(cells=[ft.DataCell(ft.Text("101")), ft.DataCell(ft.Text("Hanako Yamada")), ft.DataCell(ft.Text("hanako@email.com")), 
                              ft.DataCell(ft.Row([ft.IconButton(ft.Icons.EDIT, icon_color=ft.Colors.TEAL_700), ft.IconButton(ft.Icons.DELETE, icon_color=ft.Colors.RED_ACCENT_700)]))]),
            ft.DataRow(cells=[ft.DataCell(ft.Text("102")), ft.DataCell(ft.Text("Takeshi Tanaka")), ft.DataCell(ft.Text("takeshi@email.com")), 
                              ft.DataCell(ft.Row([ft.IconButton(ft.Icons.EDIT, icon_color=ft.Colors.TEAL_700), ft.IconButton(ft.Icons.DELETE, icon_color=ft.Colors.RED_ACCENT_700)]))]),
        ],
        border=ft.border.all(1, ft.Colors.BLACK12),
        vertical_lines=ft.border.BorderSide(0.5, ft.Colors.BLACK12),
        horizontal_lines=ft.border.BorderSide(0.5, ft.Colors.BLACK12),
    )
    
    # Coluna principal de conteúdo
    main_column = ft.Column(
        [
            ft.Text("Gestão de Alunos por Curso", size=30, weight=ft.FontWeight.BOLD),
            ft.Container(height=20),
            
            # --- 1. Seleção do Curso (TCurso) ---
            ft.Text("Selecione o Curso para Gerenciar:", size=18, weight=ft.FontWeight.W_600),
            ft.Dropdown(
                width=300,
                options=[ft.dropdown.Option(c) for c in cursos_disponiveis],
                value=cursos_disponiveis[0],
                border_color=ft.Colors.RED_ACCENT_100
            ),
            ft.Container(height=30),
            
            # --- 2. Adicionar/Editar Aluno ---
            ft.Text("Adicionar Novo Aluno", size=18, weight=ft.FontWeight.W_600),
            ft.Container(
                content=ft.Row([
                    nome_aluno,
                    email_aluno,
                    ft.ElevatedButton("Adicionar Aluno", icon=ft.Icons.ADD, bgcolor=ft.Colors.RED_700, color=ft.Colors.WHITE)
                ], spacing=20),
                padding=20, bgcolor=ft.Colors.WHITE, border_radius=10, shadow=ft.BoxShadow(blur_radius=5, color=ft.Colors.BLACK12)
            ),
            
            ft.Container(height=30),
            
            # --- 3. Visualização e Remoção ---
            ft.Text("Alunos Matriculados no Curso Selecionado", size=18, weight=ft.FontWeight.W_600),
            ft.Container(
                content=ft.Column([alunos_data_table], scroll=ft.ScrollMode.ALWAYS),
                padding=20, bgcolor=ft.Colors.WHITE, border_radius=10, shadow=ft.BoxShadow(blur_radius=5, color=ft.Colors.BLACK12),
                expand=True
            )
        ],
        scroll=ft.ScrollMode.ADAPTIVE,
        expand=True
    )
    
    return main_column