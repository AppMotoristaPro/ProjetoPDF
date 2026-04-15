import flet as ft
from processador import processar_holerites

def main(page: ft.Page):
    page.title = "Nexus/DHL - Gerenciador de Holerites"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_width = 450
    page.window_height = 600
    page.padding = 40
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Armazena qual operação está sendo processada no momento
    operacao_ativa = ft.Ref[str]()

    def ao_selecionar_pdf(e: ft.FilePickerResultEvent):
        if e.files:
            caminho_pdf = e.files[0].path
            op = operacao_ativa.current
            
            # Chama o processador
            sucesso, resultado = processar_holerites(caminho_pdf, op)
            
            if sucesso:
                # Muda a cor do botão correspondente para VERDE
                if op == "ITUPEVA": btn_itupeva.bgcolor = ft.colors.GREEN_700
                elif op == "CABREUVA": btn_cabreuva.bgcolor = ft.colors.GREEN_700
                elif op == "EMBU": btn_embu.bgcolor = ft.colors.GREEN_700
                
                page.snack_bar = ft.SnackBar(ft.Text(f"✅ Sucesso! Salvo em: {resultado}"), open=True)
            else:
                page.snack_bar = ft.SnackBar(ft.Text(f"❌ Erro: {resultado}"), bgcolor="red", open=True)
            
            page.update()

    file_picker = ft.FilePicker(on_result=ao_selecionar_pdf)
    page.overlay.append(file_picker)

    def disparar_processo(op):
        operacao_ativa.current = op
        file_picker.pick_files(allow_multiple=False, allowed_extensions=["pdf"])

    def resetar_interface(e):
        btn_itupeva.bgcolor = ft.colors.BLUE_800
        btn_cabreuva.bgcolor = ft.colors.BLUE_800
        btn_embu.bgcolor = ft.colors.BLUE_800
        page.snack_bar = ft.SnackBar(ft.Text("Status reiniciado"), open=True)
        page.update()

    # Componentes Visuais
    texto_topo = ft.Text("Selecione a Operação", size=24, weight="bold", color=ft.colors.BLUE_GREY_900)
    
    btn_itupeva = ft.ElevatedButton(
        "DHL ITUPEVA", 
        width=300, height=60, 
        bgcolor=ft.colors.BLUE_800, color="white",
        on_click=lambda _: disparar_processo("ITUPEVA")
    )
    
    btn_cabreuva = ft.ElevatedButton(
        "DHL CABREÚVA", 
        width=300, height=60, 
        bgcolor=ft.colors.BLUE_800, color="white",
        on_click=lambda _: disparar_processo("CABREUVA")
    )
    
    btn_embu = ft.ElevatedButton(
        "DHL EMBU DAS ARTES", 
        width=300, height=60, 
        bgcolor=ft.colors.BLUE_800, color="white",
        on_click=lambda _: disparar_processo("EMBU")
    )

    btn_reset = ft.TextButton("Limpar Status", on_click=resetar_interface)

    page.add(
        ft.Column(
            [
                texto_topo,
                ft.Container(height=20),
                btn_itupeva,
                btn_cabreuva,
                btn_embu,
                ft.Container(height=30),
                btn_reset
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )

ft.app(target=main)
