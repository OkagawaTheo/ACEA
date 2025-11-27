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
    titulo_campo2 = ft.Ref[ft.Text]() 
    avatar_ref = ft.Ref[ft.CircleAvatar]()

    # --- Inputs do Modal de Edição ---
    edit_email = ft.TextField(label="E-mail")
    edit_extra1 = ft.TextField(label="Telefone") # Para Aluno
    edit_extra2 = ft.TextField(label="Endereço") # Para Aluno
    # (Professor não edita especialidade por aqui geralmente, mas o email sim)

    # --- Função Helper de Layout ---
    def campo_info(titulo, ref_valor, ref_titulo=None):
        titulo_widget = ft.Text(titulo, weight=ft.FontWeight.BOLD, size=14, color=ft.Colors.BLACK87)
        if ref_titulo:
            titulo_widget = ft.Text(value=titulo, ref=ref_titulo, weight=ft.FontWeight.BOLD, size=14, color=ft.Colors.BLACK87)
        return ft.Container(
            content=ft.Column([titulo_widget, ft.Text(value="...", ref=ref_valor, size=16, color=ft.Colors.GREY_700)], spacing=5),
            width=250
        )

    # --- FUNÇÃO: Salvar Edição (PUT) ---
    def salvar_edicao(e):
        url = ""
        if role == "Aluno":
            url = "http://127.0.0.1:8000/pessoa/api/alunos/meus_dados/"
            dados = {
                "email": edit_email.value,
                "tel": edit_extra1.value,
                "endereco": edit_extra2.value
            }
        elif role == "Professor":
            url = "http://127.0.0.1:8000/pessoa/api/professores/meus_dados/"
            dados = {"email": edit_email.value} # Professor só muda email por aqui no exemplo

        try:
            headers = {'Authorization': f'Token {token}'}
            response = requests.put(url, json=dados, headers=headers)
            
            if response.status_code == 200:
                page.snack_bar = ft.SnackBar(ft.Text("Perfil atualizado!"), bgcolor="green")
                page.snack_bar.open = True
                dialog_editar.open = False # Fecha modal
                carregar_dados() # Recarrega a tela
            else:
                page.snack_bar = ft.SnackBar(ft.Text(f"Erro: {response.text}"), bgcolor="red")
                page.snack_bar.open = True
                
        except Exception as ex:
            print(ex)
        page.update()

    # --- Modal (Janela Flutuante) ---
    dialog_editar = ft.AlertDialog(
        title=ft.Text("Editar Meus Dados"),
        content=ft.Column([
            edit_email,
            edit_extra1, # Será visivel só pra aluno
            edit_extra2  # Será visivel só pra aluno
        ], height=200, width=400),
        actions=[
            ft.TextButton("Cancelar", on_click=lambda e: page.close_dialog()),
            ft.ElevatedButton("Salvar", on_click=salvar_edicao, bgcolor="blue", color="white")
        ]
    )

    # --- Modal (Janela Flutuante) ---
    # Definimos fora da função para ela existir no escopo
    dialog_editar = ft.AlertDialog(
        title=ft.Text("Editar Meus Dados"),
        content=ft.Column([
            edit_email,
            edit_extra1,
            edit_extra2
        ], height=200, width=400),
        actions=[
            ft.TextButton("Cancelar", on_click=lambda e: fechar_modal()),
            ft.ElevatedButton("Salvar", on_click=salvar_edicao, bgcolor="blue", color="white")
        ]
    )

    def fechar_modal():
        dialog_editar.open = False
        page.update()

    # --- Função CORRIGIDA para abrir o Modal ---
    def abrir_modal_edicao(e):
        print("Abrindo modal de edição...") # Debug no terminal
        
        try:
            # 1. Preenche os campos com segurança (usando .value ou vazio se der erro)
            # O 'current' pode ser None se a tela não carregou direito ainda
            val_email = email_ref.current.value if email_ref.current else ""
            val_campo1 = campo1_ref.current.value if campo1_ref.current else ""
            val_campo2 = campo2_ref.current.value if campo2_ref.current else ""

            edit_email.value = val_email
            
            if role == "Aluno":
                edit_extra1.label = "Telefone"
                edit_extra1.visible = True
                edit_extra1.value = val_campo1
                
                edit_extra2.visible = True
                edit_extra2.label = "Endereço"
                edit_extra2.value = val_campo2
            else:
                # Professor só edita email e vê os outros campos como "Bloqueados" ou invisíveis
                edit_extra1.visible = False
                edit_extra2.visible = False

            # 2. Adiciona ao Overlay (Mais seguro que page.dialog)
            page.overlay.append(dialog_editar)
            dialog_editar.open = True
            page.update()
            
        except Exception as ex:
            print(f"Erro ao abrir modal: {ex}")
            page.snack_bar = ft.SnackBar(ft.Text(f"Erro ao abrir edição: {ex}"), bgcolor="red")
            page.snack_bar.open = True
            page.update()

    # --- Carregar Dados (GET) ---
    def carregar_dados():
        if not token: return
        url = ""
        if role == "Aluno": url = "http://127.0.0.1:8000/pessoa/api/alunos/meus_dados/"
        elif role == "Professor": url = "http://127.0.0.1:8000/pessoa/api/professores/meus_dados/"
        
        if not url: return

        try:
            headers = {'Authorization': f'Token {token}'}
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                dados = response.json()
                nome_ref.current.value = dados.get("nome", "-")
                email_ref.current.value = dados.get("email", "-")
                
                if role == "Professor":
                    campo1_ref.current.value = dados.get("cpf", "Não informado") 
                    titulo_campo2.current.value = "Especialidade:"
                    campo2_ref.current.value = dados.get("especialidade", "Geral")
                else:
                    campo1_ref.current.value = dados.get("tel", "Não informado")
                    titulo_campo2.current.value = "Endereço:"
                    campo2_ref.current.value = dados.get("endereco", "Não informado")

                if dados.get("nome"):
                    iniciais = dados["nome"][0].upper()
                    avatar_ref.current.content = ft.Text(iniciais, size=30, color=ft.Colors.WHITE)
                page.update()
        except Exception as e: print(e)

    # --- Layout ---
    esquerda = ft.Column([
        ft.Stack([
            ft.CircleAvatar(ref=avatar_ref, radius=60, bgcolor=ft.Colors.BLUE_GREY_200, content=ft.Icon(ft.Icons.PERSON, size=60, color=ft.Colors.WHITE)),
            ft.Container(content=ft.IconButton(ft.Icons.CAMERA_ALT, icon_color=ft.Colors.WHITE, icon_size=18), bgcolor=ft.Colors.GREY_700, border_radius=50, width=35, height=35, alignment=ft.alignment.center, bottom=0, right=0)
        ], width=120, height=120),
        ft.Container(height=20),
        ft.OutlinedButton("Alterar Senha", icon=ft.Icons.LOCK_RESET, width=150),
    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    direita = ft.Column([
        ft.Row([campo_info("Nome:", nome_ref), campo_info("Email:", email_ref)], wrap=True),
        ft.Container(height=20),
        ft.Row([campo_info("Tel / CPF:", campo1_ref), campo_info("Endereço:", campo2_ref, ref_titulo=titulo_campo2)], wrap=True),
    ], expand=True)

    card_perfil = ft.Container(
        content=ft.Column([
            ft.Row([ft.Icon(ft.Icons.PERSON_OUTLINE), ft.Text("Perfil", size=20, weight="bold")]),
            ft.Divider(),
            ft.Container(height=10),
            ft.Row([esquerda, ft.VerticalDivider(width=40), direita], vertical_alignment=ft.CrossAxisAlignment.START),
            ft.Container(height=30),
            
            # BOTÃO EDITAR AGORA FUNCIONA
            ft.Container(content=ft.ElevatedButton(
                "Editar Perfil", icon=ft.Icons.EDIT, bgcolor=ft.Colors.GREY_200, color=ft.Colors.BLACK87, 
                height=50, width=1000, 
                on_click=abrir_modal_edicao # <--- AÇÃO AQUI
            ))
        ]),
        padding=40, bgcolor=ft.Colors.WHITE, border_radius=15,
        shadow=ft.BoxShadow(spread_radius=1, blur_radius=10, color=ft.Colors.BLACK12),
        margin=ft.margin.all(10)
    )

    carregar_dados()

    return ft.Column([
        ft.Container(height=10),
        ft.Column([ft.Text(f"Olá, {role}!", size=32, weight="bold", color=ft.Colors.BLACK87), ft.Text("Gerencie seus dados pessoais.", size=16, color=ft.Colors.GREY_600)], spacing=5),
        ft.Container(height=20),
        card_perfil
    ], scroll=ft.ScrollMode.AUTO)