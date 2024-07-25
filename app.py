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

29/03/2024 - old version
26/05/2024 _ new Version
Douglas G. Bressar
"""
import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from customtkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import sqlite3
import csv
from openpyxl import Workbook
import os
import pandas as pd
from tkinter import scrolledtext
from customtkinter import CTkLabel
import json
from Veiculos import Janela_veiculos
from Clientes import Janela_clientes
from Reservas import Janela_reservas
from Pagamentos import Janela_pagamentos
from Metodos_dashboard import Dashboard

# Definição do tema e esquema de cores
ctk.set_appearance_mode("dark")  # Modo de aparência: "dark" ou "light"
ctk.set_default_color_theme("recursos/amarelo.json")
#ctk.set_default_color_theme("recursos/red.json")
#ctk.set_default_color_theme("blue")  # Tema de cores: "blue", "green", etc.

# Bancos de dados do projeto
class Gerenciador:
    db_clientes = 'database/clientes.db'
    db_veiculos = 'database/veiculos.db'
    db_reservas = 'database/reservas.db'
    db_pagamentos = 'database/pagamentos.db'

    def __init__(self, root):
        self.janela = root
        self.janela.title("Gerenciador de Frota")
        self.janela.geometry("1280x850")  # Define a geometria da janela
        self.janela.resizable(False, False)  # Define a janela como não redimensionável
        self.cor_fundo = "#2a2d2e"  # Fundo geral
        self.janela.configure(bg=self.cor_fundo)
        self.cor2 = 'azure2' # botões
        self.cor3 =  'gray'#'wheat4' #'teal' #'SkyBlue3' #'DarkOrange3'
        # self.cor3 = 'gray50' #'white smoke' # campos de dados

        # Veiculos - instâncias
        self.listar_veiculos = Janela_veiculos(root)
        self.registar_veiculos = Janela_veiculos(root)
        self.editar_veiculos = Janela_veiculos(root)
        self.remover_veiculos = Janela_veiculos(root)
        # Clientes - instâncias
        self.listar_clientes = Janela_clientes(root)
        self.registar_clientes = Janela_clientes(root)
        self.editar_clientes = Janela_clientes(root)
        self.remover_clientes = Janela_clientes(root)
        # Reservas - instâncias
        self.listar_reservas = Janela_reservas(root)
        self.registar_reservas = Janela_reservas(root)
        self.editar_reservas = Janela_reservas(root)
        self.remover_reservas = Janela_reservas(root)
        # Pagamentos - instâncias
        self.listar_pagamentos = Janela_pagamentos(root)
        self.janela_registar_pagamentos = Janela_pagamentos(root)
        self.editar_pagamentos = Janela_pagamentos(root)
        self.remover_pagamentos = Janela_pagamentos(root)
        # Dashboard
        self.veiculos_alugados = Dashboard(root)
        self.veiculos_disponiveis = Dashboard(root)
        self.ultimos_clientes = Dashboard(root)
        self.revisao = Dashboard(root)
        self.inspecao = Dashboard(root)
        self.reservas_mes = Dashboard(root)
        self.exibir_manutencao = Dashboard(root)
        self.financeiro = Dashboard(root)


        def contar_linhas_tabela(db_path, table_name):  # Função para a contagem de linhas nas tabelas
            try:
                with sqlite3.connect(db_path) as connection:
                    cursor = connection.cursor()
                    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                    num_linhas = cursor.fetchone()[0]
                return num_linhas
            except sqlite3.Error as e:
                print(f"Erro ao contar linhas da tabela {table_name}: {e}")
                return None


        # função para personalizar a cor do texto de saída... Gambiarra Master!
        def criar_label_personalizado(master, **kwargs):
            label = ctk.CTkLabel(master, **kwargs)
            label.configure(text_color="white")
            return label


        # Cabeçalho da app
        estilo_cabecalho = ctk.CTkFont(family="Verdana", size=16, weight="bold")
        label1 = ctk.CTkLabel(root, text="Luxury Wheels - Gestão de Aluguer de Veículos",
                              font=estilo_cabecalho, width=760, height=25)
        label1.place(relx=0.5, y=20, anchor="center")

        # Menu lateral
        estilo_label_menu_lateral = ctk.CTkFont(family="Verdana", size=13, weight="bold", )
        estilo_button_menu_lateral = ctk.CTkFont(family="Verdana", size=10, weight="bold")


        # Veículos título
        label_veic = ctk.CTkLabel(root, text="Veículos", font=estilo_label_menu_lateral, width=120, height=30)
        label_veic.place(x=20, y=50)

        # Botão listar veículos
        button_listar_veic = ctk.CTkButton(root, text="Listar Veículos", font=estilo_button_menu_lateral,
                                           width=120, height=28,
                                           command=self.abrir_janela_veiculos)
        button_listar_veic.place(x=20, y=80)
        #button_listar_veic.configure(border_width=1, border_color="white")  # Borda vermelha
        button_listar_veic.place(x=20, y=80)

        # Botão registar veículos
        button_registar_veic = ctk.CTkButton(root, text="Registar", font=estilo_button_menu_lateral,
                                             width=120, height=28,
                                             command=self.abrir_registar_veiculos)
        button_registar_veic.place(x=20, y=110)

        # Botão editar veículos
        button_alterar_veic = ctk.CTkButton(root, text="Alterar", font=estilo_button_menu_lateral, width=120, height=28,
                                            command=self.abrir_editar_veiculos)
        button_alterar_veic.place(x=20, y=140)

        # Botão remover veículos
        button_remover_veic = ctk.CTkButton(root, text="Remover", font=estilo_button_menu_lateral, width=120, height=28,
                                            command=self.abrir_remover_veiculos)
        button_remover_veic.place(x=20, y=170)


        # Clientes título
        label_client = ctk.CTkLabel(root, text="Clientes", font=estilo_label_menu_lateral, width=120, height=28)
        label_client.place(x=20, y=220)

        # Botão listar clientes
        button_listar_client = ctk.CTkButton(root, text="Listar Clientes", font=estilo_button_menu_lateral,
                                             width=120, height=28, command=self.abrir_janela_clientes)
        button_listar_client.place(x=20, y=250)

        # Botão registar clientes
        button_registar_client = ctk.CTkButton(root, text="Registar", font=estilo_button_menu_lateral,
                                               width=120, height=28,
                                               command=self.abrir_registar_clientes)
        button_registar_client.place(x=20, y=280)

        # Botão alterar clientes
        button_alterar_client = ctk.CTkButton(root, text="Alterar", font=estilo_button_menu_lateral,
                                              width=120, height=28,
                                              command=self.abrir_editar_clientes)
        button_alterar_client.place(x=20, y=310)

        # Botão remover clientes
        button_remover_client = ctk.CTkButton(root, text="Remover", font=estilo_button_menu_lateral,
                                              width=120, height=28,
                                              command=self.abrir_remover_clientes)
        button_remover_client.place(x=20, y=340)


        # Reservas título
        label_reservas = ctk.CTkLabel(root, text="Reservas", font=estilo_label_menu_lateral,
                                      width=120, height=28)
        label_reservas.place(x=20, y=390)

        # Botão listar reservas
        button_listar_reservas = ctk.CTkButton(root, text="Listar Reservas", font=estilo_button_menu_lateral,
                                               width=120, height=28,
                                               command=self.abrir_janela_reservas)
        button_listar_reservas.place(x=20, y=420)

        # Botão registar reservas
        button_registar_reservas = ctk.CTkButton(root, text="Registar", font=estilo_button_menu_lateral,
                                                 width=120, height=28,
                                                 command=self.abrir_registar_reservas)
        button_registar_reservas.place(x=20, y=450)

        # Botão alterar reservas
        button_alterar_reservas = ctk.CTkButton(root, text="Alterar", font=estilo_button_menu_lateral,
                                                width=120, height=28,
                                                command=self.abrir_editar_reservas)
        button_alterar_reservas.place(x=20, y=480)

        # Botão remover reservas
        button_remover_reservas = ctk.CTkButton(root, text="Remover", font=estilo_button_menu_lateral,
                                                width=120, height=28,
                                                command=self.abrir_remover_reservas)
        button_remover_reservas.place(x=20, y=510)


        # Pagamentos título
        label_pagamentos = ctk.CTkLabel(root, text="Pagamentos", font=estilo_label_menu_lateral,
                                        width=120, height=28)
        label_pagamentos.place(x=20, y=560)

        # Botão listar pagamentos
        button_listar_pagamentos = ctk.CTkButton(root, text="Listar Pagamentos", font=estilo_button_menu_lateral,
                                                 width=120, height=28,
                                                 command=self.abrir_janela_pagamentos)
        button_listar_pagamentos.place(x=20, y=590)

        # Botão registar pagamentos
        button_registar_pagamentos = ctk.CTkButton(root, text="Registar", font=estilo_button_menu_lateral,
                                                   width=120, height=28,
                                                   command=self.abrir_registar_pagamentos)
        button_registar_pagamentos.place(x=20, y=620)

        # Botão alterar pagamentos
        button_alterar_pagamentos = ctk.CTkButton(root, text="Alterar", font=estilo_button_menu_lateral,
                                                  width=120, height=28,
                                                  command=self.abrir_editar_pagamentos)
        button_alterar_pagamentos.place(x=20, y=650)

        # Botão remover pagamentos
        button_remover_pagamentos = ctk.CTkButton(root, text="Remover", font=estilo_button_menu_lateral,
                                                  width=120, height=28,
                                                  command=self.abrir_remover_pagamentos)
        button_remover_pagamentos.place(x=20, y=680)

        # Botão agendar manutenção de veículo
        estilo_button_manutencao = ctk.CTkFont(family="Verdana", size=10, weight="bold")
        button_manutencao = ctk.CTkButton(root, text="Agendar\nManutenção\nde Veículo!", font=estilo_button_manutencao,
                                          width=120, height=50,
                                          fg_color='firebrick3', text_color="white",
                                          command=self.abrir_manutencao) # fg_color='deep sky blue'
        button_manutencao.place(x=20, y=730)

        # Botão exibir veículo
        button_exibir_veiculo = ctk.CTkButton(root, text="Exibir Veículo", font=estilo_button_manutencao,
                                              width=120, height=30,
                                              command=self.exibir_imagem)
        button_exibir_veiculo.place(x=20, y=800)


        # Quadros do Dashboard - apresentação de listas:

        # Estilo das fontes dos topos dos framebox
        estilo_label_Titulos_quadros = ctk.CTkFont(family="Verdana", size=12, weight="bold")
        estilo_total_financeiro = ctk.CTkFont(family="Verdana", size=18, weight="bold")

        # Veículos alugados
        resultado_alugados = self.veiculos_alugados.veiculos_alugados()  # variável recebe a função veiculos_alugados()
        # Contagem do número de alugados
        alugados_path = "database/alugados.db"
        table_alugados = "alugado"
        quant_veiculos_alugados = contar_linhas_tabela(alugados_path, table_alugados)
        titulo_quant_veiculos_alugados = "Veículos Alugados -> Total: " + str(quant_veiculos_alugados)
        label_veiculos_alugados = ctk.CTkLabel(root, text=titulo_quant_veiculos_alugados,
                                            font=estilo_label_Titulos_quadros)
        # Definir a cor do texto para branco
        label_veiculos_alugados.configure(text_color="white")
        label_veiculos_alugados.place(x=165, y=50)

        # Janela de Scroll usando tkinter
        veiculos_alugados_scrol = scrolledtext.ScrolledText(root, width=540, height=195, bg=self.cor3)
        veiculos_alugados_scrol.insert(tk.END, resultado_alugados)
        veiculos_alugados_scrol.pack(expand=True, fill='both')
        veiculos_alugados_scrol.place(x=165, y=80, width=540, height=195)
        """
        # versão usando CTK - fica mais bonito + deixa o texto todo desalinhado... :(
        veiculos_alugados_scrol = CTkTextbox(root, width=540, height=195)
        veiculos_alugados_scrol.insert(INSERT, resultado_alugados)
        veiculos_alugados_scrol.pack(expand=True, fill='both')
        veiculos_alugados_scrol.place(x=165, y=80)
         """

        # Veículos com data da próxima revisão
        resultado_revisao = self.revisao.revisao()  # variável recebe a função revisao()
        # Contagem do número de veículos em revisão
        revisao_path = "database/revisoes.db"
        table_revisao = "revisao"
        quant_veiculos_revisao = contar_linhas_tabela(revisao_path, table_revisao)
        titulo_quant_veiculos_prox_rev = ("Veículos com data da próxima revisão -> Total: "
                                          + str(quant_veiculos_revisao))
        label_veiculos_prox_rev = ctk.CTkLabel(root, text=titulo_quant_veiculos_prox_rev,
                                            font=estilo_label_Titulos_quadros)
        label_veiculos_prox_rev.place(x=720, y=50)

        # Janela de Scroll
        veiculos_prox_rev_scrol = scrolledtext.ScrolledText(root, width=540, height=195, bg=self.cor3)
        veiculos_prox_rev_scrol.insert(tk.END, resultado_revisao)  # inserção no Quadro
        veiculos_prox_rev_scrol.pack(expand=True, fill='both')
        veiculos_prox_rev_scrol.place(x=720, y=80, width=540, height=195)

        # Veículos disponíveis
        resultado_disponiveis = self.veiculos_disponiveis.veiculos_disponiveis()
        # Contagem do número de veículos disponíveis
        disponiveis_path = "database/disponiveis.db"
        table_disponiveis = "disponivel"
        quant_veiculos_disponiveis = contar_linhas_tabela(disponiveis_path, table_disponiveis)
        titulo_listbox_veic_disp = "Veículos Disponíveis -> Total: " + str(quant_veiculos_disponiveis)
        label_veiculos_disponiveis = ctk.CTkLabel(root, text=titulo_listbox_veic_disp,
                                               font=estilo_label_Titulos_quadros)
        label_veiculos_disponiveis.place(x=165, y=280)

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
        label_veiculos_insp = ctk.CTkLabel(root, text=titulo_veic_insp,
                                        font=estilo_label_Titulos_quadros)
        label_veiculos_insp.place(x=720, y=280)

        # Janela de Scroll
        label_veiculos_insp_scrol = scrolledtext.ScrolledText(root, width=540, height=195, bg=self.cor3)
        label_veiculos_insp_scrol.insert(tk.END, resultado_inspecao)
        label_veiculos_insp_scrol.pack(expand=True, fill='both')
        label_veiculos_insp_scrol.place(x=720, y=310, width=540, height=195)

        # Últimos Clientes Registados
        ultimos_clientes = self.ultimos_clientes.ultimos_clientes()
        # título
        titulo_clientes_regist = "Últimos Clientes Registados"
        label_ult_clientes_regist = ctk.CTkLabel(root, text=titulo_clientes_regist,
                                              font=estilo_label_Titulos_quadros)
        label_ult_clientes_regist.place(x=165, y=515)

        # Janela de Scroll
        label_ult_clientes_regist_scrol = scrolledtext.ScrolledText(root, width=540, height=195, bg=self.cor3)
        label_ult_clientes_regist_scrol.insert(tk.END,
                                               ultimos_clientes)  # insere a função da classe Dashborad no "quadro"
        label_ult_clientes_regist_scrol.pack(expand=True, fill='both')
        label_ult_clientes_regist_scrol.place(x=165, y=545, width=540, height=195)

        # Reservas do Mês
        reservas_mes = self.reservas_mes.reservas_mes()
        # Contagem do número das reservas do mês
        reserva_mes_path = "database/reservas_mes.db"
        table_reserva_mes = "reserva_mes"
        quant_reserva_mes = contar_linhas_tabela(reserva_mes_path, table_reserva_mes)
        titulo_reserva_mes = "Reservas do Mês -> Total: " + str(quant_reserva_mes)
        label_reserva_mes = ctk.CTkLabel(root, text=titulo_reserva_mes, font=estilo_label_Titulos_quadros)
        label_reserva_mes.place(x=720, y=515)

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
        titulo_5_dias_manut = ("ATENÇÃO! Veículos em manutenção -> Total:  " + str(quant_exibir_manutencao))
        label_5_dias_manut = ctk.CTkLabel(root, text=titulo_5_dias_manut, font=estilo_label_Titulos_quadros)
        label_5_dias_manut.place(x=165, y=750)

        # Janela de Scroll
        label_5_dias_manut_scrol = scrolledtext.ScrolledText(root, width=540, height=50, bg=self.cor3)
        label_5_dias_manut_scrol.insert(tk.END, exibir_manutencao)
        label_5_dias_manut_scrol.pack(expand=True, fill='both')
        label_5_dias_manut_scrol.place(x=165, y=780, width=540, height=50)

        # Total financeiro
        exibir_financeiro = self.financeiro.financeiro()
        # Soma dos pagamentos do mês
        titulo_total_financeiro = "TOTAL FINANCEIRO:  €" + str(exibir_financeiro)
        label_tot_financeiro = ctk.CTkLabel(root, text=titulo_total_financeiro,
                                         font=estilo_total_financeiro)
        label_tot_financeiro.place(x=820, y=780,)

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


if __name__ == "__main__":
    root = ctk.CTk()
    app = Gerenciador(root)
    root.mainloop()
