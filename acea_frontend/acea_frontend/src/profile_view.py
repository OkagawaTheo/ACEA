import flet as ft
import requests

def get_profile_card(page: ft.Page):
    token = page.client_storage.get("auth_token")
    role = page.client_storage.get("user_role")

    # --- Variáveis Reativas ---
    nome_ref = ft.Ref[ft.Text]()
    email_ref = ft.Ref[ft.Text]()
    campo1_ref = ft.Ref[ft.Text]() # Telefone ou CPF
    campo2_ref = ft.Ref[ft.Text]() # Endereço ou Especialidade
    
    # Títulos das labels que mudam dinamicamente
    titulo_campo2 = ft.Ref[ft.Text]() 

    avatar_ref = ft.Ref[ft.CircleAvatar]()

    def campo_info(titulo, ref_valor, ref_titulo=None):
        # Se passarmos uma ref para o título, usamos ela, senão texto fixo
        titulo_widget = ft.Text(titulo, weight=ft.FontWeight.BOLD, size=14, color=ft.Colors.BLACK87)
        if ref_titulo:
            titulo_widget = ft.Text(value=titulo, ref=ref_titulo, weight=ft.FontWeight.BOLD, size=14, color=ft.Colors.BLACK87)
            
        return ft.Container(
            content=ft.Column([
                titulo_widget,
                ft.Text(value="...", ref=ref_valor, size=16, color=ft.Colors.GREY_700)
            ], spacing=5),
            width=250
        )

    def carregar_dados():
        if not token: return

        url = ""
        if role == "Aluno":
            url = "http://127.0.0.1:8000/pessoa/api/alunos/meus_dados/"
        elif role == "Professor":
            url = "http://127.0.0.1:8000/pessoa/api/professores/meus_dados/"
        
        if not url:
            nome_ref.current.value = f"Perfil de {role} (Admin)"
            email_ref.current.value = "admin@sistema.com"
            page.update()
            return

        try:
            headers = {'Authorization': f'Token {token}'}
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                dados = response.json()
                
                nome_ref.current.value = dados.get("nome", "-")
                email_ref.current.value = dados.get("email", "-")
                
                # --- Lógica Diferente para Aluno vs Professor ---
                if role == "Professor":
                    # Professor mostra CPF e Especialidade
                    campo1_ref.current.value = dados.get("cpf", "Não informado") 
                    titulo_campo2.current.value = "Especialidade:"
                    campo2_ref.current.value = dados.get("especialidade", "Geral")
                else:
                    # Aluno mostra Telefone e Endereço
                    campo1_ref.current.value = dados.get("tel", "Não informado")
                    titulo_campo2.current.value = "Endereço:"
                    campo2_ref.current.value = dados.get("endereco", "Não informado")

                if dados.get("nome"):
                    iniciais = dados["nome"][0].upper()
                    avatar_ref.current.content = ft.Text(iniciais, size=30, color=ft.Colors.WHITE)
                
                page.update()
            else:
                nome_ref.current.value = f"Erro: {response.status_code}"
                
        except Exception as e:
            print(f"Erro: {e}")

    # --- MONTAGEM ---
    esquerda = ft.Column([
        ft.Stack([
            ft.CircleAvatar(
                ref=avatar_ref,
                radius=60, 
                bgcolor=ft.Colors.BLUE_GREY_200,
                content=ft.Icon(ft.Icons.PERSON, size=60, color=ft.Colors.WHITE),
            ),
            ft.Container(
                content=ft.IconButton(ft.Icons.CAMERA_ALT, icon_color=ft.Colors.WHITE, icon_size=18),
                bgcolor=ft.Colors.GREY_700, border_radius=50, width=35, height=35, alignment=ft.alignment.center, bottom=0, right=0
            )
        ], width=120, height=120),
        ft.Container(height=20),
        ft.OutlinedButton("Alterar Senha", icon=ft.Icons.LOCK_RESET, width=150, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5))),
    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    direita = ft.Column([
        ft.Row([
            campo_info("Nome:", nome_ref),
            campo_info("Email:", email_ref),
        ], wrap=True),
        ft.Container(height=20),
        ft.Row([
            # Rótulos genéricos que mudam no código (Tel/CPF)
            campo_info("Telefone / CPF:", campo1_ref), 
            # Este rótulo muda via ref (Endereço/Especialidade)
            campo_info("Endereço:", campo2_ref, ref_titulo=titulo_campo2), 
        ], wrap=True),
    ], expand=True)

    card_perfil = ft.Container(
        content=ft.Column([
            ft.Row([ft.Icon(ft.Icons.PERSON_OUTLINE), ft.Text("Perfil", size=20, weight="bold")]),
            ft.Divider(),
            ft.Container(height=10),
            ft.Row([esquerda, ft.VerticalDivider(width=40), direita], vertical_alignment=ft.CrossAxisAlignment.START),
        ]),
        padding=40, bgcolor=ft.Colors.WHITE, border_radius=15,
        shadow=ft.BoxShadow(spread_radius=1, blur_radius=10, color=ft.Colors.BLACK12),
        margin=ft.margin.all(10)
    )

    carregar_dados()

    return ft.Column([
        ft.Container(height=10),
        ft.Column([
            ft.Text(f"Olá, {role}!", size=32, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK87),
            ft.Text("Gerencie seus dados pessoais.", size=16, color=ft.Colors.GREY_600)
        ], spacing=5),
        ft.Container(height=20),
        card_perfil
    ], scroll=ft.ScrollMode.AUTO)