"""
Menu Flutuante - aberto a partir de app.py
Classe Janela veiculos e seus metodos de:
Listar, Registar, Alterar e Remover
ps: no app.py está a estrutura completa do dasnhborad
21/03/2024 - old version
27/05/2024 - new version
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

class Janela_veiculos:
    def __init__(self, root,):
        self.root = root
        self.db= "database/veiculos.db" # var para aceder a base de dados
        self.cor1 = "#2a2d2e"  #  fundo geral
        self.cor2 = '#FF8C00'  # botões Dark Orange
        self.cor3 = 'gray'  # campos de dados
        self.csv_path = "csv" # caminho pro arquivo csv
        self.excel_path = "excel" # caminho pro arquivo xls
        # Cria diretórios
        os.makedirs(self.csv_path, exist_ok=True)
        os.makedirs(self.excel_path, exist_ok=True)

    # função para deixar 2 cores no botão, ao se usar o mouse...
    def mudar_cor(is_hovered):
        if is_hovered:
            button_export.config(background="#FF4500")  # Cor ao passar o mouse -> OrangeRed
        else:
            button_export.config(background=self.cor2)  # Cor normal


    def exportar_csv(self): # função para exportar em .csv
        con = sqlite3.connect(self.db) # conecta ao banco de dados
        cursor = con.cursor()
        query = "SELECT * FROM veiculo" # Consulta SQL
        cursor.execute(query)
        dados = cursor.fetchall()
        con.close
        # caminho para criar o arquivo csv
        csv_file = os.path.join(self.csv_path, "veiculos.csv")
        with open(csv_file, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file, delimiter=",")
            # Escrever o cabeçalho do arquivo CSV (nomes das colunas)
            writer.writerow(["ID", "Marca", "Modelo", "Categoria", "Transmissão", "Tipo de Veículo",
                             "Quant. Pessoas", "Nome da Imagem", "Valor da Diária", "Última Rev.",
                             "Próxima Rev.", "Última Insp"])
            # Escrever os dados no arquivo CSV
            for linha in dados:
                writer.writerow(linha)


    def exportar_excel(self): # função para exportar em .csv
        con = sqlite3.connect(self.db) # conecta ao banco de dados
        cursor = con.cursor()
        query = "SELECT * FROM veiculo" # Consulta pra selecionar a tabela
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
        excel_file = os.path.join(self.excel_path, "veiculos.xlsx")# Salva o arquivo do Excel
        wb.save(excel_file)


# Método listar veículos - janela de exibição Seleciona os principais dados para exibição   
    def listar_veiculos(self):
        with sqlite3.connect(self.db) as con:
            query = "SELECT * FROM veiculo"  # Consulta tabela no .db
            data_frame = pd.read_sql_query(query, con)  # cria o dataframe para ser lido com o pandas
            # Retorna a representação em string dos dados do DataFrame
            return(data_frame.to_string(index=False)) # exibe o dataframe sem a numeração do pandas


# Método listar veículos - janela de exibição
    #Abre uma janela com uma lista da pesquisa, e tem um botão com a opção exportar em xls e csv
    def janela_listar_veiculos(self, titulo):
        nova_janela = tk.Toplevel(self.root)# para abrir uma nova janela
        nova_janela.title(titulo) # Definindo o título da nova janela com o texto da solicitação
        nova_janela.geometry("1200x500")  # Definindo o tamanho da nova janela -  Largura x Altura
        nova_janela.config(bg= self.cor1)  # Define a cor de fundo da janela
        # Título
        estilo_label_Titulos_quadros = ("Verdana Bold", 12)  # estilo de texto
        label_veiculos_listados = ttk.Label(nova_janela, text="Veículos Listados", font=estilo_label_Titulos_quadros,
                                            background= self.cor1, foreground="white")
        label_veiculos_listados.place(x=20, y=10, width=200, height=30)
        # Cria uma ScrolledText para exibir os dados
        veiculos_listados_scrol = scrolledtext.ScrolledText(nova_janela, width=1165, height=400, bg=self.cor3)
        veiculos_listados_scrol.pack(expand=True, fill='both')
        veiculos_listados_scrol.place(x=20, y=40, width=1165, height=400)
        # Obtém os dados formatados e os exibe na ScrolledText
        veiculos = self.listar_veiculos()
        veiculos_listados_scrol.insert(tk.END, veiculos)
        veiculos_listados_scrol.configure(state="disabled")
        # Botão "Exportar" com um menu suspenso (dropdown) contendo as opções de exportação para CSV e Excel
        button_export = tk.Menubutton(nova_janela, text="Exportar", font=("Verdana", 10), relief=tk.FLAT, bg=self.cor2)
        button_export.place(x = 1085, y = 450, width = 100, height = 30)
        menu_export = tk.Menu(button_export, tearoff=0)
        button_export.config(menu=menu_export)
        menu_export.add_command(label="Exportar para CSV", command=self.exportar_csv)
        menu_export.add_command(label="Exportar para Excel", command=self.exportar_excel)


    # Método inserir_veiculo -> para inserir dados no banco de dados dos veiculos
    def inserir_veiculo(self, dados):
        with sqlite3.connect(self.db) as con:
            cursor = con.cursor()
            cursor.execute("""INSERT INTO veiculo (marca, modelo, categoria, transmissao, tipo_veiculo, 
                            quant_pessoas, imagem, valor_diaria, ultima_rev, 
                            proxima_rev, ultima_insp) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                           dados)
            con.commit()
            messagebox.showinfo("Veículo registado!")


