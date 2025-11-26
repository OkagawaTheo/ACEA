import flet as ft
import requests

def create_atividades_aluno_view(page: ft.Page):
    
    URL_MEUS_CURSOS = "http://127.0.0.1:8000/curso/api/cursos/meus_cursos/"
    URL_MINHAS_ATIV = "http://127.0.0.1:8000/curso/api/atividades/minhas_atividades/"

    # Elemento que vai segurar as abas
    tabs_control = ft.Tabs(
        selected_index=0,
        animation_duration=300,
        indicator_color=ft.Colors.RED_700,
        label_color=ft.Colors.BLACK87,
        unselected_label_color=ft.Colors.BLACK45,
        tabs=[], 
        expand=True # Importante para ocupar a tela toda
    )

    loading = ft.ProgressRing()
    msg_erro = ft.Text(visible=False, color=ft.Colors.RED)

    # --- Função que desenha o CARD (Item visual) ---
    def criar_card_atividade(titulo, tipo):
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text(f"Material para: {titulo}", size=16, weight=ft.FontWeight.W_500),
                    ft.Text(f"Categoria: {tipo}", size=12, color=ft.Colors.GREY),
                    ft.Divider(),
                    
                    ft.Row(
                        [
                            ft.Icon(ft.Icons.INSERT_DRIVE_FILE_OUTLINED, color=ft.Colors.TEAL_700),
                            ft.Text("Plano de Ensino.pdf"),
                            ft.IconButton(ft.Icons.DOWNLOAD, tooltip="Baixar"),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    ),
                    
                    ft.Row(
                        [
                            ft.Icon(ft.Icons.LIVE_HELP, color=ft.Colors.RED_ACCENT_700),
                            ft.Text("Dúvidas? Contate o professor."),
                            ft.ElevatedButton("Mensagem", bgcolor=ft.Colors.RED_700, color=ft.Colors.WHITE, height=30)
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    ),
                    
                    ft.Text("\nProgresso: Em andamento", color=ft.Colors.BLACK54)
                ]
            ),
            padding=15, bgcolor=ft.Colors.WHITE, border_radius=10, shadow=ft.BoxShadow(blur_radius=3, color=ft.Colors.BLACK12),
            margin=ft.margin.all(10) 
        )

    # --- Função Principal de Carga ---
    def carregar_atividades():
        token = page.client_storage.get("auth_token")
        if not token:
            msg_erro.value = "Não autenticado."
            msg_erro.visible = True
            return

        headers = {'Authorization': f'Token {token}'}
        
        try:
            res_cursos = requests.get(URL_MEUS_CURSOS, headers=headers)
            res_ativ = requests.get(URL_MINHAS_ATIV, headers=headers)
            
            tabs_control.tabs.clear()
            encontrou_algo = False

            def adicionar_aba(titulo, tipo):
                # AQUI ESTÁ A CORREÇÃO DO SCROLL:
                # O conteúdo da aba é uma Coluna com Scroll AUTO
                content_scrollable = ft.Column(
                    controls=[
                        criar_card_atividade(titulo, tipo),
                        # Se quiser adicionar mais cards futuramente, eles vão aqui
                    ],
                    scroll=ft.ScrollMode.AUTO, # Habilita o scroll vertical
                    expand=True
                )
                
                tabs_control.tabs.append(
                    ft.Tab(
                        text=titulo,
                        content=ft.Container(content=content_scrollable, padding=10)
                    )
                )

            if res_cursos.status_code == 200:
                for curso in res_cursos.json():
                    adicionar_aba(curso['nome'], "Curso Acadêmico")
                    encontrou_algo = True

            if res_ativ.status_code == 200:
                for ativ in res_ativ.json():
                    adicionar_aba(ativ['nome'], "Esporte/Lazer")
                    encontrou_algo = True

            loading.visible = False
            
            if not encontrou_algo:
                msg_erro.value = "Você não está matriculado em nenhum curso ou atividade."
                msg_erro.visible = True
            
            # Verifica se está na tela antes de update
            if tabs_control.page:
                tabs_control.update()
                page.update()

        except Exception as e:
            loading.visible = False
            msg_erro.value = f"Erro de conexão: {e}"
            msg_erro.visible = True
            page.update()

    # --- Layout Principal ---
    view = ft.Column(
        [
            ft.Text("Minhas Atividades", size=30, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK87),
            loading,
            msg_erro,
            tabs_control
        ],
        expand=True # Garante que a coluna principal ocupe a altura toda
    )

    def inicializar(): # <--- CORRETO (Sem argumentos)
        carregar_atividades()

    view.did_mount = inicializar
    return view