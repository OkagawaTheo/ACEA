import flet as ft

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

# --- FUNÇÕES DE COMPONENTES FIXOS DO DASHBOARD ---

def create_history_mission():
    return ft.Container(
        content=ft.Column(
            [
                ft.Text("Nossa Missão", size=24, weight=ft.FontWeight.W_900, color=ft.Colors.RED_700),
                ft.Divider(height=10, color=ft.Colors.RED_ACCENT_100),
                ft.Text("Associação Cultural e Esportiva de Apucarana, fundada para preservar a cultura japonesa.", size=14, color=ft.Colors.BLACK87, selectable=True),
                ft.Container(height=15),
                ft.Text("Valores Chave:", size=16, weight=ft.FontWeight.W_600, color=ft.Colors.BLACK87),
                ft.Row(
                    [
                        ft.Icon(ft.Icons.AUTO_STORIES, color=ft.Colors.RED_ACCENT_700), ft.Text("Tradição", size=14, color=ft.Colors.BLACK87), ft.VerticalDivider(),
                        ft.Icon(ft.Icons.PEOPLE_ALT, color=ft.Colors.RED_ACCENT_700), ft.Text("Comunidade", size=14, color=ft.Colors.BLACK87), ft.VerticalDivider(),
                        ft.Icon(ft.Icons.BOOK, color=ft.Colors.RED_ACCENT_700), ft.Text("Aprendizado", size=14, color=ft.Colors.BLACK87),
                    ], spacing=10
                ),
                ft.Container(height=20),
                ft.Row([ft.ElevatedButton("Ver História Completa 📖", bgcolor=ft.Colors.TEAL_600, color=ft.Colors.WHITE)])
            ]
        ),
        padding=ft.padding.only(top=10, right=20),
    )


def create_member_events_panel(): 
    # chamado por event
    
    return ft.Container(
        content=ft.Column(
            [
                ft.Text("Visão Geral", size=18, weight=ft.FontWeight.W_600, color=ft.Colors.BLACK87),
                ft.Divider(height=10, color="transparent"),
                ft.Container(
                    content=ft.Column([ft.Text("Próximos Eventos! 🏮", size=16, weight=ft.FontWeight.W_600, color=ft.Colors.RED_700), ft.Text("Não perca a Cerimônia de Chá...", size=12, color=ft.Colors.BLACK54), ft.Container(height=5), ft.ElevatedButton("Ver Agenda", bgcolor=ft.Colors.TEAL_700, color=ft.Colors.WHITE)], spacing=5),
                    padding=15, border_radius=10, bgcolor=ft.Colors.RED_ACCENT_100
                ),
                ft.Divider(height=25, color="transparent"),
                ft.Text("Estatísticas da Associação", size=18, weight=ft.FontWeight.W_600, color=ft.Colors.BLACK87),
                
                ft.Row(
                    [
                        ft.Card(content=ft.Container(content=ft.Column([ft.Text("85", size=30, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK87), ft.Text("Membros Ativos", size=12, color=ft.Colors.BLACK54)], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.START), padding=15), elevation=0, margin=0, width=120, color=ft.Colors.WHITE),
                        ft.Card(content=ft.Container(content=ft.Column([ft.Text("12", size=30, weight=ft.FontWeight.BOLD, color=ft.Colors.RED_ACCENT_700), ft.Text("Aulas / Cursos", size=12, color=ft.Colors.BLACK54)], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.START), padding=15), elevation=0, margin=0, width=120, color=ft.Colors.WHITE),
                    ], spacing=15
                ),
            ]
        ),
        padding=10
    )

def create_dashboard_content(page, role: str):
    # 💡 AGORA, ADICIONAMOS O PAINEL DE EVENTOS AQUI
    event_panel = create_member_events_panel() 
    
    return ft.Column(
        [
            # Mantenha a Missão (que faz parte da Home)
            ft.Container(height=20),
            create_history_mission(),
            
            # Adicione o Painel de Eventos (que agora é dinâmico)
            event_panel,
            
            ft.Text(f"\nPermissão Atual: {role}", color=ft.Colors.RED_700 if role in ['Professor', 'Admin'] else ft.Colors.TEAL_700),
        ],
        expand=True
    )
