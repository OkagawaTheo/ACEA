import flet as ft
import requests # <--- BIBLIOTECA PARA CONECTAR AO DJANGO

def create_login_view(page: ft.Page, on_success):
    # Campos de entrada (Seu design original)
    username_field = ft.TextField(
        label="Usuário", icon=ft.Icons.PERSON, width=300, border_color=ft.Colors.RED_ACCENT_100
    )
    password_field = ft.TextField(
        label="Senha", password=True, can_reveal_password=True, icon=ft.Icons.LOCK, width=300, border_color=ft.Colors.RED_ACCENT_100
    )
    message_label = ft.Text(value="", color=ft.Colors.RED_400)

    def login_clicked(e):
        message_label.value = "Conectando ao servidor..."
        message_label.color = ft.Colors.BLUE_GREY
        page.update()

        API_URL = "http://127.0.0.1:8000/pessoa/api/login/"

        try:
            response = requests.post(API_URL, json={
                "username": username_field.value,
                "password": password_field.value
            })

            if response.status_code == 200:
                dados = response.json()
                
                tipo_vindo_do_back = dados.get('tipo_usuario')
                token = dados.get('token')

                mapa_papeis = {
                    'aluno': 'Aluno',
                    'professor': 'Professor',
                    'admin': 'Admin'
                }
                user_role = mapa_papeis.get(tipo_vindo_do_back)

                if user_role:
                    page.client_storage.set("auth_token", token)
                    
                    message_label.value = f"Login realizado! Bem-vindo(a) {user_role}."
                    message_label.color = ft.Colors.TEAL_600
                    page.update()
                    
                    on_success(user_role)
                else:
                    message_label.value = "Erro: Tipo de usuário desconhecido."
            
            elif response.status_code == 400:
                message_label.value = "Usuário ou senha incorretos."
                message_label.color = ft.Colors.RED_400
            else:
                message_label.value = f"Erro no servidor: {response.status_code}"
                message_label.color = ft.Colors.RED_400

        except Exception as ex:
            message_label.value = f"Erro de conexão: Verifique se o Django está rodando."
            print(ex)
            message_label.color = ft.Colors.RED_400

        page.update()

    login_button = ft.ElevatedButton(
        text="ENTRAR", on_click=login_clicked, width=300, bgcolor=ft.Colors.RED_700, color=ft.Colors.WHITE
    )

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