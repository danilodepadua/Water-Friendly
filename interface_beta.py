#------------------------------------------------------------
import sqlite3 as lite
import requests
import datetime
import customtkinter
import matplotlib.pyplot as plt
# ------------------------------------------------------------
from PIL import Image
from tkinter import messagebox
from customtkinter import *
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
quantidade_agua = {
    'ALFACE': 125000,
    'ALMEIRÃO': '200',
    'BATATA': 81000,
    'BERINJELA': '200',
    'BETERRABA': '200',
    'BROCOLIS': '200',
    'CENOURA': 57500,
    'CEBOLA': '200',
    'COUVE': '200',
    'COUVE-FLOR': '200',
    'ESPINAFRE': '200',
    'FEIJÃO': '200',
    'TOMATE':  50000,
    'PIMENTÃO': '200',
    'CAFÉ': 8000,
}
#criando o banco caso não exista------------------------------------------------
con = lite.connect('water.db')  #Nome do banco 
with con: 
    cursor = con.cursor() #Criando o cursor 
    cursor.execute("CREATE TABLE IF NOT EXISTS Usuarios (apelido TEXT PRIMARY KEY, Nome TEXT, Sobrenome TEXT, idade TEXT, email TEXT, cidade TEXT, sigla_pais TEXT, Senha TEXT)") #Primeira tabela
    cursor.execute("CREATE TABLE IF NOT EXISTS Plantacoes (User TEXT, Planta TEXT, Tamanho INTEGER, FOREIGN KEY(User) REFERENCES Usuarios(apelido) ON DELETE CASCADE)")
     
