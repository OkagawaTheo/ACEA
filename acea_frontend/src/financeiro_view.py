import flet as ft

def create_financeiro_view(page, role: str):
    
    # Componente de Título com Permissão
    titulo = ft.Text(
        "Relatórios Financeiros da Associação" if role != 'Aluno' else "Meus Pagamentos",
        size=30, weight=ft.FontWeight.BOLD
    )

    # Lógica Condicional para Acesso a Relatórios Detalhados
    if role == 'Professor' or role == 'Admin':
        main_content = ft.Column(
            [
                ft.Text("Visão Administrativa (TFinanceiro)", size=20, weight=ft.FontWeight.W_600),
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
                ft.Text("Relatório de Pagamentos (TPagamento)", size=20, weight=ft.FontWeight.W_600),
                ft.DataTable(
                    columns=[
                        ft.DataColumn(ft.Text("Assoc. (TAssociado)")),
                        ft.DataColumn(ft.Text("Valor")),
                        ft.DataColumn(ft.Text("Data Pag.")),
                    ],
                    rows=[
                        ft.DataRow(cells=[ft.DataCell(ft.Text("Takahashi")), ft.DataCell(ft.Text("R$ 150")), ft.DataCell(ft.Text("01/11/2025"))]),
                        ft.DataRow(cells=[ft.DataCell(ft.Text("Yamada")), ft.DataCell(ft.Text("R$ 200")), ft.DataCell(ft.Text("05/11/2025"))]),
                    ],
                )
            ]
        )
    else: # Usuário é Aluno (Somente Pagamentos)
        main_content = ft.Column(
            [
                ft.Text("Seu Histórico de Pagamentos (TPagamento)", size=20, weight=ft.FontWeight.W_600),
                ft.DataTable(
                    columns=[
                        ft.DataColumn(ft.Text("Tipo")),
                        ft.DataColumn(ft.Text("Valor")),
                        ft.DataColumn(ft.Text("Status")),
                    ],
                    rows=[
                        ft.DataRow(cells=[ft.DataCell(ft.Text("Mensalidade")), ft.DataCell(ft.Text("R$ 150")), ft.DataCell(ft.Text("Pago", style=ft.TextStyle(color=ft.Colors.TEAL_700)))]),
                        ft.DataRow(cells=[ft.DataCell(ft.Text("Curso Caligrafia")), ft.DataCell(ft.Text("R$ 100")), ft.DataCell(ft.Text("Pendente", style=ft.TextStyle(color=ft.Colors.RED_700)))]),
                    ],
                )
            ]
        )

    return ft.Column([titulo, ft.Container(height=20), main_content], scroll=ft.ScrollMode.ADAPTIVE)