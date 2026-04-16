import flet as ft
import logging
import sys
from processador import processar_holerite_unico, processar_holerites_unitarios

# Configura o log também na interface
logging.basicConfig(
    filename="debug_log.txt",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)

def main(page: ft.Page):
    try:
        logging.info("Interface iniciada com sucesso.")
        page.title = "Central de Holerites - Nexus/DHL"
        page.theme_mode = ft.ThemeMode.LIGHT
        page.window_width = 450
        page.window_height = 650
        page.padding = 30
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        estado = {"modo": None, "operacao": None}

        def processar_arquivos(e: ft.FilePickerResultEvent):
            if not e.files:
                return
            
            logging.info(f"Arquivos selecionados para o modo {estado['modo']}")
            page.snack_bar = ft.SnackBar(ft.Text("Processando..."), open=True)
            page.update()

            modo = estado["modo"]
            op = estado["operacao"]
            
            if modo == "MASSA":
                sucesso, msg = processar_holerite_unico(e.files[0].path, op)
            else:
                caminhos = [f.path for f in e.files]
                sucesso, msg = processar_holerites_unitarios(caminhos, op)
            
            if sucesso:
                page.snack_bar = ft.SnackBar(ft.Text("✅ Sucesso! Verifique seus Downloads."), bgcolor="green", open=True)
            else:
                page.snack_bar = ft.SnackBar(ft.Text(f"❌ Erro: {msg}"), bgcolor="red", open=True)
            page.update()

        file_picker = ft.FilePicker(on_result=processar_arquivos)
        page.overlay.append(file_picker)
        container_principal = ft.Container()

        def mostrar_menu_modos(e=None):
            container_principal.content = ft.Column([
                ft.Text("Escolha a ferramenta:", size=20, weight="bold"),
                ft.ElevatedButton("PDF ÚNICO EM MASSA", width=350, height=80, bgcolor=ft.colors.BLUE_800, color="white", on_click=lambda _: ir_para_operacoes("MASSA")),
                ft.ElevatedButton("VÁRIOS PDFs INDIVIDUAIS", width=350, height=80, bgcolor=ft.colors.DEEP_ORANGE_700, color="white", on_click=lambda _: ir_para_operacoes("UNITARIO")),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
            page.update()

        def ir_para_operacoes(modo):
            estado["modo"] = modo
            cor = ft.colors.BLUE_800 if modo == "MASSA" else ft.colors.DEEP_ORANGE_700
            container_principal.content = ft.Column([
                ft.Text(f"MÓDULO: {modo}", size=12, color=cor),
                ft.ElevatedButton("DHL ITUPEVA", width=300, height=60, bgcolor=cor, color="white", on_click=lambda _: disparar_picker("ITUPEVA")),
                ft.ElevatedButton("DHL CABREÚVA", width=300, height=60, bgcolor=cor, color="white", on_click=lambda _: disparar_picker("CABREUVA")),
                ft.ElevatedButton("DHL EMBU DAS ARTES", width=300, height=60, bgcolor=cor, color="white", on_click=lambda _: disparar_picker("EMBU")),
                ft.TextButton("← Voltar", on_click=mostrar_menu_modos)
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
            page.update()

        def disparar_picker(op):
            estado["operacao"] = op
            file_picker.pick_files(allow_multiple=(estado["modo"] == "UNITARIO"), allowed_extensions=["pdf"])

        page.add(ft.Text("Nexus/DHL - Holerites", size=28, weight="bold"), ft.Divider(height=30), container_principal)
        mostrar_menu_modos()

    except Exception as e:
        logging.critical(f"Erro fatal na interface: {e}")

if __name__ == "__main__":
    try:
        ft.app(target=main)
    except Exception as e:
        logging.critical(f"Não foi possível iniciar o motor Flet: {e}")

