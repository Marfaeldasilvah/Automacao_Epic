import customtkinter as ctk
import threading
import importlib

class InterfaceBot(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title('Garo RefreshShop')
        self.geometry('500x500')
        self.resizable(False,False)

        #Titulo
        self.titulo = ctk.CTkLabel(self, text='Garo RefreshShop', font=ctk.CTkFont(size=20, weight='bold'))
        self.titulo.pack(pady=20)

        # --- CHECKBOXES DOS ITENS ---
        self.label_itens = ctk.CTkLabel(self, text="Escolha os itens para comprar:", font=ctk.CTkFont(weight="bold"))
        self.label_itens.pack(pady=5)

        self.check_moeda = ctk.CTkCheckBox(self, text="Moeda da Amizade")
        self.check_moeda.pack(pady=5)

        self.check_mist = ctk.CTkCheckBox(self, text="Mist Loja")
        self.check_mist.select()
        self.check_mist.pack(pady=5)

        self.check_book = ctk.CTkCheckBox(self, text="Book Loja")
        self.check_book.select()
        self.check_book.pack(pady=5)

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
        # Importa aqui dentro para evitar problemas de importação circular
        bot_modulo = importlib.import_module("bot_taverna")
        instancia_bot = bot_modulo.BotTaverna(lista_final, multiplicador)

        thread = threading.Thread(target=instancia_bot.iniciar, daemon=True)
        thread.start()