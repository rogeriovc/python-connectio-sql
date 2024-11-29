import mysql.connector
from tkinter import ttk, messagebox
import tkinter as tk
import ui
def conexao_banco():
    try: 
        cnx = mysql.connector.connect(
            host= 'localhost',
            user= 'root',
            password= '',
            database = 'loja_calcados'
        )
            
        return cnx
        print("deu certo a conexao")
    except:
            print("error")

        
def buscar_todas(tabela):
    try:
        conexao = conexao_banco()
        cursor = conexao.cursor()
        query = "SELECT id,nome,preco,estoque FROM  {} ".format(tabela)
        cursor.execute(query)
        registros = cursor.fetchall()

        print(registros)

        #descricao = "\n".join(registro[0] for registro in registros)

        return registros

    except:
         print("nao foi possivel selecionar todos da tabela {}".format(tabela))

    finally:
         cursor.close()

        
def buscar_produto_nome(nome): 


    try:
        conexao = conexao_banco()
        cursor = conexao.cursor()
        query = "SELECT * FROM produto WHERE nome LIKE '%{}%'".format(nome)
        cursor.execute(query)
        registros= cursor.fetchall()

        #for registro in resposta:
           #tree.insert("", tk.END, values=registro)

        resposta = []

        for row in registros:
            resposta = [{"id": row[0], "nome": row[1], "preco": row[2], "estoque":row[3]}]


        return resposta
    except:
        print("nao encontrei nenhum registro")
    
    finally:cursor.close()

def buscar_produto_id(id_produto):
    try:
        conexao  = conexao_banco()
        cursor = conexao.cursor()
        query = "SELECT * FROM produto WHERE id = {}".format(id_produto)
        cursor.execute(query)
        resultado = cursor.fetchone()

        if resultado:
            return{
                "id":resultado[0],
                "nome":resultado[1],
                "preco":resultado[2],
                "estoque":resultado[3]
            }
    except:
        messagebox.showerror("ALERTA", "nao foi posivel encontrar o registro comm essse id")

def cadastra_produto(nome, preco, estoque):
    try:
        conexao = conexao_banco()
        cursor = conexao.cursor()

        query = "INSERT INTO produto (nome, preco, estoque) values (%s, %s, %s)"

        cursor.execute(query,(nome, preco, estoque))

        conexao.commit()
        messagebox.showwarning("sucesso","produto cadastrado com sucesso")
    except:
        messagebox.showerror("erro","nao foi possivel inserir um produto")

def excluir_produto(produto_id):
    try:
        conexao = conexao_banco()
        cursor = conexao.cursor()

        query = "DELETE FROM produto WHERE id = {}".format(produto_id)

        cursor.execute(query)
        conexao.commit()

        messagebox.showinfo("AVISO","registrado deletado com sucesso")
    except:
        messagebox.showerror("ERRO", "nao foi possivel excluir o produto")

def atualizar_produto(produto_id, nome, preco, estoque, nova_janela):
    try:
        conexao =conexao_banco()
        cursor = conexao.cursor()
        query= "UPDATE produto SET nome = %s, preco = %s, estoque = %s WHERE id = %s"
        cursor.execute(query, (nome, preco, estoque, produto_id))
        conexao.commit()
        nova_janela.destroy()
        messagebox.showinfo("aviso", "atualizado com sucessso")
    except:
        messagebox.showerror("AVISO","nao foi possivel atualizar o registro")
     