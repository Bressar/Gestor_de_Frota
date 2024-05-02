"""
Main
Classe Gerenciador:
- Exibe os dados consultados nas janelas
Veiculos alugados
Veiculos disponíveis para aluguer
Veiculos com a data da revisão a expirar
Veiculos com a data da inspeção a expirar
Últimos clientes registados
Reservas do Mês
Veículos em Manutenção
Botão Exibir Veículos
Botão Agendar manutenção de veículos

28/03/2024 - last version
Douglas G. Bressar
"""
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import scrolledtext
from PIL import Image, ImageTk
import sqlite3
import csv
from openpyxl import Workbook
import os
import pandas as pd

from Veiculos import Janela_veiculos
from Clientes import Janela_clientes
from Reservas import Janela_reservas
from Pagamentos import Janela_pagamentos
from Metodos_dashboard import Dashboard


# Bancos de dados do projeto
class Gerenciador:
    db_clientes = 'database/clientes.db'
    db_veiculos = 'database/veiculos.db'
    db_reservas = 'database/reservas.db'
    db_pagamentos = 'database/pagamentos.db'


    def __init__(self, root):
        self.janela = root
        self.janela.title("Gerenciador de Frota")
        self.janela.resizable(0, 0)  # 1,0 ou True/False Define a janela como redimensionável ou não
        #self.janela.wm_iconbitmap('recursos/logo.ico')  # precisa da terminação do arquivo ".ico"
        # cores
        self.janela.geometry("1280x840")  # Define a geometria da janela
        self.cor1 = 'azure3' # fundo geral
        self.cor2 = 'azure2' # botões
        self.cor3 = 'white smoke' # campos de dados
        self.janela.config(bg=self.cor1)  # Define a cor de fundo da janela
        # Veiculos - instâncias"
        self.listar_veiculos = Janela_veiculos(root)
        self.registar_veiculos = Janela_veiculos(root)
        self.editar_veiculos = Janela_veiculos(root)
        self.remover_veiculos = Janela_veiculos(root)
        # Clientes - instâncias"
        self.listar_clientes = Janela_clientes(root)
        self.registar_clientes = Janela_clientes(root)
        self.editar_clientes = Janela_clientes(root)
        self.remover_clientes = Janela_clientes(root)
        # Reservas - instâncias"
        self.listar_reservas = Janela_reservas(root)
        self.registar_reservas = Janela_reservas(root)
        self.editar_reservas = Janela_reservas(root)
        self.remover_reservas = Janela_reservas(root)
        # Pagamentos - instâncias"
        self.listar_pagamentos = Janela_pagamentos(root)
        self.janela_registar_pagamentos = Janela_pagamentos(root)
        self.editar_pagamentos = Janela_pagamentos(root)
        self.remover_pagamentos = Janela_pagamentos(root)
        #Dashboard
        #self.manutencao = Dashboard(root) # está definido na chamada da função
        self.veiculos_alugados = Dashboard(root)
        self.veiculos_disponiveis = Dashboard(root)
        self.ultimos_clientes = Dashboard(root)
        self.revisao = Dashboard(root)
        self.inspecao = Dashboard(root)
        self.reservas_mes = Dashboard(root)
        self.exibir_manutencao = Dashboard(root)
        self.financeiro = Dashboard(root)
        #self.exibir_imagem = Dashboard(root) # está definido na chamada da função


        def contar_linhas_tabela(db_path, table_name): # função para a contagem de linhas nas tabelas
            try:
                with sqlite3.connect(db_path) as connection:
                    cursor = connection.cursor()
                    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                    num_linhas = cursor.fetchone()[0]
                return num_linhas
            except sqlite3.Error as e:
                print(f"Erro ao contar linhas da tabela {table_name}: {e}")
                return None
            # Exemplo de uso:
            #db_path = "caminho/do/banco/de/dados.db"
            #table_name = "nome_da_tabela"
            #quantidade_linhas = contar_linhas_tabela(db_path, table_name)

        #cabeçalho da app
        estilo_cabecalho = ("Verdana Bold", 10)
        label1 = ttk.Label(root, text="Luxury Wheels  -  Gestão de Aluguer de Veículos", font=estilo_cabecalho,
                           background=self.cor1)
        label1.place(x=20, y=10, width=760, height=25)
        # Obtém a largura do texto
        largura_texto_label1 = label1.winfo_reqwidth()
        # Calcula a diferença entre a largura da janela e a largura do texto
        largura_janela = 1280  # Largura fixa definida na geometria da janela
        diferenca = largura_janela - largura_texto_label1
        # Move o rótulo para centralizá-lo horizontalmente
        label1.place(x=diferenca // 2, y=15)

        # Menu lateral
        estilo_label_menu_lateral = ("Verdana Bold", 12)
        estilo_button_menu_lateral = ("Verdana", 8)
        # Veículos título
        label_veic = ttk.Label(root, text="Veículos", font=estilo_label_menu_lateral,background=self.cor1)
        label_veic.place(x=20,y=50, width=120, height=30)
        # botão listar veículos
        button_listar_veic = tk.Button(root, text="Listar Veículos", font=estilo_button_menu_lateral,
                                       background=self.cor2,
                                       command=self.abrir_janela_veiculos)
        button_listar_veic.place(x=20, y=80, width=120, height=30)
        #botão registar veiculos
        button_registar_veic = tk.Button(root, text="Registar", font=estilo_button_menu_lateral, background=self.cor2,
                                         command=self.abrir_registar_veiculos)
        button_registar_veic.place(x=20, y=110, width=120, height=30)
        # botão editar veiculos
        button_alterar_veic = tk.Button(root, text="Alterar", font=estilo_button_menu_lateral, background=self.cor2,
                                        command=self.abrir_editar_veiculos)
        button_alterar_veic.place(x=20, y=140, width=120, height=30)
        # botão remover veiculos
        button_remover_veic = tk.Button(root, text="Remover", font=estilo_button_menu_lateral, background=self.cor2,
                                        command=self.abrir_remover_veiculos)
        button_remover_veic.place(x=20, y=170, width=120, height=30)
        # Clientes título
        label_client = ttk.Label(root, text="Clientes", font=estilo_label_menu_lateral, background=self.cor1)
        label_client.place(x=20, y=220, width=120, height=30)
        # botão listar clientes
        button_listar_client = tk.Button(root, text="Listar Clientes", font=estilo_button_menu_lateral,
                                         background=self.cor2 ,
                                         command=self.abrir_janela_clientes)
        button_listar_client.place(x=20, y=250, width=120, height=30)
        # botão registar clientes
        button_registar_client = tk.Button(root, text="Registar", font=estilo_button_menu_lateral,
                                           background=self.cor2 ,
                                           command=self.abrir_registar_clientes)
        button_registar_client.place(x=20, y=280, width=120, height=30)
        # botão alterar clientes
        button_alterar_client = tk.Button(root, text="Alterar", font=estilo_button_menu_lateral,
                                          background=self.cor2,
                                          command=self.abrir_editar_clientes)
        button_alterar_client.place(x=20, y=310, width=120, height=30)
        # botão remover clientes
        button_remover_client = tk.Button(root, text="Remover", font=estilo_button_menu_lateral, background=self.cor2,
                                          command=self.abrir_remover_clientes)
        button_remover_client.place(x=20, y=340, width=120, height=30)
        # Reservas título
        label_reservas = ttk.Label(root, text="Reservas", font=estilo_label_menu_lateral, background=self.cor1)
        label_reservas.place(x=20, y=390, width=120, height=30)
        # botão listar reservas
        button_listar_reservas = tk.Button(root, text="Listar Reservas", font=estilo_button_menu_lateral,
                                           background=self.cor2,
                                           command=self.abrir_janela_reservas)
        button_listar_reservas.place(x=20, y=420, width=120, height=30)
        # botão registar reservas
        button_registar_reservas = tk.Button(root, text="Registar", font=estilo_button_menu_lateral,
                                             background=self.cor2,
                                             command=self.abrir_registar_reservas)
        button_registar_reservas.place(x=20, y=450, width=120, height=30)
        # botão alterar reservas
        button_alterar_reservas = tk.Button(root, text="Alterar", font=estilo_button_menu_lateral, background=self.cor2,
                                            command=self.abrir_editar_reservas)
        button_alterar_reservas.place(x=20, y=480, width=120, height=30)
        # botão remover reservas
        button_remover_reservas = tk.Button(root, text="Remover", font=estilo_button_menu_lateral, background=self.cor2,
                                            command=self.abrir_remover_reservas)
        button_remover_reservas.place(x=20, y=510, width=120, height=30)
        # Pagamentos
        label_pagamentos = ttk.Label(root, text="Pagamentos", font=estilo_label_menu_lateral, background=self.cor1)
        label_pagamentos.place(x=20, y=560, width=120, height=30)
        # botão listar pagamentos
        button_listar_pagamentos = tk.Button(root, text="Listar Pagamentos", font=estilo_button_menu_lateral,
                                             background=self.cor2,
                                             command=self.abrir_janela_pagamentos)
        button_listar_pagamentos.place(x=20, y=590, width=120, height=30)
        # botão Registar pagamentos # CORRIGIR!!!
        button_registar_pagamentos = tk.Button(root, text="Registar", font=estilo_button_menu_lateral,
                                               background=self.cor2,
                                                command=self.abrir_registar_pagamentos)
        button_registar_pagamentos.place(x=20, y=620, width=120, height=30)
        # botão Alterar pagamentos
        button_alterar_pagamentos = tk.Button(root, text="Alterar", font=estilo_button_menu_lateral,
                                              background=self.cor2,
                                              command=self.abrir_editar_pagamentos)
        button_alterar_pagamentos.place(x=20, y=650, width=120, height=30)
        # botão remover pagamentos
        button_remover_pagamentos = tk.Button(root, text="Remover", font=estilo_button_menu_lateral,
                                              background=self.cor2,
                                              command=self.abrir_remover_pagamentos)
        button_remover_pagamentos.place(x=20, y=680, width=120, height=30)
        # Botão deixar veiculo em manutenção
        estilo_button_manutencao= ("Verdana Bold", 8)
        button_manutencao = tk.Button(root, text="Agendar\nManutenção\nde Veículo!", font=estilo_button_manutencao,
                                      background='azure4', foreground="white",
                                      command=self.abrir_manutencao)
        button_manutencao.place(x=20, y=730, width=120, height=50)
        # Botão exibir Veículo
        button_exibir_veiculo = tk.Button(root, text="Exibir Veículo", font=estilo_button_manutencao,
                                          background=self.cor2,
                                      command=self.exibir_imagem)
        button_exibir_veiculo.place(x=20, y=800, width=120, height=30)


        # Quadros do Dashboard - apresentação de listas:
        estilo_label_Titulos_quadros = ("Verdana Bold", 10) # estilo de texto

        # Veículos alugados
        resultado_alugados = self.veiculos_alugados.veiculos_alugados() # variável recebe a função veiculos_alugados()
        # Contagem do número de alugados
        alugados_path = "database/alugados.db"
        table_alugados = "alugado"
        quant_veiculos_alugados = contar_linhas_tabela(alugados_path, table_alugados)
        titulo_quant_veiculos_alugados = "Veículos Alugados -> Total: " + str(quant_veiculos_alugados)
        label_veiculos_alugados = ttk.Label(root, text=titulo_quant_veiculos_alugados,
                                            font=estilo_label_Titulos_quadros, background=self.cor1)
        label_veiculos_alugados.place(x=165, y=50, width=500, height=30)
        # Janela de Scroll
        veiculos_alugados_scrol = scrolledtext.ScrolledText(root, width=540, height=195, bg=self.cor3)
        veiculos_alugados_scrol.insert(tk.END, resultado_alugados)
        veiculos_alugados_scrol.pack(expand=True, fill='both')
        veiculos_alugados_scrol.place(x=165, y=80, width=540, height=195)

        # Veículos com data da próxima revisão
        resultado_revisao = self.revisao.revisao() # variável recebe a função revisao()
        # Contagem do número de veículos em revisão
        revisao_path = "database/revisoes.db"
        table_revisao = "revisao"
        quant_veiculos_revisao = contar_linhas_tabela(revisao_path, table_revisao)
        titulo_quant_veiculos_prox_rev = ("Veículos com data da próxima revisão -> Total: "
                                          + str(quant_veiculos_revisao))
        label_veiculos_prox_rev = ttk.Label(root, text=titulo_quant_veiculos_prox_rev,
                                            font=estilo_label_Titulos_quadros, background=self.cor1)
        label_veiculos_prox_rev.place(x=720, y=50, width=500, height=30)
        # Janela de Scroll
        veiculos_prox_rev_scrol = scrolledtext.ScrolledText(root, width=540, height=195, bg=self.cor3)
        veiculos_prox_rev_scrol .insert(tk.END, resultado_revisao) # inserção no Quadro
        veiculos_prox_rev_scrol.pack(expand=True, fill='both')
        veiculos_prox_rev_scrol.place(x=720, y=80, width=540, height=195)

        # Veículos disponíveis
        resultado_disponiveis = self.veiculos_disponiveis.veiculos_disponiveis()
        # Contagem do número de veículos disponíveis
        disponiveis_path = "database/disponiveis.db"
        table_disponiveis = "disponivel"
        quant_veiculos_disponiveis = contar_linhas_tabela(disponiveis_path, table_disponiveis)
        titulo_listbox_veic_disp = "Veículos Disponíveis -> Total: " + str(quant_veiculos_disponiveis)
        label_veiculos_disponiveis = ttk.Label(root, text=titulo_listbox_veic_disp,
                                               font=estilo_label_Titulos_quadros, background=self.cor1)
        label_veiculos_disponiveis.place(x=165, y=280, width=500, height=30)
        # Janela de Scroll
        label_veiculos_disponiveis_scrol = scrolledtext.ScrolledText(root, width=540, height=195, bg=self.cor3)
        label_veiculos_disponiveis_scrol.insert(tk.END, resultado_disponiveis)
        label_veiculos_disponiveis_scrol.pack(expand=True, fill='both')
        label_veiculos_disponiveis_scrol.place(x=165, y=310, width=540, height=195)

        # Veículos com data da próxima inspeção obrigatória
        resultado_inspecao = self.inspecao.inspecao()
        # Contagem do número de veículos para inspeção
        inspecao_path = "database/inspecoes.db"
        table_inspecao = "inspecao"
        quant_veic_insp = contar_linhas_tabela(inspecao_path, table_inspecao)
        titulo_veic_insp = ("Veículos com a próxima inspeção obrigatória a expirar -> Total: "
                            + str(quant_veic_insp))
        label_veiculos_insp = ttk.Label(root, text=titulo_veic_insp,
                                        font=estilo_label_Titulos_quadros, background=self.cor1)
        label_veiculos_insp.place(x=720, y=280, width=540, height=30)
        # Janela de Scroll
        label_veiculos_insp_scrol = scrolledtext.ScrolledText(root, width=540, height=195, bg=self.cor3)
        label_veiculos_insp_scrol.insert(tk.END, resultado_inspecao)
        label_veiculos_insp_scrol.pack(expand=True, fill='both')
        label_veiculos_insp_scrol.place(x=720, y=310, width=540, height=195)

        # Últimos Clientes Registados
        ultimos_clientes = self.ultimos_clientes.ultimos_clientes()
        # título
        titulo_clientes_regist = "Últimos Clientes Registados"
        label_ult_clientes_regist = ttk.Label(root, text=titulo_clientes_regist,
                                              font=estilo_label_Titulos_quadros, background=self.cor1)
        label_ult_clientes_regist.place(x=165, y=515, width=500, height=30)
        # Janela de Scroll
        label_ult_clientes_regist_scrol= scrolledtext.ScrolledText(root, width=540, height=195, bg=self.cor3)
        label_ult_clientes_regist_scrol.insert(tk.END, ultimos_clientes)# insere a função da classe Dashborad no "quadro"
        label_ult_clientes_regist_scrol.pack(expand=True, fill='both')
        label_ult_clientes_regist_scrol.place(x=165, y=545, width=540, height=195)

        # Reservas do Mês
        reservas_mes = self.reservas_mes.reservas_mes()
        # Contagem do número das reservas do mês
        reserva_mes_path = "database/reservas_mes.db"
        table_reserva_mes = "reserva_mes"
        quant_reserva_mes = contar_linhas_tabela(reserva_mes_path, table_reserva_mes)
        titulo_reserva_mes = "Reservas do Mês -> Total: " + str(quant_reserva_mes)
        label_reserva_mes = ttk.Label(root, text=titulo_reserva_mes, font=estilo_label_Titulos_quadros,
                                       background=self.cor1)
        label_reserva_mes.place(x=720, y=515, width=500, height=30)
        # Janela de Scroll
        label_reserva_mes_scrol = scrolledtext.ScrolledText(root, width=540, height=195, bg=self.cor3)
        label_reserva_mes_scrol.insert(tk.END, reservas_mes)
        label_reserva_mes_scrol.pack(expand=True, fill='both')
        label_reserva_mes_scrol.place(x=720, y=545, width=540, height=195)

        # Atenção! cinco dias até a manutenção
        exibir_manutencao = self.exibir_manutencao.exibir_manutencao()
        # Contagem do número de veículos em manutenção
        exibir_manutencao_path = "database/manutencao.db"
        table_exibir_manutencao = "manutencao_veiculos"
        quant_exibir_manutencao = contar_linhas_tabela(exibir_manutencao_path, table_exibir_manutencao)
        titulo_5_dias_manut = ("ATENÇÃO! Veículos em manutenção -> Total:  "
                               + str(quant_exibir_manutencao))
        label_5_dias_manut = ttk.Label(root, text=titulo_5_dias_manut, font=estilo_label_Titulos_quadros,
                                       background=self.cor1)
        label_5_dias_manut .place(x=165, y=750, width=530, height=30)
        # Janela de Scroll
        label_5_dias_manut_scrol = scrolledtext.ScrolledText(root, width=540, height=50, bg=self.cor3)
        label_5_dias_manut_scrol.insert(tk.END, exibir_manutencao)
        label_5_dias_manut_scrol.pack(expand=True, fill='both')
        label_5_dias_manut_scrol.place(x=165, y=780, width=540, height=50)

        # Total financeiro
        exibir_financeiro = self.financeiro.financeiro()
        # Soma dos pagamentos do mês
        titulo_total_financeiro = "TOTAL FINANCEIRO:  €" + str(exibir_financeiro)
        estilo_total_financeiro = ("Verdana Bold", 14)
        label_tot_financeiro = ttk.Label(root, text=titulo_total_financeiro,
                                         font= estilo_total_financeiro, background=self.cor1)
        label_tot_financeiro.place(x=820, y= 780, width=540, height=50)


    # Funções Botões/Veículos
    def abrir_janela_veiculos(self):
        self.listar_veiculos.janela_listar_veiculos("Listar Veículos")
    def abrir_registar_veiculos(self):
        self.registar_veiculos.janela_registar_veiculos("Registar Veículos")
    def abrir_editar_veiculos(self):
        # Cria uma nova instância da classe Janela_veiculos para editar veículos
        janela_editar_veiculos = Janela_veiculos(self.janela)  # Passando a janela principal como argumento
        # Chama o método janela_editar_veiculos para abrir a janela de edição de veículos
        janela_editar_veiculos.editar_veiculo("Alterar Veículo") # app
    def abrir_remover_veiculos(self):
        janela_remover_veiculos = Janela_veiculos(self.janela)
        janela_remover_veiculos.remover_veiculos("Remover Veículos")

    # Funções Botões/Clientes
    def abrir_janela_clientes(self):
        self.listar_clientes.janela_listar_clientes("Listar Clientes")
    def abrir_registar_clientes(self):
        self.registar_clientes.janela_registar_clientes("Registar Clientes")
    def abrir_editar_clientes(self):
        self.editar_clientes.janela_editar_cliente("Alterar Clientes")
    def abrir_remover_clientes(self):
        self.remover_clientes.janela_remover_clientes("Remover Clientes")

    # Funções Botões/Reservas
    def abrir_janela_reservas(self):
        self.listar_reservas.janela_listar_reservas("Listar Reservas")
    def abrir_registar_reservas(self):
        self.registar_reservas.janela_registar_reservas("Registar Reservas")
    def abrir_editar_reservas(self):
        self.editar_reservas.janela_editar_reservas("Alterar Reservas")
    def abrir_remover_reservas(self):
        self.remover_reservas.janela_remover_reservas("Remover Reservas")

    # Funções Botões/Pagamentos
    def abrir_janela_pagamentos(self):
       self.listar_pagamentos.janela_listar_pagamentos("Listar Pagamentos")
    def abrir_registar_pagamentos(self):
        self.janela_registar_pagamentos.janela_registar_pagamentos("Registar Pagamentos")
    def abrir_editar_pagamentos(self):
        self.editar_pagamentos.janela_editar_pagamentos("Alterar Pagamentos")
    def abrir_remover_pagamentos(self):
        self.remover_pagamentos.janela_remover_pagamentos("Remover Pagamentos")

    #Dashboard
    def abrir_manutencao(self):
        janela_manutencao = Dashboard(self.janela)
        janela_manutencao.manutencao("Manutenção")

    def exibir_manutencao(self):
        return self.exibir_manutencao.exibir_manutencao()

    def exibir_imagem(self):
        janela_imagem = Dashboard(self.janela)
        janela_imagem.imagem("Visualizar Veículo")

    def veiculos_alugados(self):
        return self.veiculos_alugados.veiculos_alugados()

    def veiculos_disponiveis(self):
        return self.veiculos_disponiveis.veiculos_disponiveis()

    def ultimos_clientes(self):
        return self.ultimos_clientes.ultimos_clientes()

    def revisao(self):
        return self.revisao.revisao()

    def inspecao(self):
        return self.inspecao.inspecao()

    def reservas_mes(self):
        return self.reservas_mes.reservas_mes()

    def financeiro(self):
        return self.financeiro.financeiro()


if __name__ == '__main__':
    root = tk.Tk()
    app = Gerenciador(root)
    root.mainloop()

