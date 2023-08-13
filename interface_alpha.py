from tkinter import messagebox
import customtkinter
import sqlite3 as lite
from customtkinter import *
from tkinter import *

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

 

# definindo cores
laranja = '#de4300'
azul = '#02179c'
amarelo = '#948501'
vermelho = '#c20404'
verde = '#00e099'
preto = '#151716'
branco = '#c9c9c9'
usuario_logado = None


# funçao para destruir frames
def destruir_frame():
    for frame in janela.winfo_children():
        frame.destroy()

# mostrar senha :
def mostrar_senha():
    if check_box.get() == 1:
        entry_senha.configure(show='')
    else:
        entry_senha.configure(show='*')

# Tela de verificar :
def verificar_credenciais(usuario, senha):
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

# verificar login :
def fazer_login():
    global usuario_logado
    usuario = entry_usuario.get()
    senha = entry_senha.get()

    if not usuario or not senha:
        messagebox.showwarning('Login', 'Preencha todos os campos!')
        return

    if usuario == 'admin' and senha == 'admin':
        messagebox.showinfo('Login', 'Seja bem-vindo, Admin!')
        tela_gerenciamento()

    elif verificar_credenciais(usuario, senha):
        usuario_logado = usuario
        messagebox.showinfo('Login', f'Seja bem-vindo, {usuario}!')
        tela_gerenciamento()

    else:
        messagebox.showwarning('Login', 'Usuário ou senha incorretos')

# tela de cadastro
def pagina_cadastro():

    frame_right.pack_forget()
    frame_left.pack_forget()
    # criando a tela nova :
    frame_cadastro_inteiro = customtkinter.CTkFrame(
        master=janela, width=700, height=396)
    frame_cadastro_inteiro.pack()

    # editando o frame
    label_cadastro = customtkinter.CTkLabel(master=frame_cadastro_inteiro, text='CADASTRO :',
                                            font=('Josefin Sans bold', 30), text_color=laranja)
    label_cadastro.place(x=25, y=5)

    # editando o entry de usuario
    entry_usuario = customtkinter.CTkEntry(
        master=frame_cadastro_inteiro, width=300, placeholder_text='Usuário')
    entry_usuario.place(x=25, y=90)

    # editando o entry do nome
    entry_nome = customtkinter.CTkEntry(
        master=frame_cadastro_inteiro, width=300, placeholder_text='Nome')
    entry_nome.place(x=25, y=160)

    # editando o entry do sobrenome
    entry_sobrenome = customtkinter.CTkEntry(
        master=frame_cadastro_inteiro, width=300, placeholder_text='Sobrenome')
    entry_sobrenome.place(x=25, y=230)

    # editando o entry da idade
    entry_idade = customtkinter.CTkEntry(
        master=frame_cadastro_inteiro, width=300, placeholder_text='Idade')
    entry_idade.place(x=25, y=300)

    # editando o entry do Email
    entry_email = customtkinter.CTkEntry(
        master=frame_cadastro_inteiro, width=300, placeholder_text='Email')
    entry_email.place(x=350, y=90)

    # editando o entry da cidade
    entry_cidade = customtkinter.CTkEntry(
        master=frame_cadastro_inteiro, width=300, placeholder_text='Cidade')
    entry_cidade.place(x=350, y=160)

    # sigla do Pais
    entry_pais = customtkinter.CTkEntry(
        master=frame_cadastro_inteiro, width=300, placeholder_text='Sigla do País')
    entry_pais.place(x=350, y=230)

    # editando o entry da senha
    entry_senha = customtkinter.CTkEntry(
        master=frame_cadastro_inteiro, width=300, placeholder_text='Senha', show='*')
    entry_senha.place(x=350, y=300)

    def cadastrar_no_banco():
        usuario = entry_usuario.get()
        nome = entry_nome.get()
        sobrenome = entry_sobrenome.get()
        idade = entry_idade.get()
        email = entry_email.get()
        cidade = entry_cidade.get()
        pais = entry_pais.get()
        senha = entry_senha.get()

        con = lite.connect('water.db')
        cursor = con.cursor()

        try:
            # Verificar se o apelido já existe no banco de dados
            cursor.execute(
                "SELECT * FROM Usuarios WHERE apelido = ?", (usuario,))
            existing_user = cursor.fetchone()

            if existing_user:
                messagebox.showerror(
                    'Cadastro', 'O apelido já está em uso. Escolha outro apelido.')
                con.close()  # Fechar a conexão com o banco de dados
                # Permanecer na página de cadastro

            else:
                cursor.execute("INSERT INTO Usuarios VALUES(?,?,?,?,?,?,?,?)",
                               (usuario, nome, sobrenome, idade, email, cidade, pais, senha))
                con.commit()
                messagebox.showinfo(
                    'Cadastro', 'Cadastro realizado com sucesso!')

                global usuario_logado
                usuario_logado = usuario

                tela_gerenciamento()
        except:
            messagebox.showerror('Cadastro', 'Erro ao cadastrar!')

        con.close()

    # botao de voltar para o login

    def voltar_login():
        # esquecer o frame do cadastro
        frame_cadastro_inteiro.pack_forget()
        # recriar os frames do login
        frame_right.pack(side=RIGHT)
        frame_left.pack(side=LEFT)

    # botao de voltar
    botao_voltar = customtkinter.CTkButton(master=frame_cadastro_inteiro, height=0, text='VOLTAR', width=150, font=(
        'Josefin Sans bold', 14), fg_color=amarelo, command=voltar_login)
    botao_voltar.place(x=150, y=350)
    botao_voltar.configure(corner_radius=10)

    def avancar_pagina():
        # condição de avançar na pagina, coleta todas as informações
        usuario = entry_usuario.get()
        nome = entry_nome.get()
        sobrenome = entry_sobrenome.get()
        idade = entry_idade.get()
        email = entry_email.get()
        cidade = entry_cidade.get()
        pais = entry_pais.get()
        senha = entry_senha.get()

        # faz a verificação se todos os campos estão preenchidos
        if any(not field for field in [usuario, nome, sobrenome, idade, email, cidade, pais, senha]):
            messagebox.showerror('Cadastro', 'Preencha todos os campos!')
            

        # Usuário que está logado no momento
        # Se a função cadastrar_no_banco() retornar False, não avança para a próxima página
        # Caso contrário, avança normalmente
  

    botao_cadastrar = customtkinter.CTkButton(
        master=frame_cadastro_inteiro, height=0, text='CADASTRAR', width=150,
        font=('Josefin Sans bold', 14), fg_color=laranja, command=avancar_pagina)
    botao_cadastrar.place(x=350, y=350)
    botao_cadastrar.configure(corner_radius=10)

