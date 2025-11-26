import flet as ft
import requests
import os
from urllib.parse import unquote

def create_gestao_documentos_view(page: ft.Page, role: str):
    
    # URL da API (Certifique-se que o backend está rodando)
    API_URL = "http://127.0.0.1:8000/documentacao/api/documentos/"

    # --- Elementos Auxiliares ---
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

    # --- Variáveis de Estado ---
    caminho_arquivo_selecionado = [None] 
    texto_arquivo_selecionado = ft.Text("Nenhum arquivo selecionado", color=ft.Colors.GREY)

    # --- FilePicker (Componente de Seleção de Arquivo) ---
    def arquivo_escolhido(e: ft.FilePickerResultEvent):
        if e.files:
            caminho = e.files[0].path
            caminho_arquivo_selecionado[0] = caminho
            texto_arquivo_selecionado.value = f"Arquivo: {e.files[0].name}"
            texto_arquivo_selecionado.color = ft.Colors.BLACK
        else:
            caminho_arquivo_selecionado[0] = None
            texto_arquivo_selecionado.value = "Seleção cancelada"
        page.update()

    file_picker = ft.FilePicker(on_result=arquivo_escolhido)
    page.overlay.append(file_picker)

    # --- Campos de Entrada ---
    titulo_documento = ft.TextField(label="Título", width=300)
    descricao_documento = ft.TextField(label="Descrição", multiline=True)
    
    tipo_documento = ft.Dropdown(
        label="Tipo",
        width=200,
        options=[
            ft.dropdown.Option("RG", "RG/CPF"),
            ft.dropdown.Option("COMP", "Comprovante Residência"),
            ft.dropdown.Option("CON", "Contrato"),
            ft.dropdown.Option("OUT", "Outro"),
        ],
        value="OUT"
    )

    # --- Configuração Dinâmica da Tabela ---
    colunas_tabela = [
        ft.DataColumn(ft.Text("ID", color=ft.Colors.BLACK)),
        ft.DataColumn(ft.Text("Título", color=ft.Colors.BLACK)),
        ft.DataColumn(ft.Text("Tipo", color=ft.Colors.BLACK)),
    ]
    
    # Admin, Presidente E PROFESSOR veem quem enviou
    if role in ["Admin", "Presidente", "Professor"]: 
        colunas_tabela.append(ft.DataColumn(ft.Text("Enviado Por", color=ft.Colors.BLACK)))
        
    colunas_tabela.append(ft.DataColumn(ft.Text("Arquivo", color=ft.Colors.BLACK)))
    colunas_tabela.append(ft.DataColumn(ft.Text("Ações", color=ft.Colors.BLACK)))

    documentos_data_table = ft.DataTable(
        columns=colunas_tabela,
        rows=[],
        border=ft.border.all(1, ft.Colors.BLACK12),
        heading_row_color=ft.Colors.GREY_200,
    )

    # --- FUNÇÃO: Carregar Documentos (GET) ---
    def carregar_documentos():
        headers = get_headers()
        if not headers: return

        try:
            response = requests.get(API_URL, headers=headers)
            if response.status_code == 200:
                lista = response.json()
                documentos_data_table.rows.clear()

                for doc in lista:
                    # Leitura segura dos dados
                    titulo = doc.get('titulo', 'Sem Título')
                    tipo = doc.get('tipo_documento', 'OUT')
                    nome_usuario = doc.get('nome_usuario', '-')
                    arquivo_url = doc.get('arquivo', '')
                    
                    # Limpeza do nome do arquivo (decodifica %20, etc)
                    nome_bruto = os.path.basename(arquivo_url)
                    nome_arquivo = unquote(nome_bruto)

                    # Botões de Ação
                    botoes = [
                        ft.IconButton(
                            ft.Icons.CLOUD_DOWNLOAD, 
                            icon_color=ft.Colors.TEAL_700,
                            tooltip="Baixar",
                            on_click=lambda e, url=arquivo_url: page.launch_url(url)
                        )
                    ]
                    
                    # Botão de deletar
                    if role in ["Admin", "Presidente", "Professor"]:
                        botoes.append(
                            ft.IconButton(
                                ft.Icons.DELETE, 
                                icon_color=ft.Colors.RED_ACCENT_700,
                                tooltip="Excluir",
                                on_click=lambda e, id=doc['id_documento']: deletar_documento(id)
                            )
                        )

                    # Montagem das células
                    celulas = [
                        ft.DataCell(ft.Text(str(doc['id_documento']), color=ft.Colors.BLACK)),
                        ft.DataCell(ft.Text(titulo, color=ft.Colors.BLACK)),
                        ft.DataCell(ft.Text(tipo, color=ft.Colors.BLACK)),
                    ]
                    
                    # Coluna extra para Admin/Prof
                    if role in ["Admin", "Presidente", "Professor"]:
                        celulas.append(ft.DataCell(ft.Text(nome_usuario, color=ft.Colors.BLACK)))
                    
                    celulas.append(ft.DataCell(ft.Text(nome_arquivo, size=12, color=ft.Colors.BLUE_GREY)))
                    celulas.append(ft.DataCell(ft.Row(botoes)))

                    documentos_data_table.rows.append(ft.DataRow(cells=celulas))
                
                if documentos_data_table.page:
                    documentos_data_table.update()

        except Exception as e:
            print(f"Erro ao carregar: {e}")

    # --- FUNÇÃO: Salvar Documento (POST) ---
    def salvar_documento(e):
        if not caminho_arquivo_selecionado[0]:
            mostrar_msg("Selecione um arquivo!", ft.Colors.RED)
            return
        
        headers = get_headers()
        caminho = caminho_arquivo_selecionado[0]

        try:
            with open(caminho, 'rb') as f:
                arquivos = {'arquivo': f}
                dados = {
                    'titulo': titulo_documento.value,
                    'descricao': descricao_documento.value,
                    'tipo_documento': tipo_documento.value
                }
                response = requests.post(API_URL, headers=headers, data=dados, files=arquivos)

            if response.status_code == 201:
                mostrar_msg("Enviado com sucesso!", ft.Colors.GREEN)
                titulo_documento.value = ""
                descricao_documento.value = ""
                texto_arquivo_selecionado.value = "Nenhum arquivo selecionado"
                caminho_arquivo_selecionado[0] = None
                carregar_documentos()
            else:
                mostrar_msg(f"Erro: {response.text}", ft.Colors.RED)

        except Exception as ex:
            mostrar_msg(f"Erro: {ex}", ft.Colors.RED)
        
        page.update()

    # --- FUNÇÃO: Deletar Documento (DELETE) ---
    def deletar_documento(id_doc):
        headers = get_headers()
        try:
            requests.delete(f"{API_URL}{id_doc}/", headers=headers)
            mostrar_msg("Excluído.", ft.Colors.ORANGE)
            carregar_documentos()
        except Exception: pass

    # --- Layout Final ---
    
    # Lógica de Títulos
    titulo_pagina = "Gestão de Documentos"
    subtitulo_pagina = "Todos os Documentos do Sistema"
    texto_upload = "Adicionar Novo Documento"
    
    # Apenas Aluno vê como "Meus Documentos"
    # Professor agora vê como "Gestão"
    if role == "Aluno":
        titulo_pagina = "Meus Documentos"
        subtitulo_pagina = "Arquivos enviados por você"
        texto_upload = "Enviar Comprovante/Documento"

    view = ft.Container(
        content=ft.Column(
            [
                ft.Text(titulo_pagina, size=30, weight="bold", color=ft.Colors.BLACK87),
                ft.Container(height=20),

                # Área de Upload
                ft.Container(
                    content=ft.Column([
                        ft.Text(texto_upload, size=18, weight="bold", color=ft.Colors.BLACK),
                        ft.Row([titulo_documento, tipo_documento]),
                        descricao_documento,
                        ft.Row([
                            ft.ElevatedButton("Selecionar Arquivo...", icon=ft.Icons.ATTACH_FILE, on_click=lambda _: file_picker.pick_files(allow_multiple=False)),
                            texto_arquivo_selecionado
                        ]),
                        ft.Container(height=10),
                        ft.ElevatedButton("Enviar", icon=ft.Icons.SEND, bgcolor=ft.Colors.RED_700, color=ft.Colors.WHITE, on_click=salvar_documento)
                    ]),
                    padding=20, bgcolor=ft.Colors.WHITE, border_radius=10, shadow=ft.BoxShadow(blur_radius=5, color=ft.Colors.BLACK12)
                ),

                ft.Divider(),

                # Área de Listagem
                ft.Row([
                    ft.Text(subtitulo_pagina, size=18, weight="bold", color=ft.Colors.BLACK),
                    ft.IconButton(ft.Icons.REFRESH, icon_color="blue", on_click=lambda _: carregar_documentos())
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),

                ft.Row([documentos_data_table], scroll=ft.ScrollMode.ADAPTIVE)
            ],
            scroll=ft.ScrollMode.AUTO,
            expand=True
        ),
        padding=20,
        expand=True
    )

    def inicializar():
        carregar_documentos()

    view.did_mount = inicializar
    return view