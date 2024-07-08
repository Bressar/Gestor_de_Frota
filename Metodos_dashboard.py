"""
Métodos a serem utilizados a partir de app.py
Classe Dashbord:
- Exibe os dados consultados nas janelas de app.py
- Salva os dados consultados em bancos de dados

- Funções para exibir:
Veiculos alugados
Veiculos disponíveis para aluguer
Veiculos com a data da revisão a expirar
Veiculos com a data da inspeção a expirar
Últimos clientes registados
Reservas do Mês
Agendar manutenção de veículos
Veículos em Manutenção
Exibir Veículos

27/05/2024 - last version
Douglas G. Bressar
"""

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import sqlite3
import csv
from openpyxl import Workbook
import os
from datetime import datetime, timedelta
import pandas as pd
import customtkinter as ctk
from customtkinter import *

from Veiculos import Janela_veiculos
from Clientes import Janela_clientes
from Reservas import Janela_reservas
from Pagamentos import Janela_pagamentos

ctk.set_appearance_mode("dark")  # Modo de aparência: "dark" ou "light"
ctk.set_default_color_theme("recursos/amarelo.json")

class Dashboard:
    def __init__(self, root):
        self.root = root
        # acesso a database
        self.db_pagamentos = "database/pagamentos.db"
        self.db_reservas = "database/reservas.db"
        self.db_clientes = "database/clientes.db"
        self.db_veiculos = "database/veiculos.db"
        self.db_manutencao = "database/manutencao.db"
        self.db_alugados = "database/alugados.db"
        self.db_disponiveis = "database/disponiveis.db"
        self.db_revisoes = "database/revisoes.db"
        self.db_inspecoes = "database/inspecoes.db"
        self.db_reservas_mes = "database/reservas_mes.db"
        self.data_hoje = datetime.now()  # data de hoje como objeto datetime
        self.cor1 = "#2a2d2e"  #  fundo geral
        self.cor2 = '#FF8C00'  # botões Dark Orange
        self.cor3 = 'gray' # campos de dados


    def manutencao(self, titulo): # Função para inserir um veículo na tabela "manutenção"
        nova_janela = tk.Toplevel(self.root)
        nova_janela.title("Manutenção de Veículo")
        nova_janela.geometry("400x350")
        nova_janela.config(bg=self.cor1)
        # Título da janela + listbox
        estilo_label_manut = ("Verdana Bold", 10)
        label_manutencao = ttk.Label(nova_janela, text="Agendar Manutenção de Veículo", font=estilo_label_manut,
                                     background=self.cor1, foreground="white")
        label_manutencao.place(x=20, y=10, width=300, height=30)
        # Label do buscar ID
        label_id = ttk.Label(nova_janela, text="Insira o ID do veículo:", font=("Verdana", 10), background=self.cor1,
                             foreground="white")
        label_id.place(x=20, y=50, width=150, height=25)
        entrada_id = ttk.Entry(nova_janela)
        entrada_id.place(x=170, y=50, width=60, height=25)
        # Listbox para exibir as informações do veículo
        manut_veiculos_listbox = tk.Listbox(nova_janela, width=360, height=210, bg=self.cor3)
        manut_veiculos_listbox.place(x=20, y=90, width=360, height=210)

        def buscar_veiculo(): # Função para buscar o veículo no banco de dados e exibir na listbox
            identificador = entrada_id.get()
            if identificador:  # Verifica se foi inserido um ID
                with sqlite3.connect(self.db_veiculos) as con:
                    cursor = con.cursor()
                    # PRAGMA - (retorna uma lista de tuplas que contem diversas tuplas em que cada coluna é uma tupla)!
                    cursor.execute("PRAGMA table_info(veiculo)")
                    colunas = [coluna[1] for coluna in cursor.fetchall()]  # Obtém os nomes das colunas
                    cursor.execute("SELECT * FROM veiculo WHERE id = ?", (identificador,))
                    veiculo = cursor.fetchone() # retorna só o id(n°)

                if veiculo:
                    # Limpa a listbox
                    manut_veiculos_listbox.delete(0, tk.END)
                    # Insere as informações do veículo (chave: valor)
                    for coluna, valor in zip(colunas, veiculo):
                        manut_veiculos_listbox.insert(tk.END, f"{coluna}: {valor}")
                else:
                    messagebox.showerror("Erro", "Veículo não encontrado!")
            else:
                messagebox.showerror("Erro", "Insira um ID para buscar!")

        # Botão para buscar o veículo
        button_buscar = tk.Button(nova_janela, text="Buscar", command=buscar_veiculo, font=("Verdana", 10),
                                  relief=tk.FLAT, bg=self.cor2)
        button_buscar.place(x=300, y=50, width=80, height=25)

        def confirmar_manutencao(): # Função para confirmar a manutenção do veículo
            identificador = entrada_id.get()
            if identificador:  # Verifica se foi inserido um ID
                with sqlite3.connect(self.db_manutencao) as con:
                    cursor = con.cursor()
                    # Busca os dados do veículo na tabela de veículos
                with sqlite3.connect(self.db_veiculos) as con_veiculos:
                    cursor_veiculos = con_veiculos.cursor()
                    cursor_veiculos.execute("SELECT id, marca, modelo, categoria, tipo_veiculo, ultima_rev"
                                            " FROM veiculo WHERE id = ?", (identificador,))
                    veiculo = cursor_veiculos.fetchone()
                if veiculo:
                    # Insere os dados do veículo na tabela de manutenção
                    cursor.execute("""INSERT INTO manutencao_veiculos (id, marca, modelo, categoria,
                                        tipo_veiculo, ultima_rev) VALUES (?, ?, ?, ?, ?, ?)""", veiculo)
                    con.commit()
                    messagebox.showinfo("Veículo em manutenção!")
                else:
                    messagebox.showerror("Erro", "Veículo não encontrado!")
            else:
                messagebox.showerror("Erro", "Insira um ID válido!")
        # Botão para confirmar a manutenção do veículo
        button_manutencao = tk.Button(nova_janela, text="Confirmar Manutenção", command=confirmar_manutencao,
                                      font=("Verdana", 10),relief=tk.FLAT, bg=self.cor2)
        button_manutencao.place(x=20, y=310, width=200, height=30)


    def exibir_manutencao(self): # Lista de veiculos em manutenção
        with sqlite3.connect(self.db_manutencao) as con_manutencao:
            # Consultar os dados da tabela user
            query = "SELECT id, marca, modelo, categoria, tipo_veiculo, ultima_rev FROM manutencao_veiculos"
            data_frame = pd.read_sql_query(query, con_manutencao)
        # Retorna a representação em string dos dados do DataFrame
        #pd.set_option('display.max_columns', None)  # Para exibir todas as colunas
        #pd.set_option('display.width', None)  # Para permitir que o Pandas exiba dados sem truncamento
        return data_frame.to_string(index=False)  # Exibe o dataframe sem a numeração do pandas


    def veiculos_alugados(self): # lista de veículos alugados
        # Abrir conexão com o banco de dados de reservas
        with sqlite3.connect(self.db_reservas) as con_reservas:
            # Consultar os veículos alugados
            cursor_reservas = con_reservas.cursor()
            cursor_reservas.execute("SELECT veiculo_id FROM reserva")
            veiculos_alugados_ids = [row[0] for row in cursor_reservas.fetchall()]
        # Abrir conexão com o banco de dados de manutenção
        with sqlite3.connect(self.db_manutencao) as con_manutencao:
            # Consultar os veículos em manutenção
            cursor_manutencao = con_manutencao.cursor()
            cursor_manutencao.execute("SELECT id FROM manutencao_veiculos")
            veiculos_manutencao_ids = [row[0] for row in cursor_manutencao.fetchall()]
        # Abrir conexão com o banco de dados de veículos
        with sqlite3.connect(self.db_veiculos) as con_veiculos:
            # Consultar os veículos alugados que não estão em manutenção
            cursor_veiculos = con_veiculos.cursor()
            cursor_veiculos.execute(
                "SELECT id, marca, modelo, tipo_veiculo FROM veiculo "
                "WHERE id IN ({}) AND id NOT IN ({})".format(
                    ",".join(["?"] * len(veiculos_alugados_ids)),
                    ",".join(["?"] * len(veiculos_manutencao_ids))
                ), veiculos_alugados_ids + veiculos_manutencao_ids
            )
            veiculos_alugados = cursor_veiculos.fetchall()
        # salva os dados na tabela alugado em alugados.db - para ir atualizando sempre...
        with sqlite3.connect("database/alugados.db") as con_alugados:
            cursor_alugados = con_alugados.cursor()
            # Limpar a tabela antes de inserir novos dados
            cursor_alugados.execute("DELETE FROM alugado")
            cursor_alugados.execute(
                "CREATE TABLE IF NOT EXISTS alugado (id INT, marca TEXT, modelo TEXT, tipo_veiculo TEXT)")
            # Inserir apenas os dados que não estão presentes na tabela usando INSERT OR IGNORE
            cursor_alugados.executemany("INSERT OR IGNORE INTO alugado VALUES (?, ?, ?, ?)", veiculos_alugados)
        # Cria DataFrame pandas com os resultados para serem exibidos ba tela inicial do programa
        df_alugados = pd.DataFrame(veiculos_alugados, columns=["ID Veículo", "Marca", "Modelo", "Tipo de Veículo"])
        return (df_alugados.to_string(index=False))


    def veiculos_disponiveis(self): # lista de veículos que não estão alugados ou em manutenção
        # Consultar os IDs de veículos em reservas
        with sqlite3.connect(self.db_alugados) as con_alugados:
            cursor_alugados = con_alugados.cursor()
            cursor_alugados.execute("SELECT id FROM alugado")
            veiculos_alugados_ids = [row[0] for row in cursor_alugados.fetchall()]


        # Consultar os IDs de veículos em manutenção
        with sqlite3.connect(self.db_manutencao) as con_manutencao:
            cursor_manutencao = con_manutencao.cursor()
            cursor_manutencao.execute("SELECT id FROM manutencao_veiculos")
            veiculos_manutencao_ids = [row[0] for row in cursor_manutencao.fetchall()]
        # Abrir conexão com o banco de dados de veículos
        with sqlite3.connect(self.db_veiculos) as con_veiculos:
            # Consultar os detalhes dos veículos disponíveis que não estão alugados e não estão em manutenção
            cursor_veiculos = con_veiculos.cursor()
            cursor_veiculos.execute(
                "SELECT id, marca, modelo, tipo_veiculo FROM veiculo "
                "WHERE id NOT IN ({}) AND id NOT IN ({})".format(
                    ",".join(["?"] * len(veiculos_alugados_ids)),
                    ",".join(["?"] * len(veiculos_manutencao_ids))
                ), veiculos_alugados_ids + veiculos_manutencao_ids
            )
            veiculos_disponiveis = cursor_veiculos.fetchall()
        # salva os dados na tabela disponivel em disponiveis.db - para ir atualizando sempre...
        with sqlite3.connect("database/disponiveis.db") as con_disponiveis:
            cursor_disponiveis = con_disponiveis.cursor()
            # Limpar a tabela antes de inserir novos dados
            cursor_disponiveis.execute("DELETE FROM disponivel")
            cursor_disponiveis.execute(
                "CREATE TABLE IF NOT EXISTS disponivel (id INT, marca TEXT, modelo TEXT, tipo_veiculo TEXT)")
            # Inserir apenas os dados que não estão presentes na tabela usando INSERT OR IGNORE
            cursor_disponiveis.executemany("INSERT OR IGNORE INTO disponivel VALUES (?, ?, ?, ?)",
                                           veiculos_disponiveis)
        # Criar DataFrame pandas com os resultados
        df_disponiveis = pd.DataFrame(veiculos_disponiveis, columns=["ID Veículo", "Marca", "Modelo", "Tipo de Veículo"])
        return (df_disponiveis.to_string(index=False))  # index=False elimina o key do pandas


    def ultimos_clientes(self): # lista dos últimos clientes cadastrados
        with sqlite3.connect(self.db_clientes) as con_clientes:
            # Consultar os dados da tabela user
            query = "SELECT id, nome, email FROM user ORDER BY id DESC" # lista do último ao primeiro
            data_frame = pd.read_sql_query(query, con_clientes)
        # Retorna a representação em string dos dados do DataFrame
        return data_frame.to_string(index=False)  # Exibe o dataframe sem a numeração do pandas


    def revisao(self): # verifica se o veiculo e encontra proximo do przo de inpeção
        data_futura = (self.data_hoje + timedelta(days=15)).strftime("%Y-%m-%d")# filtro 1
        # Abrir conexão com o banco de dados de veiculos
        with sqlite3.connect(self.db_veiculos) as con_veiculo:
        # Consultar os veículos com revisão a expirar
            cursor_veiculo = con_veiculo.cursor()
        # faz a seleção de veiculos e aplica o filtro de data de hoje até 15 dias
            cursor_veiculo.execute("SELECT id, marca, modelo, tipo_veiculo, proxima_rev FROM veiculo "
                                   "WHERE proxima_rev BETWEEN ? AND ?", (self.data_hoje, data_futura))
            veiculos_revisao = cursor_veiculo.fetchall()
        # salva os dados na tabela revisoes em revisoes.db
        with sqlite3.connect("database/revisoes.db") as con_revisao:
            cursor_revisao = con_revisao.cursor()
            # Limpar a tabela antes de inserir novos dados
            cursor_revisao.execute("DELETE FROM revisao")
            cursor_revisao.execute(
            "CREATE TABLE IF NOT EXISTS revisao (id INT, marca TEXT, modelo TEXT, tipo_veiculo TEXT, proxima_rev TEXT)")
            # Inserir apenas os dados que não estão presentes na tabela usando INSERT OR IGNORE
            cursor_revisao.executemany("INSERT OR IGNORE INTO revisao VALUES (?, ?, ?, ?, ?)", veiculos_revisao)
        # Cria DataFrame pandas com os resultados para serem exibidos na tela inicial do programa
        df_revisados = pd.DataFrame(veiculos_revisao, columns=["ID Veículo", "Marca", "Modelo",
                                                               "Tipo de Veículo", "Próxima Revisão"])
        return (df_revisados.to_string(index=False))


    # nova versão de inspeção 28/03/2024
    def inspecao(self):
        # Abrir conexão com o banco de dados de veiculos
        with sqlite3.connect(self.db_veiculos) as con_veiculo:
            cursor_veiculo = con_veiculo.cursor()
            # Selecionar todas as datas de inspeção dos veículos
            cursor_veiculo.execute("SELECT id, marca, modelo, tipo_veiculo, ultima_insp FROM veiculo")
            datas_inspecao = cursor_veiculo.fetchall()
        veiculos_inspecao = []
        # Iterar sobre as datas de inspeção dos veículos
        for id_veiculo, marca, modelo, tipo_veiculo, data_inspecao_str in datas_inspecao:
            data_inspecao = datetime.strptime(data_inspecao_str, "%Y-%m-%d")
            data_limite = data_inspecao + timedelta(days=365)
            data_atual = datetime.now()
            # Verificar se a data de inspeção já expirou (mais de um ano atrás)
            if data_inspecao + timedelta(days=365) < data_atual:
                veiculos_inspecao.append((id_veiculo, marca, modelo, tipo_veiculo, data_inspecao_str))
            # Verificar se a data atual está entre 15 dias antes da próxima inspeção e a própria data de inspeção
            elif data_atual <= data_limite and data_atual >= data_limite - timedelta(days=15):
                veiculos_inspecao.append((id_veiculo, marca, modelo, tipo_veiculo, data_inspecao_str))
        # Salvar os dados na tabela inspecao em inspecoes.db
        with sqlite3.connect("database/inspecoes.db") as con_inspecao:
            cursor_inspecao = con_inspecao.cursor()
            # Limpar a tabela antes de inserir novos dados
            cursor_inspecao.execute("DELETE FROM inspecao")
            cursor_inspecao.execute(
                "CREATE TABLE IF NOT EXISTS inspecao (id INT, marca TEXT, modelo TEXT,"
                " tipo_veiculo TEXT, ultima_insp TEXT)")
            # Inserir apenas os dados que não estão presentes na tabela usando INSERT OR IGNORE
            cursor_inspecao.executemany("INSERT OR IGNORE INTO inspecao VALUES (?, ?, ?, ?, ?)",
                                        veiculos_inspecao)
        # Se houver veículos para inspeção
        if veiculos_inspecao:
            # Criar DataFrame pandas com os resultados para serem exibidos na tela inicial do programa
            df_inspecionados = pd.DataFrame(veiculos_inspecao,
                                            columns=["ID Veículo", "Marca", "Modelo", "Tipo de Veículo",
                                                     "Última Inspeção"])
            return df_inspecionados.to_string(index=False)
        else:
            return "Nenhum veículo para inspeção"


    def reservas_mes(self): # confere as reservas dos 30 dias correntes
        data_atual = self.data_hoje #data e hora atuais
        #Define o primeiro dia do mês atual, substituindo o dia atual pelo valor 1
        primeiro_dia_mes = data_atual.replace(day=1)
        #Calcula o último dia do mês atual. Ele primeiro vai para o primeiro dia do próximo mês
        # (data_atual.replace(day=1, month=data_atual.month+1)), em seguida,
        # subtrai um dia usando datetime.timedelta(days=1) para voltar para o último dia do mês atual.
        ultimo_dia_mes = data_atual.replace(day=1, month=data_atual.month+1) - timedelta(days=1)
        ultimo_dia_mes = data_atual.replace(day=1, month=data_atual.month + 1) - timedelta(days=1)
        # Abrir conexão com o banco de dados de reservas
        with sqlite3.connect(self.db_reservas) as con_reservas:
            # Consultar as reservas do mês atual e faz o filtro entre as datas
            cursor_reservas = con_reservas.cursor()
            cursor_reservas.execute("SELECT id, cliente_id, veiculo_id, data_inicio, data_fim FROM reserva "
                                    "WHERE data_inicio BETWEEN ? AND ? OR data_fim BETWEEN ? AND ?",
                                    (primeiro_dia_mes, ultimo_dia_mes, primeiro_dia_mes, ultimo_dia_mes))
            reservas_do_mes = cursor_reservas.fetchall()
        # salva os dados na tabela reserva_mes em reservas_mes.db
        with sqlite3.connect("database/reservas_mes.db") as con_mes:
            cursor_mes= con_mes.cursor()
            # Limpar a tabela antes de inserir novos dados
            cursor_mes.execute("DELETE FROM reserva_mes")
            cursor_mes.execute(
                "CREATE TABLE IF NOT EXISTS reserva_mes (id INT, cliente_id INT, veiculo_id INT,"
                " data_inicio TEXT, data_fim TEXT)")
            # Inserir apenas os dados que não estão presentes na tabela usando INSERT OR IGNORE
            cursor_mes.executemany("INSERT OR IGNORE INTO reserva_mes VALUES (?, ?, ?, ?, ?)", reservas_do_mes)
        # Cria DataFrame pandas com os resultados para serem exibidos ba tela inicial do programa
        df_reserva_mes = pd.DataFrame(reservas_do_mes, columns=["ID Reserva", "ID cliente", "ID veículo",
                                                                "Data Inicial", "Data Final"])
        return (df_reserva_mes.to_string(index=False))


    def financeiro(self): # calcula a soma dos pagamentos da tabela pagamentos
        # Abrir conexão com o banco de dados de pagamentos
        with sqlite3.connect(self.db_pagamentos) as con_pagamentos:
            # Consultar os valores da coluna "valor_€" da tabela "pagamento"
            cursor_pagamentos = con_pagamentos.cursor()
            cursor_pagamentos.execute("SELECT valor_€ FROM pagamento")
            # Extrair os valores da lista de tuplas retornada por fetchall()
            valores_pagamentos = [row[0] for row in cursor_pagamentos.fetchall()]
        # Calcular o total dos valores
        total_pagamentos = sum(valores_pagamentos)
        return total_pagamentos


    def imagem(self, title): # exibe os dados e imagem do veículo em uma janela
        nova_janela = tk.Toplevel(self.root)
        nova_janela.title("Visualizar Veículo")
        nova_janela.geometry("440x310")
        nova_janela.config(bg=self.cor1)
        # Título da janela + listbox
        estilo_label_Titulos_quadros = ("Verdana Bold", 12)
        label_visualizar_title = ttk.Label(nova_janela, text="Visualizar Veículo", font=estilo_label_Titulos_quadros,
                                           background=self.cor1, foreground="white")
        label_visualizar_title.place(x=20, y=10, width=200, height=30)
        # Label do buscar ID
        label_id = ttk.Label(nova_janela, text="Insira o ID do Veículo", font=("Verdana", 10),background=self.cor1,
                             foreground="white")
        label_id.place(x=20, y=50, width=190, height=25)
        entrada_id = ttk.Entry(nova_janela)
        entrada_id.place(x=170, y=50, width=20, height=25)
        # Listbox para exibir as informações do veículo
        remover_veiculos_listbox = tk.Listbox(nova_janela, width=170, height=200, bg=self.cor3)
        remover_veiculos_listbox.place(x=20, y=90, width=170, height=200)

        def buscar_veiculo(): # Função para buscar o veiculo no banco de dados e exibir na listbox
            identificador = entrada_id.get()
            if identificador:  # Verifica se foi inserido um ID
                with sqlite3.connect(self.db_veiculos) as con:
                    cursor = con.cursor()
                    # PRAGMA - (retorna uma lista de tuplas que contem diversas tuplas em que cada coluna é uma tupla)!
                    cursor.execute("PRAGMA table_info(veiculo)")  # em tabela veiculo
                    colunas = [coluna[1] for coluna in cursor.fetchall()]  # Obtém os nomes das colunas
                    cursor.execute("SELECT * FROM veiculo WHERE id = ?", (identificador,))
                    veiculo = cursor.fetchone()  # retorna só o id(n°)
                if veiculo:
                    # Limpa a listbox
                    remover_veiculos_listbox.delete(0, tk.END)
                    # Insere as informações do veiculo (chave: valor)
                    for coluna, valor in zip(colunas, veiculo):
                        remover_veiculos_listbox.insert(tk.END, f"{coluna}: {valor}")

                    # Exibir a imagem do veículo
                    # Caminho para o folder e a coluna imagem na tabela veiculo
                    imagem_path = os.path.join("imagens", veiculo[7])  # nome/imagem no "7" a contar de "0" na tabela
                    if os.path.exists(imagem_path):
                        img = Image.open(imagem_path)
                        img = ImageTk.PhotoImage(img)
                        # Criando um frame para a imagem
                        frame_imagem = tk.Frame(nova_janela, bd=0, relief=tk.FLAT)
                        frame_imagem.place(x=200, y=90, width=224, height=132)
                        # Exibindo a imagem dentro do frame
                        imagem_carro = tk.Label(frame_imagem, image=img)
                        imagem_carro.image = img
                        imagem_carro.pack(padx=1, pady=1)
                    # imagem_carro.place(x=200, y=90, width=220, height=128)
                    else:
                        messagebox.showerror("Erro", "Imagem não encontrada.")
                else:
                    messagebox.showerror("Erro", "Veículo não encontrado.")
            else:
                messagebox.showerror("Erro", "Insira um ID para buscar.")
        # Botão para buscar o cliente
        button_buscar = tk.Button(nova_janela, text="Buscar", command=buscar_veiculo, font=("Verdana", 10),
                                  relief=tk.FLAT, bg=self.cor2)
        button_buscar.place(x=340, y=50, width=80, height=25)

