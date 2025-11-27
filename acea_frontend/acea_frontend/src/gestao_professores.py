import flet as ft
import requests

def create_gestao_professor_view(page: ft.Page, role: str):
    
    API_URL_PROFESSORES = "http://127.0.0.1:8000/pessoa/api/professores/"
    API_URL_CURSOS = "http://127.0.0.1:8000/curso/api/cursos/"

    id_em_edicao = [None] # Estado da edição

    snack_bar = ft.SnackBar(ft.Text(""))
    page.overlay.append(snack_bar)

    def mostrar_msg(msg, cor=ft.Colors.WHITE):
        snack_bar.content.value = msg
        snack_bar.content.color = cor
        snack_bar.open = True
        page.update()

    def get_headers():
        token = page.client_storage.get("auth_token")
        return {'Authorization': f'Token {token}'} if token else None

    # Campos
    nome_professor = ft.TextField(label="Nome Completo", width=300)
    email_professor = ft.TextField(label="E-mail", width=300)
    cpf_professor = ft.TextField(label="CPF", width=140)
    especialidade_professor = ft.TextField(label="Especialidade", width=300)
    dropdown_cursos = ft.Dropdown(label="Vincular Curso", width=300, options=[], color=ft.Colors.BLACK, border_color=ft.Colors.RED_ACCENT_100)

    # Botões
    btn_acao = ft.ElevatedButton("Adicionar Professor", icon=ft.Icons.ADD, bgcolor=ft.Colors.RED_700, color=ft.Colors.WHITE)
    btn_cancelar = ft.ElevatedButton("Cancelar", bgcolor=ft.Colors.GREY, color=ft.Colors.WHITE, visible=False)

    professor_data_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID", color=ft.Colors.BLACK)),
            ft.DataColumn(ft.Text("Nome", color=ft.Colors.BLACK)),
            ft.DataColumn(ft.Text("Especialidade", color=ft.Colors.BLACK)),
            ft.DataColumn(ft.Text("E-mail", color=ft.Colors.BLACK)),
            ft.DataColumn(ft.Text("Ações", color=ft.Colors.BLACK)),
        ],
        rows=[], 
        border=ft.border.all(1, ft.Colors.BLACK12)
    )

    # --- Lógica de Carga ---
    def carregar_cursos_dropdown():
        headers = get_headers()
        if not headers: return
        try:
            r = requests.get(API_URL_CURSOS, headers=headers)
            if r.status_code == 200:
                dropdown_cursos.options = [ft.dropdown.Option(key=str(c['id_curso']), text=c['nome']) for c in r.json()]
                if dropdown_cursos.page: dropdown_cursos.update()
        except: pass

    def carregar_professores():
        headers = get_headers()
        if not headers: return
        try:
            r = requests.get(API_URL_PROFESSORES, headers=headers)
            if r.status_code == 200:
                professor_data_table.rows.clear()
                for prof in r.json():
                    acoes = ft.Text("-", color=ft.Colors.BLACK)
                    if role == "Admin":
                        acoes = ft.Row([
                            ft.IconButton(ft.Icons.EDIT, icon_color=ft.Colors.TEAL_700, on_click=lambda e, p=prof: preparar_edicao(p)), 
                            ft.IconButton(ft.Icons.DELETE, icon_color=ft.Colors.RED_ACCENT_700, on_click=lambda e, id=prof['id_professor']: deletar_professor(id))
                        ])
                    
                    professor_data_table.rows.append(ft.DataRow(cells=[
                        ft.DataCell(ft.Text(str(prof.get('id_professor')), color=ft.Colors.BLACK)),
                        ft.DataCell(ft.Text(prof.get('nome'), color=ft.Colors.BLACK)),
                        ft.DataCell(ft.Text(prof.get('especialidade'), color=ft.Colors.BLACK)),
                        ft.DataCell(ft.Text(prof.get('email'), color=ft.Colors.BLACK)),
                        ft.DataCell(acoes)
                    ]))
                if professor_data_table.page: page.update()
        except Exception as e: print(e)

    # --- Lógica CRUD ---
    def deletar_professor(id_prof):
        try:
            requests.delete(f"{API_URL_PROFESSORES}{id_prof}/", headers=get_headers())
            mostrar_msg("Professor excluído.", ft.Colors.ORANGE)
            carregar_professores()
        except: pass

    def preparar_edicao(prof):
        id_em_edicao[0] = prof['id_professor']
        nome_professor.value = prof['nome']
        email_professor.value = prof['email']
        cpf_professor.value = prof['cpf']
        especialidade_professor.value = prof['especialidade']
        
        btn_acao.text = "Salvar Alterações"
        btn_acao.icon = ft.Icons.SAVE
        btn_cancelar.visible = True
        page.update()

    def cancelar_edicao(e):
        id_em_edicao[0] = None
        nome_professor.value = ""
        email_professor.value = ""
        cpf_professor.value = ""
        especialidade_professor.value = ""
        
        btn_acao.text = "Adicionar Professor"
        btn_acao.icon = ft.Icons.ADD
        btn_cancelar.visible = False
        page.update()

    def salvar_professor(e):
        headers = get_headers()
        dados = {
            "nome": nome_professor.value,
            "email": email_professor.value,
            "cpf": cpf_professor.value,
            "especialidade": especialidade_professor.value
        }
        try:
            if id_em_edicao[0]:
                # Edição (PUT)
                r = requests.put(f"{API_URL_PROFESSORES}{id_em_edicao[0]}/", json=dados, headers=headers)
                msg = "Atualizado com sucesso!"
            else:
                # Criação (POST)
                r = requests.post(API_URL_PROFESSORES, json=dados, headers=headers)
                msg = "Criado com sucesso!"

            if r.status_code in [200, 201]:
                mostrar_msg(msg, ft.Colors.GREEN)
                cancelar_edicao(None)
                carregar_professores()
            else:
                mostrar_msg(f"Erro: {r.text}", ft.Colors.RED)
        except Exception as ex: mostrar_msg(f"Erro: {ex}", ft.Colors.RED)

    btn_acao.on_click = salvar_professor
    btn_cancelar.on_click = cancelar_edicao

    # --- Layout ---
    secao_adicionar = ft.Container()
    if role == "Admin":
        secao_adicionar = ft.Container(
            content=ft.Column([
                ft.Text("Formulário Professor", size=18, weight="bold", color=ft.Colors.BLACK),
                ft.Container(content=ft.Column([
                    dropdown_cursos,
                    ft.Row([nome_professor, email_professor]),
                    ft.Row([cpf_professor, especialidade_professor]),
                    ft.Row([btn_acao, btn_cancelar])
                ], spacing=10), padding=20, bgcolor=ft.Colors.WHITE, border_radius=10, shadow=ft.BoxShadow(blur_radius=5, color=ft.Colors.BLACK12)),
                ft.Container(height=30),
            ])
        )

    main_column = ft.Column([ 
        ft.Text("Gestão de Professores", size=30, weight="bold", color=ft.Colors.BLACK),
        ft.Container(height=20),
        secao_adicionar,
        ft.Row([ft.Text("Lista de Professores", size=18, weight="bold", color=ft.Colors.BLACK), ft.IconButton(ft.Icons.REFRESH, icon_color="blue", on_click=lambda _: carregar_professores())], alignment="spaceBetween"),
        ft.Container(content=ft.Column([professor_data_table], scroll="always"), padding=20, bgcolor=ft.Colors.WHITE, border_radius=10, shadow=ft.BoxShadow(blur_radius=5, color=ft.Colors.BLACK12), expand=True)
    ], scroll="adaptive", expand=True)
    
    def inicializar_dados():
        if role == "Admin": carregar_cursos_dropdown()
        carregar_professores()

    main_column.did_mount = inicializar_dados
    return main_column