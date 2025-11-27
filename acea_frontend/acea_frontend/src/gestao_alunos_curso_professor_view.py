import flet as ft
import requests

def create_gestao_alunos_curso_professor_view(page: ft.Page):
    
    API_URL_ALUNOS = "http://127.0.0.1:8000/pessoa/api/alunos/"
    API_URL_CURSOS = "http://127.0.0.1:8000/curso/api/cursos/"

    # --- Estado da Edição ---
    # Se None, estamos criando. Se tiver um ID, estamos editando.
    id_em_edicao = [None] 

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

    # --- Campos ---
    nome_aluno = ft.TextField(label="Nome Completo", width=300)
    email_aluno = ft.TextField(label="E-mail", width=300)
    cpf_aluno = ft.TextField(label="CPF", width=140) 
    matricula_aluno = ft.TextField(label="Matrícula", width=140)
    
    dropdown_cursos = ft.Dropdown(
        label="Selecione o Curso", width=300, options=[], color=ft.Colors.BLACK, border_color=ft.Colors.RED_ACCENT_100
    )

    # Botão Principal (Muda de texto dinamicamente)
    btn_acao = ft.ElevatedButton("Adicionar e Matricular", icon=ft.Icons.ADD, bgcolor=ft.Colors.RED_700, color=ft.Colors.WHITE)
    
    # Botão Cancelar (Aparece só na edição)
    btn_cancelar = ft.ElevatedButton("Cancelar", bgcolor=ft.Colors.GREY, color=ft.Colors.WHITE, visible=False)

    # Tabela
    alunos_data_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID", color=ft.Colors.BLACK)),
            ft.DataColumn(ft.Text("Nome", color=ft.Colors.BLACK)),
            ft.DataColumn(ft.Text("E-mail", color=ft.Colors.BLACK)),
            ft.DataColumn(ft.Text("Matrícula", color=ft.Colors.BLACK)),
            ft.DataColumn(ft.Text("Ações", color=ft.Colors.BLACK)),
        ],
        rows=[], 
        border=ft.border.all(1, ft.Colors.BLACK12),
    )

    # --- FUNÇÃO: Carregar Dados ---
    def carregar_cursos_dropdown():
        headers = get_headers()
        if not headers: return
        try:
            response = requests.get(API_URL_CURSOS, headers=headers)
            if response.status_code == 200:
                lista = response.json()
                dropdown_cursos.options.clear()
                for c in lista:
                    dropdown_cursos.options.append(ft.dropdown.Option(key=str(c['id_curso']), text=c['nome']))
                if dropdown_cursos.page: dropdown_cursos.update()
        except Exception: pass

    def carregar_alunos():
        headers = get_headers()
        if not headers: return
        try:
            response = requests.get(API_URL_ALUNOS, headers=headers)
            if response.status_code == 200:
                alunos_data_table.rows.clear()
                for aluno in response.json():
                    
                    # Configura botões com ID específico do aluno
                    btn_edit = ft.IconButton(
                        ft.Icons.EDIT, icon_color=ft.Colors.TEAL_700, 
                        on_click=lambda e, a=aluno: preparar_edicao(a)
                    )
                    btn_delete = ft.IconButton(
                        ft.Icons.DELETE, icon_color=ft.Colors.RED_ACCENT_700,
                        on_click=lambda e, id=aluno['id_aluno']: deletar_aluno(id)
                    )

                    alunos_data_table.rows.append(ft.DataRow(cells=[
                        ft.DataCell(ft.Text(str(aluno['id_aluno']), color=ft.Colors.BLACK)), 
                        ft.DataCell(ft.Text(aluno['nome'], color=ft.Colors.BLACK)), 
                        ft.DataCell(ft.Text(aluno['email'], color=ft.Colors.BLACK)), 
                        ft.DataCell(ft.Text(aluno['matricula'], color=ft.Colors.BLACK)), 
                        ft.DataCell(ft.Row([btn_edit, btn_delete]))
                    ]))
                if alunos_data_table.page: page.update()
        except Exception as ex: print(ex)

    # --- FUNÇÃO: Deletar ---
    def deletar_aluno(id_aluno):
        headers = get_headers()
        try:
            # Chama API com DELETE
            requests.delete(f"{API_URL_ALUNOS}{id_aluno}/", headers=headers)
            mostrar_msg("Aluno excluído.", ft.Colors.ORANGE)
            carregar_alunos()
        except Exception as e:
            mostrar_msg(f"Erro: {e}", ft.Colors.RED)

    # --- FUNÇÃO: Preparar Edição (Preenche campos) ---
    def preparar_edicao(aluno):
        id_em_edicao[0] = aluno['id_aluno'] # Marca que estamos editando este ID
        
        # Preenche os campos com os dados do aluno
        nome_aluno.value = aluno['nome']
        email_aluno.value = aluno['email']
        cpf_aluno.value = aluno['cpf']
        matricula_aluno.value = aluno['matricula']
        
        # Muda o botão
        btn_acao.text = "Salvar Alterações"
        btn_acao.icon = ft.Icons.SAVE
        btn_cancelar.visible = True
        
        # Tenta selecionar o curso (se houver)
        if aluno.get('cursos_matriculados'):
            dropdown_cursos.value = str(aluno['cursos_matriculados'][0])
        
        page.update()

    def cancelar_edicao(e):
        id_em_edicao[0] = None
        nome_aluno.value = ""
        email_aluno.value = ""
        cpf_aluno.value = ""
        matricula_aluno.value = ""
        dropdown_cursos.value = None
        
        btn_acao.text = "Adicionar e Matricular"
        btn_acao.icon = ft.Icons.ADD
        btn_cancelar.visible = False
        page.update()

    # --- FUNÇÃO: Salvar (Cria ou Atualiza) ---
    def salvar_aluno(e):
        headers = get_headers()
        dados = {
            "nome": nome_aluno.value,
            "email": email_aluno.value,
            "cpf": cpf_aluno.value,
            "matricula": matricula_aluno.value,
        }
        if dropdown_cursos.value:
            dados["cursos_matriculados"] = [int(dropdown_cursos.value)]

        try:
            if id_em_edicao[0]: 
                # --- MODO EDIÇÃO (PUT) ---
                url = f"{API_URL_ALUNOS}{id_em_edicao[0]}/"
                response = requests.put(url, json=dados, headers=headers)
                msg_sucesso = "Aluno atualizado!"
            else:
                # --- MODO CRIAÇÃO (POST) ---
                response = requests.post(API_URL_ALUNOS, json=dados, headers=headers)
                msg_sucesso = "Aluno criado!"

            if response.status_code in [200, 201]:
                mostrar_msg(msg_sucesso, ft.Colors.GREEN)
                cancelar_edicao(None) # Limpa formulário
                carregar_alunos()
            else:
                mostrar_msg(f"Erro: {response.text}", ft.Colors.RED)

        except Exception as ex:
            mostrar_msg(f"Erro conexão: {ex}", ft.Colors.RED)

    # Configura evento dos botões
    btn_acao.on_click = salvar_aluno
    btn_cancelar.on_click = cancelar_edicao

    # --- Layout ---
    main_column = ft.Column(
        [
            ft.Text("Gestão de Alunos", size=30, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK87),
            ft.Container(height=20),
            
            ft.Container(
                content=ft.Column([
                    ft.Text("Formulário de Cadastro/Edição", color=ft.Colors.BLACK),
                    dropdown_cursos,
                    ft.Row([nome_aluno, email_aluno]),
                    ft.Row([cpf_aluno, matricula_aluno]),
                    ft.Row([btn_acao, btn_cancelar])
                ], spacing=10),
                padding=20, bgcolor=ft.Colors.WHITE, border_radius=10, shadow=ft.BoxShadow(blur_radius=5, color=ft.Colors.BLACK12)
            ),
            ft.Container(height=30),
            
            ft.Row([ft.Text("Lista de Alunos", size=18, weight="bold", color=ft.Colors.BLACK), ft.IconButton(ft.Icons.REFRESH, icon_color="blue", on_click=lambda _: carregar_alunos())], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Container(content=ft.Column([alunos_data_table], scroll=ft.ScrollMode.ALWAYS), padding=20, bgcolor=ft.Colors.WHITE, border_radius=10, shadow=ft.BoxShadow(blur_radius=5, color=ft.Colors.BLACK12), expand=True)
        ],
        scroll=ft.ScrollMode.ADAPTIVE, expand=True
    )
    
    def inicializar_dados():
        carregar_cursos_dropdown()
        carregar_alunos()

    main_column.did_mount = inicializar_dados
    return main_column