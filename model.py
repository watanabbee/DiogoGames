import sqlite3 as sql, random,re,bcrypt,os,shutil

class Produto:
    def __init__(self,nome, preco, ingredientes, preparo, imagem=None, id_produto=None ):
        self.id_produto = id_produto
        self.nome = nome
        self.preco = self.formataPreco(preco)
        self.ingredientes = ingredientes
        self.preparo = preparo
        self.imagem = imagem
    
    def formataPreco(self,preco):
        if preco:
            preco=float(preco)
            return f'{preco:.2f}'
        else:
            return None

class ContaUser:
    def __init__(self,nome,email,idade,senha=None):

        self.id_usuario = None
        self.nome = nome
        self.email = email
        self.idade = idade
        self.senha = senha
        
class Model:

    def __init__(self):
        self.conexao = self.conectar()
        self.criar_tabelas()
        self.pasta = "imagens"
        self.score = 0
        self.contador = 0
        self.cliques = 0
        self.mistosComidos = 0
        self.produtos = self.listarProdutos()
        self.conta = None
        self.produto = None
        self.conta = ContaUser('eu','e@g.com',18)
        self.conta.id_usuario = 1
        self.adicionarContaAdm()

    def conectar(self):
        conect = sql.connect('padaria.db')
        conect.execute("PRAGMA foreign_keys = ON")
        return conect
    
    def adicionarContaAdm(self):

        senha = bcrypt.hashpw("admin123".encode('utf-8'), bcrypt.gensalt())
        cursor = self.conexao.cursor()
        cursor.execute("SELECT COUNT(*) FROM usuarios WHERE tipo = 'adm'")
        existe_adm = cursor.fetchone()[0]

        if existe_adm > 0:
            return None
        
        cursor.execute("""
            INSERT INTO usuarios (nome, email, idade, senha, tipo)
            VALUES (?, ?, ?, ?, ?)
        """, ("Admin", "adm@admin.com", 30, senha, "adm"))

        self.conexao.commit()

    def insertVitrine(self):
        produtos = self.carregar_produtos()
        for p in produtos:
            self.cadastrarProduto(p)

    def get_Produtos(self):
        return self.listarProdutos()
    
    def filtrarProdutos(self,termoBusca):
        if termoBusca:
            produtos_filtrados = [p for p in self.produtos if termoBusca in p.nome.lower()]
            return produtos_filtrados
        else:
            return None

    def incrementar_contador(self):
        self.contador += 1
    
    def criar_tabelas(self):
        cursor = self.conexao.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS usuarios (id_usuario INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT NOT NULL, senha text not null, email text unique not null, idade int not null, tipo TEXT DEFAULT ''comum'')')
        cursor.execute('CREATE TABLE IF NOT EXISTS cupons (id_cupom INTEGER PRIMARY KEY AUTOINCREMENT, valor TEXT NOT NULL,id_usuario INTEGER NOT NULL,FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario))')
        cursor.execute('CREATE TABLE IF NOT EXISTS produtos (id_produto INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT NOT NULL, preco REAL NOT NULL, ingredientes TEXT, preparo TEXT, caminho TEXT )')
        self.conexao.commit()

    def listarProdutos(self):
        cursor = self.conexao.cursor()
        cursor.execute('SELECT * FROM produtos')
        rows = cursor.fetchall()
        produtos = []

        for row in rows:
            id_produto, nome, preco, ingredientes, preparo, caminho = row
            produto = Produto(nome, preco, ingredientes, preparo, imagem=caminho, id_produto=id_produto)
            produtos.append(produto)

        return produtos

    def registrar_clique(self):
        self.cliques +=1

    def get_Cliques(self):
        return self.cliques

    def set0_Cliques(self):

        self.score +=1
        self.cliques = 0

    def get_score(self):
        score = self.score + (self.get_Cliques()*0.1)
        return score
    
    def get_resultado(self):

        self.mistosComidos = 0
        sorte = int(self.get_score())*10
        azar = random.randint(1,100)
        azar = 1
        if azar <= sorte:
            resultado = self.gerar_cupom()
            return resultado
        else:
            return None
    
    def getImagemJogo(self):
        
        x=self.cliques
        if x>=28:
            self.mistosComidos +=1
            self.set0_Cliques()
        return [f"imagens/misto{round(x/2)}.png",self.mistosComidos]

    def gerar_cupom(self):
        cupom = str(random.choice([5, 8, 10, 14, 17, 20]))
        self.atrelaCupom(cupom)
        return f"CUPOM{cupom}%"

    def atrelaCupom(self,cupom):
        cursor = self.conexao.cursor()
        cursor.execute("INSERT INTO cupons (valor, id_usuario) VALUES (?,?)",
                       (cupom, self.conta.id_usuario))
        self.conexao.commit()

    def get_userCupons(self):
        cursor = self.conexao.cursor()
        cursor.execute("SELECT valor FROM cupons WHERE id_usuario = ?", (self.conta.id_usuario,))
        cupons = [row[0] for row in cursor.fetchall()]
        return cupons

    def criarConta(self,Conta):
        self.conta = ContaUser(Conta[0],Conta[1],Conta[2],Conta[3])
        self.salvar()
    
    def validarDados(self,Conta):
        if not Conta[0]:
            return "Nome não pode ser vazio."

        if not re.match(r"[^@]+@[^@]+\.[^@]+", Conta[1]):
            return "Email inválido. Use formato nome@dominio.com"

        try:
            idade_int = int(Conta[2])
            if idade_int < 18:
                return "Usuário deve ter 18 anos ou mais."
        except :
            return "Idade deve ser um número."

        if len(Conta[3]) < 4:
            return "Senha deve ter pelo menos 4 caracteres."
        try:
            self.criarConta(Conta)
        except:
            return "Email ja cadastrado"
        return None
    
    def salvar(self):
        cursor = self.conexao.cursor()
        senha_hash = bcrypt.hashpw(self.conta.senha.encode('utf-8'), bcrypt.gensalt())
        cursor.execute("INSERT INTO usuarios (nome, email, idade, senha) VALUES (?, ?, ?, ?)",
                       (self.conta.nome, self.conta.email, int(self.conta.idade), senha_hash))
        self.conta.id_usuario = cursor.lastrowid
        self.conexao.commit()
    
    def logarConta(self,id_usuario, nome, email, idade):
        self.conta = ContaUser(nome,email,idade)
        self.conta.id_usuario = id_usuario
    
    def verifConta(self, email, senha):
        cursor = self.conexao.cursor()
        cursor.execute("""
            SELECT id_usuario, nome, email, idade, senha, tipo FROM usuarios
            WHERE email = ?
        """, (email,))
        resultado = cursor.fetchone()

        if resultado:
            id_usuario, nome, email, idade, senha_hash, tipo = resultado

            if bcrypt.checkpw(senha.encode('utf-8'), senha_hash):

                if tipo == 'adm':
                    return (1,"Bem vindo ADM")
                
                self.logarConta(id_usuario, nome, email, idade)
                return (None,"sucesso")
            else:
                return (0,"Email ou senha inválidos")
        else:
            return (0,"Email inválido")
        
    def verifEntryProduto(self,produto):

        nome, preco, ingredientes, preparo,imagem = produto
        
        if nome == '' or preco == '' or ingredientes == '' or preparo == '':
            return "Preencha todos os campos"
        
        if not type(nome)==str:
            return "Nome deve ser uma string."
        
        try:
            preco = float(preco)
        except:
            return "Preço deve ser um número."
        
        if not type(ingredientes)==str:
            return "Ingredientes deve ser uma string."
        
        if not type(preparo)==str:
            return "Modo de preparo deve ser uma string."
        
        if imagem is not None and not type(imagem)==str:
            return "Imagem deve ser uma string (ou None)."
        
        return None
    
    def produto_existe(self, nome):
        cursor = self.conexao.cursor()
        cursor.execute('SELECT 1 FROM produtos WHERE nome = ?', (nome,))
        retorno = cursor.fetchone()
        return retorno
        
    def deletarProduto(self,produto):
        self.produto = Produto(produto[0],produto[1],produto[2],produto[3])
        cursor = self.conexao.cursor()
        if self.produto_existe(self.produto.nome):
            cursor.execute('DELETE FROM produtos WHERE nome = ?', (self.produto.nome,))
            self.conexao.commit()
            return None
        else:
            return "O produto não conta no banco"
    
    def atualizarProduto(self,produto):
        retornoEntrada = self.verifEntryProduto(produto)
        if retornoEntrada:
            return retornoEntrada
        else:
            if produto[4]!="":
                retornoImagemJaexist = self.imagemJaexiste(produto[4])
                if retornoImagemJaexist:
                    return retornoImagemJaexist
                else:
                    retornoGuardarImagem = self.guardarImagem(produto[4])
                    if retornoGuardarImagem:
                        return retornoGuardarImagem
            else:
                self.caminhoFinal = ""

        self.produto = Produto(produto[0], produto[1], produto[2], produto[3], self.caminhoFinal)
        cursor = self.conexao.cursor()
        if self.produto_existe(self.produto.nome):
            try:
                cursor.execute('''
                    UPDATE produtos SET nome = ?, preco = ?, ingredientes = ?, preparo = ?, caminho=?
                    WHERE nome = ?
                ''', (self.produto.nome, self.produto.preco, self.produto.ingredientes, self.produto.preparo, self.produto.imagem, self.produto.nome))
                self.conexao.commit()
                return None
            except:
                return "verifique as entradas de dados"
        else:
            return "O produto não conta no banco"
    
    def cadastrarProduto(self,produto):
        retornoEntrada = self.verifEntryProduto(produto)
        if retornoEntrada:
            return retornoEntrada
        else:
            retornoProdutoExiste = self.produto_existe(produto[0])
            if retornoProdutoExiste:
                return "Produto ja cadastrado"
            else:
                retornoGuardarImagem = self.guardarImagem(produto[4])
                if retornoGuardarImagem:
                    return retornoGuardarImagem

        self.produto = Produto(produto[0],produto[1],produto[2],produto[3],self.caminhoFinal)
        cursor = self.conexao.cursor()
        cursor.execute("INSERT INTO produtos (nome, preco, ingredientes, preparo, caminho) VALUES (?, ?, ?, ?, ?)",
                       (self.produto.nome, self.produto.preco, self.produto.ingredientes, self.produto.preparo, self.produto.imagem))
        self.conexao.commit()
        
        return None
    

    def verificarCupom(self,email,cupom):
        cursor = self.conexao.cursor()
        cursor.execute("""
            SELECT cupons.*
            FROM cupons
            JOIN usuarios ON cupons.id_usuario = usuarios.id_usuario
            WHERE usuarios.email = ? AND cupons.valor = ?
        """, (email, cupom))
        retorno = cursor.fetchone()

        return retorno

    def usarCupom(self,email,cupom):
        retorno = self.verificarCupom(email,cupom)
        cursor = self.conexao.cursor()
        if retorno:
            id_cupom=retorno[0]
            cursor.execute("DELETE FROM cupons WHERE id_cupom = ?", (id_cupom,))
            self.conexao.commit()
            return None
        return 'Não foi possível utilizar o cupom'    
        
    def imagemJaexiste(self,caminho):
        nomeImagem=self.getImageName(caminho)
        pasta = self.pasta
        os.path.exists(os.path.join(pasta, nomeImagem))

    def guardarImagem(self,caminho):
        def gerarNome(pasta,nomeImagem):
            nome,extensao = os.path.splitext(nomeImagem)
            contador = 1
            nomeNovo = nomeImagem

            while os.path.exists(os.path.join(pasta, nomeNovo)):
                nomeNovo = f"{nome}({contador}{extensao})"
                contador+=1
            return nomeNovo
        
        try:
            pasta = self.pasta
            os.makedirs(pasta,exist_ok=True)
            nomeImagem=self.getImageName(caminho)
            nomeNovo = gerarNome(pasta,nomeImagem)
            if nomeImagem==nomeNovo:
                nomeFinal=nomeImagem
            else:
                nomeFinal=nomeNovo

            destino = os.path.join(pasta,nomeFinal)
            self.set_caminhoImagem(destino)
            shutil.copy2(caminho,destino)
            return None
        except:
            return "Erro ao salvar imagem"
        
    def set_caminhoImagem(self,caminhoFinal):
        self.caminhoFinal = caminhoFinal

    def getImageName(self,caminho):
        nomeImagem = os.path.basename(caminho)
        return nomeImagem
    
    