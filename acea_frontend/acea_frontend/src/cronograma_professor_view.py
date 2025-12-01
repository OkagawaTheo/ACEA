import flet as ft
import requests

# --- Class to Structure Data ---
class Cronograma:
    def __init__(self, data):
        self.id = data.get('id')
        self.nome = data.get('nome', 'Curso Sem Nome')
        self.horarios = data.get('horarios', [])
    
    def formatar_horario(self):
        """Formata a lista de horários para o estilo: Sexta-feira das 10h às 11h."""
        if not self.horarios:
            return "Horário a definir"
        
        # Mapa para converter siglas em nomes completos
        mapa_dias = {
            "SEG": "Segunda-feira", "TER": "Terça-feira", "QUA": "Quarta-feira",
            "QUI": "Quinta-feira", "SEX": "Sexta-feira", "SAB": "Sábado", "DOM": "Domingo"
        }

        texto = ""
        for h in self.horarios:
            dia_sigla = h.get('dia', '')
            dia_completo = mapa_dias.get(dia_sigla, dia_sigla)
            
            # Formata hora: remove segundos e substitui :00 por h
            inicio = h.get('hora_inicio', '')[:5]
            if inicio.endswith(":00"): inicio = inicio.replace(":00", "h")
            
            fim = h.get('hora_fim', '')[:5]
            if fim.endswith(":00"): fim = fim.replace(":00", "h")

            texto += f"{dia_completo} das {inicio} às {fim}\n"
            
        return texto.strip()

def create_cronograma_professor_view(page: ft.Page):
    
    # --- Configurações e Endpoints ---
    URL_MEUS_CRONOGRAMAS = "http://127.0.0.1:8000/curso/api/cursos/meus_cronogramas/"
    
    user_role = page.client_storage.get("user_role")

    # --- Helper de Token ---
    def get_headers():
        token = page.client_storage.get("auth_token")
        return {'Authorization': f'Token {token}'} if token else None

    # --- Styles ---
    CARD_BG = ft.Colors.WHITE
    SHADOW = ft.BoxShadow(blur_radius=15, color=ft.Colors.with_opacity(0.06, ft.Colors.BLACK))
    TEXT_COLOR = ft.Colors.BLACK87
    SUB_TEXT_COLOR = ft.Colors.GREY_600

    # =============================================================================================
    # --- LISTA DE CRONOGRAMAS (Visual Atualizado) ---
    # =============================================================================================
    cronogramas_list = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True, spacing=15)

    def criar_item_ui(cronograma: Cronograma):
        return ft.Container(
            content=ft.Row(
                [
                    # Lado Esquerdo: Ícone + Info
                    ft.Row([
                        # Indicador Visual de Tempo (Ícone de Relógio)
                        ft.Container(
                            content=ft.Column([
                                ft.Icon(ft.Icons.ACCESS_TIME_FILLED, color=ft.Colors.RED_700, size=24),
                            ], alignment=ft.MainAxisAlignment.CENTER),
                            padding=12,
                            bgcolor=ft.Colors.RED_50,
                            border_radius=50,
                            width=50, height=50, alignment=ft.alignment.center
                        ),
                        
                        # Texto: Curso e Horário Formatado
                        ft.Column([
                            ft.Text(cronograma.nome, weight=ft.FontWeight.W_700, size=18, color=TEXT_COLOR),
                            ft.Container(
                                content=ft.Text(
                                    cronograma.formatar_horario(), 
                                    size=15, 
                                    color=ft.Colors.RED_700, 
                                    weight=ft.FontWeight.W_500
                                ),
                                padding=ft.padding.only(top=2)
                            ),
                        ], spacing=4, alignment=ft.MainAxisAlignment.CENTER),
                    ], vertical_alignment=ft.CrossAxisAlignment.CENTER),
                    
                    # Lado Direito: Ações (Sutil)
                    ft.IconButton(ft.Icons.MORE_VERT, icon_color=ft.Colors.GREY_400, tooltip="Opções")
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            ),
            padding=ft.padding.symmetric(horizontal=25, vertical=20), 
            border=ft.border.all(1, ft.Colors.GREY_100), 
            border_radius=12,
            bgcolor=ft.Colors.WHITE, 
            shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.with_opacity(0.03, ft.Colors.BLACK))
        )

    def carregar_dados():
        headers = get_headers()
        
        try:
            # Em produção, use requests.get(URL_MEUS_CRONOGRAMAS, headers=headers)
            # MOCK DATA para visualizar o resultado sem backend:
            mock_data = [
                {"id": 1, "nome": "Japonês Básico I", "horarios": [{"dia": "SEX", "hora_inicio": "10:00:00", "hora_fim": "11:00:00"}]},
                {"id": 2, "nome": "Judô Infantil", "horarios": [{"dia": "SEG", "hora_inicio": "14:00:00", "hora_fim": "15:30:00"}, {"dia": "QUA", "hora_inicio": "14:00:00", "hora_fim": "15:30:00"}]},
                {"id": 3, "nome": "Caligrafia Avançada", "horarios": [{"dia": "SAB", "hora_inicio": "09:00:00", "hora_fim": "12:00:00"}]},
            ]
            
            cronogramas_list.controls.clear()
            
            # Título da Lista
            cronogramas_list.controls.append(
                ft.Row([
                     ft.Text("Grade Horária", size=20, weight=ft.FontWeight.W_700, color=TEXT_COLOR),
                     ft.Container(
                         content=ft.Text(f"{len(mock_data)} Turmas Ativas", size=12, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
                         bgcolor=ft.Colors.RED_700, padding=ft.padding.symmetric(horizontal=10, vertical=5), border_radius=20
                     )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
            )
            cronogramas_list.controls.append(ft.Divider(color=ft.Colors.GREY_100, height=20))

            # Renderiza Mock Data
            if mock_data:
                for item_data in mock_data:
                    cronogramas_list.controls.append(criar_item_ui(Cronograma(item_data)))
            else:
                cronogramas_list.controls.append(ft.Text("Nenhuma aula agendada.", color=SUB_TEXT_COLOR))

        except Exception as e:
            cronogramas_list.controls.append(ft.Text(f"Erro: {e}"))
        
        page.update()

    # =============================================================================================
    # --- LAYOUT PRINCIPAL ---
    # =============================================================================================
    
    view = ft.Container(
        content=ft.Column(
            [
                ft.Text("Cronogramas & Aulas", size=24, weight=ft.FontWeight.BOLD, color=TEXT_COLOR),
                ft.Container(height=20),

                # Full width Container for the list
                ft.Container(
                    content=cronogramas_list,
                    padding=30, 
                    bgcolor=CARD_BG, 
                    border_radius=12, 
                    shadow=SHADOW,
                    expand=True, 
                    alignment=ft.alignment.top_left
                )
            ],
            expand=True
        ),
        padding=0, 
        expand=True
    )

    view.did_mount = carregar_dados
    return view