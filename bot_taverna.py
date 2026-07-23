import pydirectinput as pa
import pyautogui as pagui
import time
import keyboard
import os

class BotTaverna:
 def __init__(self, itens_escolha, velocidade, interface_app, limite_sky):
  pa.PAUSE = 0.05
  self.rodando = True

  self.itens_desejados = itens_escolha
  self.multi_tempo = velocidade
  self.interface_app = interface_app

  self.limite_sky = limite_sky
  self.sky_gasto = 0

  # REGISTRO: Guarda os itens comprados na rodada atual da loja
  self.comprados_na_rodada = set()

 def verificar_limites_gastos(self):
  """Para o bot caso o limite de Skystones estipulado seja atingido."""
  if self.sky_gasto >= self.limite_sky:
   print(f"\n[⚠️ PARADA AUTOMÁTICA] Limite de Skystones atingido! Gasto: {self.sky_gasto} / {self.limite_sky}")
   self.rodando = False
   if self.interface_app is not None:
    self.interface_app.after(0, self.interface_app.parar_bot("Meta de skystones atingida."))
   return False
  return True

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
  """Clica nos botões responsáveis por dar o refresh na loja e contabiliza o gasto."""
  pa.click(x=393, y=949)
  time.sleep(0.5 * self.multi_tempo)
  pa.click(x=1159, y=654)
  time.sleep(0.5 * self.multi_tempo)

  # Limpa os itens registrados para a próxima loja
  self.comprados_na_rodada.clear()

  # Contabiliza o custo do refresh (3 Skystones)
  self.sky_gasto += 3
  print(f"[CONTA] Skystones gastas nesta sessão: {self.sky_gasto} / {self.limite_sky}")

  # Envia o valor atualizado para o componente da interface gráfica
  if self.interface_app is not None:
   try:
    self.interface_app.atualizar_sky_interface(self.sky_gasto)
   except Exception as e:
    print(f"[FALHA AO ATUALIZAR TEXTO]: {e}")

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

    # Tentativa de escaneamento com PyAutoGUI
    posicao = None
    try:
     posicao = pagui.locateCenterOnScreen(caminho_da_imagem, confidence=0.92)
    except Exception:
     posicao = None

    # Se encontramos o item, prossegue com a compra
    if posicao is not None:
     print(f"[DEBUG] Item encontrado {nome_foto}")
     self.comprar_item(posicao, nome_foto)
     comprou_algo = True
     time.sleep(0.5 * self.multi_tempo)
    else:
     print(f"O item nao esta na tela: {nome_foto}")

  except Exception as e:
   print(f"[ERRO SCAN GLOBAL]: {e}")

  return comprou_algo

 def comprar_item(self, posicao, nome_foto):
  ajuste = 40
  botao_comprar = 1673
  botao_y = int(posicao.y)

  confirmar_x = 1149
  confirmar_y = 725

  print(f"\n[SISTEMA DE COMPRA] Iniciando rotina para: {nome_foto}")

  try:
   # Movimentos e cliques físicos
   pa.moveTo(int(botao_comprar), int(botao_y + ajuste))
   time.sleep(0.4 * self.multi_tempo)

   print("[SISTEMA DE COMPRA] Efetuando primeiro clique de compra...")
   pagui.click(x=1680, y=posicao.y + ajuste)
   time.sleep(0.3 * self.multi_tempo)
   pagui.click(x=1680, y=posicao.y + ajuste)
   time.sleep(0.3 * self.multi_tempo)

   # 2ª confirmação
   print("[SISTEMA DE COMPRA] Movendo para botão confirmar...")
   pa.moveTo(int(confirmar_x), confirmar_y)
   time.sleep(0.5 * self.multi_tempo)
   pagui.click(x=confirmar_x, y=confirmar_y)
   time.sleep(0.5 * self.multi_tempo)

   # --- TRAVA DE DUPLICIDADE NO CONTADOR ---
   if nome_foto not in self.comprados_na_rodada:
    # Marca como já contado nesta loja
    self.comprados_na_rodada.add(nome_foto)

    if self.interface_app is not None:
     self.interface_app.atualizar_contador_interface(nome_foto)
     print(f"[CONTADOR] {nome_foto} contabilizado com sucesso!")
   else:
    print(f"[CONTADOR IGNORADO] {nome_foto} já foi comprado/contado nesta rodada da loja.")

  except Exception as e:
   print(f"[ERRO CRÍTICO NO PROCESSO DE COMPRA]: {e}")

 def iniciar(self):
  """Fluxo principal com travas de segurança para evitar paradas."""
  print("BOT INICIADO! VÁ PARA A TELA DO JOGO NA TAVERNA.\nPressione ESC para parar o BOT.")

  # Garante o registro do atalho a cada nova inicialização
  try:
      keyboard.add_hotkey("esc", self.parar_bot, suppress=False)
  except Exception:
      pass

  time.sleep(3)
  self.abrir_loja()

  while self.rodando:
   try:
    # Verificação de segurança de limite estipulado
    if not self.verificar_limites_gastos() or not self.rodando:
     break

    # --- LOOP DE VERIFICAÇÃO LIMPA (TOPO) ---
    tentativas_topo = 0
    while tentativas_topo < 1:
     print(f"\n--- VARREDURA DA TELA (TOPO) - Tentativa {tentativas_topo + 1} ---")

     time.sleep(0.6) # Delay estratégico para o PyAutoGUI reconhecer o topo estático

     achou_algo_no_topo = self.identificar_item_e_comprar()

     if not achou_algo_no_topo:
      print("[TOPO LIMPO] Nenhum item desejado no topo. Prosseguindo...")
      break

     tentativas_topo += 1
     time.sleep(0.5)

    # --- ROLAR A PÁGINA ---
    self.scrollar_loja()
    time.sleep(0.4) # Aguarda a tela parar de se mover após o scroll rápido

    print("\n--- VARREDURA DA TELA (FUNDO) ---")
    self.identificar_item_e_comprar()
    time.sleep(0.5)

    # Dá o refresh na taverna para gerar novos itens
    self.resetar_loja()
    time.sleep(0.8 * self.multi_tempo)

   except Exception as e:
    print(f"[ALERTA CRÍTICO] O loop principal sofreu um erro, mas tentará continuar: {e}")
    time.sleep(2)
    continue

# ==== PONTO DE ENTRADA DO SCRIPT ====
if __name__ == "__main__":
 import Interface_B
 # CORREÇÃO: Puxamos a classe 'InterfaceBot' de dentro do módulo importado 'Interface_B'
 app = Interface_B.InterfaceBot()
 # Iniciamos a interface gráfica (ela se encarregará de disparar o bot depois)
 app.mainloop()