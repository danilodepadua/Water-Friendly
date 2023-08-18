#instruçoes para colocar o codigo de forma assincrona 
import asyncio
import aiohttp  #lembre de instelar o aiohttp na sua máquina. (pip install aiohttp)
#remova o import request, antes ele servia para salvar as informações coletadas da api, agora é o aiohttp que faz isso.

#substitua a funçao def acessar_planta por isso : 
#retirei os comandos da api da funçao e coloquei numa função assincrona separada para ficar mais organizado e mais facil
#depois so puxei essa função com o comando asyncio.run(...) 
def acessar_planta(self, planta_nome):
        # atribuindo imagens para a previsao do tempo-------------------------
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
        botao_update_2 = customtkinter.CTkButton(master=self.frame_planta, text='ATUALIZAR', command=lambda: self.alterar_tamanho(planta_nome), width=150, font=(
            'Josefin Sans bold', 14), fg_color=azul)
        botao_update_2.place(x=320, y=500)

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
        # crinado o grafico de area-------------------------------------------------------------------
        fig, ax = plt.subplots(figsize=(10, 10))
        ax.pie([area_total-area_planta, area_planta], labels=['Área total', 'Área da planta'], autopct='%1.1f%%',
               textprops={'fontsize': 30, 'color': 'white'}, colors=[azul_claro, laranja])
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
        
        #conexao com o banco de dados--------------------------------------------------------------------------------------------
        con = lite.connect('water.db')  # Abrir a conexão com o banco de dados
        cursor = con.cursor()   # Criar um cursor para executar as consultas
        # Habilitar as chaves estrangeiras
        cursor.execute("PRAGMA foreign_keys = ON")
        cursor.execute(
            "SELECT * from Usuarios WHERE apelido = ? ", (usuario_logado,))  # Consulta para obter a cidade e o país do usuário
        resultado = cursor.fetchone()  # Retorna uma tupla com os dados do usuário
        cidade_2 = resultado[5]  # A cidade está na posição 5 da tupla
        pais_2 = resultado[6]  # O país está na posição 6 da tupla
        con.close()  # Fechar a conexão com o banco de dados    
        
        
        #chamando a função de previsão do tempo e agua da chuva ---------------------------------------------------------
        asyncio.run(self.exibir_previsao(cidade_2, pais_2, tabview)) #rodar de forma assincrona dentro de uma função normal

        # relatorio de irrigação---------------------------------------------------------
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
    
    # assicronizar a previsão do tempo---------------------------------------------------
    async def exibir_previsao(self, cidade_2, pais_2, tabview):
        previsao_url = f'https://api.openweathermap.org/data/2.5/forecast?q={cidade_2},{pais_2}&appid={API_KEY}&lang=pt_br&units=metric&cnt=5' # url da previsao do tempo
        async with aiohttp.ClientSession() as session: #criar uma sessão para fazer a requisição dos dados da api,com o Client ,não precisa do request pois o aiohttp já faz isso 
            async with session.get(previsao_url) as response: #o session.get pega os dados HTTP da API, chama ele e transforma em uma variavel response pra ficar mais facil de trabalhar
                previsao_data = await response.json() #transforma a resposta da API em um dicionario com o json, o await espera a resposta da API, e depois transforma a resposta em um dicionario com o json, precisa esperar pegar todos os dados da API
                #await é sempre necessario quando for fazer uma requisição de uma API assincrona
        dia_atual = datetime.datetime.now() #pegar a data atual
        
        #colocar agua da chuva---------------------------------------------------------
        if response.status == 200:  #se retornar 200, significa que a requisição foi bem sucedida 
                    #await espera a resposta da API, e depois transforma a resposta em um dicionario com o json, precisa esperar pegar todos os dados da API 
                    if 'rain' in previsao_data['list'][0]:  #se tiver chuva na previsao diaria 
                        chuva_3h = previsao_data['list'][0]['rain']['3h'] #pegar a quantidade de chuva em 3 horas pois é assim que a API retorna, a cada 3 horas
                        quantidade_chuva_diaria = chuva_3h  * 8 #como estou rodando o programa poucas vezes, multiplico por 8 para ter uma quantidade de chuva diaria seria 3x8=24
                        #texto da chuva diaria---------------------------------------------------------
                        texto_chuva_diaria = customtkinter.CTkLabel(master=tabview.tab(
                            "Irrigação"), text=f'Chuva diária: {quantidade_chuva_diaria} mm', font=('Josefin Sans bold', 14), text_color=azul_claro)
                        texto_chuva_diaria.place(x=30, y=5) # Posiciona o texto
        
        #for pra criar a previsão do tempo---------------------------------------------------------
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
