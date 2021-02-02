from tkinter import *
from tkinter import ttk
from banco import *


def cadastrar():
    # Início Salvar
    def salvar():
        sql = f'INSERT INTO clientes (nome, whats, data_venda, plano, aceita) ' \
              f'VALUES ("{et_nome.get()}", "{et_whats.get()}", ' \
              f'"{et_data_venda.get()}", "{et_plano.get()}", "{v_aceita.get()}");'
        dml(sql)
        top_cadastro.destroy()
        buscar()
    # Fim Salvar

    # Início da tela Cadastro
    top_cadastro = Toplevel()
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

    # Colocando as Entry na tela
    et_nome.grid(row=0, column=1)
    et_whats.grid(row=1, column=1)
    et_data_venda.grid(row=2, column=1)
    et_plano.grid(row=3, column=1)
    rb_aceita_sim.place(x=110, y=95)
    rb_aceita_nao.place(x=170, y=95)
    btn_salvar = Button(top_cadastro, text='Salvar', command=salvar)
    btn_salvar.place(x=120, y=120)


def buscar():
    for i in tv_clientes.get_children():
        tv_clientes.delete(i)
    query = 'SELECT * FROM clientes ORDER BY nome'
    res = dql(query)
    for l in res:
        tv_clientes.insert('', 'end',
                           values=(l[0], l[1], l[2], l[3], l[4], l[5]))


app = Tk()
app.title('Controle Clientes Vivo')
app.geometry('600x500')

nb = ttk.Notebook(app)
nb.grid(row=0, column=0)

frm_principal = Frame(nb)

btn_novo = Button(frm_principal,
                  text='Novo',
                  command=cadastrar)
btn_novo.grid(row=0, column=0, sticky='w')

# Ínicio planilha clientes
tv_clientes = ttk.Treeview(frm_principal,
                           columns=('id', 'nome', 'whats', 'data_venda', 'plano', 'aceita'),
                           show='headings')


# Definindo a largura das colunas
tv_clientes.column('id', minwidth=10, width=20)
tv_clientes.column('nome', minwidth=10, width=150)
tv_clientes.column('whats', minwidth=10, width=40)
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

tv_clientes.grid(row=1, column=0)


nb.add(frm_principal, text='Clientes')

app.mainloop()
