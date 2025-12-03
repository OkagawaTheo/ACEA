import flet as ft

# --- Configuration ---
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

# --- Helper UI Functions ---
def create_value_card(icon, icon_color, title):
    return ft.Container(
        content=ft.Column([
            ft.Icon(icon, color=icon_color, size=32),
            ft.Container(height=5),
            ft.Text(title, weight=ft.FontWeight.W_600, color=ft.Colors.BLACK87, size=15),
        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=2),
        padding=20,
        border=ft.border.all(1, ft.Colors.GREY_200),
        border_radius=10,
        expand=True,
        height=130
    )

def create_event_item(icon, icon_bg, title, date):
    return ft.Container(
        content=ft.Row([
            ft.Container(
                content=ft.Icon(icon, color=ft.Colors.BLACK54 if icon_bg == ft.Colors.GREY_200 else ft.Colors.WHITE, size=16),
                padding=8, 
                bgcolor=icon_bg, 
                border_radius=8,
                width=36, height=36,
                alignment=ft.alignment.center
            ),
            ft.Column([
                ft.Text(title, weight=ft.FontWeight.W_600, size=13, color=ft.Colors.BLACK87),
                ft.Text(date, size=11, color=ft.Colors.GREY_500)
            ], spacing=2, expand=True, alignment=ft.MainAxisAlignment.CENTER),
            ft.Icon(ft.Icons.CHEVRON_RIGHT, size=18, color=ft.Colors.GREY_400)
        ], alignment=ft.MainAxisAlignment.START, vertical_alignment=ft.CrossAxisAlignment.CENTER),
        padding=ft.padding.symmetric(vertical=8),
    )

# --- Main Components ---
def create_history_mission(page):
    def mostrar_historia_completa(e):
        dialog = ft.AlertDialog(
            title=ft.Text("História Completa"),
            content=ft.Container(
                content=ft.Text("A Associação Cultural e Esportiva de Apucarana foi fundada em 1948...", ),
                padding=10
            ),
        )
        page.open(dialog) # Updated to page.open

    return ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Container(
                    content=ft.Icon(ft.Icons.TEMPLE_BUDDHIST, color=ft.Colors.RED_700, size=70),
                    padding=10, 
                    border_radius=8
                ),
                ft.Column([
                    ft.Text("Associação Cultural e Esportiva de Apucarana", size=32, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK87),
                    ft.Text("Fundada em 1948 • Instituição sem fins lucrativos", size=18, color=ft.Colors.GREY_500),
                ], spacing=0, alignment=ft.MainAxisAlignment.CENTER)
            ], alignment=ft.MainAxisAlignment.START, vertical_alignment=ft.CrossAxisAlignment.CENTER),
            
            ft.Container(height=20),
            ft.Text("Nossos Valores Essenciais", weight=ft.FontWeight.W_700, color=ft.Colors.BLACK87, size=24),
            ft.Container(height=10),

            ft.Row([
                create_value_card(ft.Icons.ARCHITECTURE, ft.Colors.RED_600, "Tradição"),
                create_value_card(ft.Icons.GROUPS, ft.Colors.GREEN_700, "Comunidade"),
                create_value_card(ft.Icons.SCHOOL, ft.Colors.BLUE_600, "Educação"),
            ], spacing=15),
            
            ft.Container(height=30),
            
            ft.ElevatedButton(
                content=ft.Row([
                    ft.Icon(ft.Icons.BOOK, size=16, color=ft.Colors.WHITE),
                    ft.Text("Explorar História Completa", color=ft.Colors.WHITE, weight=ft.FontWeight.W_600)
                ], alignment=ft.MainAxisAlignment.CENTER),
                style=ft.ButtonStyle(
                    bgcolor=ft.Colors.RED_800,
                    shape=ft.RoundedRectangleBorder(radius=6),
                    padding=ft.padding.symmetric(horizontal=20, vertical=18)
                ),
                on_click=mostrar_historia_completa,
                width=240
            )
        ]),
        bgcolor=ft.Colors.WHITE,
        padding=40,
        border_radius=12,
        shadow=ft.BoxShadow(blur_radius=15, color=ft.Colors.with_opacity(0.06, ft.Colors.BLACK))
    )

