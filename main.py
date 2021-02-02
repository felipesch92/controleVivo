from tkinter import *
from tkinter import ttk, messagebox
from banco import *


def cadastrar(editar=False):
    # Início Salvar
    def salvar():
        if editar:
            sql = f'UPDATE clientes SET ' \
                  f'nome = "{et_nome.get()}",' \
                  f'whats = "{et_whats.get()}",' \
                  f'data_venda = "{et_data_venda.get()}",' \
                  f'plano = "{et_plano.get()}",' \
                  f'aceita = "{v_aceita.get()}"' \
                  f'WHERE id = {cliente[0]}'
        else:
            sql = f'INSERT INTO clientes (nome, whats, data_venda, plano, aceita) ' \
                  f'VALUES ("{et_nome.get()}", "{et_whats.get()}", ' \
                  f'"{et_data_venda.get()}", "{et_plano.get()}", "{v_aceita.get()}");'
        dml(sql)
        top_cadastro.destroy()
        buscar()
    # Fim Salvar

    # Início da tela Cadastro
    top_cadastro = Toplevel()
    if editar:
        top_cadastro.title('Editar Cliente')
    else:
        top_cadastro.title('Novo Cliente')
    top_cadastro.geometry('300x200')

    v_aceita = BooleanVar()

    Label(top_cadastro, text='Nome: ').grid(row=0, column=0, sticky='e')
    Label(top_cadastro, text='WhatsApp: ').grid(row=1, column=0, sticky='e')
    Label(top_cadastro, text='Data da Venda: ').grid(row=2, column=0, sticky='e')
    Label(top_cadastro, text='Plano(s): ').grid(row=3, column=0, sticky='e')
    Label(top_cadastro, text='Aceita?: ').grid(row=4, column=0, sticky='e')

    # Criando as Entry
    et_nome = Entry(top_cadastro)
    et_whats = Entry(top_cadastro)
    et_data_venda = Entry(top_cadastro)
    et_plano = Entry(top_cadastro)
    rb_aceita_sim = Radiobutton(top_cadastro,
                                text='Sim',
                                variable=v_aceita,
                                value=True)
    rb_aceita_nao = Radiobutton(top_cadastro,
                                text='Não',
                                variable=v_aceita,
                                value=False)
    rb_aceita_sim.select()

    if editar:
        try:
            item_selecionado = tv_clientes.selection()[0]
            cliente = tv_clientes.item(item_selecionado, 'values')
            et_nome.insert(0, cliente[1])
            et_whats.insert(0, cliente[2])
            et_data_venda.insert(0, cliente[3])
            et_plano.insert(0, cliente[4])
            if cliente[5] == 'Sim':
                rb_aceita_sim.select()
            else:
                rb_aceita_nao.select()
        except:
            messagebox.showinfo('Editar', 'Selecione um registro para editar.')

    # Colocando as Entry na tela
    et_nome.grid(row=0, column=1)
    et_whats.grid(row=1, column=1)
    et_data_venda.grid(row=2, column=1)
    et_plano.grid(row=3, column=1)
    rb_aceita_sim.place(x=110, y=95)
    rb_aceita_nao.place(x=170, y=95)
    btn_salvar = Button(top_cadastro, text='Salvar', command=salvar)
    btn_salvar.place(x=120, y=120)


def buscar(f=''):
    for i in tv_clientes.get_children():
        tv_clientes.delete(i)
    if f:
        query = f'SELECT * FROM clientes WHERE nome LIKE "%{f}%" ORDER BY nome'
        et_pesquisa.delete(0, END)
    else:
        query = 'SELECT * FROM clientes ORDER BY nome'
    res = dql(query)
    for l in res:
        if l[5] == 'True':
            ac = 'Sim'
        else:
            ac = 'Não'
        tv_clientes.insert('', 'end',
                           values=(l[0], l[1], l[2], l[3], l[4], ac))


def deletar():
    try:
        item_selecionado = tv_clientes.selection()[0]
        cliente = tv_clientes.item(item_selecionado, 'values')
        res = messagebox.askyesno('Deletar registro', f'Deseja deletar o cliente {cliente[1]}?')
        if res:
            query = f'DELETE FROM clientes WHERE id = {cliente[0]}'
            dml(query)
            buscar()
    except:
        messagebox.showinfo('Deletar', 'Selecione um registro para deletar.')


app = Tk()
app.title('Controle Clientes Vivo')
app.geometry('800x500')

# Botões do topo Novo Editar e Deletar
btn_novo = Button(app,
                  text='Novo',
                  command=cadastrar)
btn_novo.place(x=5, y=5)

btn_editar = Button(app,
                    text='Editar',
                    command=lambda: cadastrar(True))
btn_editar.place(x=70, y=5)

btn_deletar = Button(app,
                     text='Deletar',
                     command=deletar)
btn_deletar.place(x=140, y=5)

# Ínicio planilha clientes
tv_clientes = ttk.Treeview(app,
                           columns=('id', 'nome', 'whats', 'data_venda', 'plano', 'aceita'),
                           show='headings')


# Definindo a largura das colunas
tv_clientes.column('id', minwidth=10, width=10)
tv_clientes.column('nome', minwidth=10, width=150)
tv_clientes.column('whats', minwidth=10, width=70)
tv_clientes.column('data_venda', minwidth=10, width=40)
tv_clientes.column('plano', minwidth=10, width=100)
tv_clientes.column('aceita', minwidth=10, width=10)

# Definindo um título para cada coluna
tv_clientes.heading('id', text='ID')
tv_clientes.heading('nome', text='Nome')
tv_clientes.heading('whats', text='WhatsApp')
tv_clientes.heading('data_venda', text='Data Venda')
tv_clientes.heading('plano', text='Plano')
tv_clientes.heading('aceita', text='Aceita')

buscar()

tv_clientes.place(x=10, y=50, width=700, height=300)

et_pesquisa = Entry(app)
et_pesquisa.place(x=10, y=370, width=200)
btn_pesquisar = Button(app,
                       text='Pesquisar',
                       command=lambda: buscar(et_pesquisa.get()))
btn_pesquisar.place(x=210, y=370, height=25)

app.mainloop()