# tela gerenciamento :
def tela_gerenciamento():
    # destroindo a tela de login
    frame_right.pack_forget()
    frame_left.pack_forget()
    
    # criando a tela nova :
    frame_gerenciamento_inteiro = customtkinter.CTkFrame(
        janela, width=700, height=706)
    frame_gerenciamento_inteiro.pack()

    # editando o frame
    label_gerenciamento = customtkinter.CTkLabel(
        master=frame_gerenciamento_inteiro, text='GERENCIAMENTO :', font=('Josefin Sans bold', 30), text_color=laranja)
    label_gerenciamento.place(x=25, y=5)
    botao_perfil = customtkinter.CTkButton(master=frame_gerenciamento_inteiro, command=tela_perfil, text='PERFIL', width=150, font=(
        'Josefin Sans bold', 14), fg_color=laranja)
    botao_perfil.place(x=150, y=120)
    botao_perfil.configure(corner_radius=10)
    botao_minhaplantacao = customtkinter.CTkButton(
        master=frame_gerenciamento_inteiro, command=tela_minhaplantacao, text='MINHA PLANTAÇÃO', width=150, font=('Josefin Sans bold', 14), fg_color=laranja)
    botao_minhaplantacao.place(x=350, y=120)
    botao_minhaplantacao.configure(corner_radius=10)

    # botao de logout
    def logout():
        janela.destroy()

    botao_logout = customtkinter.CTkButton(master=frame_gerenciamento_inteiro, command=logout, text='SAIR', width=150, font=(
        'Josefin Sans bold', 14), fg_color=vermelho)
    botao_logout.place(x=250, y=250)
    
