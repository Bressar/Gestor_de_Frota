"""
Menu Flutuante - aberto a partir de app.py
Classe Janela clientes e seus metodos de:
Listar, Registar, Alterar e Remover
ps: no app.py está a estrutura completa do DashBoard
21/03/2024 - last version
Douglas Bressar
"""
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import scrolledtext
import sqlite3
import csv
from openpyxl import Workbook
import os
import pandas as pd
import customtkinter as ctk
from customtkinter import *
from datetime import datetime, timedelta

ctk.set_appearance_mode("dark")  # Modo de aparência: "dark" ou "light"
ctk.set_default_color_theme("recursos/amarelo.json")

class Janela_clientes:
    def __init__(self, root,):
        self.root = root
        self.db= "database/clientes.db" # acesso a base de dados
        self.cor1 = "#2a2d2e"   # fundo geral
        self.cor2 = '#FF8C00'  # botões Dark Orange
        self.cor3 = 'gray'  # campos de dados
        self.csv_path = "csv"
        self.excel_path = "excel"
        # Criar diretórios se não existirem
        os.makedirs(self.csv_path, exist_ok=True)
        os.makedirs(self.excel_path, exist_ok=True)


    def exportar_csv(self): # função para exportar em .csv
        con = sqlite3.connect(self.db) # conecta ao banco de dados
        cursor = con.cursor()
        query = "SELECT * FROM user" # Consulta SQL
        cursor.execute(query)
        dados = cursor.fetchall()
        con.close
        # caminho para criar o arquivo csv
        csv_file = os.path.join(self.csv_path, "clientes.csv")
        with open(csv_file, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file, delimiter=",")
            # Escrever o cabeçalho do arquivo CSV (nomes das colunas)
            writer.writerow(["ID", "Nome do Cliente", "Utilizador", "Password", "E-mail"])
            # Escrever os dados no arquivo CSV
            for linha in dados:
                writer.writerow(linha)


    def exportar_excel(self): # função para exportar em .csv
        con = sqlite3.connect(self.db) # conecta ao banco de dados
        cursor = con.cursor()
        query = "SELECT * FROM user" # Consulta pra selecionar a tabela
        cursor.execute(query)
        dados = cursor.fetchall()
        # Obtem nome das colunas
        colunas = [descricao[0] for descricao in cursor.description]
        con.close()
        wb = Workbook() # Cria novo arquivo xls
        ws = wb.active
        ws.append(colunas) # Adiciona os nomes de colunas
        for linha in dados:
            ws.append(linha)# Adiciona os dados da tabela ao arquivo xls
        excel_file = os.path.join(self.excel_path, "clientes.xlsx")# Salva o arquivo do Excel
        wb.save(excel_file)


    def listar_clientes(self):
        with sqlite3.connect(self.db) as con:
            query = "SELECT * FROM user"  # Consulta tabela no .db
            data_frame = pd.read_sql_query(query, con)  # cria o dataframe para ser lido com o pandas
            # Retorna a representação em string dos dados do DataFrame
            return(data_frame.to_string(index=False)) # exibe o dataframe sem a numeração do pandas


    def janela_listar_clientes(self, titulo):
        nova_janela = tk.Toplevel(self.root)# para abrir uma nova janela
        nova_janela.title(titulo) # Definindo o título da nova janela com o texto da solicitação
        nova_janela.geometry("650x500")  # Definindo o tamanho da nova janela -  Largura x Altura
        nova_janela.config(bg=self.cor1)
        # Título
        estilo_label_Titulos_quadros = ("Verdana Bold", 12)  # estilo de texto
        label_clientes_listados = ttk.Label(nova_janela, text="Clientes Listados", font=estilo_label_Titulos_quadros,
                                             background=self.cor1, foreground="white")
        label_clientes_listados.place(x=20, y=10, width=300, height=30)
        # Cria uma ScrolledText para exibir os dados
        clientes_listados_scrol = scrolledtext.ScrolledText(nova_janela, width=610, height=400, bg=self.cor3)
        clientes_listados_scrol.pack(expand=True, fill='both')
        clientes_listados_scrol.place(x=20, y=40, width=610, height=400)
        # Obtém os dados formatados e os exibe na ScrolledText
        clientes = self.listar_clientes()
        clientes_listados_scrol.insert(tk.END, clientes)
        clientes_listados_scrol.configure(state="disabled")
        # Botão "Exportar" com um menu suspenso (dropdown) contendo as opções de exportação para CSV e Excel
        button_export = tk.Menubutton(nova_janela, text="Exportar", font=("Verdana", 10),
                                      relief=tk.FLAT, bg=self.cor2)
        button_export.place(x = 515, y = 450, width = 100, height = 30)
        menu_export = tk.Menu(button_export, tearoff=0)
        button_export.config(menu=menu_export)
        menu_export.add_command(label="Exportar para CSV", command=self.exportar_csv)
        menu_export.add_command(label="Exportar para Excel", command=self.exportar_excel)


