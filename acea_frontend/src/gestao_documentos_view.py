import flet as ft

def create_gestao_documentos_view(page, role: str):
    
    # Campos para Adicionar/Editar Documento (TDocumento)
    titulo_documento = ft.TextField(label="Título do Documento", width=400)
    descricao_documento = ft.TextField(label="Descrição", multiline=True)
    
    # Simulação da Tabela de Documentos
    documentos_data_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Título")),
            ft.DataColumn(ft.Text("Data")),
            ft.DataColumn(ft.Text("Ações" if role in ["Admin", "Professor"] else "Download")),
        ],
        rows=[
            ft.DataRow(cells=[ft.DataCell(ft.Text("001")), ft.DataCell(ft.Text("Estatuto Oficial")), ft.DataCell(ft.Text("01/01/2025")), 
                              ft.DataCell(ft.Row([ft.IconButton(ft.Icons.CLOUD_DOWNLOAD, icon_color=ft.Colors.TEAL_700),
                                                   *(
                                                       [ft.IconButton(ft.Icons.EDIT, icon_color=ft.Colors.TEAL_700), ft.IconButton(ft.Icons.DELETE, icon_color=ft.Colors.RED_ACCENT_700)]
                                                       if role in ["Admin", "Professor"] else []
                                                   )
                                                 ]))]),
            ft.DataRow(cells=[ft.DataCell(ft.Text("002")), ft.DataCell(ft.Text("Regras do Curso")), ft.DataCell(ft.Text("15/10/2024")), 
                              ft.DataCell(ft.Row([ft.IconButton(ft.Icons.CLOUD_DOWNLOAD, icon_color=ft.Colors.TEAL_700),
                                                   *(
                                                       [ft.IconButton(ft.Icons.EDIT, icon_color=ft.Colors.TEAL_700), ft.IconButton(ft.Icons.DELETE, icon_color=ft.Colors.RED_ACCENT_700)]
                                                       if role in ["Admin", "Professor"] else []
                                                   )
                                                 ]))]),
        ],
        border=ft.border.all(1, ft.Colors.BLACK12),
        vertical_lines=ft.border.BorderSide(0.5, ft.Colors.BLACK12),
        horizontal_lines=ft.border.BorderSide(0.5, ft.Colors.BLACK12),
    )
    
    # --- 1. Seção de CRUD (Visível apenas para Admin/Professor) ---
    crud_section = ft.Container(
        content=ft.Column(
            [
                ft.Text("Adicionar Novo Documento (TDocumento)", size=20, weight=ft.FontWeight.W_600),
                titulo_documento,
                descricao_documento,
                ft.Row([
                    ft.ElevatedButton("Selecionar PDF...", icon=ft.Icons.ATTACH_FILE, color=ft.Colors.BLACK87),
                    ft.ElevatedButton("Salvar Documento", icon=ft.Icons.SAVE, bgcolor=ft.Colors.RED_700, color=ft.Colors.WHITE)
                ]),
            ]
        ),
        padding=20, bgcolor=ft.Colors.WHITE, border_radius=10, shadow=ft.BoxShadow(blur_radius=5, color=ft.Colors.BLACK12)
    ) if role in ["Admin", "Professor"] else ft.Container()
    
    # --- 2. Seção de Visualização (Visível para todos) ---
    view_section = ft.Container(
        content=ft.Column(
            [
                ft.Text("Documentos Oficiais Disponíveis", size=20, weight=ft.FontWeight.W_600),
                documentos_data_table,
            ]
        ),
        padding=20, bgcolor=ft.Colors.WHITE, border_radius=10, shadow=ft.BoxShadow(blur_radius=5, color=ft.Colors.BLACK12),
        margin=ft.margin.only(top=20)
    )

    return ft.Column(
        [
            ft.Text("Gestão de Documentos", size=30, weight=ft.FontWeight.BOLD),
            ft.Container(height=20),
            crud_section,
            view_section
        ],
        scroll=ft.ScrollMode.ADAPTIVE,
        expand=True
    )