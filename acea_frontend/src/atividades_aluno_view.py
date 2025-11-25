import flet as ft

def create_atividades_aluno_view(page):
    
    tab_atividade = lambda title: ft.Tab(
        text=title,
        content=ft.Container(
            content=ft.Column(
                [
                    ft.Text(f"Material para a Atividade: {title}", size=16, weight=ft.FontWeight.W_500),
                    ft.Divider(),
                    
                    ft.Row(
                        [
                            ft.Icon(ft.Icons.INSERT_DRIVE_FILE_OUTLINED, color=ft.Colors.TEAL_700),
                            ft.Text("Arquivo de Leitura - Capítulo 3.pdf"),
                            ft.IconButton(ft.Icons.DOWNLOAD, tooltip="Baixar"),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    ),
                    
                    ft.Row(
                        [
                            ft.Icon(ft.Icons.LIVE_HELP, color=ft.Colors.RED_ACCENT_700),
                            ft.Text("Agendar Tutoria com o Professor."),
                            ft.ElevatedButton("Agendar", bgcolor=ft.Colors.RED_700, color=ft.Colors.WHITE, height=30)
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    ),
                    
                    ft.Text("\nProgresso da Atividade: 75% concluído.", color=ft.Colors.BLACK54)
                ]
            ),
            padding=15, bgcolor=ft.Colors.WHITE, border_radius=10, shadow=ft.BoxShadow(blur_radius=3, color=ft.Colors.BLACK12),
            margin=ft.margin.only(top=10)
        )
    )

    return ft.Column(
        [
            ft.Text("Minhas Atividades e Cronograma", size=30, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK87),
            ft.Container(height=20),
            
            ft.Text("Cronograma Atual (TAlunoAgenda)", size=20, weight=ft.FontWeight.W_600, color=ft.Colors.BLACK87),
            
            # Navegação por Tabs das Atividades
            ft.Tabs(
                selected_index=0,
                animation_duration=300,
                indicator_color=ft.Colors.RED_700,
                label_color=ft.Colors.BLACK87,
                unselected_label_color=ft.Colors.BLACK45,
                tabs=[
                    tab_atividade("Aula de Caligrafia"),
                    tab_atividade("Técnicas de Desenho"),
                    tab_atividade("Próxima Prova"),
                ],
                expand=True
            )
        ]
    )