import flet as ft

class Cronograma:
    def __init__(self, data):
        self.id = data.get('id')
        self.nome = data.get('nome', '')
        self.horarios = data.get('horarios', []) 
    
    def formatar_horario(self):
        if not self.horarios: return "Horário a definir"
        mapa_dias = {"SEG": "Segunda", "TER": "Terça", "QUA": "Quarta", "QUI": "Quinta", "SEX": "Sexta", "SAB": "Sábado", "DOM": "Domingo"}
        texto = ""
        for h in self.horarios:
            dia = mapa_dias.get(h.get('dia', ''), h.get('dia', ''))
            inicio = h.get('hora_inicio', '')[:5]
            fim = h.get('hora_fim', '')[:5]
            texto += f"{dia} • {inicio} - {fim}\n"
        return texto.strip()

def create_cronograma_view(page: ft.Page):
    
    # --- Check Admin Role Dynamically ---
    user_role = page.client_storage.get("user_role")
    IS_ADMIN = True if user_role == "Admin" else False

    # Mock DB (Simulated)
    local_db = [
        {"id": 1, "nome": "Japonês Básico I", "horarios": [{"dia": "SEX", "hora_inicio": "10:00", "hora_fim": "11:00"}]},
        {"id": 2, "nome": "Judô Infantil", "horarios": [{"dia": "SEG", "hora_inicio": "14:00", "hora_fim": "15:30"}]}
    ]

    # UI Elements
    cronogramas_list = ft.Column(spacing=15) # No expand, No scroll (Parent scrolls)
    txt_nome_curso = ft.TextField(label="Nome do Curso")
    slots_column = ft.Column(spacing=10, scroll=ft.ScrollMode.AUTO, height=200)
    current_editing_id = None 

    # --- Helper Logic ---
    def create_slot_row(dia="", start="", end=""):
        days_opts = [ft.dropdown.Option(d) for d in ["SEG", "TER", "QUA", "QUI", "SEX", "SAB", "DOM"]]
        return ft.Row(controls=[
            ft.Dropdown(options=days_opts, value=dia if dia else "SEG", width=80, dense=True, text_size=12),
            ft.TextField(value=start, label="Início", width=70, height=40, text_size=12, content_padding=5),
            ft.TextField(value=end, label="Fim", width=70, height=40, text_size=12, content_padding=5),
            ft.IconButton(icon=ft.Icons.DELETE_OUTLINE, icon_color=ft.Colors.RED_400, on_click=lambda e: remove_slot(e.control.parent))
        ])

    def remove_slot(row):
        slots_column.controls.remove(row)
        page.update()

    def add_empty_slot(e=None):
        slots_column.controls.append(create_slot_row())
        page.update()

    # --- Dialog Logic ---
    def save_data(e):
        new_horarios = []
        for row in slots_column.controls:
            d, i, f = row.controls[0].value, row.controls[1].value, row.controls[2].value
            if d and i and f: new_horarios.append({"dia": d, "hora_inicio": i, "hora_fim": f})

        data = {"nome": txt_nome_curso.value, "horarios": new_horarios}
        
        if current_editing_id:
            for item in local_db:
                if item['id'] == current_editing_id: item.update(data)
        else:
            data["id"] = len(local_db) + 100
            local_db.append(data)

        page.close(edit_dialog)
        carregar_dados()

    # Defined here so it can be referenced
    edit_dialog = ft.AlertDialog(
        title=ft.Text("Editar Curso"),
        content=ft.Container(content=ft.Column([txt_nome_curso, ft.Text("Horários:"), slots_column, ft.TextButton("+ Add Horário", on_click=add_empty_slot)], tight=True, width=350), padding=10),
        actions=[ft.TextButton("Cancelar", on_click=lambda e: page.close(edit_dialog)), ft.ElevatedButton("Salvar", on_click=save_data, bgcolor=ft.Colors.RED_700, color=ft.Colors.WHITE)]
    )

    def open_editor(e, cronograma=None):
        nonlocal current_editing_id
        slots_column.controls.clear()
        if cronograma:
            current_editing_id = cronograma.id
            txt_nome_curso.value = cronograma.nome
            for h in cronograma.horarios: slots_column.controls.append(create_slot_row(h['dia'], h['hora_inicio'], h['hora_fim']))
        else:
            current_editing_id = None
            txt_nome_curso.value = ""
            slots_column.controls.append(create_slot_row())
        
        page.open(edit_dialog) # FIX: Use page.open()
        page.update()

    def delete_cronograma(c_id):
        nonlocal local_db
        local_db = [x for x in local_db if x['id'] != c_id]
        carregar_dados()

    # --- UI Builder ---
    def criar_item_ui(c: Cronograma):
        content = ft.Row([
            ft.Row([
                ft.Container(ft.Icon(ft.Icons.ACCESS_TIME_FILLED, color=ft.Colors.RED_700), bgcolor=ft.Colors.RED_50, padding=10, border_radius=50),
                ft.Column([ft.Text(c.nome, weight="bold", size=16), ft.Text(c.formatar_horario(), size=13, color="grey")])
            ]),
            # Buttons only show if Admin
            ft.Row([
                ft.IconButton(ft.Icons.EDIT, icon_color="grey", on_click=lambda e: open_editor(e, c)),
                ft.IconButton(ft.Icons.DELETE, icon_color="red", on_click=lambda e: delete_cronograma(c.id))
            ]) if IS_ADMIN else ft.Container()
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        
        return ft.Container(content=content, padding=15, border=ft.border.all(1, ft.Colors.GREY_200), border_radius=10, bgcolor=ft.Colors.WHITE)

    def carregar_dados():
        cronogramas_list.controls.clear()
        cronogramas_list.controls.append(ft.Text("Grade Horária", size=20, weight="bold"))
        for item in local_db: cronogramas_list.controls.append(criar_item_ui(Cronograma(item)))
        page.update()

    # --- Main Container ---
    view_content = ft.Column([
        ft.Row([
            ft.Text("Painel Admin" if IS_ADMIN else "Cronogramas", size=24, weight="bold"),
            ft.FloatingActionButton(icon=ft.Icons.ADD, bgcolor=ft.Colors.RED_700, on_click=lambda e: open_editor(e)) if IS_ADMIN else ft.Container()
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        ft.Divider(),
        cronogramas_list
    ])

    # FIX: Remove expand=True to avoid conflict with Dashboard scroll
    return ft.Container(content=view_content, padding=20, bgcolor=ft.Colors.WHITE, border_radius=12, shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.with_opacity(0.05, ft.Colors.BLACK)))