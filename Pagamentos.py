"""
Menu Flutuante - aberto a partir de app.py
Classe Janela Pagamentos e seus metodos de:
Listar, Registar, Alterar e Remover
ps: no app.py está a estrutura completa do DashBord
26/03/2024 - last version
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


class Janela_pagamentos:
    def __init__(self, root):
        self.root = root
        self.db = "database/pagamentos.db"
        self.db_reservas = "database/reservas.db"
        self.db_clientes = "database/clientes.db"
        self.db_veiculos = "database/veiculos.db"
        self.cor1 = "#2a2d2e"  # fundo geral
        self.cor2 = '#FF8C00'  # botões Dark Orange
        self.cor3 = 'gray'  # campos de dados
        self.csv_path = "csv"
        self.excel_path = "excel"
        #self.criar_pagamento()  # Processa as reservas e cria os pagamentos
        os.makedirs(self.csv_path, exist_ok=True) # se não houver diretório, será criado
        os.makedirs(self.excel_path, exist_ok=True)


    def exportar_csv(self):
        con = sqlite3.connect(self.db) # conecta ao banco de dados
        cursor = con.cursor()
        query = "SELECT * FROM pagamento" # Consulta SQL
        cursor.execute(query)
        dados = cursor.fetchall()
        con.close
        # caminho para criar o arquivo csv
        csv_file = os.path.join(self.csv_path, "pagamentos.csv")
        with open(csv_file, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file, delimiter=",")
            # Escrever o cabeçalho do arquivo CSV (nomes das colunas)
            writer.writerow(["ID", "Reserva ID", "Nome do Cliente", "Email do Cliente", "Modelo", "Período de Aluguer",
                             "Forma de Pagamento", "Valor Total"])
            # Escrever os dados no arquivo CSV
            for linha in dados:
                writer.writerow(linha)


    def exportar_excel(self):
        con = sqlite3.connect(self.db)  # conecta ao banco de dados
        cursor = con.cursor()
        query = "SELECT * FROM pagamento"  # Consulta pra selecionar a tabela
        cursor.execute(query)
        dados = cursor.fetchall()
        # Obtem nome das colunas
        colunas = [descricao[0] for descricao in cursor.description]
        con.close()
        wb = Workbook()  # Cria novo arquivo xls
        ws = wb.active
        ws.append(colunas)  # Adiciona os nomes de colunas
        for linha in dados:
            ws.append(linha)  # Adiciona os dados da tabela ao arquivo xls
        excel_file = os.path.join(self.excel_path, "pagamentos.xlsx")  # Salva o arquivo do Excel
        wb.save(excel_file)


    # Método listar veículos - janela de exibição Seleciona os principais dados para exibição
    def listar_pagamentos(self):
        with sqlite3.connect(self.db) as con:
            cursor = con.cursor()
            query = "SELECT * FROM pagamento"  # Consulta tabela no .db
            data_frame = pd.read_sql_query(query, con)  # cria o dataframe para ser lido com o pandas
            # Retorna a representação em string dos dados do DataFrame
            return (data_frame.to_string(index=False))  # exibe o dataframe sem a numeração do pandas


    # Método listar pagamentos - janela de exibição
    def janela_listar_pagamentos(self, titulo):
        nova_janela = tk.Toplevel(self.root)
        nova_janela.title(titulo)
        nova_janela.geometry("1000x500")
        nova_janela.config(bg=self.cor1)
        # Título
        estilo_label_Titulos_quadros = ("Verdana Bold", 12)
        label_pagamentos_listados = ttk.Label(nova_janela, text="Pagamentos Listados",
                                            font=estilo_label_Titulos_quadros, background=self.cor1, foreground="white")
        label_pagamentos_listados.place(x=20, y=10, width=300, height=30)
        # ScrolledText para exibir os dados
        pagamentos_listados_scrol = scrolledtext.ScrolledText(nova_janela, width=760, height=400, bg=self.cor3)
        pagamentos_listados_scrol.pack(expand=True, fill='both')
        pagamentos_listados_scrol.place(x=20, y=40, width=960, height=400)
        # Obtém os dados formatados e os exibe na ScrolledText
        pagamentos = self.listar_pagamentos()# recebe os dados formatados em pandas
        pagamentos_listados_scrol.insert(tk.END, pagamentos)
        pagamentos_listados_scrol.configure(state="disabled")

        # Botão "Exportar" com um menu suspenso (dropdown) contendo as opções de exportação para CSV e Excel
        button_export = tk.Menubutton(nova_janela, text="Exportar", font=("Verdana", 10), relief=tk.FLAT, bg=self.cor2)
        button_export.place(x=860, y=450, width=100, height=30)
        menu_export = tk.Menu(button_export, tearoff=0)
        button_export.config(menu=menu_export)
        menu_export.add_command(label="Exportar para CSV", command=self.exportar_csv)
        menu_export.add_command(label="Exportar para Excel", command=self.exportar_excel)

# Método Remover pagamentos - para excluir pagamentos de pagamentos.db
    def janela_remover_pagamentos(self, id_pagamento):
        nova_janela = tk.Toplevel(self.root)
        nova_janela.title("Remover Pagamento")
        nova_janela.geometry("400x280")
        nova_janela.config(bg=self.cor1)
        # Título da janela + listbox
        estilo_label_Titulos_quadros = ("Verdana Bold", 12)
        label_pagamentos_remover = ttk.Label(nova_janela, text="Remover Pagamento", font=estilo_label_Titulos_quadros,
                                             background=self.cor1, foreground="white")
        label_pagamentos_remover.place(x=20, y=10, width=200, height=30)
        # Label do buscar ID
        label_id = ttk.Label(nova_janela, text="Insira o ID do pagamento:", font=("Verdana", 10), background=self.cor1,
                             foreground="white")
        label_id.place(x=20, y=50, width=200, height=25)
        entrada_id = ttk.Entry(nova_janela)
        entrada_id.place(x=200, y=50, width=60, height=25)
        # Listbox para exibir as informações do veículo
        remover_pagamentos_listbox = tk.Listbox(nova_janela, width=360, height=140, bg=self.cor3)
        remover_pagamentos_listbox.place(x=20, y=90, width=360, height=140)

        def buscar_pagamento(): # Função para buscar o pagamento no banco de dados e exibir na listbox
            identificador = entrada_id.get()
            if identificador:  # Verifica se foi inserido um ID
                with sqlite3.connect(self.db) as con:
                    cursor = con.cursor()
                    # PRAGMA - (retorna uma lista de tuplas que contem diversas tuplas em que cada coluna é uma tupla)!
                    cursor.execute("PRAGMA table_info(pagamento)")
                    colunas = [coluna[1] for coluna in cursor.fetchall()]  # Obtém os nomes das colunas
                    cursor.execute("SELECT * FROM pagamento WHERE id = ?", (identificador,))
                    pagamento = cursor.fetchone() # retorna só o id(n°)

                if pagamento:
                    # Limpa a listbox
                    remover_pagamentos_listbox.delete(0, tk.END)
                    # Insere as informações do pagamento (chave: valor)
                    for coluna, valor in zip(colunas, pagamento):
                        remover_pagamentos_listbox.insert(tk.END, f"{coluna}: {valor}")
                else:
                    messagebox.showerror("Pagamento não encontrado!")
            else:
                messagebox.showerror("Insira um ID para buscar!")

        # Botão para buscar o pagamento
        button_buscar = tk.Button(nova_janela, text="Buscar", command=buscar_pagamento, font=("Verdana", 10),
                                  relief=tk.FLAT, bg=self.cor2)
        button_buscar.place(x=300, y=50, width=80, height=25)

        def confirmar_exclusao(): # Função para confirmar a exclusão do pagamento
            identificador = entrada_id.get()
            if identificador:  # Verifica se foi inserido um ID
                with sqlite3.connect(self.db) as con:
                    cursor = con.cursor()
                    cursor.execute("DELETE FROM pagamento WHERE id = ?", (identificador,))
                    con.commit()
                messagebox.showinfo("Pagamento excluído!")
            else:
                messagebox.showerror("Insira um ID para excluir!")
        # Botão para confirmar a exclusão do pagamento
        button_remover = tk.Button(nova_janela, text="Remover", command=confirmar_exclusao, font=("Verdana", 10),
                                   relief=tk.FLAT, bg=self.cor2)
        button_remover.place(x=20, y=240, width=120, height=30)


# Método Editar pagamentos - Janela para editar o banco de dados dos pagamentos
    def janela_editar_pagamentos(self, titulo):
        nova_janela = tk.Toplevel(self.root)
        nova_janela.title("Editar Pagamento")
        nova_janela.geometry("400x360")
        nova_janela.config(bg=self.cor1)

        etiquetas = ["ID do Pagamento:", "ID da Reserva:", "Nome do Cliente:", "E-mail:", "Modelo do Veículo:",
                     "Total de dias de Aluguer:", "Forma de pagamento:", "Valor total: €"]
        entrada_campos = {}  # Dicionário para armazenar os campos de entrada

        def buscar_pagamento():  # Buscar e preencher os campos com os dados do pagamento
            identificador = entrada_id.get()  # Obtém o identificador do pagamento a partir do campo de entrada
            # Busca o pagamento no banco de dados
            with sqlite3.connect(self.db) as con:
                cursor = con.cursor()
                cursor.execute("SELECT * FROM pagamento WHERE id = ?", (identificador,))
                pagamento = cursor.fetchone() # Retorna a primeira linha correspondente à consulta
                if pagamento:
                    # Preenche os campos de entrada com os dados do cliente
                    for i, etiqueta in enumerate(etiquetas):  # variável etiquetas
                        entrada_campos[etiqueta].delete(0, tk.END)
                        entrada_campos[etiqueta].insert(0, pagamento[i])
                else:
                    # Define a mensagem de erro dentro do campo de busca
                    entrada_campos["Pagamento ID:"].delete(0, tk.END)
                    entrada_campos["Pagamento ID:"].insert(0, "Não encontrado!")
                    entrada_campos["Pagamento ID:"].config(fg="red")

        def salvar_alteracoes():  # Função para salvar as alterações do pagamento
            # Coleta os dados dos campos de entrada, excluindo o ID
            dados = [entrada_campos[etiqueta].get() for etiqueta in etiquetas[1:]]  # Excluindo o "ID do Pagamento:"
            # , pulando o 0
            id_pagamento = entrada_campos["ID do Pagamento:"].get() # Coleta o ID do pagamento
            # Insere os dados no banco de dados
            with sqlite3.connect(self.db) as con:
                cursor = con.cursor()
                cursor.execute("""UPDATE pagamento SET id_reserva=?,  nome_cliente=?, email_cliente=?, modelo=?,
                periodo_aluguer=?, forma_pagamento=?, valor_€=? WHERE id=?""",
                               tuple(dados + [id_pagamento]))  # Adicionando o ID do pagamento à lista de dados
                con.commit()
                messagebox.showinfo("Alterações Guardadas!")


        # Título da Janela
        estilo_label_Titulos_quadros = ("Verdana Bold", 12)
        label_reservas_registar = ttk.Label(nova_janela, text="Editar Pagamento", font=estilo_label_Titulos_quadros,
                                            background=self.cor1, foreground="white")
        label_reservas_registar.place(x=20, y=10, width=200, height=30)
        # etiquetas dos campos a serem preenchidos
        for i, etiqueta in enumerate(etiquetas):
            label_etiqueta = ttk.Label(nova_janela, text=etiqueta, background=self.cor1, foreground="white")
            label_etiqueta.place(x=20, y=50 + 30 * i, width=150, height=25)
            entrada_campos[etiqueta] = tk.Entry(nova_janela)
            entrada_campos[etiqueta].place(x=180, y=50 + 30 * i, width=200, height=25)
        # Campo de entrada para o ID da reserva
        entrada_id = tk.Entry(nova_janela)  # id que "vai" na busca!
        entrada_id.place(x=180, y=50, width=100, height=25)
        # Entrada do ID ao dicionário entrada_campos, sem isso não insere a id ao banco de dados
        entrada_campos["Pagamento ID:"] = entrada_id
        # Botões para buscar e salvar alterações
        button_buscar = tk.Button(nova_janela, text="Buscar", command=buscar_pagamento, font=("Verdana", 10),
                                  relief=tk.FLAT, bg=self.cor2)
        button_buscar.place(x=300, y=50, width=80, height=25)
        button_salvar = tk.Button(nova_janela, text="Guardar Alterações", command=salvar_alteracoes,
                                  font=("Verdana", 10), relief=tk.FLAT, bg=self.cor2)
        button_salvar.place(x=20, y=310, width=150, height=30)


# janela_registar_pagamentos()
    def janela_registar_pagamentos(self, titulo):
        def buscar_reserva():
            reserva_id = id_reserva_entry.get() # busca do id
            try:
                with sqlite3.connect(self.db_reservas) as con:
                    cursor = con.cursor()
                    cursor.execute("SELECT cliente_id, veiculo_id, data_inicio, data_fim, forma_pagamento "
                                   "FROM reserva WHERE id = ?", (reserva_id,))
                    reserva = cursor.fetchone()# recebe tudo de "reserva"
                if not reserva:
                    messagebox.showerror("Erro", f"Reserva com ID {reserva_id} não encontrada.")
                    return None
                cliente_id, veiculo_id, data_inicio, data_fim, forma_pagamento = reserva # cria variaveis para as keys
                id_reserva = reserva_id
                with sqlite3.connect(self.db_clientes) as con:
                    cursor = con.cursor()
                    cursor.execute("SELECT nome, email FROM user WHERE id = ?", (cliente_id,))
                    cliente = cursor.fetchone() # recebe dados de "cliente"
                if not cliente:
                    messagebox.showerror("Erro", f"Cliente com ID {cliente_id} não encontrado.")
                    return None
                nome_cliente, email_cliente = cliente # cria variaveis para as keys
                with sqlite3.connect(self.db_veiculos) as con:
                    cursor = con.cursor()
                    cursor.execute("SELECT modelo, valor_diaria FROM veiculo WHERE id = ?", (veiculo_id,))
                    veiculo = cursor.fetchone() # recebe dados de "veiculo"
                if not veiculo:
                    messagebox.showerror("Erro", f"Veículo com ID {veiculo_id} não encontrado.")
                    return None
                modelo_veiculo, valor_diaria = veiculo # cria variaveis para as keys
                # cálculos temporais
                data_inicio_obj = datetime.strptime(data_inicio, "%Y-%m-%d")
                data_fim_obj = datetime.strptime(data_fim, "%Y-%m-%d")
                numero_dias = (data_fim_obj - data_inicio_obj).days
                periodo_aluguer = str(numero_dias) + " dias"
                valor_total = numero_dias * valor_diaria
                dados_pagamento = {
                    "id_reserva": id_reserva,
                    "nome": nome_cliente,
                    "email": email_cliente,
                    "modelo": modelo_veiculo,
                    "periodo_aluguer": periodo_aluguer,
                    "forma_pagamento": forma_pagamento,
                    "valor_€": valor_total
                }
                messagebox.showinfo("Sucesso", "Dados da reserva encontrados.")
                return dados_pagamento # dicionário final para inserir na tabela pagamento com os dados filtrados
            except sqlite3.Error as e:
                print(f"Erro ao obter os dados da reserva: {e}")
                return None

        def verificar_existencia_pagamento(id_reserva):
            try:
                with sqlite3.connect(self.db) as con:
                    cursor = con.cursor()
                    cursor.execute("SELECT id_reserva FROM pagamento WHERE id_reserva = ?",
                                    (id_reserva,))
                    pagamento_existente = cursor.fetchone()
                    if pagamento_existente:
                        return True
                    else:
                        return False
            except sqlite3.Error as e:
                print(f"Erro ao verificar a existência de pagamento: {e}")
                return True

        def salvar_pagamento():
            dados_pagamento = buscar_reserva()
            if not dados_pagamento:
                return
            try:
                id_reserva = dados_pagamento["id_reserva"]
                if verificar_existencia_pagamento(id_reserva):
                    messagebox.showwarning("Aviso", "Já existe um pagamento registado para esta reserva.")
                    return
                else:
                    nome = dados_pagamento["nome"]
                    email = dados_pagamento["email"]
                    modelo = dados_pagamento["modelo"]
                    periodo_aluguer = dados_pagamento["periodo_aluguer"]
                    forma_pagamento = dados_pagamento["forma_pagamento"]
                    valor_total = dados_pagamento["valor_€"]
                    with sqlite3.connect(self.db) as con:
                        cursor = con.cursor()
                        cursor.execute(
                            "INSERT INTO pagamento (id_reserva, nome_cliente, email_cliente, modelo,"
                            " periodo_aluguer, forma_pagamento, valor_€) VALUES (?, ?, ?, ?, ?, ?, ?)",
                            (id_reserva, nome, email, modelo, periodo_aluguer, forma_pagamento, valor_total))
                        con.commit()
                        messagebox.showinfo("Sucesso", "Dados de pagamento salvos com sucesso.")
            except sqlite3.Error as e:
                print(f"Erro ao salvar os dados de pagamento: {e}")
        # configurações da janela
        nova_janela = tk.Toplevel()
        nova_janela.title("Registar Pagamento")
        nova_janela.geometry("240x170")
        nova_janela.config(bg=self.cor1)
        estilo_label_Titulos_quadros = ("Verdana Bold", 12)
        label_clientes_registar = ttk.Label(nova_janela, text="Registar Pagamentos", font=estilo_label_Titulos_quadros,
                                            background=self.cor1, foreground="white")
        label_clientes_registar.place(x=20, y=10, width=200, height=30)
        # campo de busca do ID
        id_reserva_label = ttk.Label(nova_janela, text="Insira o ID da Reserva:", background=self.cor1,
                                     foreground="white")
        id_reserva_label.place(x=20, y=50)
        id_reserva_entry = ttk.Entry(nova_janela)
        id_reserva_entry.place(x=20, y=80, width=200)

        buscar_button = tk.Button(nova_janela, text="Buscar", command=buscar_reserva, relief=tk.FLAT, bg=self.cor2)
        buscar_button.place(x=145, y=80, width=80, height=21)
        # Botão salvar
        salvar_button = tk.Button(nova_janela, text="Guardar Pagamento", command=salvar_pagamento,
                                   relief=tk.FLAT, bg=self.cor2)
        salvar_button.place(x=20, y=120)

