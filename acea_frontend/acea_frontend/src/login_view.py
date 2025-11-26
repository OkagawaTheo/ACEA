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

    # --- NOVA LÓGICA DE LOGIN ---
    def login_clicked(e):
        # Limpa mensagem anterior e avisa que está carregando
        message_label.value = "Conectando ao servidor..."
        message_label.color = ft.Colors.BLUE_GREY
        page.update()

        # URL que criamos no Django (Verifique se a porta é 8000 mesmo)
        API_URL = "http://127.0.0.1:8000/pessoa/api/login/"

        try:
            # 1. Envia usuario e senha para o Django
            response = requests.post(API_URL, json={
                "username": username_field.value,
                "password": password_field.value
            })

            # 2. Se o Django aceitou (Status 200 OK)
            if response.status_code == 200:
                dados = response.json()
                
                # Pegamos o tipo que veio do Python (ex: 'aluno', 'professor', 'admin')
                tipo_vindo_do_back = dados.get('tipo_usuario')
                token = dados.get('token')

                # 3. Traduzir para o padrão que seu Dashboard espera (Capitalizado)
                mapa_papeis = {
                    'aluno': 'Aluno',
                    'professor': 'Professor',
                    'admin': 'Admin'
                }
                user_role = mapa_papeis.get(tipo_vindo_do_back)

                if user_role:
                    # Guardar o Token para usar depois (Importante!)
                    page.client_storage.set("auth_token", token)
                    
                    message_label.value = f"Login realizado! Bem-vindo(a) {user_role}. 🎉"
                    message_label.color = ft.Colors.TEAL_600
                    page.update()
                    
                    # Chama o dashboard passando o papel correto
                    on_success(user_role)
                else:
                    message_label.value = "Erro: Tipo de usuário desconhecido."
            
            # 3. Se o Django recusou (Senha errada ou usuario inexistente)
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

    # Botão de login (Vermilion - Mantido seu design)
    login_button = ft.ElevatedButton(
        text="ENTRAR", on_click=login_clicked, width=300, bgcolor=ft.Colors.RED_700, color=ft.Colors.WHITE
    )

    # Cartão de Login (Mantido seu design)
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