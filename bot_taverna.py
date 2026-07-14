import pydirectinput as pa
import pyautogui as pagui
import time
import keyboard
import os

import Interface_B

class BotTaverna:
 def __init__(self, itens_escolha, velocidade): #Construtor
  # Configurações iniciais
  pa.PAUSE = 0.05
  self.rodando = True

  self.itens_desejados = itens_escolha
  self.multi_tempo = velocidade

  # Registra o atalho para parar o bot imediatamente
  keyboard.add_hotkey("esc", self.parar_bot)

 def parar_bot(self):
  """Interrompe a execução do bot."""
  print("\nBOT INTERROMPIDO (ESC)!")
  os._exit(0)

 def abrir_loja(self):
  """Ação inicial que roda apenas uma vez para abrir a loja."""
  print("Abrindo a loja...")
  pa.click(x=84, y=474)
  time.sleep(0.5 * self.multi_tempo)
  pa.click(x=84, y=474)
  time.sleep(1 * self.multi_tempo)

 def scrollar_loja(self):
  """Realiza o movimento de clique, segura e arrasta para scrollar a tela."""
  pa.moveTo(1171, 758)
  pa.mouseDown()
  time.sleep(0.3)

  # Loop de arrasto do mouse
  for eixo_y in range(758, 300, -30):
    pa.moveTo(1171, eixo_y)
    time.sleep(0.03 * self.multi_tempo)

  time.sleep(0.5)
  pa.mouseUp()


 def resetar_loja(self):

  """Clica nos botões responsáveis por dar o refresh na loja."""

  pa.click(x=393, y=949)
  time.sleep(0.5 * self.multi_tempo)
  pa.click(x=1159, y=654)
  time.sleep(0.5 * self.multi_tempo)

 def identificar_item_e_comprar(self):

  diretorio_atual = os.path.dirname(os.path.abspath(__file__))
  comprou_algo = False

  try:
   for nome_foto in self.itens_desejados:
    caminho_da_imagem = os.path.join(diretorio_atual, 'moedas_img', nome_foto)

    if not os.path.exists(caminho_da_imagem):
     print(f"[ALERTA] Arquivo NÃO encontrado: {caminho_da_imagem} - Verifique o nome!")
     continue

    print(f"[SCAN] Procurando por: {nome_foto}...")

    try:
     posicao = pagui.locateCenterOnScreen(caminho_da_imagem, confidence=0.92)

     if posicao is not None:
      #Chamou a func comprar aqui
      self.comprar_item(posicao)
      comprou_algo = True
      time.sleep(0.5 * self.multi_tempo)

     else:
      print(f"O item nao esta na tela {nome_foto} ")

    except Exception as e:
     print(f"[ERRO SCAN INTERNO]: {e}")

  except Exception as e:
   print(f"[ERRO SCAN GLOBAL]: {e}")

  return comprou_algo

 def comprar_item(self, posicao):

  #clique comprar no garo
  ajuste = 40
  botao_comprar = 1673
  botao_y = int(posicao.y)

  confirmar_x = 1149
  confirmar_y = 725

  print(f"Item detectado")

  try:

   pa.moveTo(int(botao_comprar), int(botao_y + ajuste))
   time.sleep(0.4 * self.multi_tempo)
   
   pagui.click(x=1680, y=posicao.y + ajuste)
   time.sleep(0.3 * self.multi_tempo)
   pagui.click(x=1680, y=posicao.y + ajuste)
   time.sleep(0.3 * self.multi_tempo)

   #2 confirmacao
   pa.moveTo(int(confirmar_x), confirmar_y)
   time.sleep(0.5 * self.multi_tempo)
   pagui.click(x=confirmar_x, y=confirmar_y)
   time.sleep(0.5 * self.multi_tempo)

  except Exception as e:
   print(f"[ERRO COMPRA]: {e}")

 def iniciar(self):
  """Fluxo principal com travas de segurança para evitar paradas."""
  print("BOT INICIADO! VÁ PARA A TELA DO JOGO NA TAVERNA.")
  print("Pressione ESC para parar o BOT.")
  time.sleep(3)

  self.abrir_loja()

  while self.rodando:
   try:
    # --- LOOP DE VERIFICAÇÃO LIMPA (TOPO) ---
    tentativas_topo = 0
    while tentativas_topo < 1:  # Proteção extra: não deixa o bot travar no topo em loop infinito
     print(f"\n--- VARREDURA DA TELA (TOPO) - Tentativa {tentativas_topo + 1} ---")

     achou_algo_no_topo = self.identificar_item_e_comprar()

     if not achou_algo_no_topo:
      print("[TOPO LIMPO] Nenhum item desejado no topo. Prosseguindo...")
      break

     tentativas_topo += 1
     time.sleep(0.5)

    # --- ROLAR A PÁGINA ---
    self.scrollar_loja()
    time.sleep(0.3)

    print("\n--- VARREDURA DA TELA (FUNDO) ---")
    # Busca e compra o que ficou no fundo da página
    self.identificar_item_e_comprar()
    time.sleep(0.5)

    # Dá o refresh na taverna para gerar novos itens
    self.resetar_loja()
    time.sleep(1 * self.multi_tempo)  # Tempo para a loja carregar após o reset

   except Exception as e:
    print(f"[ALERTA CRÍTICO] O loop principal sofreu um erro, mas tentará continuar: {e}")
    time.sleep(2)
    # Removemos o "self.rodando = False" e o "break" daqui para o bot NUNCA fechar sozinho se algo falhar
    continue


# ==== PONTO DE ENTRADA DO SCRIPT ====
if __name__ == "__main__":
 # CORREÇÃO: Puxamos a classe 'InterfaceBot' de dentro do módulo importado 'Interface_B'
 app = Interface_B.InterfaceBot()

 # Iniciamos a interface gráfica (ela se encarregará de disparar o bot depois)
 app.mainloop()