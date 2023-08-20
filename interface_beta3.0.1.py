# ------------------------------------------------------------
import os
import sqlite3 as lite
import asyncio
import aiohttp
import datetime
import customtkinter
import matplotlib.pyplot as plt
# ------------------------------------------------------------
from tkinter import filedialog as fd
from PIL import Image, ImageDraw, ImageFilter
from tkinter import messagebox
from customtkinter import *
import random
# minha chave da api------------------------------------------
API_KEY = '8cd78d19081f93d321e5db39e8ef13cb'
# Definindo cores e outras constantes--------------------------
laranja = '#ff3c00'
azul = '#2453ff'
amarelo = '#0b005e'
vermelho = '#c20404'
verde = '#015e0d'
preto = '#151716'
branco = '#c9c9c9'
azul_claro = '#1cb7ff'
# dicionario com a quantidade de agua que cada planta precisa por dia em litros por hectares------------------------
PlantasInfos = {
    'ALFACE': 100000,
    'ALMEIRÃO': 100000,
    'BATATA': 100000,
    'BERINJELA': 100000,
    'BETERRABA': 100000,
    'BROCOLIS': 100000,
    'CENOURA': 100000,
    'CEBOLA': 100000,
    'COUVE': 100000,
    'COUVE-FLOR': 100000,
    'ESPINAFRE': 100000,
    'FEIJÃO': 100000,
    'TOMATE':  100000,
    'PIMENTÃO': 100000,
    'CAFÉ': 100000,
}
# atribuindo imagens para a previsao do tempo-------------------------
icone_map = {
    "céu limpo": "sol.png",
    "nuvens dispersas": "nuvem_sol.png",
    "nuvens": "nuvem.png",
    "chuva": "chuva_leve.png",
    "tempestade": "chuva_Forte.png",
    "chuva com trovões ": "chuva_com_trovoes.png",
    "poucas nuvens": "poucas_nuvens.png",
    "chuva leve": "chuva_leve.png",
    "nuvens quebradas": "chuva_Forte.png",
    'nublado': 'poucas_nuvens.png',
    'parcialmente nublado': 'nuvem_sol.png',
    'algumas nuvens': 'poucas_nuvens.png',
    'chuva moderada': 'chuva_Forte.png'
}
# criando o banco caso não exista------------------------------------------------
con = lite.connect('water.db')  # Nome do banco
with con:
    cursor = con.cursor()  # Criando o cursor
    cursor.execute("CREATE TABLE IF NOT EXISTS Usuarios (apelido TEXT PRIMARY KEY, Nome TEXT, Sobrenome TEXT, idade TEXT, email TEXT, cidade TEXT, sigla_pais TEXT, Senha TEXT, imagem_perfil TEXT)")  # Primeira tabela
    cursor.execute("CREATE TABLE IF NOT EXISTS Plantacoes (id INTEGER PRIMARY KEY,User TEXT, Planta_Nome TEXT, Tamanho INTEGER, Cultura TEXT, FOREIGN KEY(User) REFERENCES Usuarios(apelido) ON DELETE CASCADE)")
    cursor.execute("CREATE TABLE IF NOT EXISTS Sensores (ident INTEGER PRIMARY KEY, id_plantacao INTEGER, absorsao INTEGER, FOREIGN KEY(id_plantacao) REFERENCES Plantacoes(id) ON DELETE CASCADE)")

