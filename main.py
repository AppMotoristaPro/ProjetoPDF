import flet as ft
from processador import processar_holerite_unico, processar_holerites_unitarios

def main(page: ft.Page):
    page.title = "Central de Holerites - Nexus/DHL"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_width = 450
    page.window_height = 650
    page.padding = 30
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Variáveis para guardar a escolha do usuário
    estado = {"modo": None, "operacao": None}

    def processar_arquivos(e: ft.FilePickerResultEvent):
        # Se ela cancelar a seleção de arquivo, não faz nada
        if not e.files:
            return
        
        # Mostra um aviso de que está pensando
        page.snack_bar = ft.SnackBar(ft.Text("Processando arquivos... Aguarde!"), duration=2000, open=True)
        page.update()

        modo = estado["modo"]
        op = estado["operacao"]
        
        if modo == "MASSA":
            caminho = e.files[0].path
            sucesso, msg = processar_holerite_unico(caminho, op)
        else: # UNITARIO
            caminhos = [f.path for f in e.files]
            sucesso, msg = processar_holerites_unitarios(caminhos, op)
        
        # Resultado
        if sucesso:
            page.snack_bar = ft.SnackBar(ft.Text(f"✅ Concluído! Arquivos em: {msg}"), bgcolor="green", open=True)
        else:
            page.snack_bar = ft.SnackBar(ft.Text(f"❌ Erro: {msg}"), bgcolor="red", open=True)
        
        page.update()

    file_picker = ft.FilePicker(on_result=processar_arquivos)
    page.overlay.append(file_picker)

    # Criação do "Palco" onde os menus vão aparecer
    container_principal = ft.Container()

    # --- TELA 1: MENU PRINCIPAL ---
    def mostrar_menu_modos(e=None):
        btn_massa = ft.ElevatedButton(
            "PDF ÚNICO EM MASSA\n(Fatiar um arquivo grande)", 
            width=350, height=80, 
            bgcolor=ft.colors.BLUE_800, color="white",
            on_click=lambda _: ir_para_operacoes("MASSA")
        )
        btn_unitario = ft.ElevatedButton(
            "VÁRIOS PDFs INDIVIDUAIS\n(Renomear arquivos)", 
            width=350, height=80, 
            bgcolor=ft.colors.DEEP_ORANGE_700, color="white",
            on_click=lambda _: ir_para_operacoes("UNITARIO")
        )
        
        container_principal.content = ft.Column(
            [
                ft.Text("Escolha a ferramenta:", size=20, weight="bold", color="grey700"),
                ft.Divider(height=20, color="transparent"),
                btn_massa,
                ft.Divider(height=10, color="transparent"),
                btn_unitario
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
        page.update()

    # --- TELA 2: MENU DE OPERAÇÕES ---
    def ir_para_operacoes(modo):
        estado["modo"] = modo
        
        # Muda o título e a cor dos botões para ela não se confundir
        titulo_modo = "MÓDULO: FATIAR PDF ÚNICO" if modo == "MASSA" else "MÓDULO: RENOMEAR VÁRIOS PDFs"
        cor_tema = ft.colors.BLUE_800 if modo == "MASSA" else ft.colors.DEEP_ORANGE_700
        
        btn_itupeva = ft.ElevatedButton("DHL ITUPEVA", width=300, height=60, bgcolor=cor_tema, color="white", on_click=lambda _: disparar_picker("ITUPEVA"))
        btn_cabreuva = ft.ElevatedButton("DHL CABREÚVA", width=300, height=60, bgcolor=cor_tema, color="white", on_click=lambda _: disparar_picker("CABREUVA"))
        btn_embu = ft.ElevatedButton("DHL EMBU DAS ARTES", width=300, height=60, bgcolor=cor_tema, color="white", on_click=lambda _: disparar_picker("EMBU"))
        btn_voltar = ft.TextButton("← Voltar ao Menu Principal", on_click=mostrar_menu_modos)

        container_principal.content = ft.Column(
            [
                ft.Text(titulo_modo, size=14, color=cor_tema, weight="bold"),
                ft.Text("Selecione a Operação", size=22, weight="bold"),
                ft.Divider(height=10, color="transparent"),
                btn_itupeva,
                btn_cabreuva,
                btn_embu,
                ft.Divider(height=20, color="transparent"),
                btn_voltar
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
        page.update()

    # Dispara a janela do Windows para selecionar os arquivos
    def disparar_picker(op):
        estado["operacao"] = op
        if estado["modo"] == "MASSA":
            file_picker.pick_files(allow_multiple=False, allowed_extensions=["pdf"])
        else: # UNITARIO
            file_picker.pick_files(allow_multiple=True, allowed_extensions=["pdf"])

    # Montagem da tela inicial fixa (Cabeçalho)
    cabecalho = ft.Text("Nexus/DHL - Holerites", size=28, weight="extrabold", color=ft.colors.BLUE_GREY_900)
    
    page.add(
        cabecalho,
        ft.Divider(height=30),
        container_principal
    )
    
    # Carrega a tela de entrada
    mostrar_menu_modos()

# Essa linha final cria o aplicativo em modo janela de Windows
ft.app(target=main)

