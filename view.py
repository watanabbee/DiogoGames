import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox,ttk,filedialog

class LayoutBase(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="white")
        
        self.frame_topo = tk.Frame(self, bg="#d2a679", height=80)
        self.frame_topo.pack(fill="x")
        tk.Label(self.frame_topo, text="Padaria VC++", bg="#d2a679", fg="black",
                 font=("Arial", 20, "bold")).grid(row=0, column=0, sticky="w", padx=10, pady=5)
        tk.Label(self.frame_topo, text="Av. Das Padarias nº92", bg="#d2a679", fg="black",
                 font=("Arial", 10)).grid(row=1, column=0, sticky="w", padx=10)

        self.frame_conteudo = tk.LabelFrame(self, bg="white")
        self.frame_conteudo.pack(fill="both", expand=True, padx=20, pady=40)

        self.frame_rodape = tk.Frame(self, bg="white", height=50)
        self.frame_rodape.pack(fill="x", pady=5)

    def adicionar_botao_rodape(self, texto, comando, lado="left"):
        tk.Button(self.frame_rodape, text=texto, width=10, bg="#f6f9fb", command=comando).pack(side=lado, padx=10)

class Main(LayoutBase):
    def __init__(self, controller):
        self.root = tk.Tk()
        self.root.title("Padaria VC++")
        self.root.geometry("700x600")
        self.root.configure(bg="white")
        self.root.resizable(False, False)

        super().__init__(self.root)

        self.controller = controller
        self.controller.set_main_view(self)


        self.telaAtual = None
        self.tela1 = Tela1View(self.root, self.controller)
        self.tela2 = Tela2View(self.root, self.controller)
        self.tela3 = Tela3View(self.root, self.controller)
        self.telaJogo = TelaJogo(self.root, self.controller)
        self.telaJogoExtendida = TelaJogoExtendida(self.root, self.controller)
        self.tela4 = Tela4View(self.root, self.controller)
        self.telaADM = TelaADM(self.root, self.controller)

        self.controller.set_telas(
            tela1=self.tela1,
            tela2=self.tela2,
            tela3=self.tela3,
            telaJogo=self.telaJogo,
            telaJogoExtendida=self.telaJogoExtendida,
            tela4=self.tela4,
            telaADM=self.telaADM
        )

    def get_root(self):
        return self.root
    
    def mostrarTela(self, tela):
        if self.telaAtual:
            self.telaAtual.pack_forget()
        self.telaAtual = tela
        self.telaAtual.pack(fill="both", expand=True)

    def get_tela_atual(self):
        return self.telaAtual

    def iniciar(self):
        self.root.mainloop()

