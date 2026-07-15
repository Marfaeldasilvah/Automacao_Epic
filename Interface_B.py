import os

import customtkinter as ctk
import threading
import importlib
from PIL import Image

class InterfaceBot(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title('Garo RefreshShop')
        self.geometry('500x550')
        self.resizable(False,False)

        #caminho pasta img
        diretorio_atual = os.path.dirname(os.path.abspath(__file__))
        self.pasta_imagens = os.path.join(diretorio_atual, 'moedas_img')

        #Titulo
        self.titulo = ctk.CTkLabel(self, text='Garo RefreshShop', font=ctk.CTkFont(size=20, weight='bold'))
        self.titulo.pack(pady=20)

        # --- SEÇÃO: ESCOLHA DE ITENS ---
        self.label_itens = ctk.CTkLabel(self, text="Escolha os itens para comprar:", font=ctk.CTkFont(weight="bold"))
        self.label_itens.pack(pady=10)

        # Container (Frame) para organizar os itens verticalmente com suas imagens
        self.frame_itens = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_itens.pack(pady=10, padx=50, fill="x")

        # 1. ITEM: Moeda da Amizade
        self.check_moeda = ctk.CTkCheckBox(self.frame_itens, text="")  # Sem texto no checkbox
        self.check_moeda.select()
        self.check_moeda.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.exibir_imagem_e_texto(row=0, img_nome="amizad_moeda.png", texto="Moeda da Amizade")

        # 2. ITEM: Mist Loja
        self.check_mist = ctk.CTkCheckBox(self.frame_itens, text="")
        self.check_mist.select()
        self.check_mist.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.exibir_imagem_e_texto(row=1, img_nome="mist_loja.png", texto="Mist Loja")

        # 3. ITEM: Book Loja
        self.check_book = ctk.CTkCheckBox(self.frame_itens, text="")
        self.check_book.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.exibir_imagem_e_texto(row=2, img_nome="book_loja.png", texto="Book Loja")

        # --- SELEÇÃO DE VELOCIDADE ---
        self.label_vel = ctk.CTkLabel(self, text="Velocidade do Bot:", font=ctk.CTkFont(weight="bold"))
        self.label_vel.pack(pady=15)

        self.menu_velocidade = ctk.CTkComboBox(self, values=["Rápido (0.5x delay)", "Normal (1.0x delay)",
                                                             "Lento (1.5x delay)"])
        self.menu_velocidade.set("Normal (1.0x delay)")
        self.menu_velocidade.pack(pady=5)

        # --- BOTÃO INICIAR ---
        self.btn_iniciar = ctk.CTkButton(self, text="LIGAR BOT", fg_color="green", hover_color="darkgreen",
                                         command=self.coletar_e_iniciar)
        self.btn_iniciar.pack(pady=40, fill="x", padx=60)

    def exibir_imagem_e_texto(self, row, img_nome, texto):
        """Função auxiliar para carregar a imagem e alinhar na tela."""
        caminho_img = os.path.join(self.pasta_imagens, img_nome)

        # Se a imagem existir, carrega e exibe
        if os.path.exists(caminho_img):
            # Abre a imagem usando a biblioteca PIL e define o tamanho visual (32x32 pixels)
            pil_img = Image.open(caminho_img)
            ctk_img = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=(32, 32))

            # Label para conter apenas a imagem
            lbl_img = ctk.CTkLabel(self.frame_itens, image=ctk_img, text="")
            lbl_img.grid(row=row, column=1, padx=5, sticky="w")
        else:
            # Caso o print não exista na pasta, avisa na tela para não quebrar a interface
            lbl_img = ctk.CTkLabel(self.frame_itens, text="[Sem foto]", text_color="red")
            lbl_img.grid(row=row, column=1, padx=5, sticky="w")

        # Label para conter o texto descritivo do item
        lbl_texto = ctk.CTkLabel(self.frame_itens, text=texto, font=ctk.CTkFont(size=14))
        lbl_texto.grid(row=row, column=2, padx=10, sticky="w")

    def coletar_e_iniciar(self):
        # 1. Monta a lista baseado no que o usuário marcou
        lista_final = []
        if self.check_moeda.get(): lista_final.append('amizad_moeda.png')
        if self.check_mist.get(): lista_final.append('mist_loja.png')
        if self.check_book.get(): lista_final.append('book_loja.png')

        # 2. Descobre o multiplicador de velocidade
        vel = self.menu_velocidade.get()
        if "Rápido" in vel:
            multiplicador = 0.5
        elif "Lento" in vel:
            multiplicador = 1.5
        else:
            multiplicador = 1.0

        # Desativa o botão temporariamente
        self.btn_iniciar.configure(state="disabled", text="BOT RODANDO (ESC PARA PARAR)")

        # 3. Importa o Bot dinamicamente e inicia em segundo plano (Thread)
        # Importa aqui dentro para evitar problemas de importação circular importando na propria string
        bot_modulo = importlib.import_module("bot_taverna")
        instancia_bot = bot_modulo.BotTaverna(lista_final, multiplicador)

        thread = threading.Thread(target=instancia_bot.iniciar, daemon=True)
        thread.start()