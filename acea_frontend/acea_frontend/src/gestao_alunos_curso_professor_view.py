import flet as ft
import requests

def create_gestao_alunos_curso_professor_view(page: ft.Page):
    
    # URLs da API
    API_URL_ALUNOS = "http://127.0.0.1:8000/pessoa/api/alunos/"
    API_URL_CURSOS = "http://127.0.0.1:8000/curso/api/cursos/"

    # --- Elementos de Feedback ---
    snack_bar = ft.SnackBar(ft.Text(""))
    page.overlay.append(snack_bar)

    def mostrar_msg(msg, cor=ft.Colors.WHITE):
        snack_bar.content.value = msg
        snack_bar.content.color = cor
        snack_bar.open = True
        page.update()

    # --- Campos para Adicionar/Editar Aluno ---
    nome_aluno = ft.TextField(label="Nome Completo", width=300)
    email_aluno = ft.TextField(label="E-mail", width=300)
    cpf_aluno = ft.TextField(label="CPF", width=140) 
    matricula_aluno = ft.TextField(label="Matrícula", width=140)

    # --- Dropdown de Cursos (Começa vazio e preenchemos via API) ---
    dropdown_cursos = ft.Dropdown(
        label="Selecione o Curso",
        width=300,
        options=[], # Será preenchido pela função carregar_cursos_dropdown
        color=ft.Colors.BLACK,
        border_color=ft.Colors.RED_ACCENT_100
    )

    # --- Tabela para Visualizar Alunos ---
    alunos_data_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID", color=ft.Colors.BLACK)),
            ft.DataColumn(ft.Text("Nome", color=ft.Colors.BLACK)),
            ft.DataColumn(ft.Text("E-mail", color=ft.Colors.BLACK)),
            ft.DataColumn(ft.Text("Cursos", color=ft.Colors.BLACK)), # Mudei para mostrar cursos
            ft.DataColumn(ft.Text("Ações", color=ft.Colors.BLACK)),
        ],
        rows=[], 
        border=ft.border.all(1, ft.Colors.BLACK12),
        vertical_lines=ft.border.BorderSide(0.5, ft.Colors.BLACK12),
        horizontal_lines=ft.border.BorderSide(0.5, ft.Colors.BLACK12),
    )

    # --- FUNÇÃO AUXILIAR: Pegar Token ---
    def get_headers():
        token = page.client_storage.get("auth_token")
        if not token:
            return None
        return {'Authorization': f'Token {token}'}

    # --- FUNÇÃO 1: Carregar Cursos no Dropdown ---
    def carregar_cursos_dropdown():
        headers = get_headers()
        if not headers: return

        try:
            response = requests.get(API_URL_CURSOS, headers=headers)
            if response.status_code == 200:
                lista_cursos = response.json()
                dropdown_cursos.options.clear()
                
                for curso in lista_cursos:
                    # Guardamos o ID na 'key' e mostramos o Nome no 'text'
                    dropdown_cursos.options.append(
                        ft.dropdown.Option(key=str(curso['id_curso']), text=curso['nome'])
                    )
                
                # Seleciona o primeiro por padrão se houver cursos
                if lista_cursos:
                    dropdown_cursos.value = str(lista_cursos[0]['id_curso'])
                
                dropdown_cursos.update()
        except Exception as ex:
            print(f"Erro ao carregar cursos: {ex}")

    # --- FUNÇÃO 2: Buscar Alunos do Django ---
    def carregar_dados_da_api():
        headers = get_headers()
        if not headers:
            mostrar_msg("Erro: Você não está logado.", ft.Colors.RED)
            return
        
        try:
            # Faz o GET na API de Alunos
            response = requests.get(API_URL_ALUNOS, headers=headers)
            
            if response.status_code == 200:
                lista_alunos = response.json()
                alunos_data_table.rows.clear()
                
                for aluno in lista_alunos:
                    # Tenta pegar os cursos matriculados (IDs)
                    # Nota: O serializer padrão retorna IDs. Para mostrar nomes, precisariamos tratar isso.
                    # Por enquanto mostra a quantidade ou IDs.
                    qtd_cursos = len(aluno.get('cursos_matriculados', []))
                    txt_cursos = f"{qtd_cursos} curso(s)"

                    linha = ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(str(aluno.get('id_aluno')), color=ft.Colors.BLACK)), 
                            ft.DataCell(ft.Text(aluno.get('nome'), color=ft.Colors.BLACK)), 
                            ft.DataCell(ft.Text(aluno.get('email'), color=ft.Colors.BLACK)), 
                            ft.DataCell(ft.Text(txt_cursos, color=ft.Colors.BLACK)), 
                            ft.DataCell(ft.Row([
                                ft.IconButton(ft.Icons.EDIT, icon_color=ft.Colors.TEAL_700), 
                                ft.IconButton(ft.Icons.DELETE, icon_color=ft.Colors.RED_ACCENT_700)
                            ]))
                        ]
                    )
                    alunos_data_table.rows.append(linha)
                
                mostrar_msg("Lista atualizada!", ft.Colors.GREEN)
            
            elif response.status_code == 403:
                mostrar_msg("Acesso Negado.", ft.Colors.RED)
            else:
                mostrar_msg(f"Erro no servidor: {response.status_code}", ft.Colors.RED)
                
        except Exception as ex:
            mostrar_msg(f"Erro de conexão: {ex}", ft.Colors.RED)
        
        page.update()

    # --- FUNÇÃO 3: Adicionar Aluno (Com Curso) ---
    def btn_adicionar_click(e):
        headers = get_headers()
        
        # Verifica se um curso foi selecionado
        id_curso_selecionado = dropdown_cursos.value
        if not id_curso_selecionado:
            mostrar_msg("Selecione um curso para o aluno!", ft.Colors.ORANGE)
            return

        dados_novo_aluno = {
            "nome": nome_aluno.value,
            "email": email_aluno.value,
            "cpf": cpf_aluno.value,
            "matricula": matricula_aluno.value,
            # AQUI ESTÁ A MÁGICA: Enviamos o ID do curso em uma lista
            "cursos_matriculados": [int(id_curso_selecionado)]
        }

        try:
            response = requests.post(API_URL_ALUNOS, json=dados_novo_aluno, headers=headers)
            
            if response.status_code == 201: 
                mostrar_msg("Aluno matriculado com sucesso!", ft.Colors.GREEN)
                # Limpa campos
                nome_aluno.value = ""
                email_aluno.value = ""
                cpf_aluno.value = ""
                matricula_aluno.value = ""
                # Recarrega a tabela
                carregar_dados_da_api()
            else:
                mostrar_msg(f"Erro ao criar: {response.text}", ft.Colors.RED)
                print(response.text)

        except Exception as ex:
            mostrar_msg(f"Erro de conexão: {ex}", ft.Colors.RED)
        
        page.update()

    # --- Layout ---
    main_column = ft.Column(
        [
            ft.Text("Gestão de Alunos", size=30, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK87),
            ft.Container(height=20),
            
            # --- 1. Adicionar Aluno ---
            ft.Text("Matricular Novo Aluno", size=18, weight=ft.FontWeight.W_600, color=ft.Colors.BLACK87),
            ft.Container(
                content=ft.Column([
                    ft.Text("Selecione o Curso:", color=ft.Colors.BLACK),
                    dropdown_cursos, # O dropdown agora é dinâmico
                    ft.Container(height=10),
                    ft.Row([nome_aluno, email_aluno]),
                    ft.Row([cpf_aluno, matricula_aluno]),
                    ft.ElevatedButton("Adicionar e Matricular", icon=ft.Icons.ADD, bgcolor=ft.Colors.RED_700, color=ft.Colors.WHITE, on_click=btn_adicionar_click)
                ], spacing=10),
                padding=20, bgcolor=ft.Colors.WHITE, border_radius=10, shadow=ft.BoxShadow(blur_radius=5, color=ft.Colors.BLACK12)
            ),
            
            ft.Container(height=30),
            
            # --- 2. Visualização ---
            ft.Row([
                ft.Text("Alunos Cadastrados", size=18, weight=ft.FontWeight.W_600, color=ft.Colors.BLACK87),
                ft.IconButton(ft.Icons.REFRESH, icon_color=ft.Colors.BLUE, tooltip="Atualizar", on_click=lambda _: carregar_dados_da_api())
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),

            ft.Container(
                content=ft.Column([alunos_data_table], scroll=ft.ScrollMode.ALWAYS),
                padding=20, bgcolor=ft.Colors.WHITE, border_radius=10, shadow=ft.BoxShadow(blur_radius=5, color=ft.Colors.BLACK12),
                expand=True
            )
        ],
        scroll=ft.ScrollMode.ADAPTIVE,
        expand=True
    )
    
    # --- CORREÇÃO: USAR DID_MOUNT ---
    def inicializar_dados(): # <--- CORRETO (Sem argumentos)
        # Agora sim, seguro para carregar
        carregar_cursos_dropdown()
        carregar_dados_da_api()

    main_column.did_mount = inicializar_dados
    return main_column