import flet as ft

def create_gestao_professor_view(page):
    # Simulação de dados (TCurso)
    cursos_disponiveis = ["Japonês Nível Básico", "Cerimônia do Chá", "Caligrafia Artística"]
    
    # Campos para Adicionar/Editar Professor (TProfessor)
    nome_professor = ft.TextField(label="Nome Completo do Professor", width=300)
    email_professor = ft.TextField(label="E-mail", width=300)
    
    # Tabela para Visualizar Professores
    professor_data_table = ft.DataTable(
        # Cores para os Cabeçalhos da Tabela (Columns)
        columns=[
            ft.DataColumn(ft.Text("ID", color=ft.Colors.BLACK)), # Corrigido o contraste
            ft.DataColumn(ft.Text("Nome (TProfessor)", color=ft.Colors.BLACK)), # Corrigido o contraste
            ft.DataColumn(ft.Text("E-mail", color=ft.Colors.BLACK)), # Corrigido o contraste
            ft.DataColumn(ft.Text("Ações", color=ft.Colors.BLACK)), # Corrigido o contraste
        ],
        rows=[
            # Linha 1: Cores para o Conteúdo da Tabela (Cells)
            ft.DataRow(cells=[
                ft.DataCell(ft.Text("101", color=ft.Colors.BLACK)), # Cor da célula ID
                ft.DataCell(ft.Text("Hanako Yamada", color=ft.Colors.BLACK)), # Cor da célula Nome
                ft.DataCell(ft.Text("hanako@email.com", color=ft.Colors.BLACK)), # Cor da célula E-mail
                ft.DataCell(ft.Row([ft.IconButton(ft.Icons.EDIT, icon_color=ft.Colors.TEAL_700), ft.IconButton(ft.Icons.DELETE, icon_color=ft.Colors.RED_ACCENT_700)]))
            ]),
            # Linha 2: Cores para o Conteúdo da Tabela (Cells)
            ft.DataRow(cells=[
                ft.DataCell(ft.Text("102", color=ft.Colors.BLACK)),
                ft.DataCell(ft.Text("Takeshi Tanaka", color=ft.Colors.BLACK)),
                ft.DataCell(ft.Text("takeshi@email.com", color=ft.Colors.BLACK)),
                ft.DataCell(ft.Row([ft.IconButton(ft.Icons.EDIT, icon_color=ft.Colors.TEAL_700), ft.IconButton(ft.Icons.DELETE, icon_color=ft.Colors.RED_ACCENT_700)]))
            ]),
        ],
        border=ft.border.all(1, ft.Colors.BLACK12),
        vertical_lines=ft.border.BorderSide(0.5, ft.Colors.BLACK12),
        horizontal_lines=ft.border.BorderSide(0.5, ft.Colors.BLACK12),
    )
    
    # Coluna principal de conteúdo
    main_column = ft.Column(
        [ 
            # 💡 Corrigindo os títulos principais
            ft.Text("Gestão de Professor(es) por Curso", size=30, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK),
            ft.Container(height=20),
            
            # --- 1. Seleção do Curso (TCurso) ---
            ft.Text("Selecione o Curso para Gerenciar:", size=18, weight=ft.FontWeight.W_600, color=ft.Colors.BLACK),
            ft.Dropdown(
                width=300,
                options=[ft.dropdown.Option(c) for c in cursos_disponiveis],
                value=cursos_disponiveis[0],
                color=ft.Colors.BLACK, # Corrigido o contraste do Dropdown
                border_color=ft.Colors.RED_ACCENT_100
            ),
            ft.Container(height=30),
            
            # --- 2. Adicionar/Editar Aluno ---
            ft.Text("Adicionar Novo Professor", size=18, weight=ft.FontWeight.W_600, color=ft.Colors.BLACK),
            ft.Container(
                content=ft.Row([
                    nome_professor,
                    email_professor,
                    # O botão já está com cores de alto contraste (vermelho no branco)
                    ft.ElevatedButton("Adicionar Aluno", icon=ft.Icons.ADD, bgcolor=ft.Colors.RED_700, color=ft.Colors.WHITE)
                ], spacing=20),
                padding=20, bgcolor=ft.Colors.WHITE, border_radius=10, shadow=ft.BoxShadow(blur_radius=5, color=ft.Colors.BLACK12)
            ),
            
            ft.Container(height=30),
            
            # --- 3. Visualização e Remoção ---
            ft.Text("Professores cadastrados", size=18, weight=ft.FontWeight.W_600, color=ft.Colors.BLACK),
            ft.Container(
                content=ft.Column([professor_data_table], scroll=ft.ScrollMode.ALWAYS),
                padding=20, bgcolor=ft.Colors.WHITE, border_radius=10, shadow=ft.BoxShadow(blur_radius=5, color=ft.Colors.BLACK12),
                expand=True
            )
        ],
        scroll=ft.ScrollMode.ADAPTIVE,
        expand=True
    )
    
    return main_column