import flet as ft

# Esta função retorna APENAS o card de conteúdo do perfil, 
# sem incluir o Top Bar ou o Sidebar do Dashboard.
def get_profile_card():
    # --- 1. Seção Imagem ---

    # Imagem de Perfil com ícone de câmera sobreposto
    profile_picture_section = ft.Container(
        content=ft.Stack(
            [
                ft.CircleAvatar(
                    radius=60,
                    content=ft.Icon(ft.Icons.PERSON_OUTLINE_ROUNDED, size=70, color=ft.Colors.BLUE_GREY_400),
                    bgcolor=ft.Colors.BLUE_GREY_100,
                ),
                ft.Container(
                    content=ft.Icon(ft.Icons.CAMERA_ALT_OUTLINED, size=18, color=ft.Colors.WHITE),
                    width=30, height=30,
                    bgcolor=ft.Colors.BLUE_GREY_400,
                    border_radius=ft.border_radius.all(15),
                    alignment=ft.alignment.center,
                    left=80, top=90, # Posição sobre a imagem
                )
            ]
        ),
        alignment=ft.alignment.center_left,
        width=150,
        height=150
    )

    # Botões LOGO e VENDOR DOCUMENTS (Colocados em uma coluna para empilhamento vertical)
    action_buttons_row = ft.Column(
        [
            ft.ElevatedButton(
                content=ft.Row([ft.Icon(ft.Icons.FOLDER_OUTLINED, size=16), ft.Text("Logo", size=12)], spacing=5),
                style=ft.ButtonStyle(
                    bgcolor={'default': ft.Colors.BLUE_GREY_50},
                    color={'default': ft.Colors.BLUE_GREY_700},
                    shape={'default': ft.RoundedRectangleBorder(radius=ft.border_radius.all(5))},
                    padding={'default': ft.padding.symmetric(vertical=8, horizontal=10)}
                ),
                height=40
            ),
            ft.ElevatedButton(
                content=ft.Row([ft.Icon(ft.Icons.UPLOAD_FILE_OUTLINED, size=16), ft.Text("Documentos", size=12)], spacing=5),
                style=ft.ButtonStyle(
                    bgcolor={'default': ft.Colors.BLUE_GREY_50},
                    color={'default': ft.Colors.BLUE_GREY_700},
                    shape={'default': ft.RoundedRectangleBorder(radius=ft.border_radius.all(5))},
                    padding={'default': ft.padding.symmetric(vertical=8, horizontal=10)}
                ),
                height=40
            )
        ],
        spacing=10,
        horizontal_alignment=ft.CrossAxisAlignment.START # Alinha botões à esquerda
    )

    # 💡 NOVO AGRUPAMENTO: Coluna que contém a Imagem E os Botões
    image_and_buttons_column = ft.Column(
        [
            profile_picture_section,
            action_buttons_row
        ],
        spacing=20, # Espaço entre a imagem e os botões
        horizontal_alignment=ft.CrossAxisAlignment.START
    )

    # --- 2. Seção Detalhes do Usuário e Botão Editar ---
    
    # Detalhes: Nome, Email, Telefone, Endereço
    profile_info = ft.Column(
        [
            # Primeira linha de informações (Nome e Email)
            ft.Row(
                [
                    ft.Column([
                        ft.Text("Nome:", size=14, color=ft.Colors.BLUE_GREY_700, weight=ft.FontWeight.W_600),
                        ft.Text("User name", size=14, color=ft.Colors.BLUE_GREY_500),
                    ], spacing=2, width=200),
                    ft.Column([
                        ft.Text("Email:", size=14, color=ft.Colors.BLUE_GREY_700, weight=ft.FontWeight.W_600),
                        ft.Text("imiega@paytech.co", size=14, color=ft.Colors.BLUE_GREY_500),
                    ], spacing=2, width=200),
                ],
                spacing=50
            ),
            ft.Container(height=20),
            # Segunda linha de informações (Telefone e Endereço)
            ft.Row(
                [
                    ft.Column([
                        ft.Text("Telefone:", size=14, color=ft.Colors.BLUE_GREY_700, weight=ft.FontWeight.W_600),
                        ft.Text("+20-01274318900", size=14, color=ft.Colors.BLUE_GREY_500),
                    ], spacing=2, width=200),
                    ft.Column([
                        ft.Text("Endereço:", size=14, color=ft.Colors.BLUE_GREY_700, weight=ft.FontWeight.W_600),
                        ft.Text("285 N Broad St, Elizabeth, NJ 07208, USA", size=14, color=ft.Colors.BLUE_GREY_500),
                    ], spacing=2, width=200),
                ],
                spacing=50
            ),
            ft.Container(height=30),
            # Botão EDIT PROFILE
            ft.ElevatedButton(
                content=ft.Row([ft.Icon(ft.Icons.EDIT_OUTLINED, size=16), ft.Text("Editar Perfil", size=12)], spacing=5),
                style=ft.ButtonStyle(
                    bgcolor={'default': ft.Colors.BLUE_GREY_50},
                    color={'default': ft.Colors.BLUE_GREY_700},
                    shape={'default': ft.RoundedRectangleBorder(radius=ft.border_radius.all(5))},
                    padding={'default': ft.padding.symmetric(vertical=10, horizontal=15)}
                ),
                height=40
            )
        ],
        expand=True
    )

    # --- Card Principal (Main Profile Container) ---
    main_profile_content = ft.Container(
        content=ft.Column(
            [
                # Título "Profile"
                ft.Row(
                    [
                        ft.Icon(ft.Icons.PERSON_OUTLINE, size=24, color=ft.Colors.BLUE_GREY_700),
                        ft.Text("Perfil", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_GREY_700)
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.CENTER
                ),
                ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                # Linha de Conteúdo: AGRUPAMENTO DE IMAGEM/BOTÕES + Detalhes
                ft.Row(
                    [
                        image_and_buttons_column, # 💡 NOVO: Coluna contendo Imagem e Botões
                        ft.VerticalDivider(width=30, color=ft.Colors.TRANSPARENT), 
                        profile_info,            # Informações de Contato
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.START,
                    spacing=20,
                    expand=True
                )
            ],
            scroll=ft.ScrollMode.ADAPTIVE,
            expand=True
        ),
        padding=20,
        bgcolor=ft.Colors.WHITE,
        border_radius=ft.border_radius.all(10),
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=5,
            color=ft.Colors.BLACK12,
            offset=ft.Offset(0, 0),
        ),
        expand=True
    )
    
    # Retorna uma Coluna contendo apenas o card para ser injetado no layout principal
    return ft.Column([main_profile_content], expand=True)