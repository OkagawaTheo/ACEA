import flet as ft

def create_financeiro_view(page, role: str):
    
    # 💡 Handler de Pagamento (Função que seria chamada ao clicar no botão)
    def handle_pagamento_click(e):
        # Aqui você colocaria a lógica real:
        # 1. Obter ID do aluno
        # 2. Chamar uma API de pagamento (Stripe, Mercado Pago, etc.)
        # 3. Abrir uma nova janela ou modal de confirmação.
        print(f"Botão 'Realizar Pagamento' clicado pelo {role}.")
        
        # Exemplo de feedback simples no Flet (usando Snackbar/Banner)
        page.show_snack_bar(
            ft.SnackBar(ft.Text("Iniciando processo de pagamento..."), duration=3000)
        )
        page.update()

    # 🎯 1. CRIAÇÃO DO BOTÃO MOVIDA PARA FORA DO IF/ELSE
    botao_pagamento = ft.ElevatedButton(
        text="Realizar Pagamento",
        icon=ft.Icons.PAYMENT_ROUNDED,
        on_click=handle_pagamento_click,
        # Cores de destaque para ação principal
        bgcolor=ft.Colors.BLUE_ACCENT_700,
        color=ft.Colors.WHITE,
        style=ft.ButtonStyle(padding=20) # Aumenta o padding para destaque
    )

    # Componente de Título com Permissão
    titulo = ft.Text(
        "Relatórios Financeiros da Associação" if role != 'Aluno' else "Meus Pagamentos",
        size=30, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK
    )

    # Lógica Condicional para Acesso a Relatórios Detalhados
    if role == 'Professor' or role == 'Admin':
        
        # Título da Seção Administrativa
        administrative_title = ft.Text("Visão Administrativa (TFinanceiro)", size=20, weight=ft.FontWeight.W_600, color=ft.Colors.BLACK)
        
        # Define os controles que vão no cabeçalho
        header_controls = [
            administrative_title,
            ft.Container(expand=True), # Empurrador de espaço
        ]

        # 🎯 CONDIÇÃO: ADICIONA O BOTÃO SOMENTE SE FOR PROFESSOR (role != 'Admin')
        if role != 'Admin':
             header_controls.append(botao_pagamento)
        
        header_row = ft.Row(
            header_controls,
            vertical_alignment=ft.CrossAxisAlignment.CENTER
        )
        
        main_content = ft.Column(
            [
                header_row, # Novo cabeçalho com o botão (ou sem ele para Admin)
                ft.Row(
                    [
                        # Card de Receitas (Verde)
                        ft.Card(
                            content=ft.Container(content=ft.Text("R$ 15.400,00\nReceita Total", size=16, color=ft.Colors.WHITE), padding=15),
                            width=200, color=ft.Colors.TEAL_700
                        ),
                        # Card de Doações (Vermilion)
                        ft.Card(
                            content=ft.Container(content=ft.Text("R$ 3.100,00\nDoações (TDoacao)", size=16, color=ft.Colors.WHITE), padding=15),
                            width=200, color=ft.Colors.RED_700
                        ),
                    ],
                    spacing=20
                ),
                ft.Container(height=20),
                ft.Text("Relatório de Pagamentos (TPagamento)", size=20, weight=ft.FontWeight.W_600, color=ft.Colors.BLACK),
                ft.DataTable(
                    columns=[
                        ft.DataColumn(ft.Text("Assoc. (TAssociado)", color=ft.Colors.BLACK)),
                        ft.DataColumn(ft.Text("Valor", color=ft.Colors.BLACK)),
                        ft.DataColumn(ft.Text("Data Pag.", color=ft.Colors.BLACK)),
                    ],
                    rows=[
                        ft.DataRow(cells=[
                            ft.DataCell(ft.Text("Takahashi", color=ft.Colors.BLACK)), 
                            ft.DataCell(ft.Text("R$ 150", color=ft.Colors.BLACK)), 
                            ft.DataCell(ft.Text("01/11/2025", color=ft.Colors.BLACK))
                        ]),
                        ft.DataRow(cells=[
                            ft.DataCell(ft.Text("Yamada", color=ft.Colors.BLACK)), 
                            ft.DataCell(ft.Text("R$ 200", color=ft.Colors.BLACK)), 
                            ft.DataCell(ft.Text("05/11/2025", color=ft.Colors.BLACK))
                        ]),
                    ],
                )
            ]
        )
    else: # Usuário é Aluno (Somente Pagamentos e Histórico)
        
        main_content = ft.Column(
            [
                # O botão é incluído aqui, pois o bloco ELSE é exclusivo para 'Aluno'
                ft.Row(
                    [
                        # Título e Botão lado a lado para destaque
                        ft.Text("Seu Histórico de Pagamentos (TPagamento)", size=20, weight=ft.FontWeight.W_600, color=ft.Colors.BLACK),
                        ft.Container(expand=True), # Empurrador de espaço
                        botao_pagamento # Botão no canto direito (reutilizado)
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.CENTER
                ),
                ft.Container(height=20),
                
                ft.DataTable(
                    columns=[
                        ft.DataColumn(ft.Text("Tipo", color=ft.Colors.BLACK)),
                        ft.DataColumn(ft.Text("Valor", color=ft.Colors.BLACK)),
                        ft.DataColumn(ft.Text("Status", color=ft.Colors.BLACK)),
                    ],
                    rows=[
                        ft.DataRow(cells=[
                            ft.DataCell(ft.Text("Mensalidade", color=ft.Colors.BLACK)), 
                            ft.DataCell(ft.Text("R$ 150", color=ft.Colors.BLACK)), 
                            ft.DataCell(ft.Text("Pago", style=ft.TextStyle(color=ft.Colors.TEAL_700)))
                        ]),
                        ft.DataRow(cells=[
                            ft.DataCell(ft.Text("Curso Caligrafia", color=ft.Colors.BLACK)), 
                            ft.DataCell(ft.Text("R$ 100", color=ft.Colors.BLACK)), 
                            ft.DataCell(ft.Text("Pendente", style=ft.TextStyle(color=ft.Colors.RED_700)))]),
                    ],
                )
            ]
        )

    return ft.Column([titulo, ft.Container(height=20), main_content], scroll=ft.ScrollMode.ADAPTIVE)