# Método Registar veículos - Abre uma janela com diversos campos para registar um veiculo no veiculos.db
    def janela_registar_veiculos(self, titulo):
        nova_janela = tk.Toplevel(self.root)  # para abrir uma nova janela
        nova_janela.title("Registar Veículo")  # Definindo o título da nova janela com o texto da solicitação
        # self.janela.wm_iconbitmap('Falta o ícone.ico')  # Lembrar de por o ícone!!!!
        nova_janela.geometry("400x430")
        nova_janela.config(bg=self.cor1)  # Define a cor de fundo da janela
        # Criar um widget com os campos para a edição
        estilo_label_Titulos_quadros = ("Verdana Bold", 12)
        label_veiculos_registar = ttk.Label(nova_janela, text="Registar Veículos", font=estilo_label_Titulos_quadros,
                                            background= self.cor1, foreground="white")
        label_veiculos_registar.place(x=20, y=10, width=200, height=30)

        # Campos de entrada para os dados do veículo
        etiquetas = ["Marca:", "Modelo:", "Categoria:", "Transmissão:", "Tipo de Veículo:",
                     "Quantidade de Pessoas:", "Imagem:", "Valor da Diária:", "Última Revisão:",
                     "Próxima Revisão:", "Última Inspeção:"]
        entrada_campos = {}  # Dicionário para armazenar os campos de entrada

        # Posicionar e criar campos de entrada para cada etiqueta
        for i, etiqueta in enumerate(etiquetas):
            label_etiqueta = ttk.Label(nova_janela, text=etiqueta, background=self.cor1, foreground="white")
            label_etiqueta.place(x=20, y=50 + 30 * i, width=150, height=25)
            entrada_campos[etiqueta] = tk.Entry(nova_janela)
            entrada_campos[etiqueta].place(x=180, y=50 + 30 * i, width=200, height=25)

        # Botão para inserir o veículo no banco de dados
        button_inserir = tk.Button(nova_janela, text="Inserir Veículo", command=lambda: self.inserir_veiculo([
            entrada_campos["Marca:"].get(), entrada_campos["Modelo:"].get(), entrada_campos["Categoria:"].get(),
            entrada_campos["Transmissão:"].get(), entrada_campos["Tipo de Veículo:"].get(),
            entrada_campos["Quantidade de Pessoas:"].get(), entrada_campos["Imagem:"].get(),
            entrada_campos["Valor da Diária:"].get(), entrada_campos["Última Revisão:"].get(),
            entrada_campos["Próxima Revisão:"].get(), entrada_campos["Última Inspeção:"].get()
        ]), font=("Verdana", 10), relief=tk.FLAT, bg=self.cor2)
        button_inserir.place(x=260, y=390, width=120, height=30)