class Tela1View(LayoutBase):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.criar_frames()

    def criar_frames(self):

        frame_corpo = tk.Frame(self.frame_conteudo,bg="white")
        frame_corpo.pack(expand=True, pady=20)
        frame_login = tk.LabelFrame(frame_corpo, text="Login",bg="white", padx=10, pady=10)
        frame_login.grid(row=0, column=0, padx=20, pady=10)

        tk.Label(frame_login, text="Email:",bg="white").grid(row=0, column=0, sticky="e")
        tk.Label(frame_login, text="Senha:",bg="white").grid(row=1, column=0, sticky="e")
        tk.Label(frame_login,bg="white").grid(row=2, column=0, sticky="e")
        tk.Label(frame_login,bg="white").grid(row=3, column=0, sticky="e")

        self.email_login_var = tk.StringVar()
        self.senha_login_var = tk.StringVar()

        tk.Entry(frame_login, textvariable=self.email_login_var).grid(row=0, column=1)
        tk.Entry(frame_login, textvariable=self.senha_login_var, show="*").grid(row=1, column=1)

        tk.Button(frame_login, text="Entrar", bg="#f6f9fb", command=lambda: self.entrarConta()).grid(row=4, column=0, columnspan=2, pady=(70,0))

        frame_criar = tk.LabelFrame(frame_corpo, text="Criar Usuário",bg="white", padx=10, pady=10)
        frame_criar.grid(row=0, column=1, padx=20, pady=10)

        tk.Label(frame_criar, text="Nome:",bg="white").grid(row=0, column=0, sticky="e")
        tk.Label(frame_criar, text="Email:",bg="white").grid(row=1, column=0, sticky="e")
        tk.Label(frame_criar, text="Idade:",bg="white").grid(row=2, column=0, sticky="e")
        tk.Label(frame_criar, text="Senha:",bg="white").grid(row=3, column=0, sticky="e")

        self.nome_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.idade_var = tk.StringVar()
        self.senha_var = tk.StringVar()

        tk.Entry(frame_criar, textvariable=self.nome_var).grid(row=0, column=1)
        tk.Entry(frame_criar, textvariable=self.email_var).grid(row=1, column=1)
        tk.Entry(frame_criar, textvariable=self.idade_var).grid(row=2, column=1)
        tk.Entry(frame_criar, textvariable=self.senha_var, show="*").grid(row=3, column=1)

        tk.Button(frame_criar, text="Criar Conta", bg="#f6f9fb",command=lambda: self.set_CriarConta()).grid(row=4, column=0, columnspan=2, pady=(70,0))

        self.adicionar_botao_rodape("Sair", comando=lambda: self.controller.exit(), lado="left")
    
    def get_entradas(self):
        nome = self.nome_var.get()
        email = self.email_var.get()
        idade = self.idade_var.get()
        senha = self.senha_var.get()
        Conta = (nome,email,idade,senha)
        return Conta
    
    def set_CriarConta(self):
        conta = self.get_entradas()
        retorno = self.controller.set_criarConta(conta)
        if retorno:
            messagebox.showerror("Erro de Validação", retorno)
        else:
            messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")
            self.limpar_campos()
            self.controller.gerenciador_telas(2)

    def entrarConta(self):
        email = self.email_login_var.get()
        senha = self.senha_login_var.get()
        retorno = self.controller.verifConta(email,senha)

        if retorno:
            if type(retorno) == str:
                messagebox.showerror("Erro de Login", retorno)
            elif type(retorno) == int:
                messagebox.showinfo("Sucesso", 'Bem vindo ADM')
                self.limpar_campos()
        else:
            messagebox.showinfo("Sucesso", 'Logado com Sucesso')
            self.limpar_campos()


    def limpar_campos(self):
        self.email_login_var.set("")
        self.senha_login_var.set("")
        self.nome_var.set("")
        self.email_var.set("")
        self.idade_var.set("")
        self.senha_var.set("")