# tela minhas plantaçao :
def tela_minhaplantacao():
    destruir_frame()

    # criando a tela nova :
    frame_scroll = customtkinter.CTkScrollableFrame(
        master=janela, width=700, height=396)
    frame_scroll.pack()

    # botao de voltar

    def botao_voltar():
        frame_scroll.pack_forget()
        tela_gerenciamento()

    botao_voltar_1 = customtkinter.CTkButton(master=frame_scroll, command=botao_voltar, text='VOLTAR', width=150, font=(
        'Josefin Sans bold', 14), fg_color=amarelo)
    botao_voltar_1.place(x=290, y=350)

    def adicionar_area():
        destruir_frame()

        # criando a tela nova :
        frame_adicionar_area = customtkinter.CTkFrame(
            master=janela, width=700, height=396)
        frame_adicionar_area.pack()

        # editando o frame
        label_adicionar_area = customtkinter.CTkLabel(
            master=frame_adicionar_area, text='ADICIONAR ÁREA :', font=('Josefin Sans bold', 30), text_color=laranja)
        label_adicionar_area.place(x=25, y=5)

        # editando o entry de usuario
        entry_area = customtkinter.CTkEntry(
            master=frame_adicionar_area, width=300, placeholder_text='Tamanho da área da planta em hectares')
        entry_area.place(x=25, y=90)

        entry_cultura = customtkinter.CTkEntry(
            master=frame_adicionar_area, width=300, placeholder_text='Tipo de planta')
        entry_cultura.place(x=350, y=90)

        # coletando dados e salvando no banco de dados
        def AdicionarPlantacao():
            tamanho = entry_area.get()
            planta = entry_cultura.get()

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

            except:
                messagebox.showerror('Cadastro', 'Erro ao cadastrar!')

            con.close()

        botao_salvar = customtkinter.CTkButton(master=frame_adicionar_area, text='SALVAR', width=150,
                                               font=('Josefin Sans bold', 14), fg_color=laranja, command=AdicionarPlantacao)
        botao_salvar.place(x=360, y=300)

        # botao de voltar
        def botao_voltar():
            frame_adicionar_area.pack_forget()
            tela_minhaplantacao()
        botaovoltar = customtkinter.CTkButton(master=frame_adicionar_area, command=botao_voltar,
                                              text='VOLTAR', width=150, font=('Josefin Sans bold', 14), fg_color=amarelo)
        botaovoltar.place(x=190, y=300)

    con = lite.connect('water.db')
    cursor = con.cursor()
    cursor.execute("SELECT Planta FROM Plantacoes WHERE User=?",
                   (usuario_logado,))
    plantas = cursor.fetchall()
    con.close()
    
    #acessando o botão de cada planta
    def acessar_planta():
        frame_scroll.pack_forget()
        frame_planta = customtkinter.CTkFrame(janela, width=700, height=396)
        frame_planta.pack()


    # Configuração do espaçamento entre os botões das plantas
    espacamento_vertical = 100
    espacamento_horizontal = 100

    # Configuração da linha que contém os botões das plantas
    frame_scroll.rowconfigure(2, minsize=espacamento_vertical)

    # Configuração das colunas para os botões das plantas
    for i in range(3):  # Número de colunas para os botões das plantas
        frame_scroll.columnconfigure(i, minsize=espacamento_horizontal)

    coluna = 0
    linha = 3

    # criar botao para cada planta
    for i in range(len(plantas)):
        botao_planta = customtkinter.CTkButton(master=frame_scroll,command=acessar_planta ,text=plantas[i][0], width=150, font=(
            'Josefin Sans bold', 14), fg_color='#737373')
        botao_planta.grid(row=linha, column=coluna, padx=10, pady=5)

        coluna += 1
        if coluna > 2:
            coluna = 0
            linha += 1

    # editando o frame
    label_minhaplantacao = customtkinter.CTkLabel(
        master=frame_scroll, text='MINHA PLANTAÇÃO :', font=('Josefin Sans bold', 30), text_color=laranja)
    label_minhaplantacao.grid(
        row=0, column=0, columnspan=3, padx=25, pady=5, sticky='w')

    botao_remover = customtkinter.CTkButton(frame_scroll, text='REMOVER', width=150, font=(
        'Josefin Sans bold', 14), fg_color=vermelho)
    botao_remover.grid(row=2, column=0, padx=10, pady=5)

    botao_adicionar_crud = customtkinter.CTkButton(master=frame_scroll, command=adicionar_area, text='ADICIONAR', width=150, font=(
        'Josefin Sans bold', 14), fg_color=verde, text_color='black')
    botao_adicionar_crud.grid(row=2, column=1, padx=10, pady=5)

    botao_update = customtkinter.CTkButton(
        frame_scroll, text='UPDATE', width=150, font=('Josefin Sans bold', 14), fg_color=azul)
    botao_update.grid(row=2, column=2, padx=10, pady=5)

    botao_voltar_1 = customtkinter.CTkButton(master=frame_scroll, command=botao_voltar, text='VOLTAR', width=150, font=(
        'Josefin Sans bold', 14), fg_color=amarelo)
    botao_voltar_1.grid(row=2, column=3, padx=10, pady=5)