def create_right_sidebar(role, switch_content_callback):
    return ft.Column([
        ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Text("Próximos Eventos", size=15, weight=ft.FontWeight.W_700, color=ft.Colors.BLACK87),
                    ft.Icon(ft.Icons.CALENDAR_TODAY, color=ft.Colors.RED_700, size=18)
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                
                ft.Container(height=10),
                create_event_item(ft.Icons.LOCAL_FLORIST, ft.Colors.BROWN_200, "Sakura Matsuri", "15 Mar"),
                create_event_item(ft.Icons.BRUSH, ft.Colors.BLUE_100, "Aula de Caligrafia", "18 Mar"),
                create_event_item(ft.Icons.SPORTS_MARTIAL_ARTS, ft.Colors.GREY_700, "Campeonato de Judô", "22 Mar"),
                create_event_item(ft.Icons.NATURE, ft.Colors.BROWN_300, "Workshop de Ikebana", "25 Mar"),
                
                ft.Container(height=15),
                
                ft.ElevatedButton(
                    content=ft.Row([
                        ft.Icon(ft.Icons.CALENDAR_MONTH, size=16, color=ft.Colors.RED_700),
                        ft.Text("Ver Agenda Completa", color=ft.Colors.RED_700, size=12)
                    ], alignment=ft.MainAxisAlignment.CENTER),
                    style=ft.ButtonStyle(
                        bgcolor=ft.Colors.GREY_300,
                        shape=ft.RoundedRectangleBorder(radius=6),
                        padding=15
                    ),
                    width=400,
                    on_click=lambda _: switch_content_callback("Cronogramas", role) if switch_content_callback else None
                )
            ]),
            bgcolor=ft.Colors.WHITE,
            padding=25,
            border_radius=12,
            shadow=ft.BoxShadow(blur_radius=15, color=ft.Colors.with_opacity(0.06, ft.Colors.BLACK))
        ),
        
        ft.Container(height=20),
        
        ft.Container(
            content=ft.Column([
                ft.Text("Permissão Atual", weight=ft.FontWeight.W_700, size=14, color=ft.Colors.BLACK87),
                ft.Container(height=5),
                ft.Container(
                    content=ft.Row([
                        ft.Icon(ft.Icons.SECURITY, color=ft.Colors.WHITE, size=20),
                        ft.Text(role if role else "Admin", weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE, size=16)
                    ], alignment=ft.MainAxisAlignment.CENTER, spacing=10),
                    bgcolor=ft.Colors.RED_700,
                    padding=15,
                    border_radius=8,
                    on_click=lambda _: switch_content_callback("Perfil", role) if switch_content_callback else None,
                    ink=True
                ),
            ]),
            bgcolor=ft.Colors.WHITE,
            padding=25,
            border_radius=12,
            shadow=ft.BoxShadow(blur_radius=15, color=ft.Colors.with_opacity(0.06, ft.Colors.BLACK))
        )
    ])

def create_dashboard_content(page, role: str):
    return create_history_mission(page)

def create_dashboard_view(page, switch_to_login, switch_content, role: str):
    
    def navigation_rail_change(e):
        selected_item_key = list(VIEW_MAPPING.keys())[e.control.selected_index]
        switch_content(selected_item_key, role)
    
    # Sidebar (Standard)
    rail = ft.NavigationRail(
        selected_index=0, 
        label_type=ft.NavigationRailLabelType.ALL, 
        min_width=100, 
        min_extended_width=100,
        bgcolor=ft.Colors.BLACK,
        indicator_color=ft.Colors.GREY_800,
        indicator_shape=ft.RoundedRectangleBorder(radius=10),
        leading=ft.Container(
            content=ft.Text("文.", size=40, weight=ft.FontWeight.BOLD, color=ft.Colors.RED_ACCENT_400),
            alignment=ft.alignment.center, 
            height=100
        ),
        destinations=[
            ft.NavigationRailDestination(icon=ft.Icons.HOME_OUTLINED, selected_icon=ft.Icons.HOME, label="Home"),
            ft.NavigationRailDestination(icon=ft.Icons.PERSON_OUTLINE, selected_icon=ft.Icons.PERSON, label="Perfil"),
            ft.NavigationRailDestination(icon=ft.Icons.CALENDAR_MONTH_OUTLINED, selected_icon=ft.Icons.CALENDAR_MONTH, label="Cronogramas"),
            ft.NavigationRailDestination(icon=ft.Icons.GROUP_OUTLINED, selected_icon=ft.Icons.GROUP, label="Gestão Alunos"),
            ft.NavigationRailDestination(icon=ft.Icons.SCHOOL_OUTLINED, selected_icon=ft.Icons.SCHOOL, label="Gestão Profs"),
            ft.NavigationRailDestination(icon=ft.Icons.FOLDER_OUTLINED, selected_icon=ft.Icons.FOLDER, label="Documentos"),
            ft.NavigationRailDestination(icon=ft.Icons.EDIT_NOTE_OUTLINED, selected_icon=ft.Icons.EDIT_NOTE, label="Atividades"),
            ft.NavigationRailDestination(icon=ft.Icons.VOLUNTEER_ACTIVISM_OUTLINED, selected_icon=ft.Icons.VOLUNTEER_ACTIVISM, label="Doações"),
        ],
        trailing=ft.Container(
            content=ft.IconButton(icon=ft.Icons.LOGOUT_ROUNDED, icon_color=ft.Colors.WHITE, tooltip="Sair / Logout", on_click=lambda e: switch_to_login()),
            margin=ft.margin.only(top=50) 
        ),
        on_change=navigation_rail_change
    )

    initial_main_content = create_dashboard_content(page, role)
    right_sidebar = create_right_sidebar(role, switch_content)

    # --- LAYOUT FIX: Removed scroll=ft.ScrollMode.HIDDEN from inner columns ---
    # This allows the cronogram list to calculate its height correctly.
    content_row = ft.Row(
        [
            ft.Column([initial_main_content], expand=7), # Removed scroll=Hidden
            ft.Container(width=20),
            ft.Column([right_sidebar], expand=3)  # Removed scroll=Hidden
        ],
        vertical_alignment=ft.CrossAxisAlignment.START,
        # Removed expand=True from Row to let content flow naturally
    )

    dashboard_layout = ft.Container(
        content=ft.Column(
            [
                ft.Container(height=10),
                content_row
            ],
            scroll=ft.ScrollMode.AUTO, # The main container handles the scroll
            expand=True
        ),
        padding=ft.padding.all(30), 
        expand=True,
        bgcolor="#FFF9F6" 
    )

    return ft.Row(
        [
            rail, 
            ft.VerticalDivider(width=1, color=ft.Colors.TRANSPARENT), 
            dashboard_layout
        ], 
        expand=True, 
        spacing=0
    )