# Método Editar Veículos - Abre uma janela com diversos campos para editar o banco de dados dos veiculos
    def editar_veiculo(self, titulo):
        nova_janela = tk.Toplevel(self.root)# para abrir uma nova janela
        nova_janela.title("Editar Veículo")
        nova_janela.geometry("400x500")
        nova_janela.config(bg=self.cor1)


        def buscar_veiculo(): # Função para buscar e preencher os campos com os dados do veículo
            identificador = entrada_id.get()# Obtém o identificador do veículo a partir do campo de entrada
            # Busca o veículo no banco de dados
            with sqlite3.connect(self.db) as con:
                cursor = con.cursor()
                cursor.execute("SELECT * FROM veiculo WHERE id = ?", (identificador,))
                veiculo = cursor.fetchone()  # Retorna a primeira linha correspondente à consulta
                if veiculo:
                    # Preenche os campos de entrada com os dados do veículo
                    for i, etiqueta in enumerate(etiquetas):
                        entrada_campos[etiqueta].delete(0, tk.END)
                        entrada_campos[etiqueta].insert(0, veiculo[i])
                else:
                    # Define a mensagem de erro dentro do campo de busca
                    entrada_id.delete(0, tk.END)
                    entrada_id.insert(0, "Não encontrado!")
                    entrada_id.config(fg="red")


        def salvar_alteracoes(): # Função para salvar as alterações do veículo
            # Coleta os dados dos campos de entrada, excluindo o ID do veículo
            dados = [entrada_campos[etiqueta].get() for etiqueta in etiquetas if etiqueta != "ID:"]
            id_veiculo = entrada_campos["ID:"].get() # Coleta o ID do veículo
            # print("ID do veículo:", id_veiculo) # Para debug - verificar o valor do ID
            # Insere os dados no banco de dados
            with sqlite3.connect(self.db) as con:
                cursor = con.cursor()
                cursor.execute("""UPDATE veiculo SET marca=?, modelo=?, categoria=?, transmissao=?, tipo_veiculo=?, 
                                        quant_pessoas=?, imagem=?, valor_diaria=?, ultima_rev=?, 
                                        proxima_rev=?, ultima_insp=? WHERE id=?""",
                               tuple(dados + [id_veiculo])) # Adicionando o ID do veículo à lista de dados
                con.commit()
                messagebox.showinfo("Alterações Guardadas!")
        # Título da Janela
        estilo_label_Titulos_quadros = ("Verdana Bold", 12)
        label_veiculos_registar = ttk.Label(nova_janela, text="Editar Veículo", font=estilo_label_Titulos_quadros,
                                            background=self.cor1, foreground="white")
        label_veiculos_registar.place(x=20, y=10, width=200, height=30)

        etiquetas = ["ID:", "Marca:", "Modelo:", "Categoria:", "Transmissão:", "Tipo de Veículo:",
                     "Quantidade de Pessoas:", "Imagem:", "Valor da Diária:", "Última Revisão:",
                     "Próxima Revisão:", "Última Inspeção:"]
        entrada_campos = {} # Dicionário para armazenar os campos de entrada

        for i, etiqueta in enumerate(etiquetas):
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
        button_buscar = tk.Button(nova_janela, text="Buscar", command=buscar_veiculo, font=("Verdana", 10),
                                  relief=tk.FLAT, bg=self.cor2)
        button_buscar.place(x=300, y=50, width=80, height=25)
        button_salvar = tk.Button(nova_janela, text="Guardar Alterações", command=salvar_alteracoes, relief=tk.FLAT,
                                  font=("Verdana", 10), bg=self.cor2)
        button_salvar.place(x=20, y=450, width=150, height=30)