# -----------------------------------------------------------------------------------
class WaterFriendlyApp:
    # construtor da classe------------------------------------------------------
    def __init__(self, root):
        self.root = root
        self.root.title("Water friendly")
        self.root.geometry("800x600")
        self.root.resizable(width=False, height=False)
        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("dark-blue")
        self.create_frames()
        self.loop = asyncio.get_event_loop()
        self.MMchuva = 0
    #adicionar os sensores-----------------------------------------------------
    def Adicionar_Sensores(self, Quantidade, id):
        conn = lite.connect('water.db')  # Abrir a conexão com o banco de dados
        cursorr = conn.cursor()  # Criar um cursor para executar as consultas
        # Habilitar as chaves estrangeiras
        cursorr.execute("PRAGMA foreign_keys = ON")
        for i in range(0, Quantidade):
            cursorr.execute("INSERT INTO Sensores (id_plantacao, absorsao) VALUES (?, ?)",
                            (id, random.randint(1, 10)))  # Inserir os dados na tabela
        conn.commit()  # Salvar as alterações no banco de dados
        conn.close()  # Fechar a conexão com o banco de dados
    #atualizar os sensores-----------------------------------------------------
    def Renovar_Sensores(self, Quantidade, id):
        con = lite.connect('water.db')  # Abrir a conexão com o banco de dados
        cursor = con.cursor()  # Criar um cursor para executar as consultas
        # Habilitar as chaves estrangeiras
        cursor.execute("PRAGMA foreign_keys = ON")
        # Consulta para obter a quantidade de sensores
        cursor.execute(
            "SELECT COUNT(*) FROM Sensores WHERE id_plantacao = ?", (id,))
        QuantidadeAtual = cursor.fetchone()[0]
        sensores = cursor.execute(
            'SELECT * FROM Sensores WHERE id_plantacao = ?', (id,)).fetchall()
        if QuantidadeAtual < Quantidade:
            for i in range(0, Quantidade - QuantidadeAtual):
                cursor.execute(
                    "INSERT INTO Sensores (id_plantacao, absorsao) VALUES (?, ?)", (id, random.randint(1, 10)))
        elif QuantidadeAtual > Quantidade:
            for i in range(0, QuantidadeAtual - Quantidade):
                id_sensor = sensores[i][0]
                cursor.execute(
                    "DELETE FROM Sensores WHERE ident = ?", (id_sensor,))
        con.commit()  # Salvar as alterações no banco de dados
        con.close()  # Fechar a conexão com o banco de dados
    #agua absorvida pelo solo---------------------------------------------------
    def AguaChuva(self, id, planta_nome, usuario_logado):
        con = lite.connect('water.db')
        cursor = con.cursor()
        # Consulta para obter a quantidade de sensores
        cursor.execute(
            "SELECT COUNT(*) FROM Sensores WHERE id_plantacao = ?", (id,))
        quant = cursor.fetchone()[0]
        # Consulta para obter os sensores
        cursor.execute("SELECT * FROM Sensores WHERE id_plantacao = ?", (id,))
        Sensores = cursor.fetchall()

        # Consulta para obter o tamanho da área da planta
        cursor.execute("SELECT Tamanho FROM Plantacoes WHERE User=? AND Planta_Nome=?",
                       (usuario_logado, planta_nome))
        resultado = cursor.fetchone()
        tamanho_area_planta_1 = resultado[0]
        con.close()
        AguaTotal = 0
        div = int(tamanho_area_planta_1) * 10000 / quant
        for i in range(0, quant):
            # Obtém o valor da absorção aleatória
            variacao = Sensores[i][2] * 0.1
            # Multiplica pela absorção correspondente (de 0.1 a 1.0)
            AguaTotal += self.MMchuva * div * variacao

        return AguaTotal
    #exibir frame login---------------------------------------------------------
    def create_frames(self):
        self.frame_right = CTkFrame(master=self.root, width=400, height=596)
        self.frame_right.pack(side=RIGHT)
        self.frame_left = CTkFrame(
            master=self.root, width=400, height=596, fg_color=preto)
        self.frame_left.pack(side=LEFT)
        # Editando o frame-------------------------------------------------------
        wf = customtkinter.CTkImage(light_image=Image.open(
            'logo.png'), dark_image=Image.open('logo.png'), size=(150, 150))
        label_logo = customtkinter.CTkLabel(
            master=self.frame_right, image=wf, text='')
        label_logo.place(x=120, y=20)
        # Editando o entry de usuario--------------------------------------------
        self.entry_usuario = customtkinter.CTkEntry(master=self.frame_right, width=350,
                                                    font=('Josefin Sans bold', 14), placeholder_text='Nome de usuário')
        self.entry_usuario.place(x=25, y=200)
        # Editando o entry da senha-----------------------------------------------
        self.entry_senha = customtkinter.CTkEntry(master=self.frame_right, width=350,
                                                  font=('Josefin Sans bold', 14), placeholder_text='Senha', show='*')
        self.entry_senha.place(x=25, y=270)
        # Botão de login----------------------------------------------------------
        btn_login = customtkinter.CTkButton(master=self.frame_right, text='Login', width=350,
                                            font=('Josefin Sans bold', 15), fg_color=laranja, text_color=branco, command=self.fazer_login)
        btn_login.place(x=25, y=390)
        # check--box para mostrar a senha-----------------------------------------
        self.check_box = customtkinter.CTkCheckBox(
            master=self.frame_right, text='Mostrar senha', command=self.mostrar_senha, font=('Josefin Sans bold', 14))
        self.check_box.place(x=25, y=330)
        # Label de cadastro-------------------------------------------------------
        label_cadastro = customtkinter.CTkLabel(master=self.frame_left, text='Não tem uma conta?', font=(
            'Josefin Sans bold', 25), text_color=laranja, bg_color=preto)
        label_cadastro.place(x=70, y=200)
        label_cadastro2 = customtkinter.CTkLabel(
            master=self.frame_left, text='Cadastre-se agora', bg_color=preto, font=('Josefin Sans bold', 20))
        label_cadastro2.place(x=100, y=250)
        # Botão de cadastro-------------------------------------------------------
        botao_cadastro = customtkinter.CTkButton(master=self.frame_left, text='CADASTRAR', width=200, font=(
            'Josefin Sans bold', 12), fg_color=laranja, command=self.create_registration_page)
        botao_cadastro.place(x=90, y=300)
    # verificar se o usuario e senha estao corretos----------------------------
    def verificar_credenciais(self, usuario, senha):
        try:
            con = lite.connect('water.db')  # conecta com o banco de dados
            cursor = con.cursor()  # cria um cursor para executar as consultas
            # consulta para verificar se o usuario e senha estao corretos no banco de dados
            consulta = "SELECT * FROM Usuarios WHERE apelido = ? AND Senha = ?"
            cursor.execute(consulta, (usuario, senha))  # executa a consulta
            resultado = cursor.fetchone()  # retorna uma tupla com os dados do usuario
            cursor.close()  # fecha o cursor
            con.close()  # fecha a conexão com o banco de dados
            return resultado is not None  # retorna True se o usuário existe e False se não existe
        except lite.Error as e:
            messagebox.showerror('Erro no Banco de Dados',
                                 f"Ocorreu um erro no banco de dados: {e}")  # mostra uma mensagem de erro caso ocorra um erro no banco de dados
            return False  # retorna False
    # mostrar a senha do usuario caso ele queira----------------------------------
    def mostrar_senha(self):
        if self.check_box.get() == 1:  # pega o valor do check box e verifica se ele esta marcado com o 1
            self.entry_senha.configure(show='')  # mostra a senha sem os *
        else:
            # senão mostra a senha com os *
            self.entry_senha.configure(show='*')
    # verificar e ir adiante-----------------------------------------------------
    def fazer_login(self):
        # variavel global para armazenar o usuario logado e busca-lo futuramente
        global usuario_logado
        usuario = self.entry_usuario.get()  # pega o usuario digitado
        senha = self.entry_senha.get()  # pega a senha digitada
        if not usuario or not senha:  # verifica se o campo de usuario e senha foram digitados
            # mostra uma mensagem de aviso
            messagebox.showwarning('Login', 'Preencha todos os campos!')
            return  # retorna pra nao executar o resto do codigo
        if usuario == 'admin' and senha == 'admin':  # verifica se o usuario e senha são iguais a admin
            # mostra uma mensagem de boas vindas
            messagebox.showinfo('Login', 'Seja bem-vindo, Admin!')
            self.tela_gerenciamento()  # chama a tela de gerenciamento
        # verifica se o usuario e senha estão corretos chamando a função verificar_credenciais do banco
        elif self.verificar_credenciais(usuario, senha):
            usuario_logado = usuario  # armazena o usuario na variavel global
            # mostra uma mensagem de boas vindas
            messagebox.showinfo('Login', f'Seja bem-vindo, {usuario}!')
            self.tela_gerenciamento()  # chama a tela de gerenciamento
        else:
            # mostra uma mensagem de aviso caso o usuario ou senha estejam incorretos
            messagebox.showwarning('Login', 'Usuário ou senha incorretos')
    # destroi o frame anterior---------------------------------------------------
    def destruir_frame(self):
        for frame in root.winfo_children():  # Itera pelos frames
            frame.destroy()  # Destroi o frame atual
    # cria a tela de cadastro----------------------------------------------------
    def create_registration_page(self):
        self.frame_right.pack_forget()  # esquecer o frame do login
        self.frame_left.pack_forget()  # esquecer o frame do login
        # Criando a tela nova-----------------------------------------------------
        frame_cadastro_inteiro = customtkinter.CTkFrame(
            master=self.root, width=800, height=596)
        frame_cadastro_inteiro.pack()
        # Editando o frame--------------------------------------------------------
        label_cadastro = customtkinter.CTkLabel(master=frame_cadastro_inteiro, text='CADASTRO :',
                                                font=('Josefin Sans bold', 30), text_color=laranja)
        label_cadastro.place(x=25, y=45)
        # Editando o entry de usuario---------------------------------------------
        self.entry_usuario_1 = customtkinter.CTkEntry(
            master=frame_cadastro_inteiro, width=350, placeholder_text='Usuário')
        self.entry_usuario_1.place(x=25, y=140)
        # Editando o entry do nome------------------------------------------------
        self.entry_nome = customtkinter.CTkEntry(
            master=frame_cadastro_inteiro, width=350, placeholder_text='Nome')
        self.entry_nome.place(x=25, y=210)
        # Editando o entry do sobrenome--------------------------------------------
        self.entry_sobrenome = customtkinter.CTkEntry(
            master=frame_cadastro_inteiro, width=350, placeholder_text='Sobrenome')
        self.entry_sobrenome.place(x=25, y=270)
        # editando o entry da idade------------------------------------------------
        self.entry_idade = customtkinter.CTkEntry(
            master=frame_cadastro_inteiro, width=350, placeholder_text='Idade')
        self.entry_idade.place(x=25, y=340)
        # editando o entry do Email------------------------------------------------
        self.entry_email = customtkinter.CTkEntry(
            master=frame_cadastro_inteiro, width=350, placeholder_text='Email')
        self.entry_email.place(x=400, y=140)
        # editando o entry da cidade------------------------------------------------
        self.entry_cidade = customtkinter.CTkEntry(
            master=frame_cadastro_inteiro, width=350, placeholder_text='Cidade')
        self.entry_cidade.place(x=400, y=210)
        # sigla do Pais-------------------------------------------------------------
        self.entry_pais = customtkinter.CTkEntry(
            master=frame_cadastro_inteiro, width=350, placeholder_text='Sigla do País')
        self.entry_pais.place(x=400, y=270)
        # editando o entry da senha------------------------------------------------
        self.entry_senha_1 = customtkinter.CTkEntry(
            master=frame_cadastro_inteiro, width=350, placeholder_text='Senha', show='*')
        self.entry_senha_1.place(x=400, y=340)
        # editando o entry da confirmar senha--------------------------------------
        self.entry_confirmar_senha = customtkinter.CTkEntry(
            master=frame_cadastro_inteiro, width=350, placeholder_text='Confirmar senha', show='*')
        self.entry_confirmar_senha.place(x=400, y=400)
        # botao de cadastrar-------------------------------------------------------
        self.botao_cadastrar = customtkinter.CTkButton(
            master=frame_cadastro_inteiro, height=0, text='CADASTRAR', width=200,
            font=('Josefin Sans bold', 14), fg_color=laranja, command=self.avancar_pagina)
        self.botao_cadastrar.place(x=400, y=500)
        self.botao_cadastrar.configure(corner_radius=10)
        # botao de voltar----------------------------------------------------------

        def voltar_login():
            frame_cadastro_inteiro.pack_forget()  # esquecer o frame do cadastro
            # recriar os frames do login
            self.frame_right.pack(side=RIGHT)
            self.frame_left.pack(side=LEFT)
        # botao de voltar----------------------------------------------------------
        botao_voltar = customtkinter.CTkButton(master=frame_cadastro_inteiro, height=0, text='VOLTAR', width=200, font=(
            'Josefin Sans bold', 14), fg_color=amarelo, command=voltar_login)
        botao_voltar.place(x=160, y=500)
        botao_voltar.configure(corner_radius=10)  # arredondar o botao
    # Função para cadastrar no banco de dados a partir da tela de cadastro---------
    def cadastrar_no_banco(self):
        # Pegar os valores dos campos do cadastro-------------------------
        usuario_1 = self.entry_usuario_1.get()
        nome = self.entry_nome.get()
        sobrenome = self.entry_sobrenome.get()
        idade = self.entry_idade.get()
        email = self.entry_email.get()
        cidade = self.entry_cidade.get()
        pais = self.entry_pais.get()
        senha_1 = self.entry_senha_1.get()
        imagem_perfil = 'usuario.png'
        con = lite.connect('water.db')  # Abrir a conexão com o banco de dados
        cursor = con.cursor()  # Criar um cursor para executar as consultas
        try:
            # Verificar se o apelido já existe no banco de dados (se já existe, não pode cadastrar)
            cursor.execute(
                "SELECT * FROM Usuarios WHERE apelido = ?", (usuario_1,))  # Consulta para verificar se o apelido já existe
            existing_user = cursor.fetchone()  # Retorna uma tupla com os dados do usuário
            if existing_user:  # Se o apelido já existe, não pode cadastrar e mostra uma mensagem de erro
                messagebox.showerror(
                    'Cadastro', 'O apelido já está em uso. Escolha outro apelido.')
                con.close()  # Fechar a conexão com o banco de dados
                # Permanecer na página de cadastro
                return False  # Retorna False e não continua o código
            else:
                cursor.execute("INSERT INTO Usuarios VALUES(?,?,?,?,?,?,?,?,?)",  # Inserir os dados no banco de dados a partir do comando INSERT INTO
                               (usuario_1, nome, sobrenome, idade, email, cidade, pais, senha_1, imagem_perfil))  # Os valores são passados como uma tupla
                con.commit()  # Salvar as alterações no banco de dados
                messagebox.showinfo(
                    'Cadastro', 'Cadastro realizado com sucesso!')  # Mostrar uma mensagem de sucesso
                return True  # Retorna True e continua o código
        except:
            # Mostrar uma mensagem de erro caso ocorra um erro no banco de dados
            messagebox.showerror('Cadastro', 'Erro ao cadastrar!')
            return False  # Retorna False e não continua o código
        finally:  # Executa o código abaixo, independente se ocorreu um erro ou não para fecha a conexão com o banco de dados
            con.close()
    # avancar para a tela de gerenciamento depois do botao de cadastrar-----------
    def avancar_pagina(self):
        # Pegar os valores dos campos do cadastro-------------------------
        usuario_1 = self.entry_usuario_1.get()
        nome = self.entry_nome.get()
        sobrenome = self.entry_sobrenome.get()
        idade = self.entry_idade.get()
        email = self.entry_email.get()
        cidade = self.entry_cidade.get()
        pais = self.entry_pais.get()
        senha_1 = self.entry_senha_1.get()
        # Verificar se todos os campos foram preenchidos----------------------------
        if any(not field for field in [usuario_1, nome, sobrenome, idade, email, cidade, pais, senha_1]):
            messagebox.showerror('Cadastro', 'Preencha todos os campos!')

        elif senha_1 != self.entry_confirmar_senha.get():  # Verificar se as senhas são iguais
            messagebox.showerror(
                'Cadastro', 'As senhas não coincidem! Tente novamente.')

        elif len(senha_1) < 8:  # Verificar se a senha tem pelo menos 8 caracteres
            messagebox.showerror(
                'Cadastro', 'A senha deve ter no mínimo 8 caracteres!')

        elif int(idade) < 18:  # Verificar se a idade é maior que 18
            messagebox.showerror(
                'Cadastro', 'Você deve ter mais de 18 anos para se cadastrar!')
        else:
            # Se a função cadastrar_no_banco() retornar False, não avança
            if not self.cadastrar_no_banco():
                return
            # Se a função cadastrar_no_banco() retornar True, avança
            # Variável global para armazenar o usuário logado e buscá-lo futuramente
            global usuario_logado
            usuario_logado = usuario_1  # Armazena o usuário na variável global
            self.tela_gerenciamento()  # Chama a tela de gerenciamento
    # criando a tela de gerenciamento--------------------------------------------
    def tela_gerenciamento(self):
        # Destruindo o frame anterior
        self.destruir_frame()
        # Criando a tela nova--------------------------------------------
        frame_gerenciamento_inteiro = customtkinter.CTkFrame(
            master=self.root, width=800, height=596)
        frame_gerenciamento_inteiro.pack()
        frame_corzinha = customtkinter.CTkFrame(
            master=frame_gerenciamento_inteiro, width=600, height=130, border_width=5)
        frame_corzinha.place(x=80, y=160)
        # Editando o frame--------------------------------------------
        label_gerenciamento = customtkinter.CTkLabel(
            master=frame_gerenciamento_inteiro, text='GERENCIAMENTO ', font=('Josefin Sans bold', 30), text_color=laranja)
        label_gerenciamento.place(x=50, y=25)
        # Botão de perfil--------------------------------------------
        self.botao_perfil = customtkinter.CTkButton(
            master=frame_corzinha, text='PERFIL', width=100, font=('Josefin Sans bold', 14), fg_color=laranja, command=self.tela_perfil)
        self.botao_perfil.place(x=50, y=40)
        self.botao_perfil.configure(corner_radius=10)
        # Botão de minha plantação--------------------------------------------
        self.botao_minhaplantacao = customtkinter.CTkButton(
            master=frame_corzinha, command=self.tela_minhaplantacao, text='MINHA PLANTAÇÃO', width=100, font=('Josefin Sans bold', 14), fg_color=laranja)
        self.botao_minhaplantacao.place(x=300, y=40)
        self.botao_minhaplantacao.configure(corner_radius=10)
        # Botão de logout--------------------------------------------

        def logout():
            self.destruir_frame()  # Destruir o frame atual
            self.create_frames()  # Criar os frames do login novamente
        # botao de logout --------------------------------------------
        self.botao_logout = customtkinter.CTkButton(
            master=frame_gerenciamento_inteiro, command=logout, text='SAIR', width=100, font=('Josefin Sans bold', 14), fg_color=vermelho)
        self.botao_logout.place(x=200, y=500)
    # criando a tela de perfil---------------------------------------------------
    def tela_minhaplantacao(self):
        self.destruir_frame()  # Destruindo o frame anterior
        self.frame_myplant = customtkinter.CTkFrame(  # Criando o frame
            master=self.root, width=800, height=596)
        self.frame_myplant.pack()
        self.frame_corzao = customtkinter.CTkFrame(
            master=self.frame_myplant, width=700, height=400, border_width=5)
        self.frame_corzao.place(x=50, y=150)
        self.exibir_plantas()  # chamando a função para exibir os botões das plantas

        # Editando o frame--------------------------------------------
        label_minhaplantacao = customtkinter.CTkLabel(
            master=self.frame_myplant, text='MINHA PLANTAÇÃO', font=('Josefin Sans bold', 30), text_color=laranja)
        label_minhaplantacao.place(x=50, y=5)
        # Botão de adicionar plantação--------------------------------------------
        botao_adicionar_crud = customtkinter.CTkButton(master=self.frame_myplant, command=self.adicionar_area, text='ADICIONAR', width=100, font=(
            'Josefin Sans bold', 12), fg_color=verde)
        botao_adicionar_crud.place(x=50, y=95)
        # Botão de remover plantação--------------------------------------------
        botao_voltar = customtkinter.CTkButton(master=self.frame_myplant, command=self.tela_gerenciamento, text='VOLTAR', width=100, font=(
            'Josefin Sans bold', 12), fg_color=amarelo)
        botao_voltar.place(x=170, y=95)
    # criando a tela de perfil---------------------------------------------------
    def salvar_area(self):
        tamanho = self.entry_area.get()  # pega o tamanho da area
        plantacao_Nome = self.Entry_Nome.get().upper()  # pega o nome da planta
        Cultura = self.ComboBox_Cultuta.get()  # pega a cultura
        Quantidade = self.entry_Sensores.get()
        con = lite.connect('water.db')  # Abrir a conexão com o banco de dados
        cursor = con.cursor()  # Criar um cursor para executar as consultas
        # Habilitar as chaves estrangeiras
        cursor.execute("PRAGMA foreign_keys = ON")
        if not tamanho and not plantacao_Nome and not Cultura:  # Verificar se os campos foram preenchidos
            messagebox.showwarning(
                'Erro no Cadastro', 'Preencha todos os campos!')  # Mostrar uma mensagem de aviso
            return  # Retorna pra não executar o resto do código
        try:
            cursor.execute("INSERT INTO Plantacoes (User, Planta_Nome, tamanho, Cultura) VALUES (?, ?, ?, ?)",  # Inserir os dados no banco de dados a partir do comando INSERT INTO
                           (usuario_logado, plantacao_Nome, tamanho, Cultura))  # Os valores são passados como uma tupla
            con.commit()
            self.Adicionar_Sensores(int(Quantidade), cursor.lastrowid)
            messagebox.showinfo(
                'Cadastro', 'Cadastro realizado com sucesso!')  # Mostrar uma mensagem de sucesso
            # Após cadastrar a planta, chame a função para exibir as plantas novamente
            self.exibir_plantas()
        except:
            # Mostrar uma mensagem de erro caso ocorra um erro no banco de dados
            messagebox.showerror('Cadastro', 'Erro ao cadastrar!')
        con.close()  # Fechar a conexão com o banco de dados
    # exibir as plantas cadastradas----------------------------------------------
    def adicionar_area(self):
        self.frame_myplant.pack_forget()  # Destruindo o frame anterior
        # Criando a tela nova--------------------------------------------
        self.frame_adicionar_area = customtkinter.CTkFrame(
            master=self.root, width=800, height=596)
        self.frame_adicionar_area.pack()
        # Editando o frame--------------------------------------------
        self.entry_area = customtkinter.CTkEntry(
            master=self.frame_adicionar_area, width=300, placeholder_text='Tamanho da área da cultura em hectares')
        self.entry_area.place(x=25, y=200)
        # Editando o frame--------------------------------------------
        self.Entry_Nome = customtkinter.CTkEntry(
            master=self.frame_adicionar_area, width=300, placeholder_text='Nome do botão')
        self.Entry_Nome.place(x=350, y=200)
        self.entry_Sensores = customtkinter.CTkEntry(
            master=self.frame_adicionar_area, width=300, placeholder_text='Quantidade de sensores')
        self.entry_Sensores.place(x=25, y=300)
        self.ComboBox_Cultuta = customtkinter.CTkComboBox(
            master=self.frame_adicionar_area, width=300, values=list(PlantasInfos.keys()))
        self.ComboBox_Cultuta.set('Selecione a cultura')
        self.ComboBox_Cultuta.place(x=350, y=300)
        # Editando o frame--------------------------------------------
        label_adicionar_area = customtkinter.CTkLabel(
            master=self.frame_adicionar_area, text='ADICIONAR ÁREA :', font=('Josefin Sans bold', 30), text_color=laranja)
        label_adicionar_area.place(x=25, y=3)
        # Botão de salvar--------------------------------------------
        botao_salvar = customtkinter.CTkButton(master=self.frame_adicionar_area, text='SALVAR', width=150,
                                               font=('Josefin Sans bold', 14), fg_color=laranja, command=self.salvar_area)
        botao_salvar.place(x=360, y=450)

        def botao_voltar():  # Função para voltar para a tela de gerenciamento
            self.frame_adicionar_area.pack_forget()  # esquecer o frame de adicionar area
            self.frame_myplant.pack()  # mostrar o frame de gerenciamento
        # Botão de voltar--------------------------------------------
        botaovoltar = customtkinter.CTkButton(master=self.frame_adicionar_area, command=botao_voltar,
                                              text='VOLTAR', width=150, font=('Josefin Sans bold', 14), fg_color=amarelo)
        botaovoltar.place(x=190, y=450)
    # exibir as plantas cadastradas----------------------------------------------
    def acessar_planta(self, planta_nome):
        # Destruindo o frame anterior----------------------
        self.frame_myplant.pack_forget()
        # Criando a tela nova-----------------------------
        self.frame_planta = customtkinter.CTkFrame(
            root, width=800, height=596)
        self.frame_planta.pack()
        # Editando o frame-----------------------------
        label_planta = customtkinter.CTkLabel(master=self.frame_planta, text=planta_nome, font=(
            'Josefin Sans bold', 30), text_color=laranja)
        label_planta.place(x=70, y=5)
        # Botão de voltar-----------------------------
        botao_voltar_5 = customtkinter.CTkButton(master=self.frame_planta, command=self.tela_minhaplantacao, text='VOLTAR', width=100, font=(
            'Josefin Sans bold', 14), fg_color=amarelo)
        botao_voltar_5.place(x=70, y=500)
        # Botão de remover-----------------------------
        botao_remover_planta = customtkinter.CTkButton(master=self.frame_planta, text='REMOVER', width=100, font=(
            'Josefin Sans bold', 14), fg_color=vermelho, command=lambda: self.remover_planta(planta_nome))
        botao_remover_planta.place(x=370, y=500)
        # Conectando no banco de dados-------------------------------------
        botao_update_2 = customtkinter.CTkButton(master=self.frame_planta, text='ATUALIZAR', command=lambda: self.alterar_tamanho(planta_nome), width=100, font=(
            'Josefin Sans bold', 14), fg_color=azul)
        botao_update_2.place(x=220, y=500)
        # Criando o tabview------------------------------------
        tabview = customtkinter.CTkTabview(
            master=self.frame_planta, width=690, height=400)
        tabview.place(x=70, y=75)
        tabview.add("Informações")  # Adicionando as abas
        tabview.add("Tempo")  # Adicionando as abas
        tabview.add("Irrigação")  # Adicionando as abas
        tabview.tab('Informações').grid_columnconfigure(
            0, weight=1)  # Configurando o grid
        tabview.tab('Tempo').grid_columnconfigure(
            0, weight=1)  # Configurando o grid
        tabview.tab('Irrigação').grid_columnconfigure(
            0, weight=1)  # Configurando o grid
        # ------------------------------------------------
        con = lite.connect('water.db')  # Abrir a conexão com o banco de dados
        cursor = con.cursor()  # Criar um cursor para executar as consultas
        # Consulta para obter a área total de todas as culturas do usuário-------------------------
        cursor.execute(
            "SELECT SUM(Tamanho) FROM Plantacoes WHERE User=?", (usuario_logado,))  # Consulta para obter a área total de todas as culturas do usuário
        area_total = cursor.fetchone()[0]  # Área total de todas as culturas
        # Consulta para obter a área da planta ESPECÍFICA selecionada
        cursor.execute("SELECT Tamanho FROM Plantacoes WHERE User=? AND Planta_Nome=?",  # Consulta para obter a área da planta ESPECÍFICA selecionada
                       (usuario_logado, planta_nome))
        area_planta = cursor.fetchone()[0]  # Área da planta específica
        con.close()  # Fechar a conexão com o banco de dados
        # editando o tabview de informaçoes---------------------------------------------------------
        l_area = customtkinter.CTkLabel(master=tabview.tab('Informações'), text='Área da planta:', font=(
            'Josefin Sans bold', 14), text_color=laranja)
        l_area.place(x=20, y=20)
        # editando o tabview de informaçoes---------------------------------------------------------
        l_area_planta = customtkinter.CTkLabel(master=tabview.tab('Informações'), text=f"{area_planta} Ha", font=(
            'Josefin Sans bold', 14), text_color=branco)
        l_area_planta.place(x=150, y=20)
        # crinado o grafico de area-------------------------------------------------------------------
        fig, ax = plt.subplots(figsize=(10, 10))
        labels = ['Área total', 'Área da planta']
        ax.pie([area_total-area_planta, area_planta], autopct='%1.1f%%',
               textprops={'fontsize': 30, 'color': 'white'}, colors=[azul_claro, laranja])
        plt.legend(labels, fontsize="20", loc="upper right")
        ax.axis('equal')
        plt.savefig('grafico.png', transparent=True)
        plt.close()
        # Criar a imagem--------------------------------------------------------------------------------------------------------------------------
        imagem_grafico = customtkinter.CTkImage(light_image=Image.open(
            'grafico.png'), dark_image=Image.open('grafico.png'), size=(250, 250))  # Criar a imagem
        # Posicionar a imagem
        label_imagem_grafico = customtkinter.CTkLabel(
            master=tabview.tab('Informações'), image=imagem_grafico, text='')  # Posicionar a imagem
        # Posicionar a imagem no tabview
        label_imagem_grafico.place(x=370, y=20)
        # conexao com o banco de dados--------------------------------------------------------------------------------------------
        con = lite.connect('water.db')  # Abrir a conexão com o banco de dados
        cursor = con.cursor()   # Criar um cursor para executar as consultas
        # Habilitar as chaves estrangeiras
        cursor.execute("PRAGMA foreign_keys = ON")
        cursor.execute(
            "SELECT * from Usuarios WHERE apelido = ? ", (usuario_logado,))  # Consulta para obter a cidade e o país do usuário
        resultado = cursor.fetchone()  # Retorna uma tupla com os dados do usuário
        cidade_2 = resultado[5]  # A cidade está na posição 5 da tupla
        pais_2 = resultado[6]  # O país está na posição 6 da tupla
        cursor.execute(
            "SELECT * FROM Plantacoes WHERE Planta_Nome = ?", (planta_nome,))
        resultado = cursor.fetchone()
        id = resultado[0]
        con.close()  # Fechar a conexão com o banco de dados
        # chamando a função de previsão do tempo e agua da chuva ---------------------------------------------------------
        # rodar de forma assincrona dentro de uma função normal
        asyncio.run(self.exibir_previsao(cidade_2, pais_2, tabview))
        # relatorio de irrigação---------------------------------------------------------
        b_dia_1 = customtkinter.CTkButton(master=tabview.tab("Irrigação"), text='Dia 1', width=100, font=(
            'Josefin Sans bold', 14), fg_color=azul, command=lambda: self.dia_1(planta_nome))
        b_dia_1.place(x=20, y=50)
        b_dia_2 = customtkinter.CTkButton(master=tabview.tab("Irrigação"), text='Dia 2', width=100, font=(
            'Josefin Sans bold', 14), fg_color=azul)
        b_dia_2.place(x=150, y=50)
        b_dia_3 = customtkinter.CTkButton(master=tabview.tab("Irrigação"), text='Dia 3', width=100, font=(
            'Josefin Sans bold', 14), fg_color=azul)
        b_dia_3.place(x=280, y=50)
        b_dia_4 = customtkinter.CTkButton(master=tabview.tab("Irrigação"), text='Dia 4', width=100, font=(
            'Josefin Sans bold', 14), fg_color=azul)
        b_dia_4.place(x=410, y=50)
        b_dia_5 = customtkinter.CTkButton(master=tabview.tab("Irrigação"), text='Dia 5', width=100, font=(
            'Josefin Sans bold', 14), fg_color=azul)
        b_dia_5.place(x=540, y=50)
    # assicronizar a previsão do tempo---------------------------------------------------
    async def exibir_previsao(self, cidade_2, pais_2, tabview):
        # url da previsao do tempo
        previsao_url = f'https://api.openweathermap.org/data/2.5/forecast?q={cidade_2},{pais_2}&appid={API_KEY}&lang=pt_br&units=metric&cnt=5'
        # criar uma sessão para fazer a requisição dos dados da api,com o Client ,não precisa do request pois o aiohttp já faz isso
        async with aiohttp.ClientSession() as session:
            # o session.get pega os dados HTTP da API, chama ele e transforma em uma variavel response pra ficar mais facil de trabalhar
            async with session.get(previsao_url) as response:
                previsao_data = await response.json()  # transforma a resposta da API em um dicionario com o json, o await espera a resposta da API, e depois transforma a resposta em um dicionario com o json, precisa esperar pegar todos os dados da API
                # await é sempre necessario quando for fazer uma requisição de uma API assincrona
        dia_atual = datetime.datetime.now()  # pegar a data atual
        # colocar agua da chuva---------------------------------------------------------
        if response.status == 200:  # se retornar 200, significa que a requisição foi bem sucedida
            # await espera a resposta da API, e depois transforma a resposta em um dicionario com o json, precisa esperar pegar todos os dados da API
            # se tiver chuva na previsao diaria
            if 'rain' in previsao_data['list'][0]:
                # pegar a quantidade de chuva em 3 horas pois é assim que a API retorna, a cada 3 horas
                chuva_3h = previsao_data['list'][0]['rain']['3h']
                # como estou rodando o programa poucas vezes, multiplico por 8 para ter uma quantidade de chuva diaria seria 3x8=24
                self.MMchuva = chuva_3h * 3
                # texto da chuva diaria---------------------------------------------------------
                texto_chuva_diaria = customtkinter.CTkLabel(master=tabview.tab(
                    "Irrigação"), text=f'Chuva diária: {self.MMchuva} mm', font=('Josefin Sans bold', 14), text_color=azul_claro)
                texto_chuva_diaria.place(x=30, y=5)  # Posiciona o texto
        # for pra criar a previsão do tempo---------------------------------------------------------
        for i in range(0, 5):
            previsao = previsao_data['list'][i]['weather'][0]['description']
            temperatura_previsao = previsao_data['list'][i]['main']['temp']
            # Data da previsão do tempo---------------------------------------------------------
            texto_Data_previsao = customtkinter.CTkLabel(master=tabview.tab(
                "Tempo"), text=f'{dia_atual.day+i}/{dia_atual.month}', font=('Josefin Sans bold', 14), text_color=branco)
            texto_Data_previsao.place(x=50+135*i, y=50)
            # Imagem da previsão do tempo---------------------------------------------------------
            imagem_previsao = customtkinter.CTkImage(light_image=Image.open(icone_map.get(
                previsao, "nuvem.png")), dark_image=Image.open(icone_map.get(previsao, "nuvem.png")), size=(70, 70))
            # Posiciona a imagem---------------------------------------------------------
            label_imagem_previsao = customtkinter.CTkLabel(
                master=tabview.tab("Tempo"), image=imagem_previsao, text='')
            label_imagem_previsao.place(x=40+130*i, y=80)
            # Quebrar linha de palavra composta---------------------------------------------------------
            previsao = previsao.replace(' ', '\n')
            texto_previsao = customtkinter.CTkLabel(master=tabview.tab(
                "Tempo"), text=previsao, font=('Josefin Sans bold', 14), text_color=azul_claro)
            texto_previsao.place(x=40+130*i, y=160)
            # Posiciona a temperatura---------------------------------------------------------
            texto_temp_previsao = customtkinter.CTkLabel(master=tabview.tab(
                "Tempo"), text=f'{temperatura_previsao:.2f}°C', font=('Josefin Sans bold', 14), text_color=branco)
            texto_temp_previsao.place(x=40+130*i, y=210)
    # funçao de remover a planta---------------------------------------------------
    def remover_planta(self, planta_nome):
        con = lite.connect('water.db')  # Abrir a conexão com o banco de dados
        cursor = con.cursor()  # Criar um cursor para executar as consultas
        # Habilitar as chaves estrangeiras
        cursor.execute("PRAGMA foreign_keys = ON")
        resposta_1 = messagebox.askyesno('Remover', 'Deseja remover a planta?')
        if resposta_1 == True:
            cursor.execute(
                "DELETE FROM Plantacoes WHERE Planta = ?", (planta_nome,))  # Remover a planta do banco de dados
            con.commit()  # Salvar as alterações no banco de dados com o comando commit
            con.close()  # Fechar a conexão com o banco de dados
            # adicionando a mensegem de sucesso
            messagebox.showinfo('Remoção', 'Planta removida com sucesso!')
            self.botao_planta.destroy()  # Remover o botão após a remoção da planta
            self.tela_minhaplantacao()  # Atualizar a tela
        else:
            return
    # exibir as plantas cadastradas----------------------------------------------
    def exibir_plantas(self):
        x_pos_planta = 40  # Posição inicial x do botão
        y_pos_planta = 40  # Posição inicial y do botão
        botao_width_planta = 100  # Largura do botão
        botao_height_planta = 40  # Altura do botão
        botao_margin_x_planta = 27  # Margem x entre os botões
        botao_margin_y_planta = 30  # Margem y entre os botões
        con = lite.connect('water.db')  # Conectando no banco de dados
        cursor = con.cursor()  # Criando o cursor
        cursor.execute(
            "SELECT Planta_Nome FROM Plantacoes WHERE User=?", (usuario_logado,))  # Obtendo as plantas do usuário, a partir da chave estrangeira
        plantas = cursor.fetchall()
        con.close()
        # Lógica do for : plantas é o resultado apartir do fetchall recupera todas as plantas do usuário e cria um botão ate que o número limites das
        # plantas seja atingido, por isso o uso do for
        for planta in plantas:
            self.botao_planta = customtkinter.CTkButton(master=self.frame_corzao, text=planta[0], width=botao_width_planta, font=(
                'Josefin Sans bold', 12), fg_color=laranja, command=lambda planta_nome=planta[0]: self.acessar_planta(planta_nome))  # Acessar a planta
            self.botao_planta.place(
                x=x_pos_planta, y=y_pos_planta)  # Posicionar o botão

            x_pos_planta += botao_width_planta + botao_margin_x_planta

            if x_pos_planta + botao_width_planta > 800:  # Verificar se o botão ultrapassou a largura da tela que é 700
                x_pos_planta = 40  # Posicionar o botão na posição inicial
                # atualizar o valor de y para que o botão seja posicionado na linha de baixo
                y_pos_planta += botao_height_planta + botao_margin_y_planta
    # tela de alterar o tamanho------------------------------------------------------------
    def alterar_tamanho(self, planta_nome):
        self.destruir_frame()
        # Criando a nova tela--------------------------------------------
        self.frame_alterar_tamanho = customtkinter.CTkFrame(
            master=self.root, width=800, height=596)
        self.frame_alterar_tamanho.pack()
        # Editando o frame--------------------------------------------
        label_alterar_tamanho = customtkinter.CTkLabel(
            master=self.frame_alterar_tamanho, text='ALTERAR TAMANHO',
            font=('Josefin Sans bold', 30), text_color=laranja)
        label_alterar_tamanho.place(x=25, y=3)
        # Editando a entrada do usuário--------------------------------------------
        self.entry_tamanho_2 = customtkinter.CTkEntry(
            master=self.frame_alterar_tamanho, width=300,
            placeholder_text='Tamanho da área da cultura em hectares')
        self.entry_tamanho_2.place(x=225, y=200)
        self.entry_Sensores2 = customtkinter.CTkEntry(
            master=self.frame_alterar_tamanho, width=300, placeholder_text='Quantidade de sensores')
        self.entry_Sensores2.place(x=225, y=300)
        # Função para salvar o tamanho----------------------------------------------
        def salvar_tamanho(planta_nome):
            novo_tamanho = self.entry_tamanho_2.get()  # Obter o novo tamanho da entrada
            Quantidade = self.entry_Sensores2.get()
            if not novo_tamanho:
                messagebox.showwarning(
                    'Erro no Cadastro', 'Preencha todos os campos!')
                return  # Sai da função se o campo estiver vazio
            # Conectar ao banco de dados e executar a atualização---------------------
            con = lite.connect('water.db')
            cursor = con.cursor()
            cursor.execute("PRAGMA foreign_keys = ON")
            cursor.execute("UPDATE Plantacoes SET tamanho = ? WHERE User = ? AND Planta_Nome = ?", (
                novo_tamanho, usuario_logado, planta_nome))  # Atualizar o tamanho da planta
            con.commit()  # Salvar as alterações
            id = cursor.execute("SELECT id FROM Plantacoes WHERE User = ? AND Planta_Nome = ?", (
                usuario_logado, planta_nome)).fetchone()[0]
            self.Renovar_Sensores(int(Quantidade), id)
            con.close()  # Fechar a conexão com o banco de dados
            # Exibir mensagem de sucesso e atualizar a exibição das plantas----------
            messagebox.showinfo(
                'Alteração', 'Alteração realizada com sucesso!')
        # Botão de salvar--------------------------------------------
        botao_salvar = customtkinter.CTkButton(
            master=self.frame_alterar_tamanho, text='SALVAR', width=150,
            font=('Josefin Sans bold', 14), fg_color=laranja,
            command=lambda: salvar_tamanho(planta_nome))
        botao_salvar.place(x=425, y=450)
        # Botão de voltar--------------------------------------------
        def botao_voltar_4():  # Função para voltar para a tela de gerenciamento
            self.frame_alterar_tamanho.pack_forget()  # esquecer o frame de alterar tamanho
            self.acessar_planta(planta_nome)  # mostrar o frame de update
        # Botão de voltar--------------------------------------------
        botaovoltar = customtkinter.CTkButton(master=self.frame_alterar_tamanho, text='VOLTAR', width=150, font=(
            'Josefin Sans bold', 14), fg_color=amarelo, command=botao_voltar_4)
        botaovoltar.place(x=225, y=450)
    # BOTAO DIA 1 ---------------------------------------------------
    def dia_1(self, planta_nome):
        self.destruir_frame()
        self.frame_dia_1 = customtkinter.CTkFrame(
            master=self.root, width=800, height=596)
        self.frame_dia_1.pack()

        # Editando o frame --------------------------------------------
        label_dia_1 = customtkinter.CTkLabel(
            master=self.frame_dia_1, text='DIA 1', font=('Josefin Sans bold', 30), text_color=laranja)
        label_dia_1.place(x=25, y=3)

        # Editando o frame --------------------------------------------
        con = lite.connect('water.db')
        cursor = con.cursor()
        cursor.execute("SELECT Tamanho, id FROM Plantacoes WHERE User=? AND Planta_Nome=?",
                       (usuario_logado, planta_nome))
        resultado = cursor.fetchone()
        con.close()

        if resultado is not None:  # Verifica se a consulta retornou resultados
            tamanho_area_planta = resultado[0]
            id_planta = resultado[1]

            # Chamar a função AguaChuva com o ID e tamanho da área da planta
            agua_absorvida = self.AguaChuva(
                id_planta, planta_nome, usuario_logado)
            quantidade_agua_necessaria = PlantasInfos[planta_nome] * \
                tamanho_area_planta
            quantidade_agua_gastadada = quantidade_agua_necessaria - agua_absorvida
            # fazendo o grafico de barra ---------------------------------------------------
            fig, ax = plt.subplots(figsize=(20, 20))
            label_aguas = ['Água\nnecessária','Água\neconomizada' ,'Água\ngasta']
            ax.barh = plt.barh([quantidade_agua_necessaria, agua_absorvida ,quantidade_agua_gastadada], color=[
                                 azul_claro, laranja, vermelho])
            plt.legend(label_aguas, fontsize="20", loc="lower right")
            ax.set_ylabel('Litros')
            ax.set_title('')
            plt.tight_layout()
            ax.tick_params(axis='y', colors='white', labelsize=35)  
            plt.savefig('grafico_2.png', transparent=True)
            plt.close()
            # Criar a imagem--------------------------------------------------------------------------------------------------------------------------
            imagem_grafico = customtkinter.CTkImage(light_image=Image.open(
                'grafico_2.png'), dark_image=Image.open('grafico_2.png'), size=(400, 400))  # Criar a imagem
            # Posicionar a imagem
            label_imagem_grafico = customtkinter.CTkLabel(
                master=self.frame_dia_1, image=imagem_grafico, text='')  # Posicionar a imagem
            label_imagem_grafico.place(x=370, y=20)

        else:
            label_texto = 'Planta não encontrada nas informações.'
            label_planta = customtkinter.CTkLabel(master=self.frame_dia_1, text=label_texto, font=(
                'Josefin Sans bold', 30), text_color=laranja)
    #adicionar imagem de perfil---------------------------------------------------
    def adicionar_imagem(self):
        filename = fd.askopenfilename(
            filetypes=[("Imagens", "*.png;*.jpg;*.jpeg")])
        if filename:
            # Arredondar a imagem
            img = Image.open(filename)
            mask = Image.new("L", img.size, 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0) + img.size, fill=255)
            mask = mask.filter(ImageFilter.GaussianBlur(10))
            result = img.copy()
            result.putalpha(mask)

            # Especificar o nome da pasta para salvar o arquivo
            pasta_destino = "imagem_perfil_arredondado"

            # Verificar se a pasta de destino existe, caso contrário, criar
            if not os.path.exists(pasta_destino):
                os.makedirs(pasta_destino)

            temp_filename = os.path.join(
                pasta_destino, f"{usuario_logado}_temp_rounded_image.png")

            result.save(temp_filename)

            con = lite.connect('water.db')
            cursor = con.cursor()

            # Atualizar o caminho da imagem no banco de dados
            cursor.execute(
                "UPDATE Usuarios SET imagem_perfil = ? WHERE apelido = ?", (temp_filename, usuario_logado))
            con.commit()  # Salvar as alterações no banco de dados
            con.close()   # Fechar a conexão

            # Atualizar a imagem exibida no rótulo
            nova_imagem = customtkinter.CTkImage(
                light_image=Image.open(temp_filename), dark_image=Image.open(temp_filename), size=(130, 130))
            self.label_imagem_1.configure(image=nova_imagem)
    #tela de perfil---------------------------------------------------
    def tela_perfil(self):
        # Destruindo o frame anterior
        self.destruir_frame()
        # Criando a tela nova--------------------------------------------
        frame_perfil = customtkinter.CTkFrame(
            master=self.root, width=800, height=596)
        frame_perfil.pack()
        frame_cor_de_fundo = customtkinter.CTkFrame(
            master=frame_perfil, width=700, height=300, border_width=5)
        frame_cor_de_fundo.place(x=50, y=130)
        # Editando o frame--------------------------------------------
        label_prefil = customtkinter.CTkLabel(
            master=frame_perfil, text='PERFIL', font=('Josefin Sans bold', 30), text_color=laranja)
        label_prefil.place(x=45, y=25)
        con = lite.connect('water.db')  # Abrir a conexão com o banco de dados
        cursor = con.cursor()  # Criar um cursor para executar as consultas
        cursor.execute(
            "SELECT imagem_perfil FROM Usuarios WHERE apelido = ?", (usuario_logado,))
        resultado = cursor.fetchone()
        con.close()
        # colocar a imagem de perfil---------------------------------------------------------
        imagem_perfil = customtkinter.CTkImage(light_image=Image.open(
            resultado[0]), dark_image=Image.open(resultado[0]), size=(130, 130))
        self.label_imagem_1 = customtkinter.CTkLabel(
            master=frame_cor_de_fundo, image=imagem_perfil, text='')
        self.label_imagem_1.place(x=40, y=60)
        btn_adicionar = customtkinter.CTkButton(master=frame_cor_de_fundo, text='ADICIONAR IMAGEM', width=100, font=(
            'Josefin Sans bold', 10),  command=self.adicionar_imagem, fg_color='transparent')
        btn_adicionar.place(x=50, y=200)
        label_apelido = customtkinter.CTkLabel(
            master=frame_cor_de_fundo, text='Apelido:', font=('Josefin Sans bold', 14), text_color=laranja)
        label_apelido.place(x=200, y=50)
        label_nome_2 = customtkinter.CTkLabel(
            master=frame_cor_de_fundo, text=usuario_logado, font=('Josefin Sans bold', 12), text_color=branco)
        label_nome_2.place(x=270, y=50)
        label_nome_3 = customtkinter.CTkLabel(
            master=frame_cor_de_fundo, text='Nome:', font=('Josefin Sans bold', 14), text_color=laranja)
        label_nome_3.place(x=200, y=100)
        label_email = customtkinter.CTkLabel(
            master=frame_cor_de_fundo, text='Email:', font=('Josefin Sans bold', 14), text_color=laranja)
        label_email.place(x=400, y=150)
        btn_editar_3 = customtkinter.CTkButton(master=frame_cor_de_fundo, text='Editar', width=50, font=(
            'Josefin Sans bold', 10), fg_color='transparent', anchor=NW, text_color=azul_claro, command=self.alterar_email)
        btn_editar_3.place(x=400, y=170)
        label_sobrenome = customtkinter.CTkLabel(
            master=frame_cor_de_fundo, text='Sobrenome:', font=('Josefin Sans bold', 14), text_color=laranja)
        label_sobrenome.place(x=200, y=150)
        label_cidade = customtkinter.CTkLabel(
            master=frame_cor_de_fundo, text='Cidade:', font=('Josefin Sans bold', 14), text_color=laranja)
        label_cidade.place(x=400, y=50)
        btn_editar_5 = customtkinter.CTkButton(master=frame_cor_de_fundo, text='Editar', width=50, font=(
            'Josefin Sans bold', 10), fg_color='transparent', anchor=NW, text_color=azul_claro, command=self.alterar_cidade)
        btn_editar_5.place(x=400, y=70)
        label_pais = customtkinter.CTkLabel(
            master=frame_cor_de_fundo, text='País:', font=('Josefin Sans bold', 14), text_color=laranja)
        label_pais.place(x=200, y=200)
        label_senha_5 = customtkinter.CTkLabel(
            master=frame_cor_de_fundo, text='Senha:', font=('Josefin Sans bold', 14), text_color=laranja)
        label_senha_5.place(x=400, y=100)
        btn_senha = customtkinter.CTkButton(master=frame_cor_de_fundo, text='Editar', width=50, font=(
            'Josefin Sans bold', 10), fg_color='transparent', anchor=NW, text_color=azul_claro, command=self.alterar_senha)
        btn_senha.place(x=400, y=120)
        # -----------------------------------------------------------------------------------------------
        con = lite.connect('water.db')  # Abrir a conexão com o banco de dados
        cursor = con.cursor()  # Criar um cursor para executar as consultas
        cursor.execute(
            "SELECT * FROM Usuarios WHERE apelido = ?", (usuario_logado,))
        resultado_3 = cursor.fetchone()  # Retorna uma tupla com os dados do usuário
        con.close()  # Fechar a conexão com o banco de dados
        # adicionando os dados do usuario---------------------------------------------------------
        l_nome = customtkinter.CTkLabel(master=frame_cor_de_fundo, text=resultado_3[1], font=(
            'Josefin Sans bold', 12), text_color=branco)
        l_nome.place(x=260, y=100)
        l_sobrenome = customtkinter.CTkLabel(master=frame_cor_de_fundo, text=resultado_3[2], font=(
            'Josefin Sans bold', 12), text_color=branco)
        l_sobrenome.place(x=300, y=150)
        l_email = customtkinter.CTkLabel(master=frame_cor_de_fundo, text=resultado_3[4], font=(
            'Josefin Sans bold', 12), text_color=branco)
        l_email.place(x=450, y=150)
        l_cidade = customtkinter.CTkLabel(master=frame_cor_de_fundo, text=resultado_3[5], font=(
            'Josefin Sans bold', 12), text_color=branco)
        l_cidade.place(x=460, y=50)
        l_pais = customtkinter.CTkLabel(master=frame_cor_de_fundo, text=resultado_3[6], font=(
            'Josefin Sans bold', 12), text_color=branco)
        l_pais.place(x=250, y=200)
        l_senha = customtkinter.CTkLabel(master=frame_cor_de_fundo, text='', font=(
            'Josefin Sans bold', 12), text_color=branco)
        l_senha.place(x=460, y=100)

        def mostrar_senha_2():
            if check_senha.get():
                l_senha.configure(text=resultado_3[7])
            else:
                l_senha.configure(text='')

        check_senha = customtkinter.CTkCheckBox(master=frame_cor_de_fundo, text='Mostrar senha', font=(
            'Josefin Sans bold', 12), text_color=branco, command=mostrar_senha_2)
        check_senha.place(x=400, y=230)
        # Botão de voltar--------------------------------------------

        def botao_voltar_perfil():
            frame_perfil.pack_forget()  # Destruir o frame atual
            self.tela_gerenciamento()  # Criar os frames do login novamente
        b_voltar = customtkinter.CTkButton(master=frame_perfil, command=botao_voltar_perfil,
                                           text='VOLTAR', width=100, font=('Josefin Sans bold', 14), fg_color=amarelo)  # Criando o botão
        b_voltar.place(x=45, y=500)
        b_remover_conta = customtkinter.CTkButton(master=frame_perfil, text='EXCLUIR', width=100, font=(
            'Josefin Sans bold', 14), fg_color=vermelho, command=self.remover_conta)  # Criando o botão
        b_remover_conta.place(x=175, y=500)
    # criando a função de remover conta---------------------------------------------------
    def remover_conta(self):
        # Exibir um diálogo de confirmação--------------------------------------------
        resposta = messagebox.askyesno(
            "Confirmação", "Tem certeza que deseja excluir a conta?")  # Exibir um diálogo de confirmação askyesno retorna true ou false
        # Se a resposta for verdadeira, excluir a conta--------------------------------------------
        if resposta:
            # Abrir a conexão com o banco de dados
            con = lite.connect('water.db')
            cursor = con.cursor()  # Criar um cursor para executar as consultas
            cursor.execute(
                "DELETE FROM Usuarios WHERE apelido = ?", (usuario_logado,))
            # Remover a conta do banco de dados
            cursor.execute(
                "DELETE FROM Plantacoes WHERE User = ?", (usuario_logado,))
            con.commit()  # Salvar as alterações no banco de dados
            con.close()  # Fechar a conexão com o banco de dados
            # Exibir uma mensagem de sucesso
            messagebox.showinfo('Remoção', 'Conta removida com sucesso!')
            self.destruir_frame()  # Destruir o frame atual
            self.create_frames()  # Criar os frames do login novamente
    # criando a tela de editar perfil---------------------------------------------------

        self.destruir_frame()
        # Criando a nova tela--------------------------------------------
        self.frame_alterar_sobrenome = customtkinter.CTkFrame(
            master=self.root, width=800, height=596)
        self.frame_alterar_sobrenome.pack()
        label_alterar_sobrenome = customtkinter.CTkLabel(
            master=self.frame_alterar_sobrenome, text='ALTERAR SOBRENOME', font=('Josefin Sans bold', 30), text_color=laranja)
        label_alterar_sobrenome.place(x=25, y=3)
        self.entry_sobrenome = customtkinter.CTkEntry(
            master=self.frame_alterar_sobrenome, width=300, placeholder_text='Digite seu novo sobrenome')
        self.entry_sobrenome.place(x=225, y=200)
        # Função para salvar o sobrenome----------------------------------------------

        def salvar_sobrenome():
            novo_sobrenome = self.entry_sobrenome.get()
            if not novo_sobrenome:
                messagebox.showwarning(
                    'Erro no Cadastro', 'Preencha todos os campos!')
                return
            else:
                con = lite.connect('water.db')
                cursor = con.cursor()
                cursor.execute("PRAGMA foreign_keys = ON")
                cursor.execute("UPDATE Usuarios SET sobrenome = ? WHERE apelido = ?", (
                    novo_sobrenome, usuario_logado))
                con.commit()
                con.close()
                messagebox.showinfo(
                    'Alteração', 'Alteração realizada com sucesso!')
        botao_salvar_2 = customtkinter.CTkButton(
            master=self.frame_alterar_sobrenome, text='SALVAR', width=100, font=('Josefin Sans bold', 14), fg_color=laranja, command=salvar_sobrenome)
        botao_salvar_2.place(x=400, y=450)
        # Botão de voltar--------------------------------------------
        botaovoltar_2 = customtkinter.CTkButton(master=self.frame_alterar_sobrenome, text='VOLTAR', width=100, font=(
            'Josefin Sans bold', 14), fg_color=amarelo, command=self.tela_perfil)
        botaovoltar_2.place(x=250, y=450)
    def alterar_email(self):
        self.destruir_frame()
        # Criando a nova tela--------------------------------------------
        self.frame_alterar_email = customtkinter.CTkFrame(
            master=self.root, width=800, height=596)
        self.frame_alterar_email.pack()
        label_alterar_email = customtkinter.CTkLabel(
            master=self.frame_alterar_email, text='ALTERAR EMAIL', font=('Josefin Sans bold', 30), text_color=laranja)
        label_alterar_email.place(x=25, y=3)
        self.entry_email = customtkinter.CTkEntry(
            master=self.frame_alterar_email, width=300, placeholder_text='Digite seu novo email')
        self.entry_email.place(x=225, y=200)
        # Função para salvar o email----------------------------------------------

        def salvar_email():
            novo_email = self.entry_email.get()
            if not novo_email:
                messagebox.showwarning(
                    'Erro no Cadastro', 'Preencha todos os campos!')
                return
            else:
                con = lite.connect('water.db')
                cursor = con.cursor()
                cursor.execute("PRAGMA foreign_keys = ON")
                cursor.execute("UPDATE Usuarios SET email = ? WHERE apelido = ?", (
                    novo_email, usuario_logado))
                con.commit()
                con.close()
                messagebox.showinfo(
                    'Alteração', 'Alteração realizada com sucesso!')
        botao_salvar_3 = customtkinter.CTkButton(
            master=self.frame_alterar_email, text='SALVAR', width=100, font=('Josefin Sans bold', 14), fg_color=laranja, command=salvar_email)
        botao_salvar_3.place(x=400, y=450)
        # Botão de voltar--------------------------------------------
        botaovoltar_3 = customtkinter.CTkButton(master=self.frame_alterar_email, text='VOLTAR', width=100, font=(
            'Josefin Sans bold', 14), fg_color=amarelo, command=self.tela_perfil)
        botaovoltar_3.place(x=250, y=450)
    def alterar_cidade(self):
        self.destruir_frame()
        # Criando a nova tela--------------------------------------------
        self.frame_alterar_cidade = customtkinter.CTkFrame(
            master=self.root, width=800, height=596)
        self.frame_alterar_cidade.pack()
        label_alterar_cidade = customtkinter.CTkLabel(
            master=self.frame_alterar_cidade, text='ALTERAR CIDADE', font=('Josefin Sans bold', 30), text_color=laranja)
        label_alterar_cidade.place(x=25, y=3)
        self.entry_cidade = customtkinter.CTkEntry(
            master=self.frame_alterar_cidade, width=300, placeholder_text='Digite sua nova cidade')
        self.entry_cidade.place(x=225, y=200)
        self.entry_pais = customtkinter.CTkEntry(
            master=self.frame_alterar_cidade, width=300, placeholder_text='Digite seu novo país')
        self.entry_pais.place(x=225, y=250)

        # Função para salvar a cidade----------------------------------------------
        def salvar_cidade():
            nova_cidade = self.entry_cidade.get()
            novo_pais = self.entry_pais.get()
            if not nova_cidade and not novo_pais:
                messagebox.showwarning(
                    'Erro no Cadastro', 'Preencha todos os campos!')
                return
            else:
                con = lite.connect('water.db')
                cursor = con.cursor()
                cursor.execute("PRAGMA foreign_keys = ON")
                cursor.execute("UPDATE Usuarios SET cidade = ?, sigla_pais = ? WHERE apelido = ?", (
                    nova_cidade, novo_pais, usuario_logado))
                con.commit()
                con.close()
                messagebox.showinfo(
                    'Alteração', 'Alteração realizada com sucesso!')
        botao_salvar_4 = customtkinter.CTkButton(
            master=self.frame_alterar_cidade, text='SALVAR', width=100, font=('Josefin Sans bold', 14), fg_color=laranja, command=salvar_cidade)
        botao_salvar_4.place(x=400, y=450)
        # Botão de voltar--------------------------------------------
        botaovoltar_4 = customtkinter.CTkButton(master=self.frame_alterar_cidade, text='VOLTAR', width=100, font=(
            'Josefin Sans bold', 14), fg_color=amarelo, command=self.tela_perfil)
        botaovoltar_4.place(x=250, y=450)
    def alterar_senha(self):
        self.destruir_frame()
        # Criando a nova tela--------------------------------------------
        self.frame_alterar_senha = customtkinter.CTkFrame(
            master=self.root, width=800, height=596)
        self.frame_alterar_senha.pack()
        label_alterar_senha = customtkinter.CTkLabel(
            master=self.frame_alterar_senha, text='ALTERAR SENHA', font=('Josefin Sans bold', 30), text_color=laranja)
        label_alterar_senha.place(x=25, y=3)
        self.entry_senha = customtkinter.CTkEntry(
            master=self.frame_alterar_senha, width=300, placeholder_text='Digite sua nova senha')
        self.entry_senha.place(x=225, y=200)
        # Função para salvar a senha----------------------------------------------

        def salvar_senha():
            nova_senha = self.entry_senha.get()
            if not nova_senha:
                messagebox.showwarning(
                    'Erro no Cadastro', 'Preencha todos os campos!')
                return
            else:
                con = lite.connect('water.db')
                cursor = con.cursor()
                cursor.execute("PRAGMA foreign_keys = ON")
                cursor.execute("UPDATE Usuarios SET senha = ? WHERE apelido = ?", (
                    nova_senha, usuario_logado))
                con.commit()
                con.close()
                messagebox.showinfo(
                    'Alteração', 'Alteração realizada com sucesso!')
        botao_salvar_5 = customtkinter.CTkButton(
            master=self.frame_alterar_senha, text='SALVAR', width=100, font=('Josefin Sans bold', 14), fg_color=laranja, command=salvar_senha)
        botao_salvar_5.place(x=400, y=450)
        # Botão de voltar--------------------------------------------
        botaovoltar_5 = customtkinter.CTkButton(master=self.frame_alterar_senha, text='VOLTAR', width=100, font=(
            'Josefin Sans bold', 14), fg_color=amarelo, command=self.tela_perfil)
        botaovoltar_5.place(x=250, y=450)

# chamamando o app ---------------------------------------------------
if __name__ == "__main__":
    root = CTk()
    app = WaterFriendlyApp(root)
    root.mainloop()
