import flet as ft

def create_cronograma_professor_view(page):
    
    # Campo para edição
    nome_cronograma = ft.TextField(label="Nome do Cronograma", width=400)
    descricao_cronograma = ft.TextField(label="Descrição", multiline=True)
    
    # Simulação da lista de Cronogramas existentes
    cronogramas_list = ft.Column(
        [
            ft.Text("Cronogramas Ativos", size=18, weight=ft.FontWeight.W_600, color=ft.Colors.BLACK87),
            ft.Divider(color=ft.Colors.BLACK12),
            
            # Item: Título + Botão de Edição/Exclusão
            ft.Container(
                content=ft.Row(
                    [
                        ft.Text("Aulas de Idioma Nível 1", weight=ft.FontWeight.W_500),
                        ft.Row([
                            ft.IconButton(ft.Icons.EDIT, icon_color=ft.Colors.TEAL_700, tooltip="Editar"),
                            ft.IconButton(ft.Icons.DELETE, icon_color=ft.Colors.RED_ACCENT_700, tooltip="Excluir"),
                        ])
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
                padding=10, border=ft.border.all(1, ft.Colors.RED_ACCENT_100), border_radius=5
            ),
            ft.Container(height=10),
            ft.Text("Lista completa dos cronogramas do TProfessor...", color=ft.Colors.BLACK54)
        ]
    )

    save_button = ft.ElevatedButton(
        text="Salvar Novo Cronograma",
        bgcolor=ft.Colors.RED_700,
        color=ft.Colors.WHITE,
        icon=ft.Icons.SAVE
    )

    return ft.Column(
        [
            ft.Text("Gerenciamento de Cronogramas", size=30, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK87),
            ft.Container(height=20),

            ft.Row(
                [
                    # Coluna de Criação/Edição
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Text("Criar/Editar Novo", size=20, weight=ft.FontWeight.W_600, color=ft.Colors.BLACK87),
                                nome_cronograma,
                                descricao_cronograma,
                                ft.Container(height=10),
                                save_button
                            ]
                        ),
                        padding=20,
                        bgcolor=ft.Colors.WHITE,
                        border_radius=10,
                        shadow=ft.BoxShadow(blur_radius=5, color=ft.Colors.BLACK12),
                        width=500
                    ),
                    
                    ft.Container(width=40), # Espaçamento
                    
                    # Coluna de Listagem
                    ft.Container(
                        content=cronogramas_list,
                        padding=20,
                        bgcolor=ft.Colors.WHITE,
                        border_radius=10,
                        shadow=ft.BoxShadow(blur_radius=5, color=ft.Colors.BLACK12),
                        expand=True
                    )
                ],
                vertical_alignment=ft.CrossAxisAlignment.START
            )
        ],
        scroll=ft.ScrollMode.ADAPTIVE
    )