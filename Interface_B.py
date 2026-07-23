import os
import customtkinter as ctk
import threading
import importlib
from PIL import Image

ctk.set_appearance_mode('dark')


class InterfaceBot(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title('Garo RefreshShop')
        self.geometry('500x620')
        self.resizable(False, False)

        #Controle se o bot tá ativo

        self.bot_rodando = False
        self.instancia_bot = None #Referencia do bot PERGUNTA SOBRE

        # caminho pasta img
        diretorio_atual = os.path.dirname(os.path.abspath(__file__))
        self.pasta_imagens = os.path.join(diretorio_atual, 'moedas_img')

        self.contadores = {
            'amizad_moeda.png': 0,
            'mist_loja.png': 0,
            'book_loja.png': 0
        }

        # Dicionário para guardar as referências dos textos na tela que mostram os números
        self.labels_contadores = {}

        # Titulo
        self.titulo = ctk.CTkLabel(self, text='Garo RefreshShop', font=ctk.CTkFont(size=20, weight='bold'))
        self.titulo.pack(pady=10)

        # --- SEÇÃO: ESCOLHA DE ITENS ---
        self.label_itens = ctk.CTkLabel(self, text="Escolha os itens para comprar:", font=ctk.CTkFont(weight="bold"))
        self.label_itens.pack(pady=10)

        # Container (Frame) para organizar os itens verticalmente com suas imagens
        self.frame_itens = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_itens.pack(pady=10, padx=20, fill="x")  # margem ficou menor

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
        self.label_vel.pack(pady=5)

        self.menu_velocidade = ctk.CTkComboBox(self, values=["Rápido (0.7x delay)", "Normal (1.0x delay)",
                                                             "Lento (1.5x delay)"])
        self.menu_velocidade.set("Normal (1.0x delay)")
        self.menu_velocidade.pack(pady=5)

        # --- SEÇÃO: LIMITE DE GASTOS ---

        # Este frame usa pack para se posicionar na tela principal
        self.frame_limites = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_limites.pack(pady=10, padx=20, fill="x")

        # Todos os componentes internos agora usam .pack() para evitar o conflito de layout
        lbl_limite_sky = ctk.CTkLabel(
            self.frame_limites,
            text="Limite de Skystones para gastar (3 por Refresh):",
            font=ctk.CTkFont(weight="bold")
        )
        lbl_limite_sky.pack(pady=2, anchor="n")

        self.input_sky = ctk.CTkEntry(
            self.frame_limites,
            placeholder_text="Ex: 90",
            width=200,
            justify="center"
        )
        self.input_sky.pack(pady=4, anchor="n")

        self.lbl_sky_gastas = ctk.CTkLabel(
            self.frame_limites,
            text="Skystones gastas: 0",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="orange"
        )
        self.lbl_sky_gastas.pack(pady=2, anchor="n")

        # --- BOTÃO INICIAR/ PAUSAR ---
        self.btn_iniciar = ctk.CTkButton(self, text="LIGAR BOT", fg_color="green", hover_color="darkgreen",
                                         command=self.coletar_e_iniciar)
        self.btn_iniciar.pack(pady=25, fill="x", padx=60)

    def atualizar_sky_interface(self, total_gasto):
        """Atualiza o contador de Skystones gastas na tela de forma segura."""
        self.after(0, lambda: self.lbl_sky_gastas.configure(text=f"Skystones gastas: {total_gasto}"))

    def exibir_imagem_e_texto(self, row, img_nome, texto):
        """Função auxiliar para carregar a imagem e alinhar na tela com espaço garantido."""
        caminho_img = os.path.join(self.pasta_imagens, img_nome)

        # Distribuímos a largura das colunas de forma estrita para evitar cortes:
        self.frame_itens.grid_columnconfigure(0, minsize=40)  # Checkbox
        self.frame_itens.grid_columnconfigure(1, minsize=45)  # Imagem
        self.frame_itens.grid_columnconfigure(2, minsize=160)  # Nome do item
        self.frame_itens.grid_columnconfigure(3, minsize=120)  # Contador (garante espaço para todo o texto)

        # Se a imagem existir, carrega e exibe
        if os.path.exists(caminho_img):
            pil_img = Image.open(caminho_img)
            ctk_img = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=(32, 32))

            # Label da Imagem (Coluna 1)
            lbl_img = ctk.CTkLabel(self.frame_itens, image=ctk_img, text="")
            lbl_img.grid(row=row, column=1, padx=5, sticky="w")
        else:
            lbl_img = ctk.CTkLabel(self.frame_itens, text="[Sem foto]", text_color="red")
            lbl_img.grid(row=row, column=1, padx=5, sticky="w")

        # Label do Texto do Item (Coluna 2)
        lbl_texto = ctk.CTkLabel(self.frame_itens, text=texto, font=ctk.CTkFont(size=14))
        lbl_texto.grid(row=row, column=2, padx=5, sticky="w")

        # Label do Contador de compras (Coluna 3)
        lbl_contador = ctk.CTkLabel(
            self.frame_itens,
            text="Comprados: 0",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="cyan"
        )
        lbl_contador.grid(row=row, column=3, padx=5, sticky="w")

        # Guardamos a referência desse texto para podermos alterá-lo depois
        self.labels_contadores[img_nome] = lbl_contador

    def atualizar_contador_interface(self, img_nome):
        """Função que atualiza a contagem de forma segura na thread principal."""
        if img_nome in self.contadores:
            self.contadores[img_nome] += 1
            novo_total = self.contadores[img_nome]

            # O .after(0, ...) força a interface a atualizar o texto imediatamente sem travar
            self.after(0, lambda: self.labels_contadores[img_nome].configure(text=f"Comprados: {novo_total}"))

    def alternar_estado_bot(self):
        """"Alternar entre ligar e pausar"""
        if not self.bot_rodando:
            self.coletar_e_iniciar()
        else:
            self.parar_bot()

    def coletar_e_iniciar(self):
        lista_final = []
        if self.check_moeda.get(): lista_final.append('amizad_moeda.png')
        if self.check_mist.get(): lista_final.append('mist_loja.png')
        if self.check_book.get(): lista_final.append('book_loja.png')

        vel = self.menu_velocidade.get()
        if "Rápido" in vel:
            multiplicador = 0.7
        elif "Lento" in vel:
            multiplicador = 1.5
        else:
            multiplicador = 1.0

        valor_digitado = self.input_sky.get().strip()
        limite_sky = int(valor_digitado) if valor_digitado.isdigit() else 99999

        # Atualiza estado e visual do botão
        self.bot_rodando = True
        self.btn_iniciar.configure(text="PAUSAR BOT (ESC)", fg_color="red", hover_color="darkred")

        bot_modulo = importlib.import_module("bot_taverna")
        self.instancia_bot = bot_modulo.BotTaverna(lista_final, multiplicador, self, limite_sky)

        thread = threading.Thread(target=self.instancia_bot.iniciar, daemon=True)
        thread.start()

        # Inicia o monitoramento seguro da tecla ESC pela própria interface
        self.verificar_tecla_esc()

    def verificar_tecla_esc(self):
        """Monitora a tecla ESC de forma 100% integrada ao Tkinter sem travar threads."""
        import keyboard
        if self.bot_rodando:
            if keyboard.is_pressed('esc'):
                print("\n[TECLADO] ESC detectado pela interface!")
                self.parar_bot("Bot pausado via teclado (ESC)")
            else:
                # Checa a cada 100ms se o ESC foi pressionado
                self.after(100, self.verificar_tecla_esc)

    def parar_bot(self, mensagem="Bot pausado"):
        """Interrompe a flag e restaura totalmente o botão da interface."""
        self.bot_rodando = False

        if self.instancia_bot:
            self.instancia_bot.rodando = False  # Para o loop do bot

        # Força o botão a voltar ao estado ativo normal na cor verde
        self.btn_iniciar.configure(
            text="LIGAR BOT",
            fg_color="green",
            hover_color="darkgreen",
            state="normal",
            command=self.alternar_estado_bot
        )
        print(f"[STATUS] {mensagem}")

# ==== PONTO DE ENTRADA OFICIAL DO PROGRAMA ====
if __name__ == "__main__":
    app = InterfaceBot()
    app.mainloop()