# Método Remover Veículos - para excluir veiculos do veiculos.db
    def remover_veiculos(self, id_veiculo):
        nova_janela = tk.Toplevel(self.root)
        nova_janela.title("Remover Veículo")
        nova_janela.geometry("400x350")
        nova_janela.config(bg=self.cor1)
        # Título da janela + listbox
        estilo_label_Titulos_quadros = ("Verdana Bold", 12)
        label_veiculos_remover = ttk.Label(nova_janela, text="Remover Veículo", font=estilo_label_Titulos_quadros,
                                           background=self.cor1, foreground="white")
        label_veiculos_remover.place(x=20, y=10, width=200, height=30)
        # Label do buscar ID
        label_id = ttk.Label(nova_janela, text="Insira o ID do veículo:", font=("Verdana", 10),
                             background=self.cor1, foreground="white")
        label_id.place(x=20, y=50, width=150, height=25)
        entrada_id = ttk.Entry(nova_janela)
        entrada_id.place(x=170, y=50, width=60, height=25)
        # Listbox para exibir as informações do veículo
        remover_veiculos_listbox = tk.Listbox(nova_janela, width=360, height=210, bg=self.cor3)
        remover_veiculos_listbox.place(x=20, y=90, width=360, height=210)


        def buscar_veiculo(): # Função para buscar o veículo no banco de dados e exibir na listbox
            identificador = entrada_id.get()
            if identificador:  # Verifica se foi inserido um ID
                with sqlite3.connect(self.db) as con:
                    cursor = con.cursor()
                    # PRAGMA - (retorna uma lista de tuplas que contem diversas tuplas em que cada coluna é uma tupla)!
                    cursor.execute("PRAGMA table_info(veiculo)")
                    colunas = [coluna[1] for coluna in cursor.fetchall()]  # Obtém os nomes das colunas
                    cursor.execute("SELECT * FROM veiculo WHERE id = ?", (identificador,))
                    veiculo = cursor.fetchone() # retorna só o id(n°)

                if veiculo:
                    # Limpa a listbox
                    remover_veiculos_listbox.delete(0, tk.END)
                    # Insere as informações do veículo (chave: valor)
                    for coluna, valor in zip(colunas, veiculo):
                        remover_veiculos_listbox.insert(tk.END, f"{coluna}: {valor}")
                else:
                    messagebox.showerror("Erro", "Veículo não encontrado!")
            else:
                messagebox.showerror("Erro", "Insira um ID para buscar!")

        # Botão para buscar o veículo
        button_buscar = tk.Button(nova_janela, text="Buscar", command=buscar_veiculo, font=("Verdana", 10),
                                  relief=tk.FLAT, bg=self.cor2)
        button_buscar.place(x=300, y=50, width=80, height=25)


        def confirmar_exclusao(): # Função para confirmar a exclusão do veículo
            identificador = entrada_id.get()
            if identificador:  # Verifica se foi inserido um ID
                with sqlite3.connect(self.db) as con:
                    cursor = con.cursor()
                    cursor.execute("DELETE FROM veiculo WHERE id = ?", (identificador,))
                    con.commit()
                messagebox.showinfo("Veículo excluído!")
            else:
                messagebox.showerror("Erro", "Insira um ID para excluir!")
        # Botão para confirmar a exclusão do veículo
        button_remover = tk.Button(nova_janela, text="Remover", command=confirmar_exclusao, font=("Verdana", 10),
                                   relief=tk.FLAT, bg=self.cor2)
        button_remover.place(x=20, y=310, width=120, height=30)
