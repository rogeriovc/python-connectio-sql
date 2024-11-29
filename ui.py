import tkinter as tk
import database as db
from tkinter import  ttk, messagebox
from PIL import Image, ImageTk


#titulo da minha janela
def listagem_registros():
    nova_janela = tk.Toplevel()
    nova_janela.title("listagem de produtos")
    nova_janela.geometry("600x600")

    def aplicar_filtro():

        for item in tabelas_produtos.get_children():
            tabelas_produtos.delete(item)

        registros_filtro = db.buscar_produto_nome(entry_nome.get())
        for registros_filtro_aplicado in registros_filtro:
            tabelas_produtos.insert("", "end", values=(
                registros_filtro_aplicado.get("id",""),
                registros_filtro_aplicado.get("nome",""),
                registros_filtro_aplicado.get("preco",""),
                registros_filtro_aplicado.get("estoque","")
            ))


    #titulo da miha janela
    label_titulo = tk.Label(nova_janela, text="listagem de produtos")
    label_titulo.pack(pady=10)

    tk.Label(nova_janela, text="pesquise o produto").pack(pady=10)
    entry_nome = tk.Entry(nova_janela, width=50)
    entry_nome.pack(pady=10)
    pesquisar = tk.Button(nova_janela,text="pesquisar", command=lambda:aplicar_filtro())
    pesquisar.pack(pady=10)

    colunas = ("ID", "nome", "preco", "estoque")
    tabelas_produtos = ttk.Treeview(nova_janela,columns=colunas, show="headings")
    tabelas_produtos.pack(fill="both")

    #configura o cabeçalho da coluna
    tabelas_produtos.heading("ID",text="ID")
    tabelas_produtos.heading("nome",text="nome")
    tabelas_produtos.heading("preco",text="preco")
    tabelas_produtos.heading("estoque",text="estoque")

    #especificar tamanho das colunas
    tabelas_produtos.column("ID",width=50)
    tabelas_produtos.column("nome",width=80)
    tabelas_produtos.column("preco",width=100)
    tabelas_produtos.column("estoque",width=100)

    btn_lista_produtos = tk.Button(nova_janela,text="listar produtos", command=lambda:carregar_produtos())
    btn_lista_produtos.pack(pady=10)

    #carregar os nomes dos produtos
    def carregar_produtos():
        registros = db.buscar_todas("produto")

        for item in tabelas_produtos.get_children():
            tabelas_produtos.delete(item)

        for registro in registros:
            tabelas_produtos.insert("",tk.END, values=registro)

    def excluir_registro():
        selected_item = tabelas_produtos.selection()
        if selected_item:
            item = tabelas_produtos.item(selected_item)
            produto_id = item["values"][0]

            print(produto_id)

            db.excluir_produto(produto_id)

    def editar_registro ():
        selected_item = tabelas_produtos.selection()
        if selected_item:
            item = tabelas_produtos.item(selected_item)
            produto_id = item["values"][0]
            abrir_janela_editar_registro(produto_id)



    #icon_delete_image = Image.open("assets/delete.png").resize((16,16))
    #icon = ImageTk.PhotoImage(icon_delete_image)

    btn_editar_registro = tk.Button(nova_janela, text="editar item selecionado", command=lambda: editar_registro())
    btn_editar_registro.pack(pady=10)

    btn_delete = tk.Button(nova_janela, text="deletar item selecionado", command=lambda: excluir_registro())
    #btn_delete.icon = icon_delete_image
    btn_delete.pack(pady=10)    

def abrir_janela_editar_registro (id_produto):
    lancamentos = db.buscar_produto_id(id_produto)

    nova_janela = tk.Toplevel()
    nova_janela.title("editar registro")
    nova_janela.geometry("600x600")

    tk.Label(nova_janela, text= "ID DO PRODUTO").pack(pady=10)
    entry_id = tk.Entry(nova_janela)
    entry_id.insert(0, str(id_produto))
    entry_id.config(state="disabled")
    entry_id.pack(pady=10)

    tk.Label(nova_janela,text= "nome").pack(pady=10)
    entry_nome = tk.Entry(nova_janela)
    entry_nome.insert(0, str(lancamentos.get('nome', '')))
    entry_nome.pack(pady=10)

    tk.Label(nova_janela,text = "preco").pack(pady=10)
    entry_preco = tk.Entry(nova_janela)
    entry_preco.insert(0, str(lancamentos.get('preco', '')))
    entry_preco.pack(pady=10)

    tk.Label(nova_janela,text ="estoque").pack(pady=10)
    entry_estoque = tk.Entry(nova_janela)
    entry_estoque.insert(0, str(lancamentos.get('estoque', '')))
    entry_estoque.pack(pady=10)

    btn_salvar_alteracao = tk.Button(nova_janela, text="salvar alteração", command=lambda:db.atualizar_produto(id_produto, entry_nome.get(), entry_preco.get(), entry_estoque.get(), nova_janela))
    btn_salvar_alteracao.pack(pady=10)

def abrir_janela_cadastro_produtos():
 
    #METODO QUE LIMPA INPUTS
    def limpa_campos():
        input_nome.delete(0,tk.END)
        input_preco.delete(0,tk.END)
        input_estoque.delete(0,tk.END)

    #METODO QUE SALVA PRODUTO NO BANCO E LIMPA OS INPUTS
    def salva_produto():
        db.cadastra_produto(input_nome.get(),input_preco.get(),input_estoque.get())
        limpa_campos()


    nova_janela = tk.Toplevel()
    nova_janela.title("cadastro de produto")
    nova_janela.geometry("400x600")

    #label input do nome
    label_nome = tk.Label(nova_janela,text="nome")
    label_nome.pack(pady=0)
    input_nome = tk.Entry(nova_janela)
    input_nome.pack(pady=5)

    #input do preco
    label_preco = tk.Label(nova_janela,text="preco")
    label_preco.pack(pady=0)
    input_preco = tk.Entry(nova_janela)
    input_preco.pack(pady=5)

    #label input do estoque
    label_estoque = tk.Label(nova_janela,text="estoque")
    label_estoque.pack(pady=0)
    input_estoque = tk.Entry(nova_janela)
    input_estoque.pack(pady=5)

    #botao que vai cadastrar o nome e os outros dados
    btn_cadastrar_produto = tk.Button(nova_janela,text="cadastrar", command=lambda:salva_produto())
    btn_cadastrar_produto.pack(pady=10)

def tela_principal():
    root = tk.Tk() 
    root.title("loja de calcados ")
    root.geometry("600x600")

    registros_texto = tk.Label(root, text="", justify="left", anchor="center")
    registros_texto.pack(pady=10)


    btn_abrir_janela_listagem_produtos  = tk.Button(root, text="abrir lista de produtos", command=listagem_registros)
    btn_abrir_janela_listagem_produtos.pack(pady=10)

    btn_abrir_janela_cadastra_produto = tk.Button(root, text="cadastrar produto",command=abrir_janela_cadastro_produtos)
    btn_abrir_janela_cadastra_produto.pack(pady=10)


    root.mainloop()
