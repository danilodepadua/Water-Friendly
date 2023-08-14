import tkinter as tk
import sqlite3 as lite
import requests
import datetime
import customtkinter

from PIL import Image
from tkinter import messagebox
from customtkinter import *

API_KEY = '8cd78d19081f93d321e5db39e8ef13cb'

# Definindo cores e outras constantes
laranja = '#de4300'
azul = '#2453ff'
amarelo = '#0b005e'
vermelho = '#c20404'
verde = '#015e0d'
preto = '#151716'
branco = '#c9c9c9'
azul_claro = '#1cb7ff'


# organizar o codigo em classes
class WaterFriendlyApp:
    # construtor da classe
    def __init__(self, root):
        self.root = root
        self.root.title("Water friendly")
        self.root.geometry("700x400")
        self.root.resizable(width=False, height=False)
        self.create_frames()
    # criar os frames da tela de login

    def create_frames(self):
        self.frame_right = CTkFrame(master=self.root, width=350, height=396)
        self.frame_right.pack(side=tk.RIGHT)
        self.frame_left = CTkFrame(
            master=self.root, width=350, height=396, fg_color=preto)
        self.frame_left.pack(side=tk.LEFT)

        # Editando o frame
        label_login = customtkinter.CTkLabel(master=self.frame_right, text='LOGIN :', font=(
            'Josefin Sans bold', 25), text_color=laranja)
        label_login.place(x=25, y=5)

        # Editando o entry de usuario
        self.entry_usuario = customtkinter.CTkEntry(master=self.frame_right, width=300,
                                                    font=('Josefin Sans bold', 14), placeholder_text='Nome de usuário')
        self.entry_usuario.place(x=25, y=105)
        # Editando o entry da senha
        self.entry_senha = customtkinter.CTkEntry(master=self.frame_right, width=300,
                                                  font=('Josefin Sans bold', 14), placeholder_text='Senha', show='*')
        self.entry_senha.place(x=25, y=175)

        # Botão de login
        btn_login = customtkinter.CTkButton(master=self.frame_right, text='Login', width=300,
                                            font=('Josefin Sans bold', 14), fg_color=laranja, text_color=branco, command=self.fazer_login)
        btn_login.place(x=25, y=270)
        # check
        self.check_box = customtkinter.CTkCheckBox(
            master=self.frame_right, text='Mostrar senha', command=self.mostrar_senha, font=('Josefin Sans bold', 14))
        self.check_box.place(x=25, y=230)

        # Label de cadastro
        label_cadastro = customtkinter.CTkLabel(master=self.frame_left, text='Não tem uma conta?', font=(
            'Josefin Sans bold', 25), text_color=laranja, bg_color=preto)
        label_cadastro.place(x=35, y=70)
        label_cadastro2 = customtkinter.CTkLabel(
            master=self.frame_left, text='Cadastre-se agora', bg_color=preto, font=('Josefin Sans bold', 20))
        label_cadastro2.place(x=70, y=135)
        # Botão de cadastro
        botao_cadastro = customtkinter.CTkButton(master=self.frame_left, text='CADASTRAR', width=200, font=(
            'Josefin Sans bold', 15), fg_color=laranja, command=self.create_registration_page)
        botao_cadastro.place(x=60, y=190)

    # verificar se o usuario e senha estao corretos
    def verificar_credenciais(self, usuario, senha):
        try:
            con = lite.connect('water.db')
            cursor = con.cursor()

            consulta = "SELECT * FROM Usuarios WHERE apelido = ? AND Senha = ?"
            cursor.execute(consulta, (usuario, senha))
            resultado = cursor.fetchone()

            cursor.close()
            con.close()

            return resultado is not None

        except lite.Error as e:
            messagebox.showerror('Erro no Banco de Dados',
                                 f"Ocorreu um erro no banco de dados: {e}")
            return False

    # mostrar a senha do usuario caso ele queira
    def mostrar_senha(self):
        if self.check_box.get() == 1:
            self.entry_senha.configure(show='')
        else:
            self.entry_senha.configure(show='*')

    # verificar e ir adiante
    def fazer_login(self):
        global usuario_logado
        usuario = self.entry_usuario.get()
        senha = self.entry_senha.get()

        if not usuario or not senha:
            messagebox.showwarning('Login', 'Preencha todos os campos!')
            return

        if usuario == 'admin' and senha == 'admin':
            messagebox.showinfo('Login', 'Seja bem-vindo, Admin!')
            self.tela_gerenciamento()

        elif self.verificar_credenciais(usuario, senha):
            usuario_logado = usuario
            messagebox.showinfo('Login', f'Seja bem-vindo, {usuario}!')
            self.tela_gerenciamento()

        else:
            messagebox.showwarning('Login', 'Usuário ou senha incorretos')

    # destroi o frame anterior
    def destruir_frame(self):
        for frame in root.winfo_children():
            frame.destroy()

    # cria a tela de cadastro
    def create_registration_page(self):
        self.frame_right.pack_forget()
        self.frame_left.pack_forget()

        # Criando a tela nova
        frame_cadastro_inteiro = customtkinter.CTkFrame(
            master=self.root, width=700, height=396)
        frame_cadastro_inteiro.pack()

        # Editando o frame
        label_cadastro = customtkinter.CTkLabel(master=frame_cadastro_inteiro, text='CADASTRO :',
                                                font=('Josefin Sans bold', 30), text_color=laranja)
        label_cadastro.place(x=25, y=5)

        # Editando o entry de usuario
        self.entry_usuario_1 = customtkinter.CTkEntry(
            master=frame_cadastro_inteiro, width=300, placeholder_text='Usuário')
        self.entry_usuario_1.place(x=25, y=90)

        # Editando o entry do nome
        self.entry_nome = customtkinter.CTkEntry(
            master=frame_cadastro_inteiro, width=300, placeholder_text='Nome')
        self.entry_nome.place(x=25, y=160)

        # Editando o entry do sobrenome
        self.entry_sobrenome = customtkinter.CTkEntry(
            master=frame_cadastro_inteiro, width=300, placeholder_text='Sobrenome')
        self.entry_sobrenome.place(x=25, y=230)

        # editando o entry da idade
        self.entry_idade = customtkinter.CTkEntry(
            master=frame_cadastro_inteiro, width=300, placeholder_text='Idade')
        self.entry_idade.place(x=25, y=300)

        # editando o entry do Email
        self.entry_email = customtkinter.CTkEntry(
            master=frame_cadastro_inteiro, width=300, placeholder_text='Email')
        self.entry_email.place(x=350, y=90)

        # editando o entry da cidade
        self.entry_cidade = customtkinter.CTkEntry(
            master=frame_cadastro_inteiro, width=300, placeholder_text='Cidade')
        self.entry_cidade.place(x=350, y=160)

        # sigla do Pais
        self.entry_pais = customtkinter.CTkEntry(
            master=frame_cadastro_inteiro, width=300, placeholder_text='Sigla do País')
        self.entry_pais.place(x=350, y=230)

        # editando o entry da senha
        self.entry_senha = customtkinter.CTkEntry(
            master=frame_cadastro_inteiro, width=300, placeholder_text='Senha', show='*')
        self.entry_senha.place(x=350, y=300)

        self.botao_cadastrar = customtkinter.CTkButton(
            master=frame_cadastro_inteiro, height=0, text='CADASTRAR', width=150,
            font=('Josefin Sans bold', 14), fg_color=laranja, command=self.avancar_pagina)
        self.botao_cadastrar.place(x=350, y=350)
        self.botao_cadastrar.configure(corner_radius=10)

        def voltar_login():
            # esquecer o frame do cadastro
            frame_cadastro_inteiro.pack_forget()
            # recriar os frames do login
            self.frame_right.pack(side=RIGHT)
            self.frame_left.pack(side=LEFT)

        # botao de voltar
        botao_voltar = customtkinter.CTkButton(master=frame_cadastro_inteiro, height=0, text='VOLTAR', width=150, font=(
            'Josefin Sans bold', 14), fg_color=amarelo, command=voltar_login)
        botao_voltar.place(x=150, y=350)
        botao_voltar.configure(corner_radius=10)

        # Função para cadastrar no banco de dados

    # cadastrar no banco de dados a partir da tela de cadastro
    def cadastrar_no_banco(self):
        usuario_1 = self.entry_usuario_1.get()
        nome = self.entry_nome.get()
        sobrenome = self.entry_sobrenome.get()
        idade = self.entry_idade.get()
        email = self.entry_email.get()
        cidade = self.entry_cidade.get()
        pais = self.entry_pais.get()
        senha = self.entry_senha.get()

        con = lite.connect('water.db')
        cursor = con.cursor()

        try:
            # Verificar se o apelido já existe no banco de dados
            cursor.execute(
                "SELECT * FROM Usuarios WHERE apelido = ?", (usuario_1,))
            existing_user = cursor.fetchone()

            if existing_user:
                messagebox.showerror(
                    'Cadastro', 'O apelido já está em uso. Escolha outro apelido.')
                con.close()  # Fechar a conexão com o banco de dados
                # Permanecer na página de cadastro
                return False

            else:
                cursor.execute("INSERT INTO Usuarios VALUES(?,?,?,?,?,?,?,?)",
                               (usuario_1, nome, sobrenome, idade, email, cidade, pais, senha))
                con.commit()
                messagebox.showinfo(
                    'Cadastro', 'Cadastro realizado com sucesso!')
                return True
        except:
            messagebox.showerror('Cadastro', 'Erro ao cadastrar!')
            return False

        finally:
            con.close()

        # avançar para a tela de gerenciamento

    # avancar para a tela de gerenciamento depois do botao de cadastrar
    def avancar_pagina(self):
        usuario = self.entry_usuario_1.get()
        nome = self.entry_nome.get()
        sobrenome = self.entry_sobrenome.get()
        idade = self.entry_idade.get()
        email = self.entry_email.get()
        cidade = self.entry_cidade.get()
        pais = self.entry_pais.get()
        senha = self.entry_senha.get()

        # Verificar se todos os campos foram preenchidos
        if any(not field for field in [usuario, nome, sobrenome, idade, email, cidade, pais, senha]):
            messagebox.showerror('Cadastro', 'Preencha todos os campos!')
        elif len(senha) < 8:  # Verificar se a senha tem pelo menos 8 caracteres
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
            global usuario_logado
            usuario_logado = usuario
            self.tela_gerenciamento()

    # criando a tela de gerenciamento
    def tela_gerenciamento(self):
        # Destruindo o frame anterior
        self.destruir_frame()

        # Criando a tela nova
        frame_gerenciamento_inteiro = customtkinter.CTkFrame(
            master=self.root, width=700, height=706)
        frame_gerenciamento_inteiro.pack()

        # Editando o frame
        label_gerenciamento = customtkinter.CTkLabel(
            master=frame_gerenciamento_inteiro, text='GERENCIAMENTO :', font=('Josefin Sans bold', 30), text_color=laranja)
        label_gerenciamento.place(x=25, y=5)

        # Botão de perfil
        botao_perfil = customtkinter.CTkButton(
            master=frame_gerenciamento_inteiro, text='PERFIL', width=150, font=('Josefin Sans bold', 14), fg_color=laranja, command=self.tela_perfil)
        botao_perfil.place(x=150, y=120)
        botao_perfil.configure(corner_radius=10)

        # Botão de minha plantação
        botao_minhaplantacao = customtkinter.CTkButton(
            master=frame_gerenciamento_inteiro, command=self.tela_minhaplantacao, text='MINHA PLANTAÇÃO', width=150, font=('Josefin Sans bold', 14), fg_color=laranja)
        botao_minhaplantacao.place(x=350, y=120)
        botao_minhaplantacao.configure(corner_radius=10)

        # Botão de logout
        def logout():
            self.destruir_frame()
            self.create_frames()

        # botao de logout
        botao_logout = customtkinter.CTkButton(
            master=frame_gerenciamento_inteiro, command=logout, text='SAIR', width=150, font=('Josefin Sans bold', 14), fg_color=vermelho)
        botao_logout.place(x=250, y=250)

        # Armazenar referência aos botões para acesso posterior, se necessário
        self.botao_perfil = botao_perfil
        self.botao_minhaplantacao = botao_minhaplantacao
        self.botao_logout = botao_logout

    # criando a tela de perfil
    def tela_minhaplantacao(self):
        self.destruir_frame()

        self.frame_myplant = customtkinter.CTkFrame(
            master=self.root, width=700, height=396)
        self.frame_myplant.pack()

        self.exibir_plantas()

        label_minhaplantacao = customtkinter.CTkLabel(
            master=self.frame_myplant, text='MINHA PLANTAÇÃO :', font=('Josefin Sans bold', 30), text_color=laranja)
        label_minhaplantacao.place(x=170, y=5)

        botao_adicionar_crud = customtkinter.CTkButton(master=self.frame_myplant, command=self.adicionar_area, text='ADICIONAR', width=100, font=(
            'Josefin Sans bold', 12), fg_color=verde)
        botao_adicionar_crud.place(x=225, y=75)

        botao_update = customtkinter.CTkButton(
            self.frame_myplant, text='ATUALIZAR', width=100, font=('Josefin Sans bold', 12), fg_color=azul)
        botao_update.place(x=350, y=75)

        botao_voltar = customtkinter.CTkButton(master=self.frame_myplant, command=self.tela_gerenciamento, text='VOLTAR', width=100, font=(
            'Josefin Sans bold', 12), fg_color=amarelo)
        botao_voltar.place(x=475, y=75)

    # criando a tela de perfil
    def salvar_area(self):
        tamanho = self.entry_area.get()
        planta = self.entry_cultura.get().upper()

        con = lite.connect('water.db')
        cursor = con.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")

        if not tamanho and not planta:
            messagebox.showwarning(
                'Erro no Cadastro', 'Preencha todos os campos!')
            return
        try:
            cursor.execute("INSERT INTO Plantacoes (User, Planta, tamanho ) VALUES (?, ?, ?)",
                           (usuario_logado, planta, tamanho))
            con.commit()
            messagebox.showinfo(
                'Cadastro', 'Cadastro realizado com sucesso!')
            # Após cadastrar a planta, chame a função para exibir as plantas novamente
            self.exibir_plantas()
        except:
            messagebox.showerror('Cadastro', 'Erro ao cadastrar!')

        con.close()

    # exibir as plantas cadastradas
    def adicionar_area(self):
        self.frame_myplant.pack_forget()

        self.frame_adicionar_area = customtkinter.CTkFrame(
            master=self.root, width=700, height=396)
        self.frame_adicionar_area.pack()

        self.entry_area = customtkinter.CTkEntry(
            master=self.frame_adicionar_area, width=300, placeholder_text='Tamanho da área da planta em hectares')
        self.entry_area.place(x=25, y=90)

        self.entry_cultura = customtkinter.CTkEntry(
            master=self.frame_adicionar_area, width=300, placeholder_text='Tipo de planta')
        self.entry_cultura.place(x=350, y=90)

        label_adicionar_area = customtkinter.CTkLabel(
            master=self.frame_adicionar_area, text='ADICIONAR ÁREA :', font=('Josefin Sans bold', 30), text_color=laranja)
        label_adicionar_area.place(x=25, y=5)

        botao_salvar = customtkinter.CTkButton(master=self.frame_adicionar_area, text='SALVAR', width=150,
                                               font=('Josefin Sans bold', 14), fg_color=laranja, command=self.salvar_area)
        botao_salvar.place(x=360, y=300)

        def botao_voltar():
            self.frame_adicionar_area.pack_forget()
            self.frame_myplant.pack()

        botaovoltar = customtkinter.CTkButton(master=self.frame_adicionar_area, command=botao_voltar,
                                              text='VOLTAR', width=150, font=('Josefin Sans bold', 14), fg_color=amarelo)
        botaovoltar.place(x=190, y=300)

    def acessar_planta(self, planta_nome):

        # atribuindo imagens para a previsao do tempo
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

        # Destruindo o frame anterior
        self.frame_myplant.pack_forget()

        # Criando a tela nova
        self.frame_planta = customtkinter.CTkFrame(
            root, width=700, height=396)
        self.frame_planta.pack()

        # Editando o frame
        label_planta = customtkinter.CTkLabel(master=self.frame_planta, text=planta_nome, font=(
            'Josefin Sans bold', 30), text_color=laranja)
        label_planta.place(x=25, y=5)

        botao_voltar_5 = customtkinter.CTkButton(master=self.frame_planta, command=self.tela_minhaplantacao, text='VOLTAR', width=150, font=(
            'Josefin Sans bold', 14), fg_color=amarelo)
        botao_voltar_5.place(x=475, y=25)       

        botao_remover_planta = customtkinter.CTkButton(master=self.frame_planta, text='REMOVER', width=150, font=(
        'Josefin Sans bold', 14), fg_color=vermelho, command=lambda: self.remover_planta(planta_nome))
        botao_remover_planta.place(x=275, y=25)

        # Conectando no banco de dados
        con = lite.connect('water.db')
        cursor = con.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")
        cursor.execute(
            "SELECT * from Usuarios WHERE apelido = ? ", (usuario_logado,))
        resultado = cursor.fetchone()  # Retorna uma tupla com os dados do usuário
        cidade = resultado[5]  # A cidade está na posição 5 da tupla
        pais = resultado[6]  # O país está na posição 6 da tupla
        con.close()  # Fechar a conexão com o banco de dados

        # Criando o tabview
        tabview = customtkinter.CTkTabview(
            master=self.frame_planta, width=650, height=300)
        tabview.place(x=25, y=75)
        tabview.add("Informações")  # Adicionando as abas
        tabview.add("Tempo")  # Adicionando as abas
        tabview.add("Irrigação")  # Adicionando as abas
        tabview.tab('Informações').grid_columnconfigure(
            0, weight=1)  # Configurando o grid
        tabview.tab('Tempo').grid_columnconfigure(
            0, weight=1)  # Configurando o grid
        tabview.tab('Irrigação').grid_columnconfigure(
            0, weight=1)  # Configurando o grid
        texto_1 = customtkinter.CTkLabel(master=tabview.tab(
            'Informações'), text=planta_nome, font=('Josefin Sans bold', 14), text_color=branco)
        texto_1.place(x=15, y=2)

        # Hora atual
        dia_atual = datetime.datetime.now()  # Obtém a data e hora atual

        # Conectando na API e fazendo a requisição para pegar os dados e fazer a previsão do tempo
        for i in range(0, 5):  # Itera pelos próximos 5 dias
            previsao_url = f'https://api.openweathermap.org/data/2.5/forecast?q={cidade},{pais}&appid={API_KEY}&lang=pt_br&units=metric&cnt=5'
            previsao_request = requests.get(previsao_url)  # Faz a requisição
            previsao_data = previsao_request.json()  # Converte os dados para JSON
            # Obtém a previsão do tempo
            previsao = previsao_data['list'][i]['weather'][0]['description']
            # Obtém a temperatura
            temperatura_previsao = previsao_data['list'][i]['main']['temp']

            texto_Data_previsao = customtkinter.CTkLabel(master=tabview.tab(
                "Tempo"), text=f'{dia_atual.day+i}/{dia_atual.month}', font=('Josefin Sans bold', 14), text_color=branco)
            texto_Data_previsao.place(x=30+135*i, y=0)  # Posiciona o texto

            # Imagem da previsão do tempo
            imagem_previsao = customtkinter.CTkImage(light_image=Image.open(icone_map.get(
                previsao, "nuvem.png")), dark_image=Image.open(icone_map.get(previsao, "nuvem.png")), size=(70, 70))

            # Posiciona a imagem
            label_imagem_previsao = customtkinter.CTkLabel(
                master=tabview.tab("Tempo"), image=imagem_previsao, text='')
            label_imagem_previsao.place(x=20+130*i, y=30)

            # Quebrar linha de palavra composta
            previsao = previsao.replace(' ', '\n')
            texto_previsao = customtkinter.CTkLabel(master=tabview.tab(
                "Tempo"), text=previsao, font=('Josefin Sans bold', 14), text_color=azul_claro)
            texto_previsao.place(x=20+130*i, y=110)

            # Posiciona a temperatura
            texto_temp_previsao = customtkinter.CTkLabel(master=tabview.tab(
                "Tempo"), text=f'{temperatura_previsao:.2f}°C', font=('Josefin Sans bold', 14), text_color=branco)
            texto_temp_previsao.place(x=20+130*i, y=160)

        # Milimetragem da chuva
        url_chuva = f'https://api.openweathermap.org/data/2.5/forecast?q={cidade},{pais}&appid={API_KEY}&lang=pt_br'
        request_chuva = requests.get(url_chuva)

        # Verifica se a solicitação foi bem-sucedida
        if request_chuva.status_code == 200:
            data_chuva = request_chuva.json()

            # Variável para armazenar a quantidade total de chuva
            total_chuva = 0

            # Itera pelos dados horários para obter a quantidade de chuva em cada intervalo de 3 horas
            for forecast in data_chuva['list']:
                # Converte o timestamp para a hora local
                hora_local = forecast['dt']

                # Verifica se a hora está entre 00:00 e 17:00
                if 0 <= hora_local <= 17 * 3600:
                    # Obtém a quantidade de chuva em cada intervalo de 3 horas
                    quantidade_chuva = forecast.get('rain', {}).get('3h', 0)
                    total_chuva += quantidade_chuva  # Soma a quantidade de chuva ao total

            # Atualiza a interface com a quantidade total de chuva
            texto_total_chuva = customtkinter.CTkLabel(master=tabview.tab(
                "Irrigação"), text=f'Total de chuva até as 17:00: {total_chuva} mm', font=('Josefin Sans bold', 14), text_color=azul_claro)
            texto_total_chuva.place(x=30, y=5)
            # Restante do código aqui...

    # funçao de remover a planta
    def remover_planta(self, planta_nome):
        con = lite.connect('water.db')
        cursor = con.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")

        cursor.execute(
            "DELETE FROM Plantacoes WHERE Planta = ?", (planta_nome,))
        con.commit()
        con.close()

        #adicionando a mensegem de sucesso
        messagebox.showinfo('Remoção', 'Planta removida com sucesso!')
        self.botao_planta.destroy()  # Remover o botão após a remoção da planta
        self.tela_minhaplantacao()  # Atualizar a tela

    def exibir_plantas(self):
        x_pos_planta = 55  # Posição inicial x do botão
        y_pos_planta = 150  # Posição inicial y do botão
        botao_width_planta = 100  # Largura do botão
        botao_height_planta = 40  # Altura do botão
        botao_margin_x_planta = 20  # Margem x entre os botões
        botao_margin_y_planta = 30  # Margem y entre os botões

        con = lite.connect('water.db')  # Conectando no banco de dados
        cursor = con.cursor()  # Criando o cursor
        cursor.execute(
            "SELECT Planta FROM Plantacoes WHERE User=?", (usuario_logado,))  # Obtendo as plantas do usuário, a partir da chave estrangeira
        plantas = cursor.fetchall()
        con.close()
        
        #Lógica do for : plantas é o resultado apartir do fetchall recupera todas as plantas do usuário e cria um botão ate que o número limites das 
        #plantas seja atingido, por isso o uso do for
        for planta in plantas:
            self.botao_planta = customtkinter.CTkButton(master=self.frame_myplant, text=planta[0], width=botao_width_planta, font=(
                'Josefin Sans bold', 12), fg_color='#ab4e02', command=lambda planta_nome=planta[0]: self.acessar_planta(planta_nome)) # Acessar a planta
            self.botao_planta.place(x=x_pos_planta, y=y_pos_planta) # Posicionar o botão

            x_pos_planta += botao_width_planta + botao_margin_x_planta

            if x_pos_planta + botao_width_planta > 700:  # Verificar se o botão ultrapassou a largura da tela que é 700
                x_pos_planta = 55  # Posicionar o botão na posição inicial 
                y_pos_planta += botao_height_planta + botao_margin_y_planta #atualizar o valor de y para que o botão seja posicionado na linha de baixo


    def tela_perfil(self):
        # Destruindo o frame anterior
        self.destruir_frame()

        # Criando a tela nova
        frame_perfil = customtkinter.CTkFrame(
            master=self.root, width=700, height=396)
        frame_perfil.pack()

        # Editando o frame
        label_perfil = customtkinter.CTkLabel(master=frame_perfil, text='PERFIL :', font=(
            'Josefin Sans bold', 30), text_color=laranja)
        label_perfil.place(x=25, y=5)

        l_apelido = customtkinter.CTkLabel(master=frame_perfil, text='Apelido :', font=(
            'Josefin Sans bold', 20), text_color=laranja)
        l_apelido.place(x=25, y=110)

        l_senha = customtkinter.CTkLabel(master=frame_perfil, text='Senha :', font=(
            'Josefin Sans bold', 20), text_color=laranja)
        l_senha.place(x=345, y=110)

        l_nome = customtkinter.CTkLabel(master=frame_perfil, text='Nome :', font=(
            'Josefin Sans bold', 20), text_color=laranja)
        l_nome.place(x=25, y=160)

        l_sobrenome = customtkinter.CTkLabel(master=frame_perfil, text='Sobrenome :', font=(
            'Josefin Sans bold', 20), text_color=laranja)
        l_sobrenome.place(x=345, y=160)

        l_idade = customtkinter.CTkLabel(master=frame_perfil, text='Idade :', font=(
            'Josefin Sans bold', 20), text_color=laranja)
        l_idade.place(x=25, y=210)

        l_email = customtkinter.CTkLabel(master=frame_perfil, text='Email :', font=(
            'Josefin Sans bold', 20), text_color=laranja)
        l_email.place(x=345, y=210)

        l_cidade = customtkinter.CTkLabel(master=frame_perfil, text='Cidade :', font=(
            'Josefin Sans bold', 20), text_color=laranja)
        l_cidade.place(x=25, y=260)

        l_pais = customtkinter.CTkLabel(master=frame_perfil, text='País :', font=(
            'Josefin Sans bold', 20), text_color=laranja)
        l_pais.place(x=345, y=260)

        con = lite.connect('water.db')
        cursor = con.cursor()

        consulta = "SELECT * FROM Usuarios WHERE apelido = ?"
        cursor.execute(consulta, (usuario_logado,))
        resultado = cursor.fetchone()

        if resultado:
            # Preencher os labels com os dados do usuário
            l_apelido_valor = customtkinter.CTkLabel(master=frame_perfil, text=resultado[0], font=(
                'Josefin Sans bold', 14), text_color=branco)
            l_apelido_valor.place(x=120, y=115)

            l_senha_valor = customtkinter.CTkLabel(master=frame_perfil, text=resultado[7], font=(
                'Josefin Sans bold', 14), text_color=branco)
            l_senha_valor.place(x=420, y=115)

            l_nome_valor = customtkinter.CTkLabel(master=frame_perfil, text=resultado[1], font=(
                'Josefin Sans bold', 14), text_color=branco)
            l_nome_valor.place(x=110, y=160)

            l_sobrenome_valor = customtkinter.CTkLabel(master=frame_perfil, text=resultado[2], font=(
                'Josefin Sans bold', 14), text_color=branco)
            l_sobrenome_valor.place(x=470, y=165)

            l_idade_valor = customtkinter.CTkLabel(master=frame_perfil, text=resultado[3], font=(
                'Josefin Sans bold', 14), text_color=branco)
            l_idade_valor.place(x=110, y=215)

            l_email_valor = customtkinter.CTkLabel(master=frame_perfil, text=resultado[4], font=(
                'Josefin Sans bold', 14), text_color=branco)
            l_email_valor.place(x=415, y=215)

            l_cidade_valor = customtkinter.CTkLabel(master=frame_perfil, text=resultado[5], font=(
                'Josefin Sans bold', 14), text_color=branco)
            l_cidade_valor.place(x=110, y=265)

            l_pais_valor = customtkinter.CTkLabel(master=frame_perfil, text=resultado[6], font=(
                'Josefin Sans bold', 14), text_color=branco)
            l_pais_valor.place(x=410, y=265)
        con.close()

        # Botão de voltar
        def botao_voltar_perfil():
            frame_perfil.pack_forget()
            self.tela_gerenciamento()

        b_voltar = customtkinter.CTkButton(master=frame_perfil, command=botao_voltar_perfil,
                                           text='VOLTAR', width=150, font=('Josefin Sans bold', 14), fg_color=amarelo)
        b_voltar.place(x=25, y=350)


if __name__ == "__main__":
    root = CTk()
    app = WaterFriendlyApp(root)
    root.mainloop()