class Tela2View(LayoutBase):

    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.produtos = self.controller.get_Produto()
        self.fotos = []
        self.criar_frames()
        self.exibir_produtos(self.produtos)

        
    def criar_frames(self):
        cardapioLabel = tk.Label(self.frame_conteudo, text="Cardápio", bg="white",
                 font=("Arial", 18, "bold"))
        cardapioLabel.pack(pady=10)

        frame_busca = tk.Frame(self.frame_conteudo, bg="white", height=50)
        frame_busca.pack(fill="x", pady=5)

        buscarLabel = tk.Label(frame_busca, text="Buscar:", bd=3,bg="white", font=("Arial", 12))
        buscarLabel.pack(side="left", padx=10)

        self.busca_var = tk.StringVar()
        self.busca_entry = tk.Entry(frame_busca, textvariable=self.busca_var,bd=2, width=50)
        self.busca_entry.pack(side="left", padx=5)

        pesqButton = tk.Button(frame_busca, text="Pesquisar", command=lambda: self.filtrarProdutos())
        pesqButton.pack(side="left", padx=5)
        LimparButton =tk.Button(frame_busca, text="Limpar Filtro", command=lambda: self.limparFiltro())
        LimparButton.pack(side="left", padx=5)

        frame_conteudo = tk.Frame(self.frame_conteudo, bg="white")
        frame_conteudo.pack(fill="both", expand=True, padx=10, pady=5)

        canvas = tk.Canvas(self.frame_conteudo, bd=3,bg="white")
        scrollbar = ttk.Scrollbar(self.frame_conteudo, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        self.produtos_frame = tk.Frame(canvas,bd=3, bg="white")
        self.produtos_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.produtos_frame, anchor="nw")

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.adicionar_botao_rodape("Voltar", comando=lambda: self.controller.gerenciador_telas(1), lado="left")
        self.adicionar_botao_rodape("Seguir", comando=lambda: self.controller.gerenciador_telas(3), lado="right")

    def setProdutos(self):
        self.produtos = self.controller.get_Produto()

    def filtrarProdutos(self):
        termoBusca = self.busca_entry.get().lower()
        self.controller.filtrarProdutos(termoBusca)
    
    def limparFiltro(self):
        self.controller.filtrarProdutos(None)
        self.busca_var.set("")

    def carregar_imagem(self, caminho, tamanho=(80, 80)):
        try:
            imagem = Image.open(caminho).resize(tamanho, Image.LANCZOS)
            foto = ImageTk.PhotoImage(imagem)
            self.fotos.append(foto)  
            return foto
        except:
            print(f"Erro ao carregar {caminho}")
            return None
        
    def exibir_produtos(self, produtos):
        for widget in self.produtos_frame.winfo_children():
            widget.destroy()

        max_colunas = 4

        for index, produto in enumerate(produtos):
            linha = index // max_colunas
            coluna = index % max_colunas

            frame = tk.Frame(self.produtos_frame, bd=1, relief="solid", bg="white", padx=10, pady=10)
            frame.grid(row=linha, column=coluna, padx=15, pady=15, sticky="nsew")

            foto = self.carregar_imagem(produto.imagem)
            if foto:
                tk.Label(frame, image=foto, bg="white").grid(row=0, column=0, columnspan=2)
            else:
                tk.Label(frame, text="[Imagem]", bg="white").grid(row=0, column=0, columnspan=2)

            tk.Label(frame, text=produto.nome, bg="white", font=("Arial", 12, "bold"), wraplength=120, justify="center").grid(row=2, column=0, columnspan=2, pady=5)
            tk.Label(frame, text=f"R$ {produto.preco}", bg="white", font=("Arial", 10)).grid(row=1, column=0, pady=5, sticky="w")
            btn_plus = tk.Button(frame, text="+", bg="#4CAF50", fg="white",width=2,
                             command=lambda p=produto: self.controller.mostrar_detalhes(p))
            btn_plus.place(relx=1.0, rely=0, anchor="ne")


class Tela2extendidaView(LayoutBase):

    def __init__(self, master, controller, produto):
        super().__init__(master)
        self.controller = controller
        self.produto = produto
        self.foto = None
        self.criar_frames()

    def criar_frames(self):

        frame = tk.Frame(self.frame_conteudo, bd=1, relief="solid", bg="white", padx=10, pady=10)
        frame.pack(fill="both", expand=True)

        tk.Label(frame, text=self.produto.nome, bg="white", font=("Arial", 16, "bold")).grid(
            row=0, column=0, columnspan=2, sticky="w", padx=10, pady=5
        )

        try:
            imagem = Image.open(self.produto.imagem).resize((150, 150), Image.LANCZOS)
            self.foto = ImageTk.PhotoImage(imagem)
            tk.Label(frame, image=self.foto, bg="white").grid(row=1, column=0, padx=10, pady=5)
        except:
            tk.Label(frame, text="[Imagem não disponível]", bg="white").grid(row=1, column=0, padx=10, pady=5)

        tk.Label(frame, text="Imagem ilustrativa", bg="white", font=("Arial", 8, "italic")).grid(
            row=2, column=0, padx=10, sticky="n"
        )

        info = f"Ingredientes: {self.produto.ingredientes}\n\nModo de Preparo: {self.produto.preparo}"
        tk.Label(frame, text=info, bg="white", justify="left", anchor="w", wraplength=400).grid(
            row=1, column=1, rowspan=2, sticky="nw", padx=10, pady=5
        )

        self.adicionar_botao_rodape("Voltar", comando=lambda: self.controller.gerenciador_telas(2), lado="left")