# Método inserir_cliente -> para inserir dados no banco de dados dos clientes
    def inserir_cliente(self, dados):
        with sqlite3.connect(self.db) as con:
            cursor = con.cursor()
            cursor.execute("""INSERT INTO user (nome, user, password, email)
                                    VALUES (?, ?, ?, ?)""", dados)
            con.commit()
            messagebox.showinfo("Cliente registado!")


# Método Registar clientes - Abre uma janela com diversos campos para registar um cliente em clientes.db
    def janela_registar_clientes(self, titulo):
        nova_janela = tk.Toplevel(self.root)
        nova_janela.title("Registar Cliente")
        nova_janela.geometry("400x230")
        nova_janela.config(bg=self.cor1)
        # Criar um widget com os campos para a edição
        estilo_label_Titulos_quadros = ("Verdana Bold", 12)
        label_clientes_registar = ttk.Label(nova_janela, text="Registar Clientes", font=estilo_label_Titulos_quadros,
                                            background=self.cor1, foreground="white")
        label_clientes_registar.place(x=20, y=10, width=200, height=30)

        # Campos de entrada para os dados do cliente
        etiquetas = ["Nome:", "Utilizador:", "Palavra-passe:", "E-mail:"]
        entrada_campos = {}  # Dicionário para armazenar os campos de entrada

        # Posicionar e criar campos de entrada para cada etiqueta
        for i, etiqueta in enumerate(etiquetas):
            label_etiqueta = ttk.Label(nova_janela, text=etiqueta, background=self.cor1, foreground="white")
            label_etiqueta.place(x=20, y=50 + 30 * i, width=150, height=25)
            entrada_campos[etiqueta] = tk.Entry(nova_janela)
            entrada_campos[etiqueta].place(x=180, y=50 + 30 * i, width=200, height=25)

        # Botão para inserir o veículo no banco de dados
        button_inserir = tk.Button(nova_janela, text="Inserir Cliente", command=lambda: self.inserir_cliente([
            entrada_campos["Nome:"].get(), entrada_campos["Utilizador:"].get(),
            entrada_campos["Palavra-passe:"].get(), entrada_campos["E-mail:"].get()
        ]), font=("Verdana", 10), relief=tk.FLAT, bg=self.cor2)
        button_inserir.place(x=260, y=180, width=120, height=30)


# Método Editar Clientes - Janela para editar o banco de dados dos clientes
    def janela_editar_cliente(self, titulo):
        nova_janela = tk.Toplevel(self.root)# abre nova janela
        nova_janela.title("Editar Cliente")
        nova_janela.geometry("400x270")
        nova_janela.config(bg=self.cor1)


        def buscar_cliente(): # Buscar e preencher os campos com os dados do cliente
            identificador = entrada_id.get()# Obtém o identificador do cliente a partir do campo de entrada
            # Busca o cliente no banco de dados
            with sqlite3.connect(self.db) as con:
                cursor = con.cursor()
                cursor.execute("SELECT * FROM user WHERE id = ?", (identificador,))
                cliente = cursor.fetchone()  # Retorna a primeira linha correspondente à consulta
                if cliente:
                    # Preenche os campos de entrada com os dados do cliente
                    for i, etiqueta in enumerate(etiquetas):
                        entrada_campos[etiqueta].delete(0, tk.END)
                        entrada_campos[etiqueta].insert(0, cliente[i])
                else:
                    # Define a mensagem de erro dentro do campo de busca
                    entrada_id.delete(0, tk.END)
                    entrada_id.insert(0, "Não encontrado!")
                    entrada_id.config(fg="red")

        def salvar_alteracoes(): # Função para salvar as alterações do cliente
            # Coleta os dados dos campos de entrada, excluindo o ID do cliente
            dados = [entrada_campos[etiqueta].get() for etiqueta in etiquetas if etiqueta != "ID:"]
            id_cliente = entrada_campos["ID:"].get() # Coleta o ID do cliente
            # Insere os dados no banco de dados
            with sqlite3.connect(self.db) as con:
                cursor = con.cursor()
                cursor.execute("""UPDATE user SET nome=?, user=?, password=?, email=? WHERE id=?""",
                               tuple(dados + [id_cliente])) # Adicionando o ID do clienteo à lista de dados
                con.commit()
                messagebox.showinfo("Alterações Guardadas!")
        # Título da Janela
        estilo_label_Titulos_quadros = ("Verdana Bold", 12)
        label_clientes_registar = ttk.Label(nova_janela, text="Editar Cliente", font=estilo_label_Titulos_quadros,
                                             background=self.cor1, foreground="white")
        label_clientes_registar.place(x=20, y=10, width=200, height=30)

        etiquetas = ["ID:", "Nome:", "Utilizador:", "Palavra-passe:", "E-mail:"]
        entrada_campos = {} # Dicionário para armazenar os campos de entrada

        for i, etiqueta in enumerate(etiquetas):# etiquetas dos campos a serem preenchidos
            label_etiqueta = ttk.Label(nova_janela, text=etiqueta, background=self.cor1, foreground="white")
            label_etiqueta.place(x=20, y=50 + 30 * i, width=150, height=25)
            entrada_campos[etiqueta] = tk.Entry(nova_janela)
            entrada_campos[etiqueta].place(x=180, y=50 + 30 * i, width=200, height=25)

        # Campo de entrada para o ID do veículo
        entrada_id = tk.Entry(nova_janela) # id que "vai" na busca!
        entrada_id.place(x=180, y=50, width=100, height=25)
        # Entrada do ID ao dicionário entrada_campos, sem isso não insere a id ao banco de dados
        entrada_campos["ID:"] = entrada_id

       # Botões para buscar e salvar alterações
        button_buscar = tk.Button(nova_janela, text="Buscar", command=buscar_cliente, font=("Verdana", 10),
                                  relief=tk.FLAT, bg=self.cor2)
        button_buscar.place(x=300, y=50, width=80, height=25)
        button_salvar = tk.Button(nova_janela, text="Guardar Alterações", command=salvar_alteracoes,
                                  font=("Verdana", 10), relief=tk.FLAT, bg=self.cor2)
        button_salvar.place(x=20, y=220, width=150, height=30)


