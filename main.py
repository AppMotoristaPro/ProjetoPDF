import sys
import builtins
import ssl
import flet as ft
import logging
from processador import processar_holerite_unico, processar_holerites_unitarios

# Configurações de segurança e sistema para ambiente Windows Corporativo
ssl._create_default_https_context = ssl._create_unverified_context
builtins.exit = sys.exit 

def main(page: ft.Page):
    logging.info("--- Iniciando Interface Nativa ---")
    page.title = "Nexus/DHL - Gerenciador de Holerites"
    page.window_width = 450
    page.window_height = 600
    page.theme_mode = ft.ThemeMode.LIGHT
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    estado = {"modo": None, "operacao": None}

    # Função que lida com o resultado da seleção de arquivos
    def ao_selecionar_arquivos(e):
        if not e.files: 
            logging.info("Seleção de arquivos cancelada pelo usuário.")
            return
            
        logging.info(f"Arquivos selecionados para modo {estado['modo']}")
        page.snack_bar = ft.SnackBar(ft.Text("Processando... Aguarde."), open=True)
        page.update()

        if estado["modo"] == "MASSA":
            sucesso, msg = processar_holerite_unico(e.files[0].path, estado["operacao"])
        else:
            caminhos = [f.path for f in e.files]
            sucesso, msg = processar_holerites_unitarios(caminhos, estado["operacao"])
        
        if sucesso:
            page.snack_bar = ft.SnackBar(ft.Text("✅ Sucesso! Verifique a pasta Downloads."), bgcolor="green", open=True)
        else:
            page.snack_bar = ft.SnackBar(ft.Text(f"❌ Erro: {msg}"), bgcolor="red", open=True)
        page.update()

    # REGISTRO DO FILE PICKER: Criamos e adicionamos à página imediatamente
    file_picker = ft.FilePicker()
    file_picker.on_result = ao_selecionar_arquivos
    page.overlay.append(file_picker)
    page.update() # Força o Windows a reconhecer o FilePicker logo na abertura

    container_principal = ft.Container()

    def mostrar_menu_modos(e=None):
        container_principal.content = ft.Column([
            ft.Text("Escolha a ferramenta:", size=20, weight="bold"),
            ft.ElevatedButton("PDF ÚNICO EM MASSA", width=350, height=80, on_click=lambda _: ir_para_operacoes("MASSA")),
            ft.ElevatedButton("VÁRIOS PDFs INDIVIDUAIS", width=350, height=80, on_click=lambda _: ir_para_operacoes("UNITARIO")),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        page.update()

    def ir_para_operacoes(modo):
        estado["modo"] = modo
        cor = ft.colors.BLUE_800 if modo == "MASSA" else ft.colors.DEEP_ORANGE_700
        container_principal.content = ft.Column([
            ft.Text(f"MODO: {modo}", size=12, weight="bold", color=cor),
            ft.ElevatedButton("DHL ITUPEVA", width=300, height=60, bgcolor=cor, color="white", on_click=lambda _: disparar_picker("ITUPEVA")),
            ft.ElevatedButton("DHL CABREÚVA", width=300, height=60, bgcolor=cor, color="white", on_click=lambda _: disparar_picker("CABREUVA")),
            ft.ElevatedButton("DHL EMBU DAS ARTES", width=300, height=60, bgcolor=cor, color="white", on_click=lambda _: disparar_picker("EMBU")),
            ft.TextButton("← Voltar", on_click=mostrar_menu_modos)
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        page.update()

    def disparar_picker(op):
        estado["operacao"] = op
        logging.info(f"Abrindo seletor para operação: {op}")
        file_picker.pick_files(
            allow_multiple=(estado["modo"] == "UNITARIO"), 
            allowed_extensions=["pdf"]
        )

    page.add(
        ft.Text("Nexus/DHL - Holerites", size=26, weight="bold"), 
        ft.Divider(height=20), 
        container_principal
    )
    mostrar_menu_modos()

if __name__ == "__main__":
    try:
        ft.app(target=main)
    except Exception as e:
        logging.critical(f"ERRO FATAL NO MOTOR VISUAL: {e}")

