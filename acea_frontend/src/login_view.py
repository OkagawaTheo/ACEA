import flet as ft

def create_login_view(page: ft.Page, on_success):
    # Campos de entrada
    username_field = ft.TextField(
        label="Usuário", icon=ft.Icons.PERSON, width=300, border_color=ft.Colors.RED_ACCENT_100
    )
    password_field = ft.TextField(
        label="Senha", password=True, can_reveal_password=True, icon=ft.Icons.LOCK, width=300, border_color=ft.Colors.RED_ACCENT_100
    )
    message_label = ft.Text(value="", color=ft.Colors.RED_400)

    # Função de Ação de Login
    def login_clicked(e):
        # Simulação de autenticação com atribuição de papel
        if username_field.value == "professor":
            user_role = "Professor"
        elif username_field.value == "admin":
            user_role = "Admin"
        elif username_field.value == "aluno" and password_field.value == "123":
            user_role = "Aluno"
        else:
            user_role = None

        if user_role:
            message_label.value = f"Login realizado! Bem-vindo(a) {user_role}. 🎉"
            message_label.color = ft.Colors.TEAL_600
            page.update()
            
            try:
                on_success(user_role) # Chama o dashboard com o papel
            except Exception as ex:
                print(f"Erro ao navegar para o Dashboard: {ex}")
                page.clean()
                page.add(ft.Text(f"Erro fatal: {ex}"))
                page.update()
        else:
            message_label.value = "Usuário ou senha incorretos."
            message_label.color = ft.Colors.RED_400
            page.update()

    # Botão de login (Vermilion)
    login_button = ft.ElevatedButton(
        text="ENTRAR", on_click=login_clicked, width=300, bgcolor=ft.Colors.RED_700, color=ft.Colors.WHITE
    )

    # Cartão de Login
    return ft.Container(
        content=ft.Column(
            [
                ft.Text("Login", size=30, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK87),
                ft.Divider(color=ft.Colors.RED_ACCENT_100),
                username_field,
                password_field,
                ft.Container(height=10),
                login_button,
                ft.Container(height=10),
                message_label,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=15
        ),
        padding=30, border_radius=15, bgcolor=ft.Colors.WHITE,
        shadow=ft.BoxShadow(
            spread_radius=1, blur_radius=15, color=ft.Colors.BLACK12, offset=ft.Offset(0, 0), blur_style=ft.ShadowBlurStyle.NORMAL,
        )
    )