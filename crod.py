import sqlite3
from tkinter import *
import tkinter.ttk
from tkinter import messagebox


conn = sqlite3.connect("inventario.db")
cr = conn.cursor()


cr.execute("""
CREATE TABLE IF NOT EXISTS productos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    precio REAL NOT NULL,
    stock INTEGER NOT NULL
)
""")
conn.commit()


def rell():
    for algo in tabla.get_children():
        tabla.delete(algo)
    cr.execute("SELECT * FROM productos")
    for dato in cr.fetchall():
        tabla.insert("", "end", values=dato)


def agregar():
    nombre = entry_nombre.get()
    precio = entry_precio.get()
    stock = entry_stock.get()
    if nombre and precio.replace('.', '', 1).isdigit() and stock.isdigit():#('. =viejo', ' = nuevo', 1 = solo 1 vez)
        cr.execute("INSERT INTO productos (nombre, precio, stock) VALUES (?, ?, ?)",
                   (nombre, float(precio), int(stock)))
        conn.commit()
        rell()
        entry_nombre.delete(0, END)
        entry_precio.delete(0, END)
        entry_stock.delete(0, END)
    else:
        messagebox.showwarning("datos no validos", "no dejes ningun cuadro vacío")


def eliminar():
    ide = entry_ide.get()
    if ide.isdigit():
        cr.execute("DELETE FROM productos WHERE id = ?", (int(ide),))
        conn.commit()
        rell()
        entry_ide.delete(0, END)
    else:
        messagebox.showwarning("ID no valido", "ingesa un ID valido")


def modificar():
    idv = entry_ide.get()
    nombre = entry_nombre.get()
    precio = entry_precio.get()
    stock = entry_stock.get()
    if idv.isdigit() and nombre and precio.replace('.', '', 1).isdigit() and stock.isdigit():
        cr.execute("UPDATE productos SET nombre = ?, precio = ?, stock = ? WHERE id = ?",
                   (nombre, float(precio), int(stock), int(idv)))
        conn.commit()
        rell()
        entry_ide.delete(0, END)
        entry_nombre.delete(0, END)
        entry_precio.delete(0, END)
        entry_stock.delete(0, END)
    else:
        messagebox.showwarning("datos no validos", "no dejes ningun cuadro vacío")


app = Tk()
app.title("inventario de productos")


tabla = tkinter.ttk.Treeview(app, columns=("ID", "Nombre", "Precio", "Stock"), show="headings")# Treeview lo uso para tablas de inventario y es especifico para ttk
tabla.heading("ID", text="ID")
tabla.heading("Nombre", text="Nombre")
tabla.heading("Precio", text="Precio")
tabla.heading("Stock", text="Stock")


for col in tabla["columns"]:
    tabla.column(col, anchor="center", width=100)#centra el texto en cada columna y les da un ancho fijo de 100 pixeles
tabla.grid(row=0, column=0, columnspan=4, padx=10, pady=10)


Label(app, text="ID:").grid(row=1, column=0, sticky="e")
entry_ide = Entry(app)
entry_ide.grid(row=1, column=1, sticky="w")

Label(app, text="Nombre:").grid(row=2, column=0, sticky="e")
entry_nombre = Entry(app)
entry_nombre.grid(row=2, column=1, sticky="w")

Label(app, text="Precio:").grid(row=3, column=0, sticky="e")
entry_precio = Entry(app)
entry_precio.grid(row=3, column=1, sticky="w")

Label(app, text="Stock:").grid(row=4, column=0, sticky="e")
entry_stock = Entry(app)
entry_stock.grid(row=4, column=1, sticky="w")


Button(app, text="Agregar", command=agregar).grid(row=5, column=0, pady=10)
Button(app, text="Eliminar por ID", command=eliminar).grid(row=5, column=1, pady=10)
Button(app, text="Modificar por ID", command=modificar).grid(row=5, column=2, pady=10)


rell()

app.mainloop()


    