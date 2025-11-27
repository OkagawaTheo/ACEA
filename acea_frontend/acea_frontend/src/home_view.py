import flet as ft
import requests

def create_home_content(page: ft.Page, role: str):
    
    # URLs
    URL_ALUNOS = "http://127.0.0.1:8000/pessoa/api/alunos/"
    URL_PROFESSORES = "http://127.0.0.1:8000/pessoa/api/professores/"
    URL_AULAS_PROF = "http://127.0.0.1:8000/curso/api/cursos/meus_cronogramas/"
    URL_AULAS_ALUNO = "http://127.0.0.1:8000/curso/api/cursos/meus_cursos/"

    def get_headers():
        token = page.client_storage.get("auth_token")
        return {'Authorization': f'Token {token}'} if token else None

    # --- TEXTO LONGO DA HISTÓRIA ---
    HISTORIA_COMPLETA = """
    Fundada em 1990, nossa Associação Cultural nasceu do sonho de um grupo de educadores 
    e artistas locais que acreditavam no poder transformador da educação e da cultura.
    
    No início, operávamos em uma pequena sala cedida pela comunidade, oferecendo apenas 
    aulas de alfabetização e oficinas de artesanato. Com o passar dos anos e o apoio 
    incansável de nossos voluntários e doadores, expandimos nossas atividades.

    Hoje, atendemos mais de 500 alunos em diversos cursos, desde idiomas e reforço escolar 
    até artes marciais e dança. Nossa missão permanece a mesma: democratizar o acesso 
    ao conhecimento e criar oportunidades para que jovens e adultos possam desenvolver 
    todo o seu potencial.

    Acreditamos que a cultura é a base de uma sociedade justa e que a educação é a chave 
    para a liberdade. Junte-se a nós nessa jornada!
    """

    # --- Modal da História ---
    modal_historia = ft.AlertDialog(
        title=ft.Text("Nossa História Completa"),
        content=ft.Column([
            ft.Text(HISTORIA_COMPLETA, size=16, text_align=ft.TextAlign.JUSTIFY),
        ], height=400, width=600, scroll=ft.ScrollMode.AUTO), # Scroll se o texto for grande
        actions=[
            ft.TextButton("Fechar", on_click=lambda e: page.close_dialog())
        ]
    )

    def abrir_historia(e):
        page.dialog = modal_historia
        modal_historia.open = True
        page.update()

    # --- 1. Seção História (Banner) ---
    secao_historia = ft.Container(
        content=ft.Column([
            ft.Text("Bem-vindo à Associação Cultural", size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
            ft.Text(
                "Desde 1990 promovendo educação, cultura e esporte para a comunidade. "
                "Nossa missão é transformar vidas através do conhecimento.",
                size=16, color=ft.Colors.WHITE70, text_align=ft.TextAlign.CENTER
            ),
            ft.Container(height=10),
            # O Botão Novo:
            ft.ElevatedButton(
                "Ler História Completa", 
                icon=ft.Icons.READ_MORE,
                bgcolor=ft.Colors.WHITE, 
                color=ft.Colors.BLUE_GREY_900,
                on_click=abrir_historia
            )
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        
        padding=40,
        bgcolor=ft.Colors.BLUE_GREY_800,
        border_radius=10,
        alignment=ft.alignment.center,
        # Background Image (opcional, se quiser manter)
        image_src="https://picsum.photos/1000/300?grayscale", 
        image_fit=ft.ImageFit.COVER,
        image_opacity=0.2,
        shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.BLACK26)
    )

    # --- 2. Seção Dinâmica (Agenda ou Stats) ---
    conteudo_dinamico = ft.Column(spacing=20)

    def criar_card_stats(titulo, valor, icone, cor):
        return ft.Container(
            content=ft.Column([
                ft.Icon(icone, size=40, color=cor),
                ft.Text(valor, size=30, weight="bold", color=ft.Colors.BLACK87),
                ft.Text(titulo, color=ft.Colors.GREY)
            ], horizontal_alignment="center"),
            padding=20, bgcolor=ft.Colors.WHITE, border_radius=10,
            shadow=ft.BoxShadow(blur_radius=5, color=ft.Colors.BLACK12),
            width=200, height=150, alignment=ft.alignment.center
        )

    def carregar_dados_home():
        headers = get_headers()
        if not headers: return

        try:
            if role == "Admin":
                res_alunos = requests.get(URL_ALUNOS, headers=headers)
                res_profs = requests.get(URL_PROFESSORES, headers=headers)
                
                qtd_alunos = len(res_alunos.json()) if res_alunos.status_code == 200 else "-"
                qtd_profs = len(res_profs.json()) if res_profs.status_code == 200 else "-"
                
                conteudo_dinamico.controls = [
                    ft.Text("Resumo do Sistema", size=20, weight="bold", color=ft.Colors.BLACK87),
                    ft.Row([
                        criar_card_stats("Alunos Ativos", str(qtd_alunos), ft.Icons.PEOPLE, ft.Colors.BLUE),
                        criar_card_stats("Professores", str(qtd_profs), ft.Icons.SCHOOL, ft.Colors.ORANGE),
                        criar_card_stats("Eventos Hoje", "3", ft.Icons.EVENT, ft.Colors.GREEN),
                    ], wrap=True)
                ]

            else:
                url = URL_AULAS_PROF if role == "Professor" else URL_AULAS_ALUNO
                response = requests.get(url, headers=headers)
                
                lista_aulas = ft.Column()
                if response.status_code == 200:
                    cursos = response.json()
                    if not cursos:
                        lista_aulas.controls.append(ft.Text("Nenhuma aula encontrada."))
                    else:
                        for c in cursos:
                            horarios = c.get('horarios', [])
                            txt_horario = f"{horarios[0]['dia']} às {horarios[0]['hora_inicio'][:5]}" if horarios else "Horário a definir"
                            
                            lista_aulas.controls.append(
                                ft.ListTile(
                                    leading=ft.Icon(ft.Icons.BOOK, color=ft.Colors.TEAL),
                                    title=ft.Text(c['nome'], weight="bold"),
                                    subtitle=ft.Text(txt_horario)
                                )
                            )
                
                conteudo_dinamico.controls = [
                    ft.Text(f"Minha Agenda ({role})", size=20, weight="bold", color=ft.Colors.BLACK87),
                    ft.Container(
                        content=lista_aulas,
                        padding=10, bgcolor=ft.Colors.WHITE, border_radius=10,
                        shadow=ft.BoxShadow(blur_radius=5, color=ft.Colors.BLACK12)
                    )
                ]
            page.update()

        except Exception as e:
            print(f"Erro Home: {e}")

    view = ft.Column(
        [secao_historia, ft.Container(height=20), conteudo_dinamico],
        scroll=ft.ScrollMode.AUTO, expand=True
    )

    def inicializar():
        carregar_dados_home()

    view.did_mount = inicializar
    return view