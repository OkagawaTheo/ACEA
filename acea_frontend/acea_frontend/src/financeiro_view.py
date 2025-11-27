import flet as ft
import requests

def create_financeiro_view(page: ft.Page, role: str):
    
    # URLs da API
    URL_PAGAMENTOS = "http://127.0.0.1:8000/documentacao/api/pagamentos/"
    URL_DOACOES = "http://127.0.0.1:8000/documentacao/api/doacoes/"

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

    # =================================================================
    # ABA 1: PAGAMENTOS (Mensalidades)
    # =================================================================
    
    tabela_pagamentos = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID", color=ft.Colors.BLACK)),
            ft.DataColumn(ft.Text("Ref/Aluno", color=ft.Colors.BLACK)),
            ft.DataColumn(ft.Text("Tipo", color=ft.Colors.BLACK)),
            ft.DataColumn(ft.Text("Valor", color=ft.Colors.BLACK)),
            ft.DataColumn(ft.Text("Status", color=ft.Colors.BLACK)),
            ft.DataColumn(ft.Text("Detalhes", color=ft.Colors.BLACK)),
        ],
        rows=[],
        border=ft.border.all(1, ft.Colors.BLACK12),
        vertical_lines=ft.border.BorderSide(0.5, ft.Colors.BLACK12),
        horizontal_lines=ft.border.BorderSide(0.5, ft.Colors.BLACK12),
        heading_row_color=ft.Colors.GREY_200,
    )

    def carregar_pagamentos():
        headers = get_headers()
        if not headers: return
        try:
            response = requests.get(URL_PAGAMENTOS, headers=headers)
            if response.status_code == 200:
                lista = response.json()
                tabela_pagamentos.rows.clear()
                for p in lista:
                    status_cod = p['status']
                    eh_pago = status_cod == 'PG'
                    cor_status = ft.Colors.GREEN if eh_pago else ft.Colors.ORANGE
                    txt_status = "PAGO" if eh_pago else "PENDENTE"
                    
                    conteudo_acao = ft.Text("-", color=ft.Colors.BLACK)
                    if role in ["Admin", "Presidente"]:
                        if not eh_pago:
                            conteudo_acao = ft.IconButton(ft.Icons.CHECK_CIRCLE, icon_color="green", on_click=lambda e, id=p['id_pagamento']: confirmar_pagamento(id))
                        else:
                            conteudo_acao = ft.Icon(ft.Icons.CHECK, color="green")
                    elif role == "Aluno":
                        conteudo_acao = ft.Row([ft.Icon(ft.Icons.THUMB_UP if eh_pago else ft.Icons.ACCESS_TIME, color="green" if eh_pago else "orange", size=20), ft.Text("Quitado" if eh_pago else "Aguardando", color=ft.Colors.BLACK, size=12)])

                    tabela_pagamentos.rows.append(ft.DataRow(cells=[
                        ft.DataCell(ft.Text(str(p['id_pagamento']), color=ft.Colors.BLACK)),
                        ft.DataCell(ft.Text(f"Aluno {p['id_aluno']}", color=ft.Colors.BLACK)),
                        ft.DataCell(ft.Text(p['tipo_pagamento'], color=ft.Colors.BLACK)),
                        ft.DataCell(ft.Text(f"R$ {p['valor']}", color=ft.Colors.BLACK, weight="bold")),
                        ft.DataCell(ft.Container(content=ft.Text(txt_status, color=ft.Colors.WHITE, size=11, weight="bold"), bgcolor=cor_status, padding=5, border_radius=15)),
                        ft.DataCell(conteudo_acao),
                    ]))
                if tabela_pagamentos.page: tabela_pagamentos.update()
        except Exception as e: print(e)

    def confirmar_pagamento(id_pagamento):
        headers = get_headers()
        try:
            requests.patch(f"{URL_PAGAMENTOS}{id_pagamento}/gerenciar_pagamento/", json={"status": "PG"}, headers=headers)
            mostrar_msg("Pagamento confirmado!", ft.Colors.GREEN)
            carregar_pagamentos()
        except Exception: pass

    # =================================================================
    # ABA 2: DOAÇÕES (Apenas Visualização)
    # =================================================================
    
    tabela_doacoes = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID", color=ft.Colors.BLACK)),
            ft.DataColumn(ft.Text("Doador", color=ft.Colors.BLACK)),
            ft.DataColumn(ft.Text("Valor", color=ft.Colors.BLACK)),
            ft.DataColumn(ft.Text("Data", color=ft.Colors.BLACK))
        ],
        rows=[],
        border=ft.border.all(1, ft.Colors.BLACK12),
        heading_row_color=ft.Colors.GREY_200,
    )

    def carregar_doacoes():
        headers = get_headers()
        try:
            response = requests.get(URL_DOACOES, headers=headers)
            if response.status_code == 200:
                lista = response.json()
                tabela_doacoes.rows.clear()
                for d in lista:
                    tabela_doacoes.rows.append(ft.DataRow(cells=[
                        ft.DataCell(ft.Text(str(d['id_doacao']), color=ft.Colors.BLACK)),
                        ft.DataCell(ft.Text(d.get('doador_nome') or "Anônimo", color=ft.Colors.BLACK)),
                        ft.DataCell(ft.Text(f"R$ {d['valor']}", color=ft.Colors.BLACK)),
                        ft.DataCell(ft.Text(d['data_doacao'][:10], color=ft.Colors.BLACK)),
                    ]))
                if tabela_doacoes.page: tabela_doacoes.update()
        except Exception: pass

    # =================================================================
    # LAYOUT FINAL
    # =================================================================

    # Aba Pagamentos
    aba_pagamentos = ft.Container(
        content=ft.ListView(
            controls=[
                ft.Row([ft.Text("Mensalidades", size=20, weight="bold", color=ft.Colors.BLACK), ft.IconButton(ft.Icons.REFRESH, icon_color="blue", on_click=lambda _: carregar_pagamentos())]),
                ft.Row([tabela_pagamentos], scroll=ft.ScrollMode.ADAPTIVE),
            ], 
            padding=10
        )
    )

    # Aba Doações (Simplificada)
    if role in ["Admin", "Presidente"]:
        aba_doacoes = ft.Container(
            content=ft.ListView(
                controls=[
                    ft.Row([
                        ft.Text("Histórico de Doações Recebidas", size=20, weight="bold", color=ft.Colors.BLACK),
                        ft.IconButton(ft.Icons.REFRESH, icon_color="blue", on_click=lambda _: carregar_doacoes())
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    ft.Container(height=10),
                    ft.Row([tabela_doacoes], scroll=ft.ScrollMode.ADAPTIVE)
                ],
                padding=10
            )
        )
    else:
        aba_doacoes = ft.Container(
            content=ft.Text("Acesso restrito à diretoria.", color=ft.Colors.RED),
            padding=20,
            alignment=ft.alignment.top_left
        )

    # Tabs
    tabs = ft.Tabs(
        selected_index=0,
        label_color=ft.Colors.BLACK,
        tabs=[
            ft.Tab(text="Pagamentos", content=aba_pagamentos),
            ft.Tab(text="Doações", content=aba_doacoes),
        ],
        expand=True,
    )

    def inicializar_dados():
        carregar_pagamentos()
        if role in ["Admin", "Presidente"]: carregar_doacoes()

    view = ft.Container(content=tabs, expand=True)
    view.did_mount = inicializar_dados

    return view