class Tela3View(LayoutBase):
    def __init__(self, master,controller):
        super().__init__(master)
        self.controller = controller
        self.criar_frames()

    def criar_frames(self):
        
        self.frame_conteudo.grid_columnconfigure(0, weight=1)
        self.frame_conteudo.grid_columnconfigure(1, weight=1)

        self.container_esquerdo = tk.Frame(self.frame_conteudo, bg="white")
        self.container_esquerdo.grid(row=0, column=0, sticky="nsew", padx=20, pady=10)
        self.container_esquerdo.grid_rowconfigure(0, weight=1)
        self.container_esquerdo.grid_rowconfigure(1, weight=1)
        self.container_esquerdo.grid_rowconfigure(2, weight=1)
        self.container_esquerdo.grid_columnconfigure(0, weight=1)

        self.container_direito = tk.Frame(self.frame_conteudo, bg="white")
        self.container_direito.grid(row=0, column=1, sticky="nsew", padx=(0,20), pady=10)
        self.container_direito.grid_rowconfigure(0, weight=1)
        self.container_direito.grid_rowconfigure(1, weight=1)
        self.container_direito.grid_rowconfigure(2, weight=1)
        self.container_direito.grid_rowconfigure(3, weight=1)
        self.container_direito.grid_columnconfigure(0, weight=1)


        self.criarContainerJogo()

        self.adicionar_botao_rodape("Voltar", comando=lambda: self.controller.gerenciador_telas(2), lado="left")

    def criarContainerCupons(self):

        tk.Label(self.container_esquerdo, text="Interessado em ganhar até\n20% de desconto em suas\ncompras físicas?",
                 bg="white", font=("Arial", 11), justify="left").grid(row=0, column=0, sticky="n", pady=(0, 20))

        frame_botoes = tk.Frame(self.container_esquerdo, bg="white")
        frame_botoes.grid(row=1, column=0, sticky="s")

        frame_botoes.grid_columnconfigure(0, weight=1)
        frame_botoes.grid_columnconfigure(1, weight=1)

        descontos = [5,8,10,14,17,20]

        for i, desc in enumerate(descontos):
            btn = tk.Button(frame_botoes, text=f"{desc}% OFF",font=("Arial", 10, "bold"), bg="#FFD700",
                            width=10, height=2)
            
            btn.grid(row=i // 2, column=i % 2, padx=5, pady=(0,30), sticky="nsew")

        tk.Button(self.container_esquerdo, text="Meus Cupons", command=lambda: self.controller.gerenciador_telas(6), width=15,
                  relief="solid").grid(row=2, column=0, pady=(40,0), sticky="s")

    def criarContainerJogo(self):

        tk.Label(self.container_direito, text="Então coma todos os Mistos\nQuentes possíveis!",
                 bg="white", font=("Arial", 11)).grid(row=0, column=0, sticky="n", pady=(0, 20))

        try:
            imagem = Image.open("imagens/misto.png")
            imagem = imagem.resize((240, 200), Image.LANCZOS)
            self.foto = ImageTk.PhotoImage(imagem)
            tk.Label(self.container_direito, image=self.foto, bg="white").grid(row=1,column=0,sticky="n")
        except:
            tk.Label(self.container_direito, text="[Imagem]", bg="white").grid(row=1,column=0)

        tk.Button(self.container_direito, text="Jogar", command = lambda: self.controller.gerenciador_telas(4), bg="#00cc00", fg="white",
                  width=15).grid(row=3, column=0, pady=(40,0), sticky="s")


class TelaJogo(LayoutBase):

    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.criar_frames()

    def criar_frames(self):


        self.frame_corpo = tk.Frame(self.frame_conteudo, bg="white")
        self.frame_corpo.pack(expand=True, pady=20)

        self.label_imagem = tk.Label(self.frame_corpo, text="mistos quentes comidos: 0", bg="white")
        self.label_imagem.grid(row=0, column=0)
        self.botao_imagem = None

        self.cronometro_label = tk.Label(self.frame_corpo, text="Tempo: 0.00 segundos", bg="white")
        self.cronometro_label.grid(row=2, column=0)
        

        self.adicionar_botao_rodape("Voltar", comando=lambda: self.controller.gerenciador_telas(3), lado="left")
        self.adicionar_botao_rodape("Seguir", comando=lambda: self.controller.gerenciador_telas(5), lado="right")
    
    def atualizar_mistoQuentes(self, comidos):
        self.label_imagem.config(text=f"mistos quentes comidos: {comidos}")

    def atualizar_tempo(self, tempo):
        self.cronometro_label.config(text=f"Tempo: {tempo:.2f} segundos")

    def atualizar_contador(self):
        self.atualizar_imagem()

    def atualizar_imagem(self):
        caminho = self.controller.get_CaminhoJogo()

        try:
            img = Image.open(caminho)
            img = img.resize((400, 300))
            self.foto = ImageTk.PhotoImage(img)

            if self.botao_imagem:
                self.botao_imagem.config(image=self.foto)
            else:
                self.botao_imagem = tk.Button(
                    self.frame_corpo, image=self.foto, command=lambda: self.acao_botao_imagem(),
                    borderwidth=0, highlightthickness=0, bg="white", activebackground="white"
                )
                self.botao_imagem.grid(row=1, column=0)

        except:
            print(f"Erro ao carregar {caminho}")
            if self.botao_imagem:
                self.botao_imagem.destroy()
            self.label_imagem.config(text="Imagem não encontrada", image="")

    def acao_botao_imagem(self):
        self.controller.incrementar_cliques()


class TelaJogoExtendida(LayoutBase):

    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.criar_frames()
    
    def criar_frames(self):
        
        self.frame_conteudo.grid_columnconfigure(0, weight=1)
        self.frame_conteudo.grid_columnconfigure(1, weight=1)

        self.container_esquerdo = tk.Frame(self.frame_conteudo, bg="white")
        self.container_esquerdo.grid(row=0, column=0, sticky="nsew", padx=20, pady=10)
        self.container_esquerdo.grid_rowconfigure(0, weight=1)
        self.container_esquerdo.grid_rowconfigure(1, weight=1)
        self.container_esquerdo.grid_rowconfigure(2, weight=1)
        self.container_esquerdo.grid_rowconfigure(3, weight=1)


        self.container_direito = tk.Frame(self.frame_conteudo, bg="white")
        self.container_direito.grid(row=0, column=1, sticky="nsew", padx=0, pady=10)
        self.container_direito.grid_rowconfigure(0, weight=1)
        self.container_direito.grid_rowconfigure(1, weight=1)
        self.container_direito.grid_rowconfigure(2, weight=1)
        self.container_direito.grid_rowconfigure(3, weight=1)

        self.label_imagem = None
        self.imagem_final = None
        self.cronometro_label = None
        self.fimJogo_label = None
        
        self.adicionar_botao_rodape("Voltar", comando=lambda: self.controller.gerenciador_telas(3), lado="left")
        self.adicionar_botao_rodape("Jogar", comando=lambda: self.controller.gerenciador_telas(4), lado="right")
    
    def get_imagemFinal(self):
        caminho = self.controller.get_CaminhoJogo()
        try:
            imagem = Image.open(caminho)
            imagem = imagem.resize((240, 200), Image.LANCZOS)
            self.foto = ImageTk.PhotoImage(imagem)
            self.imagem_final =tk.Label(self.container_esquerdo, image=self.foto, bg="white").grid(row=1,column=0,sticky="n")
        except:
            self.imagem_final =tk.Label(self.container_esquerdo, text="[Imagem]", bg="white").grid(row=1,column=0,sticky="n")

    def get_score(self):
        tempoFinal = self.controller.get_tempo_final()
        misto_comidos = self.controller.get_mistoComidos()
        
        self.label_imagem = tk.Label(self.container_esquerdo,text=f"mistos quentes comidos: {misto_comidos}", bg="white")
        self.label_imagem.grid(row=0, column=0, sticky="n",pady=(30,10))
        self.cronometro_label = tk.Label(self.container_esquerdo,text=f"Tempo: {tempoFinal:.2f} segundos", bg="white")
        self.cronometro_label.grid(row=2, column=0, sticky="s",pady=(30,70))
    
    def get_fimJogo(self):
        
        resultado = self.controller.get_resultado()
        if resultado:
            self.fimJogo_label = tk.Label(self.container_direito, text=f"Parabéns você ganhou um cupom:", bg="white")
            self.fimJogo_label.grid(row=0, column=0, sticky="n",pady=(30,10))
            cupom = tk.Button(self.container_direito, text=resultado, bg="#FFD700",width=20, height=4)
            cupom.grid(row=1, column=0, sticky="s",pady=(0,70))

        else:
            self.fimJogo_label = tk.Label(self.container_direito, text="Não foi dessa vez", bg="white")
            self.fimJogo_label.grid(row=0, column=0, sticky="n", pady=(0, 10))
    
class Tela4View(LayoutBase):

    def __init__(self, master,controller):
        super().__init__(master)
        self.controller = controller
        self.criar_frames()

    def criar_frames(self):
        self.frame_conteudo.grid_columnconfigure(0, weight=1)
        self.frame_conteudo.grid_rowconfigure(0, weight=1)

        self.adicionar_botao_rodape("Voltar", comando=lambda: self.controller.gerenciador_telas(3), lado="left")

    def criarContainerCupons(self):
        tk.Label(self.frame_conteudo, text="Meus Cupons",
                 bg="white", font=("Arial", 18, "bold"), justify="left").grid(row=0, column=0, sticky="n", pady=(0, 20))
        frame_botoes = tk.Frame(self.frame_conteudo, bg="white")
        frame_botoes.grid(row=0, column=0, sticky="nsew", pady=(60, 0))

        frame_botoes.grid_columnconfigure(0, weight=1)
        frame_botoes.grid_columnconfigure(1, weight=1)
        frame_botoes.grid_columnconfigure(2, weight=1)
        frame_botoes.grid_columnconfigure(3, weight=1)

        descontos = self.controller.get_cupons()

        for i, desc in enumerate(descontos):
            btn = tk.Button(frame_botoes, text=f"Cupom {desc}%",font=("Arial", 10, "bold"), bg="#FFD700",
                            width=10, height=2)
            btn.grid(row=i//4, column=i%4, padx=10, pady=10, sticky="nsew")

class TelaADM(LayoutBase):

    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.criar_frames()
        
    def criar_frames(self):

        frame_corpo = tk.Frame(self.frame_conteudo, bg="white")
        frame_corpo.pack(expand=True, pady=20)

        frameEsquerdo = tk.LabelFrame(frame_corpo, text="Produtos", bg="white", padx=10, pady=10)
        frameEsquerdo.grid(row=0, column=0, padx=(5,25), pady=10)

        tk.Label(frameEsquerdo, text="Nome:", bg="white").grid(row=0, column=0, sticky="e", pady=3)
        tk.Label(frameEsquerdo, text="Ingredientes:", bg="white").grid(row=1, column=0, sticky="e", pady=3)
        tk.Label(frameEsquerdo, text="Modo de preparo:", bg="white").grid(row=2, column=0, sticky="ne", pady=3)
        tk.Label(frameEsquerdo, text="Preço:", bg="white").grid(row=3, column=0, sticky="e", pady=3)

        self.nomeProduto_var = tk.StringVar()
        self.ingredienteProduto_var = tk.StringVar()
        self.precoProduto_var = tk.StringVar()
        self.ImageName = tk.StringVar(value="imagem.png")
        self.caminho_imagem = tk.StringVar()
        
        tk.Entry(frameEsquerdo, textvariable=self.nomeProduto_var, width=40).grid(row=0, column=1, pady=3, sticky="w")
        tk.Entry(frameEsquerdo, textvariable=self.ingredienteProduto_var, width=40).grid(row=1, column=1, pady=3, sticky="w")
        self.preparoProduto_text = tk.Text(frameEsquerdo, width=30, height=5, wrap="word", font=("Arial", 10))
        self.preparoProduto_text.grid(row=2, column=1, pady=3, sticky="w")
        tk.Entry(frameEsquerdo, textvariable=self.precoProduto_var, width=20).grid(row=3, column=1, pady=3, sticky="w")

        tk.Button(frameEsquerdo, text="Upload Imagem", command=self.selecionar_imagem).grid(row=4, column=1,sticky="w")

        self.LabelUploadImagem = tk.Label(frameEsquerdo, textvariable=self.ImageName,bg="white", anchor="w", wraplength=240, justify="left")
        self.LabelUploadImagem.grid(row=5, column=1, pady=(0, 30), sticky="w")
        
        frame_botoes = tk.Frame(frameEsquerdo, bg="white")
        frame_botoes.grid(row=5, column=0, columnspan=2, pady=(30, 0))

        tk.Button(frame_botoes, text="Deletar", bg="#f6f9fb", command=self.deletarProduto).pack(side="left", padx=(180,5))
        tk.Button(frame_botoes, text="Atualizar", bg="#f6f9fb", command=self.atualizarProduto).pack(side="left", padx=(0,5))
        tk.Button(frame_botoes, text="Cadastrar", bg="#f6f9fb", command=self.cadastrarProduto).pack(side="left", padx=(0,5))

        frameDireito = tk.LabelFrame(frame_corpo, text="Cupom Loja", bg="white", padx=10, pady=10)
        frameDireito.grid(row=0, column=1, padx=(0,10), pady=10)

        tk.Label(frameDireito, text="Email:", bg="white").grid(row=0, column=0, sticky="w")
        tk.Label(frameDireito, text="Cupom:", bg="white").grid(row=1, column=0, sticky="w")

        self.email_var = tk.StringVar()
        self.cupom_var = tk.StringVar()

        tk.Entry(frameDireito, textvariable=self.email_var).grid(row=0, column=1, sticky="w", padx=(0, 30))
        tk.Entry(frameDireito, textvariable=self.cupom_var).grid(row=1, column=1, sticky="w")

        tk.Label(frameDireito, text="*Coloque as informações para confirmar o uso do cupom na loja",
                 bg="white", wraplength=200).place(x=-10, y=45)

        tk.Button(frameDireito, text="Utilizar Cupom", bg="#f6f9fb", command=self.removerCupom).grid(
            row=4, column=0, columnspan=2, pady=(160, 0))

        self.adicionar_botao_rodape("Voltar", comando=lambda: self.controller.gerenciador_telas(1), lado="left")

    def get_entradas(self):
        nome = self.nomeProduto_var.get()
        ingrediente = self.ingredienteProduto_var.get()
        preparo = self.preparoProduto_text.get("1.0", "end").strip()
        preco = self.precoProduto_var.get()
        imagem = self.caminho_imagem.get()
        return (nome, preco, ingrediente, preparo, imagem)

    def selecionar_imagem(self):
        
        caminho = filedialog.askopenfilename(
            title="Selecionar imagem",
            filetypes=[("Imagens", "*.png *.jpg *.jpeg *.gif")]
        )
        if caminho:
            self.caminho_imagem.set(f"{caminho}")
            self.ImageName.set(f"{self.controller.getImageName(caminho)}")

    def removerCupom(self):
        email = self.email_var.get()
        cupom = self.cupom_var.get()
        retorno = self.controller.usarCupom(email,cupom)

        if retorno:
            messagebox.showerror("Erro", retorno) 
        else:
            messagebox.showinfo("Sucesso", "Cupom utilizado com êxito")
            self.limpar_campos()
    
    def deletarProduto(self):
        produto = self.get_entradas()
        retorno = self.controller.deletarProduto(produto)
        if retorno:
            messagebox.showerror("Erro", retorno) 
        else:
            messagebox.showinfo("Sucesso", "Produto deletado com êxito")
            self.limpar_campos()

    def atualizarProduto(self):
        produto = self.get_entradas()
        retorno = self.controller.atualizarProduto(produto)
        if retorno:
            messagebox.showerror("Erro", retorno) 
        else:
            messagebox.showinfo("Sucesso", "Produto Atualizado com êxito")
            self.limpar_campos()
    
    def cadastrarProduto(self):
        produto = self.get_entradas()
        retorno = self.controller.cadastrarProduto(produto)
        if retorno:
            messagebox.showerror("Erro", retorno) 
        else:
            messagebox.showinfo("Sucesso", "Produto Cadastrado com êxito")
            self.limpar_campos()

    def limpar_campos(self):
        self.nomeProduto_var.set("")
        self.ingredienteProduto_var.set("")
        self.preparoProduto_text.delete("1.0", "end")
        self.precoProduto_var.set("")
        self.email_var.set("")
        self.cupom_var.set("")
        self.caminho_imagem.set("")
        self.ImageName.set("Imagem.png")

            