# Método Remover Clientes - para excluir clientes de clientes.db
    def janela_remover_clientes(self, id_cliente):
        nova_janela = tk.Toplevel(self.root)
        nova_janela.title("Remover Cliente")
        nova_janela.geometry("400x240")
        nova_janela.config(bg=self.cor1)
        # Título da janela + listbox
        estilo_label_Titulos_quadros = ("Verdana Bold", 12)
        label_clientes_remover = ttk.Label(nova_janela, text="Remover Cliente", font=estilo_label_Titulos_quadros,
                                           background=self.cor1, foreground="white")
        label_clientes_remover.place(x=20, y=10, width=200, height=30)
        # Label do buscar ID
        label_id = ttk.Label(nova_janela, text="Insira o ID do cliente:", font=("Verdana", 10), background=self.cor1,
                             foreground="white")
        label_id.place(x=20, y=50, width=150, height=25)
        entrada_id = ttk.Entry(nova_janela)
        entrada_id.place(x=170, y=50, width=60, height=25)
        # Listbox para exibir as informações do veículo
        remover_clientes_listbox = tk.Listbox(nova_janela, width=360, height=100, bg=self.cor3)
        remover_clientes_listbox.place(x=20, y=90, width=360, height=100)


        def buscar_cliente(): # Função para buscar o cliente no banco de dados e exibir na listbox
            identificador = entrada_id.get()
            if identificador:  # Verifica se foi inserido um ID
                with sqlite3.connect(self.db) as con:
                    cursor = con.cursor()
                    # PRAGMA - (retorna uma lista de tuplas que contem diversas tuplas em que cada coluna é uma tupla)!
                    cursor.execute("PRAGMA table_info(user)")
                    colunas = [coluna[1] for coluna in cursor.fetchall()]  # Obtém os nomes das colunas
                    cursor.execute("SELECT * FROM user WHERE id = ?", (identificador,))
                    cliente = cursor.fetchone() # retorna só o id(n°)

                if cliente:
                    # Limpa a listbox
                    remover_clientes_listbox.delete(0, tk.END)
                    # Insere as informações do veículo (chave: valor)
                    for coluna, valor in zip(colunas, cliente):
                        remover_clientes_listbox.insert(tk.END, f"{coluna}: {valor}")
                else:
                    messagebox.showerror("Cliente não encontrado!")
            else:
                messagebox.showerror("Insira um ID para buscar!")

        # Botão para buscar o cliente
        button_buscar = tk.Button(nova_janela, text="Buscar", command=buscar_cliente, font=("Verdana", 10),
                                  relief=tk.FLAT, bg=self.cor2)
        button_buscar.place(x=300, y=50, width=80, height=25)


        def confirmar_exclusao(): # Função para confirmar a exclusão do veículo
            identificador = entrada_id.get()
            if identificador:  # Verifica se foi inserido um ID
                with sqlite3.connect(self.db) as con:
                    cursor = con.cursor()
                    cursor.execute("DELETE FROM user WHERE id = ?", (identificador,))
                    con.commit()
                messagebox.showinfo("Cliente excluído!")
            else:
                messagebox.showerror("Insira um ID para excluir!")
        # Botão para confirmar a exclusão do cliente
        button_remover = tk.Button(nova_janela, text="Remover", command=confirmar_exclusao, font=("Verdana", 10),
                                   relief=tk.FLAT, bg=self.cor2)
        button_remover.place(x=20, y=200, width=120, height=30)
