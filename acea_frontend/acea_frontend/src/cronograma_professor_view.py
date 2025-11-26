import flet as ft
import requests

def create_cronograma_professor_view(page: ft.Page):
    
    URL_CRONOGRAMA = "http://127.0.0.1:8000/curso/api/cursos/meus_cronogramas/"

    # --- Helper de Token ---
    def get_headers():
        token = page.client_storage.get("auth_token")
        return {'Authorization': f'Token {token}'} if token else None

    # --- Campo para edição (Visual - Lembretes) ---
    nome_cronograma = ft.TextField(label="Título do Lembrete", width=400)
    descricao_cronograma = ft.TextField(label="Detalhes", multiline=True)
    
    # Botão de Salvar (Simulação visual)
    save_button = ft.ElevatedButton(
        text="Salvar Lembrete",
        bgcolor=ft.Colors.RED_700,
        color=ft.Colors.WHITE,
        icon=ft.Icons.SAVE,
        on_click=lambda e: print("Lógica de salvar lembrete pessoal futuramente")
    )

    # --- Coluna da Lista (Onde os dados reais vão aparecer) ---
    # Começa com Scroll Auto para não dar o bug de tela
    cronogramas_list = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)

    # --- Função que desenha cada Item da Lista ---
    def criar_item_lista(curso):
        nome_curso = curso.get('nome', 'Curso Sem Nome')
        horarios = curso.get('horarios', [])

        # Formata os horários para exibir bonito (Ex: SEG: 14:00 - 16:00)
        texto_horarios = ""
        if horarios:
            for h in horarios:
                hora_inicio = h['hora_inicio'][:5] # Pega só HH:MM
                hora_fim = h['hora_fim'][:5]
                texto_horarios += f"• {h['dia']}: {hora_inicio} às {hora_fim}\n"
        else:
            texto_horarios = "Sem horários definidos."

        # O Container Vermelho que você desenhou
        return ft.Container(
            content=ft.Row(
                [
                    ft.Column([
                        ft.Text(nome_curso, weight=ft.FontWeight.W_600, size=16),
                        ft.Text(texto_horarios, size=12, color=ft.Colors.BLACK54),
                    ], expand=True),
                    
                    ft.Row([
                        # Botão para ver alunos (Exemplo funcional)
                        ft.IconButton(ft.Icons.GROUP, icon_color=ft.Colors.BLUE, tooltip="Ver Turma"),
                        # Edit/Delete visuais
                        ft.IconButton(ft.Icons.EDIT, icon_color=ft.Colors.TEAL_700, tooltip="Editar Nota"),
                    ])
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            ),
            padding=10, 
            border=ft.border.all(1, ft.Colors.RED_ACCENT_100), 
            border_radius=5,
            bgcolor=ft.Colors.RED_50,
            margin=ft.margin.only(bottom=10)
        )

    # --- Função que busca na API ---
    def carregar_dados():
        headers = get_headers()
        if not headers: return

        try:
            response = requests.get(URL_CRONOGRAMA, headers=headers)
            cronogramas_list.controls.clear()
            
            # Título da lista
            cronogramas_list.controls.append(
                ft.Text("Minhas Aulas Ativas", size=18, weight=ft.FontWeight.W_600, color=ft.Colors.BLACK87)
            )
            cronogramas_list.controls.append(ft.Divider(color=ft.Colors.BLACK12))

            if response.status_code == 200:
                cursos = response.json()
                if not cursos:
                    cronogramas_list.controls.append(ft.Text("Nenhuma aula atribuída a você."))
                else:
                    for curso in cursos:
                        cronogramas_list.controls.append(criar_item_lista(curso))
            
            elif response.status_code == 403:
                cronogramas_list.controls.append(ft.Text("Acesso restrito a professores.", color=ft.Colors.RED))
            else:
                cronogramas_list.controls.append(ft.Text(f"Erro: {response.status_code}"))

        except Exception as e:
            cronogramas_list.controls.append(ft.Text(f"Erro de conexão: {e}"))
        
        page.update()

    # --- Layout Principal (Mantendo sua estrutura de 2 colunas) ---
    view = ft.Column(
        [
            ft.Text("Gerenciamento de Cronogramas", size=30, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK87),
            ft.Container(height=20),

            ft.Row(
                [
                    # Coluna da Esquerda: Criar/Editar (Visual)
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Text("Adicionar Lembrete", size=20, weight=ft.FontWeight.W_600, color=ft.Colors.BLACK87),
                                nome_cronograma,
                                descricao_cronograma,
                                ft.Container(height=10),
                                save_button
                            ]
                        ),
                        padding=20,
                        bgcolor=ft.Colors.WHITE,
                        border_radius=10,
                        shadow=ft.BoxShadow(blur_radius=5, color=ft.Colors.BLACK12),
                        width=400, # Ajustei um pouco a largura
                        alignment=ft.alignment.top_center
                    ),
                    
                    ft.Container(width=40), # Espaçamento
                    
                    # Coluna da Direita: Listagem Real (Vinda do Django)
                    ft.Container(
                        content=cronogramas_list,
                        padding=20,
                        bgcolor=ft.Colors.WHITE,
                        border_radius=10,
                        shadow=ft.BoxShadow(blur_radius=5, color=ft.Colors.BLACK12),
                        expand=True, # Ocupa o resto da tela
                        alignment=ft.alignment.top_left
                    )
                ],
                vertical_alignment=ft.CrossAxisAlignment.START,
                expand=True
            )
        ],
        scroll=ft.ScrollMode.ADAPTIVE,
        expand=True
    )

    # Inicialização (Sem o 'e' para não dar erro)
    def inicializar():
        carregar_dados()

    view.did_mount = inicializar
    return view