#-----------------------------------------------------------------------------------
class WaterFriendlyApp:
    # construtor da classe------------------------------------------------------
    def __init__(self, root):
        self.root = root
        self.root.title("Water friendly")
        self.root.geometry("800x600")
        self.root.resizable(width=False, height=False)
        self.create_frames()
    # criar os frames da tela de login----------------------------------------
    def create_frames(self):
        self.frame_right = CTkFrame(master=self.root, width=400, height=596)
        self.frame_right.pack(side=RIGHT)
        self.frame_left = CTkFrame(
            master=self.root, width=400, height=596, fg_color=preto)
        self.frame_left.pack(side=LEFT)
        # Editando o frame-------------------------------------------------------
        label_login = customtkinter.CTkLabel(master=self.frame_right, text='Water Friendly ', font=(
            'Goudy Bookletter 1911', 35, 'bold'), text_color=laranja)
        label_login.place(x=25, y=110)
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
                cursor.execute("INSERT INTO Usuarios VALUES(?,?,?,?,?,?,?,?)",  # Inserir os dados no banco de dados a partir do comando INSERT INTO
                               (usuario_1, nome, sobrenome, idade, email, cidade, pais, senha_1))  # Os valores são passados como uma tupla
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
        # Editando o frame--------------------------------------------
        label_gerenciamento = customtkinter.CTkLabel(
            master=frame_gerenciamento_inteiro, text='GERENCIAMENTO ', font=('Josefin Sans bold', 30), text_color=laranja)
        label_gerenciamento.place(x=30, y=25)
        # Botão de perfil--------------------------------------------
        self.botao_perfil = customtkinter.CTkButton(
            master=frame_gerenciamento_inteiro, text='PERFIL', width=200, font=('Josefin Sans bold', 14), fg_color=laranja, command=self.tela_perfil)
        self.botao_perfil.place(x=100, y=200)
        self.botao_perfil.configure(corner_radius=10)
        # Botão de minha plantação--------------------------------------------
        self.botao_minhaplantacao = customtkinter.CTkButton(
            master=frame_gerenciamento_inteiro, command=self.tela_minhaplantacao, text='MINHA PLANTAÇÃO', width=200, font=('Josefin Sans bold', 14), fg_color=laranja)
        self.botao_minhaplantacao.place(x=450, y=200)
        self.botao_minhaplantacao.configure(corner_radius=10)
        # Botão de logout--------------------------------------------
        def logout():
            self.destruir_frame()  # Destruir o frame atual
            self.create_frames()  # Criar os frames do login novamente
        # botao de logout --------------------------------------------
        self.botao_logout = customtkinter.CTkButton(
            master=frame_gerenciamento_inteiro, command=logout, text='SAIR', width=200, font=('Josefin Sans bold', 14), fg_color=vermelho)
        self.botao_logout.place(x=270, y=350)
    # criando a tela de perfil---------------------------------------------------
    def tela_minhaplantacao(self):
        self.destruir_frame()  # Destruindo o frame anterior
        self.frame_myplant = customtkinter.CTkFrame(  # Criando o frame
            master=self.root, width=800, height=596)
        self.frame_myplant.pack()
        self.exibir_plantas()  # chamando a função para exibir os botões das plantas
        # Editando o frame--------------------------------------------
        label_minhaplantacao = customtkinter.CTkLabel(
            master=self.frame_myplant, text='MINHA PLANTAÇÃO', font=('Josefin Sans bold', 30), text_color=laranja)
        label_minhaplantacao.place(x=20, y=5)
        # Botão de adicionar plantação--------------------------------------------
        botao_adicionar_crud = customtkinter.CTkButton(master=self.frame_myplant, command=self.adicionar_area, text='ADICIONAR', width=100, font=(
            'Josefin Sans bold', 12), fg_color=verde)
        botao_adicionar_crud.place(x=20, y=95)
        # Botão de remover plantação--------------------------------------------
        botao_voltar = customtkinter.CTkButton(master=self.frame_myplant, command=self.tela_gerenciamento, text='VOLTAR', width=100, font=(
            'Josefin Sans bold', 12), fg_color=amarelo)
        botao_voltar.place(x=140, y=95)
    # criando a tela de perfil---------------------------------------------------
    def salvar_area(self):
        tamanho = self.entry_area.get()  # pega o tamanho da area
        planta = self.entry_cultura.get().upper()  # pega o nome da planta
        con = lite.connect('water.db')  # Abrir a conexão com o banco de dados
        cursor = con.cursor()  # Criar um cursor para executar as consultas
        # Habilitar as chaves estrangeiras
        cursor.execute("PRAGMA foreign_keys = ON")
        if not tamanho and not planta:  # Verificar se os campos foram preenchidos
            messagebox.showwarning(
                'Erro no Cadastro', 'Preencha todos os campos!')  # Mostrar uma mensagem de aviso
            return  # Retorna pra não executar o resto do código
        try:
            cursor.execute("INSERT INTO Plantacoes (User, Planta, tamanho ) VALUES (?, ?, ?)",  # Inserir os dados no banco de dados a partir do comando INSERT INTO
                           (usuario_logado, planta, tamanho))  # Os valores são passados como uma tupla
            con.commit()
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
        self.entry_cultura = customtkinter.CTkEntry(
            master=self.frame_adicionar_area, width=300, placeholder_text='Tipo de cultura')
        self.entry_cultura.place(x=350, y=200)
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
            'algumas nuvens': 'poucas_nuvens.png'
        }
        # Destruindo o frame anterior----------------------
        self.frame_myplant.pack_forget()
        # Criando a tela nova-----------------------------
        self.frame_planta = customtkinter.CTkFrame(
            root, width=800, height=596)
        self.frame_planta.pack()
        # Editando o frame-----------------------------
        label_planta = customtkinter.CTkLabel(master=self.frame_planta, text=planta_nome, font=(
            'Josefin Sans bold', 30), text_color=laranja)
        label_planta.place(x=25, y=5)
        # Botão de voltar-----------------------------
        botao_voltar_5 = customtkinter.CTkButton(master=self.frame_planta, command=self.tela_minhaplantacao, text='VOLTAR', width=150, font=(
            'Josefin Sans bold', 14), fg_color=amarelo)
        botao_voltar_5.place(x=120, y=500)
        # Botão de remover-----------------------------
        botao_remover_planta = customtkinter.CTkButton(master=self.frame_planta, text='REMOVER', width=150, font=(
            'Josefin Sans bold', 14), fg_color=vermelho, command=lambda: self.remover_planta(planta_nome))
        botao_remover_planta.place(x=520, y=500)
        # Conectando no banco de dados-------------------------------------
        botao_update_2= customtkinter.CTkButton(master=self.frame_planta, text='ATUALIZAR',command= lambda: self.alterar_tamanho(planta_nome) , width=150, font=(
            'Josefin Sans bold', 14), fg_color=azul)
        botao_update_2.place(x=320, y=500)
       
        con = lite.connect('water.db')  # Abrir a conexão com o banco de dados
        cursor = con.cursor()   # Criar um cursor para executar as consultas
        # Habilitar as chaves estrangeiras
        cursor.execute("PRAGMA foreign_keys = ON")
        cursor.execute(
            "SELECT * from Usuarios WHERE apelido = ? ", (usuario_logado,))  # Consulta para obter a cidade e o país do usuário
        resultado = cursor.fetchone()  # Retorna uma tupla com os dados do usuário
        cidade = resultado[5]  # A cidade está na posição 5 da tupla
        pais = resultado[6]  # O país está na posição 6 da tupla
        con.close()  # Fechar a conexão com o banco de dados
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
        cursor.execute("SELECT Tamanho FROM Plantacoes WHERE User=? AND Planta=?",  # Consulta para obter a área da planta ESPECÍFICA selecionada
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
        #crinado o grafico de area-------------------------------------------------------------------
        fig, ax = plt.subplots(figsize=(10, 10))
        ax.pie([area_total,area_planta], labels=['Área total', 'Área da planta'], autopct='%1.1f%%', textprops={'fontsize': 30, 'color': 'white'}, colors=[azul_claro, laranja])
        ax.axis('equal')
        plt.tight_layout()
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
        # Hora atual--------------------------------------------------------------------------------------------------------------------------
        dia_atual = datetime.datetime.now()  # Obtém a data e hora atual
        # Conectando na API e fazendo a requisição para pegar os dados e fazer a previsão do tempo
        for i in range(0, 5):  # Itera pelos próximos 5 dias com um laço de repetição
            # URL da API
            previsao_url = f'https://api.openweathermap.org/data/2.5/forecast?q={cidade},{pais}&appid={API_KEY}&lang=pt_br&units=metric&cnt=5'
            previsao_request = requests.get(previsao_url)  # Faz a requisição
            previsao_data = previsao_request.json()  # Converte os dados para JSON
            # Obtém a previsão do tempo 'i' é o indice do dia que vai aumentar em cada repetição indo pro dia dia seguinte
            previsao = previsao_data['list'][i]['weather'][0]['description'] #forma de acessar os dados da api 
            # Obtém a temperatura 'i' é o indice que vai chamar a temperatura do dia seguinte a cada repetição
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
        
        #relatorio de irrigação---------------------------------------------------------
        b_dia_1 = customtkinter.CTkButton(master=tabview.tab("Irrigação"), text='Dia 1', width=100, font=(
            'Josefin Sans bold', 14), fg_color=azul)
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

        # cnt=1 é para pegar a previsão diária em intervalos de 3 horas
        url_previsao_diaria = f'https://api.openweathermap.org/data/2.5/forecast?q={cidade},{pais}&appid={API_KEY}&lang=pt_br&cnt=1'
        request_previsao_diaria = requests.get(url_previsao_diaria)
        # se a verificaçao for verdadeira ele vai entrar no if e pegar a quantidade de chuva dos 5 dias---------------------------------------------------------
        if request_previsao_diaria.status_code == 200:
            # pega os dados da api e converte para json e armazena na variavel data_previsao_diaria
            data_previsao_diaria = request_previsao_diaria.json()
            # Verifica se a chave 'rain' existe na previsão diária
            # Se existir, significa que há previsão de chuva para o dia
            if 'rain' in data_previsao_diaria['list'][0]:
                # Obtém a quantidade de chuva em intervalo de 3 horas (milímetros)
                # Obtém a quantidade de chuva em intervalo de 3 horas (milímetros) pois é assim que a api funciona a cada 3 horas
                chuva_3h = data_previsao_diaria['list'][0]['rain']['3h']
                # Para obter uma estimativa da quantidade total de chuva no dia, você pode multiplicar o valor de chuva_3h por 8
                # Multiplica por 8 para obter a quantidade total de chuva no dia 3*8= 24 fazendo uma estimativa
                quantidade_chuva_diaria = chuva_3h * 8
                # Atualiza a interface com a quantidade total de chuva no dia---------------------------------------------------------
                texto_chuva_diaria = customtkinter.CTkLabel(master=tabview.tab(
                    "Irrigação"), text=f'Chuva diária: {quantidade_chuva_diaria} mm', font=('Josefin Sans bold', 14), text_color=azul_claro)
                texto_chuva_diaria.place(x=30, y=5)
    # funçao de remover a planta---------------------------------------------------
    def remover_planta(self, planta_nome):
        con = lite.connect('water.db')  # Abrir a conexão com o banco de dados
        cursor = con.cursor()  # Criar um cursor para executar as consultas
        # Habilitar as chaves estrangeiras
        cursor.execute("PRAGMA foreign_keys = ON")
        resposta_1=  messagebox.askyesno('Remover', 'Deseja remover a planta?')
        if resposta_1 == True : 
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
        x_pos_planta = 20  # Posição inicial x do botão
        y_pos_planta = 200  # Posição inicial y do botão
        botao_width_planta = 100  # Largura do botão
        botao_height_planta = 40  # Altura do botão
        botao_margin_x_planta = 27  # Margem x entre os botões
        botao_margin_y_planta = 30  # Margem y entre os botões
        con = lite.connect('water.db')  # Conectando no banco de dados
        cursor = con.cursor()  # Criando o cursor
        cursor.execute(
            "SELECT Planta FROM Plantacoes WHERE User=?", (usuario_logado,))  # Obtendo as plantas do usuário, a partir da chave estrangeira
        plantas = cursor.fetchall()
        con.close()
        # Lógica do for : plantas é o resultado apartir do fetchall recupera todas as plantas do usuário e cria um botão ate que o número limites das
        # plantas seja atingido, por isso o uso do for
        for planta in plantas:
            self.botao_planta = customtkinter.CTkButton(master=self.frame_myplant, text=planta[0], width=botao_width_planta, font=(
                'Josefin Sans bold', 12), fg_color=laranja, command=lambda planta_nome=planta[0]: self.acessar_planta(planta_nome))  # Acessar a planta
            self.botao_planta.place(
                x=x_pos_planta, y=y_pos_planta)  # Posicionar o botão

            x_pos_planta += botao_width_planta + botao_margin_x_planta

            if x_pos_planta + botao_width_planta > 800:  # Verificar se o botão ultrapassou a largura da tela que é 700
                x_pos_planta = 20  # Posicionar o botão na posição inicial
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
        # Função para salvar o tamanho----------------------------------------------
        def salvar_tamanho(planta_nome):
            novo_tamanho = self.entry_tamanho_2.get()  # Obter o novo tamanho da entrada
            if not novo_tamanho:
                messagebox.showwarning(
                    'Erro no Cadastro', 'Preencha todos os campos!')
                return  # Sai da função se o campo estiver vazio
            # Conectar ao banco de dados e executar a atualização---------------------
            con = lite.connect('water.db')
            cursor = con.cursor()
            cursor.execute("PRAGMA foreign_keys = ON")
            cursor.execute("UPDATE Plantacoes SET tamanho = ? WHERE User = ? AND Planta = ?", (
                novo_tamanho, usuario_logado, planta_nome))  # Atualizar o tamanho da planta
            con.commit()  # Salvar as alterações
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
            self.acessar_planta(planta_nome) # mostrar o frame de update
        # Botão de voltar--------------------------------------------
        botaovoltar = customtkinter.CTkButton(master=self.frame_alterar_tamanho, text='VOLTAR', width=150, font=(
            'Josefin Sans bold', 14), fg_color=amarelo, command=botao_voltar_4)
        botaovoltar.place(x=225, y=450)
    # criando a tela de perfil---------------------------------------------------
    def tela_perfil(self):
        # Destruindo o frame anterior
        self.destruir_frame()
        # Criando a tela nova--------------------------------------------
        frame_perfil = customtkinter.CTkFrame(
            master=self.root, width=800, height=596)
        frame_perfil.pack()
        # Editando o frame--------------------------------------------
        label_perfil = customtkinter.CTkLabel(master=frame_perfil, text='PERFIL :', font=(
            'Josefin Sans bold', 30), text_color=laranja)
        label_perfil.place(x=25, y=35)
        l_apelido = customtkinter.CTkLabel(master=frame_perfil, text='Apelido :', font=(
            'Josefin Sans bold', 20), text_color=laranja)  # Criando o label
        l_apelido.place(x=25, y=190)
        l_senha = customtkinter.CTkLabel(master=frame_perfil, text='Senha :', font=(
            'Josefin Sans bold', 20), text_color=laranja)  # Criando o label
        l_senha.place(x=345, y=190)
        l_nome = customtkinter.CTkLabel(master=frame_perfil, text='Nome :', font=(
            'Josefin Sans bold', 20), text_color=laranja)  # Criando o label
        l_nome.place(x=25, y=240)
        l_sobrenome = customtkinter.CTkLabel(master=frame_perfil, text='Sobrenome :', font=(
            'Josefin Sans bold', 20), text_color=laranja)  # Criando o label
        l_sobrenome.place(x=345, y=240)
        l_idade = customtkinter.CTkLabel(master=frame_perfil, text='Idade :', font=(
            'Josefin Sans bold', 20), text_color=laranja)  # Criando o label
        l_idade.place(x=25, y=290)
        l_email = customtkinter.CTkLabel(master=frame_perfil, text='Email :', font=(
            'Josefin Sans bold', 20), text_color=laranja)  # Criando o label
        l_email.place(x=345, y=290)
        l_cidade = customtkinter.CTkLabel(master=frame_perfil, text='Cidade :', font=(
            'Josefin Sans bold', 20), text_color=laranja)  # Criando o label
        l_cidade.place(x=25, y=340)
        l_pais = customtkinter.CTkLabel(master=frame_perfil, text='País :', font=(
            'Josefin Sans bold', 20), text_color=laranja)  # Criando o label
        l_pais.place(x=345, y=340)
        # Conectando no banco de dados--------------------------------------------
        con = lite.connect('water.db')
        cursor = con.cursor()  # Criar um cursor para executar as consultas
        # Consulta para obter os dados do usuário
        consulta = "SELECT * FROM Usuarios WHERE apelido = ?"
        cursor.execute(consulta, (usuario_logado,))  # Executar a consulta
        resultado = cursor.fetchone()  # Retorna uma tupla com os dados do usuário
        if resultado:
            # Preencher os labels com os dados do usuário---------------------------------------------------------
            l_apelido_valor = customtkinter.CTkLabel(master=frame_perfil, text=resultado[0], font=(
                'Josefin Sans bold', 14), text_color=branco)
            l_apelido_valor.place(x=120, y=195)
            # senha = resultado[7] indice 7
            l_senha_valor = customtkinter.CTkLabel(master=frame_perfil, text=resultado[7], font=(
                'Josefin Sans bold', 14), text_color=branco)
            l_senha_valor.place(x=420, y=195)
            # senha = resultado[1] indice 1
            l_nome_valor = customtkinter.CTkLabel(master=frame_perfil, text=resultado[1], font=(
                'Josefin Sans bold', 14), text_color=branco)
            l_nome_valor.place(x=110, y=240)
            # senha = resultado[2] indice 2
            l_sobrenome_valor = customtkinter.CTkLabel(master=frame_perfil, text=resultado[2], font=(
                'Josefin Sans bold', 14), text_color=branco)
            l_sobrenome_valor.place(x=470, y=245)
            # senha = resultado[3] indice 3
            l_idade_valor = customtkinter.CTkLabel(master=frame_perfil, text=resultado[3], font=(
                'Josefin Sans bold', 14), text_color=branco)
            l_idade_valor.place(x=110, y=295)
            # senha = resultado[4] indice 4
            l_email_valor = customtkinter.CTkLabel(master=frame_perfil, text=resultado[4], font=(
                'Josefin Sans bold', 14), text_color=branco)
            l_email_valor.place(x=415, y=295)
            # senha = resultado[5] indice 5
            l_cidade_valor = customtkinter.CTkLabel(master=frame_perfil, text=resultado[5], font=(
                'Josefin Sans bold', 14), text_color=branco)
            l_cidade_valor.place(x=110, y=345)
            # senha = resultado[6] indice 6
            l_pais_valor = customtkinter.CTkLabel(master=frame_perfil, text=resultado[6], font=(
                'Josefin Sans bold', 14), text_color=branco)
            l_pais_valor.place(x=410, y=345)
        con.close()  # Fechar a conexão com o banco de dados
        # Botão de voltar--------------------------------------------
        def botao_voltar_perfil():
            frame_perfil.pack_forget()  # Destruir o frame atual
            self.tela_gerenciamento()  # Criar os frames do login novamente
        b_voltar = customtkinter.CTkButton(master=frame_perfil, command=botao_voltar_perfil,
                                           text='VOLTAR', width=150, font=('Josefin Sans bold', 14), fg_color=amarelo)  # Criando o botão
        b_voltar.place(x=25, y=500)
        b_editar = customtkinter.CTkButton(master=frame_perfil,
                                           text='EDITAR', width=150, font=('Josefin Sans bold', 14), fg_color=laranja)  # Criando o botão
        b_editar.place(x=225, y=500)
        b_remover_conta = customtkinter.CTkButton(master=frame_perfil, text='EXCLUIR CONTA', width=150, font=(
            'Josefin Sans bold', 14), fg_color=vermelho, command=self.remover_conta)  # Criando o botão
        b_remover_conta.place(x=425, y=500)
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
            cursor.execute("DELETE FROM Usuarios WHERE apelido = ?", (usuario_logado,))
            cursor.execute("DELETE FROM Plantacoes WHERE User = ?", (usuario_logado,)) # Remover a conta do banco de dados
            con.commit()  # Salvar as alterações no banco de dados
            con.close()  # Fechar a conexão com o banco de dados
            # Exibir uma mensagem de sucesso
            messagebox.showinfo('Remoção', 'Conta removida com sucesso!')
            self.destruir_frame()  # Destruir o frame atual
            self.create_frames()  # Criar os frames do login novamente
    # programar irrigação---------------------------------------------------
    def programar_irrigacao(self):
        pass
# chamamando o app ---------------------------------------------------
if __name__ == "__main__":
    root = CTk()
    app = WaterFriendlyApp(root)
    root.mainloop()
