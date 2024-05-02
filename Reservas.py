"""
Menu Flutuante - aberto a partir de app.py
Classe Janela Reservas e seus metodos de:
Listar, Registar, Alterar e Remover
ps: no app.py está a estrutura completa do DashBord
22/03/2024 - last version
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

class Janela_reservas:
    def __init__(self, root,):
        self.root = root
        self.db= "database/reservas.db" # acesso a base de dados "reservas"
        self.cor1 = 'azure3'  # fundo geral
        self.cor2 = 'azure2'  # botões
        self.cor3 = 'white smoke'  # campos de dados
        self.csv_path = "csv"
        self.excel_path = "excel"
        # Criar diretórios se não existirem
        os.makedirs(self.csv_path, exist_ok=True)
        os.makedirs(self.excel_path, exist_ok=True)


    def exportar_csv(self): # função para exportar em .csv
        con = sqlite3.connect(self.db) # conecta ao banco de dados
        cursor = con.cursor()
        query = "SELECT * FROM reserva" # Consulta SQL
        cursor.execute(query)
        dados = cursor.fetchall()
        con.close
        # caminho para criar o arquivo csv
        csv_file = os.path.join(self.csv_path, "reservas.csv")
        with open(csv_file, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file, delimiter=",")
            # Escrever o cabeçalho do arquivo CSV (nomes das colunas)
            writer.writerow(["ID", "Cliente ID", "Veículo ID", "Data Inicial", "Data Final", "Forma de Pagamento"])
            # Escrever os dados no arquivo CSV
            for linha in dados:
                writer.writerow(linha)



    def exportar_excel(self): # função para exportar em .csv
        con = sqlite3.connect(self.db) # conecta ao banco de dados
        cursor = con.cursor()
        query = "SELECT * FROM reserva" # Consulta pra selecionar a tabela
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
        excel_file = os.path.join(self.excel_path, "reservas.xlsx")# Salva o arquivo do Excel
        wb.save(excel_file)


    def listar_reservas(self):# função para criar a lista de reservas
        with sqlite3.connect(self.db) as con:
            query = "SELECT * FROM reserva"  # Consulta tabela no .db
            data_frame = pd.read_sql_query(query, con)  # cria o dataframe para ser lido com o pandas
            # Retorna a representação em string dos dados do DataFrame
            return (data_frame.to_string(index=False))  # exibe o dataframe sem a numeração do pandas


    # Método listar reservas - janela de exibição
    def janela_listar_reservas(self, titulo):
        nova_janela = tk.Toplevel(self.root)
        nova_janela.title(titulo)
        nova_janela.geometry("600x500")
        nova_janela.config(bg=self.cor1)
        # título
        estilo_label_Titulos_quadros = ("Verdana Bold", 12)
        label_reservas_listados = ttk.Label(nova_janela, text="Reservas Listadas", font=estilo_label_Titulos_quadros,
                                            background=self.cor1)
        label_reservas_listados.place(x=20, y=10, width=300, height=30)
        # Cria uma ScrolledText para exibir os dados
        reservas_listados_scrol = scrolledtext.ScrolledText(nova_janela, width=600, height=400)
        reservas_listados_scrol.pack(expand=True, fill='both')
        reservas_listados_scrol.place(x=20, y=40, width=580, height=400)
        # Obter os dados das reservas e os exibe na ScrolledText
        reservas = self.listar_reservas()
        reservas_listados_scrol.insert(tk.END, reservas)
        reservas_listados_scrol.configure(state="disabled")
        # Criar um botão "Exportar" com um menu suspenso (dropdown) contendo as opções de exportação para CSV e Excel
        button_export = tk.Menubutton(nova_janela, text="Exportar", font=("Verdana", 10),
                                      relief=tk.RAISED, bg=self.cor2)
        button_export.place(x = 485, y = 450, width = 100, height = 30)
        menu_export = tk.Menu(button_export, tearoff=0)
        button_export.config(menu=menu_export)
        menu_export.add_command(label="Exportar para CSV", command=self.exportar_csv)
        menu_export.add_command(label="Exportar para Excel", command=self.exportar_excel)


# Método para inserir uma nova reserva no banco de dados "reservas.db""
    def inserir_reserva(self, dados):
        with sqlite3.connect(self.db) as con:
            cursor = con.cursor()
            cursor.execute("""INSERT INTO reserva (cliente_id, veiculo_id, data_inicio, data_fim, forma_pagamento)
                                    VALUES (?, ?, ?, ?, ?)""", dados)
            con.commit()
            messagebox.showinfo("Reserva registada!")


# Método Registar reservas - Abre uma janela para registar uma nova reserva
    def janela_registar_reservas(self, titulo):
        nova_janela = tk.Toplevel(self.root)
        nova_janela.title("Registar Reserva")
        nova_janela.geometry("400x260")
        nova_janela.config(bg=self.cor1)
        estilo_label_Titulos_quadros = ("Verdana Bold", 12)
        label_clientes_registar = ttk.Label(nova_janela, text="Registar Reservas", font=estilo_label_Titulos_quadros,
                                            background=self.cor1)
        label_clientes_registar.place(x=20, y=10, width=200, height=30)

        # campo de entrada de dados para a reserva
        etiquetas = ["Cliente ID:", "Veículo ID:", "Data inicial:", "Data final:", "Forma de Pagamento:"]
        entrada_campos ={} # os dados de entrada ficarão nesse dicionário

        # Posicionar e criar campos de entrada para cada etiqueta
        for i, etiqueta in enumerate(etiquetas):
            label_etiqueta = ttk.Label(nova_janela, text=etiqueta, background=self.cor1)
            label_etiqueta.place(x=20, y=50 + 30 * i, width=150, height=25)
            entrada_campos[etiqueta] = tk.Entry(nova_janela)
            entrada_campos[etiqueta].place(x=180, y=50 + 30 * i, width=200, height=25)

        # Botão para inserir a reserva no banco de dados
        button_inserir = tk.Button(nova_janela, text="Inserir Reserva", command=lambda: self.inserir_reserva([
            entrada_campos["Cliente ID:"].get(), entrada_campos["Veículo ID:"].get(),
            entrada_campos["Data inicial:"].get(), entrada_campos["Data final:"].get(),
            entrada_campos["Forma de Pagamento:"].get()
        ]), font=("Verdana", 10), relief=tk.RAISED, bg=self.cor2)
        button_inserir.place(x=260, y=210, width=120, height=30)


# Método Editar reservas - Janela para editar o banco de dados dos clientes
    def janela_editar_reservas(self, titulo):
        nova_janela = tk.Toplevel(self.root)
        nova_janela.title("Editar Reserva")
        nova_janela.geometry("400x300")
        nova_janela.config(bg=self.cor1)

        etiquetas = ["Reserva ID:", "Cliente ID:", "Veículo ID:", "Data inicial:", "Data final:", "Forma de pagamento:"]
        entrada_campos = {}  # Dicionário para armazenar os campos de entrada

        def buscar_reserva():  # Buscar e preencher os campos com os dados da reserva
            identificador = entrada_id.get()  # Obtém o identificador da reserva a partir do campo de entrada
            # Busca a reserva no banco de dados
            with sqlite3.connect(self.db) as con:
                cursor = con.cursor()
                cursor.execute("SELECT * FROM reserva WHERE id = ?", (identificador,))
                reserva = cursor.fetchone() # Retorna a primeira linha correspondente à consulta
                if reserva:
                    # Preenche os campos de entrada com os dados do cliente
                    for i, etiqueta in enumerate(etiquetas):# variável etiquetas vem da função registar!
                        entrada_campos[etiqueta].delete(0, tk.END)
                        entrada_campos[etiqueta].insert(0, reserva[i])
                else:
                    # Define a mensagem de erro dentro do campo de busca
                    entrada_id.delete(0, tk.END)
                    entrada_id.insert(0, "Não encontrado!")
                    entrada_id.config(fg="red")

        def salvar_alteracoes():  # Função para salvar as alterações da resrva
            # Coleta os dados dos campos de entrada, excluindo o ID
            dados = [entrada_campos[etiqueta].get() for etiqueta in etiquetas[1:]]# Ignorando o "Reserva ID, "pula o 0"
            # dados = [entrada_campos[etiqueta].get() for etiqueta in etiquetas if etiqueta != "ID:"] # Bugou!!!
            id_reserva = entrada_campos["ID:"].get()  # Coleta o ID da reserva
            # Insere os dados no banco de dados
            with sqlite3.connect(self.db) as con:
                cursor = con.cursor()
                cursor.execute("""UPDATE reserva SET cliente_id=?, veiculo_id=?,
                data_inicio=?, data_fim=?, forma_pagamento=? WHERE id=?""",
                               tuple(dados + [id_reserva]))  # Adicionando o ID da reserva à lista de dados
                con.commit()
                messagebox.showinfo("Alterações Guardadas!")

        # Título da Janela
        estilo_label_Titulos_quadros = ("Verdana Bold", 12)
        label_reservas_registar = ttk.Label(nova_janela, text="Editar Reserva", font=estilo_label_Titulos_quadros,
                                            background=self.cor1)
        label_reservas_registar.place(x=20, y=10, width=200, height=30)

        for i, etiqueta in enumerate(etiquetas):  # etiquetas dos campos a serem preenchidos
            label_etiqueta = ttk.Label(nova_janela, text=etiqueta, background=self.cor1)
            label_etiqueta.place(x=20, y=50 + 30 * i, width=150, height=25)
            entrada_campos[etiqueta] = tk.Entry(nova_janela)
            entrada_campos[etiqueta].place(x=180, y=50 + 30 * i, width=200, height=25)
        # Campo de entrada para o ID da reserva
        entrada_id = tk.Entry(nova_janela)  # id que "vai" na busca!
        entrada_id.place(x=180, y=50, width=100, height=25)
        # Entrada do ID ao dicionário entrada_campos, sem isso não insere a id ao banco de dados
        entrada_campos["ID:"] = entrada_id
        # Botões para buscar e salvar alterações
        button_buscar = tk.Button(nova_janela, text="Buscar", command=buscar_reserva, font=("Verdana", 10),
                                  relief=tk.RAISED, bg=self.cor2)
        button_buscar.place(x=300, y=50, width=80, height=25)
        button_salvar = tk.Button(nova_janela, text="Guardar Alterações", command=salvar_alteracoes,
                                  font=("Verdana", 10), relief=tk.RAISED, bg=self.cor2)
        button_salvar.place(x=20, y=250, width=150, height=30)


# Método Remover reservas - para excluir de reservas.db
    def janela_remover_reservas(self, id_cliente):
        nova_janela = tk.Toplevel(self.root)
        nova_janela.title("Remover Reserva")
        nova_janela.geometry("400x240")
        nova_janela.config(bg=self.cor1)
        # Título da janela + listbox
        estilo_label_Titulos_quadros = ("Verdana Bold", 12)
        label_reservas_remover = ttk.Label(nova_janela, text="Remover Reserva", font=estilo_label_Titulos_quadros,
                                           background=self.cor1)
        label_reservas_remover.place(x=20, y=10, width=200, height=30)
        # Label do buscar ID
        label_id = ttk.Label(nova_janela, text="Insira o ID da reserva:", font=("Verdana", 10), background=self.cor1)
        label_id.place(x=20, y=50, width=150, height=25)
        entrada_id = ttk.Entry(nova_janela)
        entrada_id.place(x=170, y=50, width=60, height=25)
        # Listbox para exibir as informações do veículo
        remover_reservas_listbox = tk.Listbox(nova_janela, width=360, height=100)
        remover_reservas_listbox.place(x=20, y=90, width=360, height=100)

        def buscar_reserva(): # Função para buscar a reserva no banco de dados e exibir na listbox
            identificador = entrada_id.get()
            if identificador:  # Verifica se foi inserido um ID
                with sqlite3.connect(self.db) as con:
                    cursor = con.cursor()
                    # PRAGMA - (retorna uma lista de tuplas que contem diversas tuplas em que cada coluna é uma tupla)!
                    cursor.execute("PRAGMA table_info(reserva)")# em tabela reserva
                    colunas = [coluna[1] for coluna in cursor.fetchall()]  # Obtém os nomes das colunas
                    cursor.execute("SELECT * FROM reserva WHERE id = ?", (identificador,))
                    reserva = cursor.fetchone() # retorna só o id(n°)
                if reserva:
                    # Limpa a listbox
                    remover_reservas_listbox.delete(0, tk.END)
                    # Insere as informações da reserva (chave: valor)
                    for coluna, valor in zip(colunas, reserva):
                        remover_reservas_listbox.insert(tk.END, f"{coluna}: {valor}")
                else:
                    messagebox.showerror("Reserva não encontrada!")
            else:
                messagebox.showerror("Insira um ID para buscar!")
        # Botão para buscar o cliente
        button_buscar = tk.Button(nova_janela, text="Buscar", command=buscar_reserva, font=("Verdana", 10),
                                  relief=tk.RAISED, bg=self.cor2)
        button_buscar.place(x=300, y=50, width=80, height=25)

        def confirmar_exclusao(): # Função para confirmar a exclusão da reserva
            identificador = entrada_id.get()
            if identificador:  # Verifica se foi inserido um ID
                with sqlite3.connect(self.db) as con:
                    cursor = con.cursor()
                    cursor.execute("DELETE FROM reserva WHERE id = ?", (identificador,))
                    con.commit()
                messagebox.showinfo("Cliente excluído!")
            else:
                messagebox.showerror("Insira um ID para excluir!")
        # Botão para confirmar a exclusão da Reserva
        button_remover = tk.Button(nova_janela, text="Remover", command=confirmar_exclusao, font=("Verdana", 10),
                                   relief=tk.RAISED, bg=self.cor2)
        button_remover.place(x=20, y=200, width=120, height=30)