def create_dashboard_view(page, switch_to_login, switch_content, role: str):
    
    def navigation_rail_change(e):
        selected_item_key = list(VIEW_MAPPING.keys())[e.control.selected_index]
        switch_content(selected_item_key, role)
    
    # --- Painel Lateral (Navigation Rail) ---
    rail = ft.NavigationRail(
        selected_index=0, label_type=ft.NavigationRailLabelType.ALL, min_width=80, min_extended_width=100,
        bgcolor=ft.Colors.BLACK,
        destinations=[
            ft.NavigationRailDestination(icon=ft.Icons.HOME_OUTLINED, selected_icon=ft.Icons.HOME, label="Home"),
            ft.NavigationRailDestination(icon=ft.Icons.PERSON_OUTLINE, selected_icon=ft.Icons.PERSON, label="Perfil"),
            ft.NavigationRailDestination(icon=ft.Icons.CALENDAR_MONTH_OUTLINED, selected_icon=ft.Icons.CALENDAR_MONTH, label="Cronogramas"),
            ft.NavigationRailDestination(icon=ft.Icons.GROUP_OUTLINED, selected_icon=ft.Icons.GROUP, label="Gestão Alunos"),
            ft.NavigationRailDestination(icon=ft.Icons.SCHOOL_OUTLINED, selected_icon=ft.Icons.SCHOOL, label="Gestão Professores"),
            ft.NavigationRailDestination(icon=ft.Icons.FOLDER_OUTLINED, selected_icon=ft.Icons.FOLDER, label="Documentos"),
            ft.NavigationRailDestination(icon=ft.Icons.EDIT_NOTE_OUTLINED, selected_icon=ft.Icons.EDIT_NOTE, label="Atividades"),
            ft.NavigationRailDestination(icon=ft.Icons.VOLUNTEER_ACTIVISM_OUTLINED, selected_icon=ft.Icons.VOLUNTEER_ACTIVISM, label="Doações"),
        ],
        trailing=ft.Container(
            content=ft.IconButton(
                icon=ft.Icons.LOGOUT_ROUNDED, icon_color=ft.Colors.WHITE, tooltip="Sair / Logout",
                on_click=lambda e: switch_to_login()
            ),
            margin=ft.margin.only(top=150)
        ),
        leading=ft.Container(content=ft.Text("文.", size=30, weight=ft.FontWeight.BOLD, color=ft.Colors.RED_ACCENT_400), alignment=ft.alignment.center, height=70),
        on_change=navigation_rail_change
    )

    dashboard_content = ft.Container(
        content=ft.Column(
            [
                # 1. Cabeçalho/Saudação
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Column([ft.Text(f"Bem-vindo(a), {role}!", size=30, weight=ft.FontWeight.W_600, color=ft.Colors.BLACK87), ft.Text("Gerencie membros, aulas e eventos.", color=ft.Colors.BLACK54)], alignment=ft.MainAxisAlignment.START, spacing=2),
                            ft.Icon(ft.Icons.ARCHITECTURE_OUTLINED, size=80, color=ft.Colors.BLACK87),
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    ),
                    padding=ft.padding.only(left=20, right=20, top=20, bottom=20),
                    bgcolor=ft.Colors.WHITE, border_radius=10,
                ),

                ft.Row(
                    [
                        ft.Column(
                            [
                                # Este placeholder será preenchido pelo app.py
                            ],
                            expand=2,
                            scroll=ft.ScrollMode.ADAPTIVE
                        ),

                        ft.Column(
                            [
                                ft.Container(height=20),
                        
                            ],
                            expand=1,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER
                        )
                    ],
                    expand=True, vertical_alignment=ft.CrossAxisAlignment.START
                ),
            ],
            scroll=ft.ScrollMode.ADAPTIVE, expand=True
        ),
        padding=ft.padding.only(top=0, left=20, right=20, bottom=20), expand=True
    )

    return ft.Row([rail, ft.VerticalDivider(width=1, color=ft.Colors.BLACK12), dashboard_content], expand=True, spacing=0, vertical_alignment=ft.CrossAxisAlignment.START)