# Tela de perfil : 
def tela_perfil():
    destruir_frame()

    # criando a tela nova :
    frame_perfil = customtkinter.CTkFrame(master=janela, width=700, height=396)
    frame_perfil.pack()

    # editando o frame
    label_perfil = customtkinter.CTkLabel(master=frame_perfil, text='PERFIL :', font=(
        'Josefin Sans bold', 30), text_color=laranja)
    label_perfil.place(x=25, y=5)

    l_apelido = customtkinter.CTkLabel(master=frame_perfil, text='Apelido :', font=(
        'Josefin Sans bold', 20), text_color=laranja)
    l_apelido.place(x=25, y=110)

    l_senha = customtkinter.CTkLabel(master=frame_perfil, text='Senha :', font=(
        'josefin Sans bold', 20), text_color=laranja)
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

    # botao de voltar
    def botao_voltar_perfil():
        frame_perfil.pack_forget()
        tela_gerenciamento()

    b_voltar = customtkinter.CTkButton(master=frame_perfil, command=botao_voltar_perfil,
                                       text='VOLTAR', width=150, font=('Josefin Sans bold', 14), fg_color=amarelo)
    b_voltar.place(x=25, y=350)

# criando a janela
janela = customtkinter.CTk()
janela.title("Water friendly")
janela.geometry("700x400")
janela.resizable(width=False, height=False)
# dividindo a janela com frames:
frame_right = customtkinter.CTkFrame(master=janela, width=350, height=396)
frame_right.pack(side=RIGHT)
frame_left = customtkinter.CTkFrame(
    master=janela, width=350, height=396, fg_color='#151716')
frame_left.pack(side=LEFT)
# editando o frame
label_login = customtkinter.CTkLabel(master=frame_right, text='LOGIN :', font=(
    'Josefin Sans bold', 25), text_color=laranja)
label_login.place(x=25, y=5)
# editando o entry de login
entry_usuario = customtkinter.CTkEntry(master=frame_right, width=300,
                                       font=('Josefin Sans bold', 14), placeholder_text='Nome de usuário')
entry_usuario.place(x=25, y=105)
# editando o entry da senha
entry_senha = customtkinter.CTkEntry(master=frame_right, width=300,
                                     font=('Josefin Sans bold', 14), placeholder_text='Senha', show='*')
entry_senha.place(x=25, y=175)
# checkbutton
check_box = customtkinter.CTkCheckBox(
    master=frame_right, text='Mostrar senha', onvalue=1, offvalue=0, command=mostrar_senha)
check_box.place(x=25, y=245)
# botão de login
botao_login = customtkinter.CTkButton(
    master=frame_right, text='ENTRAR', width=300, font=('Josefin Sans bold', 14), fg_color=laranja, command=fazer_login)
botao_login.place(x=25, y=285)
# label de cadastro
label_cadastro = customtkinter.CTkLabel(master=janela, text='Não tem uma conta?', font=(
    'Josefin Sans bold', 25), text_color=laranja, bg_color='#151716')
label_cadastro.place(x=35, y=95)
label_cadastro2 = customtkinter.CTkLabel(
    master=janela, text='Cadastre-se agora', bg_color='#151716', font=('Josefin Sans bold', 20))
label_cadastro2.place(x=70, y=135)
# botão de cadastro
botao_cadastro = customtkinter.CTkButton(master=janela, text='CADASTRAR', command=pagina_cadastro, width=200, font=(
    'Josefin Sans bold', 15), fg_color=laranja)
botao_cadastro.place(x=60, y=190)
janela.mainloop()
