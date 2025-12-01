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

def create_history_mission(page):

    def mostrar_historia_completa(e):
        dialog = ft.AlertDialog(
            modal=True,
            bgcolor=ft.Colors.WHITE,
            title=ft.Text("História Completa", size=22, weight=ft.FontWeight.BOLD),
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Text(
                            "A Associação Cultural e Esportiva de Apucarana foi fundada com o objetivo de "
                            "preservar, fortalecer e transmitir a cultura japonesa para as futuras gerações. "
                            "Ao longo dos anos, tornou-se um ponto de encontro para celebrações tradicionais, "
                            "práticas esportivas, eventos culturais e atividades comunitárias.\n\n"
                            "Com forte dedicação de voluntários e membros ativos, a associação promove "
                            "integração, respeito, educação e valorização da identidade cultural. Hoje, "
                            "continua sendo um espaço acolhedor, onde tradição e modernidade caminham lado "
                            "a lado para fortalecer a comunidade nikkei da região.",
                            size=14,
                            color=ft.Colors.BLACK87,
                            selectable=True,
                        )
                    ],
                    scroll=ft.ScrollMode.AUTO,
                    height=250 #
                ),
                padding=10,
                width=400, 
            ),
            actions=[
                # Usa lambda para chamar page.close passando o próprio dialog
                ft.TextButton("Fechar", on_click=lambda e: page.close(dialog))
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        # MÉTODO NOVO E CORRETO DE ABRIR O DIALOG
        page.open(dialog)

    # --- Retorno do Widget Visual ---
    return ft.Container(
        content=ft.Column(
            [
                ft.Text("Associação Cultural e Esportiva de Apucarana", size=24, weight=ft.FontWeight.W_900, color=ft.Colors.RED_700),
                ft.Divider(height=10, color=ft.Colors.RED_ACCENT_100),
                ft.Text(
                    "A ACEA é uma instituição sem fins lucrativos, fundada em 1948, com o propósito de preservar, promover e difundir a herança cultural japonesa no município de Apucarana e em toda a região do norte do Paraná. ",
                    size=14,
                    color=ft.Colors.BLACK87,
                    selectable=True
                ),
                ft.Container(height=15),
                ft.Text("Valores Chave:", size=16, weight=ft.FontWeight.W_600, color=ft.Colors.BLACK87),
                ft.Row(
                    [
                        ft.Icon(ft.Icons.AUTO_STORIES, color=ft.Colors.BLACK87),
                        ft.Text("Tradição", size=14, color=ft.Colors.BLACK87),
                        ft.VerticalDivider(),
                        ft.Icon(ft.Icons.PEOPLE_ALT, color=ft.Colors.BLACK87),
                        ft.Text("Comunidade", size=14, color=ft.Colors.BLACK87),
                        ft.VerticalDivider(),
                        ft.Icon(ft.Icons.BOOK, color=ft.Colors.BLACK87),
                        ft.Text("Aprendizado", size=14, color=ft.Colors.BLACK87),
                    ], spacing=10
                ),
                ft.Container(height=20),

                ft.ElevatedButton(
                    "Ver História Completa",
                    bgcolor=ft.Colors.TEAL_600,
                    color=ft.Colors.WHITE,
                    on_click=mostrar_historia_completa
                )
            ]
        ),
        padding=ft.padding.only(top=10, right=20),
    )

def create_member_events_panel(): 
    return ft.Container(
        content=ft.Column(
            [
                ft.Divider(height=10, color=ft.Colors.RED_ACCENT_100),
                ft.Text("Visão Geral", size=18, weight=ft.FontWeight.W_600, color=ft.Colors.BLACK87),
                ft.Container(
                    content=ft.Column([
                        ft.Text("Próximos Eventos!", size=16, weight=ft.FontWeight.W_600, color=ft.Colors.RED_700), 
                        ft.Container(height=5), 
                        ft.ElevatedButton("Ver Agenda", bgcolor=ft.Colors.TEAL_700, color=ft.Colors.WHITE)
                    ], spacing=5),
                    padding=15, border_radius=10, bgcolor=ft.Colors.RED_ACCENT_100
                ),
            ]
        ),
        padding=10
    )


def create_dashboard_content(page, role: str):
    # Cria os componentes
    mission_panel = create_history_mission(page)
    event_panel = create_member_events_panel()
    
    return ft.Column(
        [
            ft.Container(height=20),
            mission_panel,  
            event_panel,
            ft.Text(f"\nPermissão Atual: {role}", color=ft.Colors.RED_700 if role in ['Professor', 'Admin'] else ft.Colors.TEAL_700),
        ],
        expand=True
    )

def create_dashboard_view(page, switch_to_login, switch_content, role: str):
    
    def navigation_rail_change(e):
        selected_item_key = list(VIEW_MAPPING.keys())[e.control.selected_index]
        switch_content(selected_item_key, role)
    
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

    # AQUI ESTAVA O PROBLEMA: Precisamos gerar o conteúdo inicial
    initial_content = create_dashboard_content(page, role)

    dashboard_content = ft.Container(
        content=ft.Column(
            [
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
                        # Coluna da Esquerda (Conteúdo Principal)
                        ft.Column(
                            [
                                # INSERÇÃO CORRETA DO CONTEÚDO AQUI
                                initial_content 
                            ],
                            expand=2,
                            scroll=ft.ScrollMode.ADAPTIVE
                        ),

                        # Coluna da Direita (Espaço Extra)
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