import sys
import builtins
import ssl
import os
import platform

# Desativa a verificação de segurança SSL (bypass do firewall)
ssl._create_default_https_context = ssl._create_unverified_context
builtins.exit = sys.exit 

import flet as ft
import logging
from processador import processar_holerite_unico, processar_holerites_unitarios

# --- FORÇA O LOG A SER SALVO NA PASTA DOWNLOADS DELA ---
if platform.system() == "Windows":
    pasta_downloads = os.path.join(os.environ.get('USERPROFILE', ''), 'Downloads')
else:
    pasta_downloads = "Downloads"

caminho_log = os.path.join(pasta_downloads, "debug_log_holerites.txt")

logging.basicConfig(
    filename=caminho_log,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8",
    force=True # Força essa configuração ser a chefe de todos os arquivos
)

def main(page: ft.Page):
    logging.info("--- Iniciando Interface Nativa ---")
    page.title = "Nexus/DHL - Gerenciador de Holerites"
    page.window_width = 450
    page.window_height = 600
    page.theme_mode = ft.ThemeMode.LIGHT
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    estado = {"modo": None, "operacao": None}

    def ao_selecionar_arquivos(e):
        if not e.files: 
            logging.info("Seleção cancelada pelo usuário.")
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

    # Cria o FilePicker de forma correta e sem cortes
    file_picker = ft.FilePicker()
    file_picker.on_result = ao_selecionar_arquivos
    page.overlay.append(file_picker)
    page.update()

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
        logging.info(f"Disparando picker para {op}")
        file_picker.pick_files(allow_multiple=(estado["modo"] == "UNITARIO"), allowed_extensions=["pdf"])

    page.add(ft.Text("Nexus/DHL - Holerites", size=26, weight="bold"), ft.Divider(height=20), container_principal)
    mostrar_menu_modos()

if __name__ == "__main__":
    try:
        ft.app(target=main)
    except Exception as e:
        logging.critical(f"ERRO FATAL NO MOTOR VISUAL: {e}")

