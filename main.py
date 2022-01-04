from tkinter import *
import tkinter.ttk as ttk
import tkinter as tk
import sqlite3
import win32
import win32api
from ttkthemes import themed_tk
from tkinter import LabelFrame

root = themed_tk.ThemedTk(theme='adapta')
root.iconbitmap('searchhss.ico') 
root.title('K.Tariff App')
#root.configure(bg='grey')
#root.geometry('700x620')
root.resizable(False, False)

app_width = 870
app_height = 620

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x = (screen_width / 2) - (app_width / 2)
y = (screen_height / 3 ) - (app_height / 3)

root.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')

style = ttk.Style()
style.theme_use()
style.configure('style.Treeview', font=('Arial', 16), anchor=E)
style.configure('style.Treeview.Heading', font=('Arial', 16),background='blue',padding=5)
style.configure("Treeview", rowheight=30)
style.configure("S.Labelframe", font=('Arial', 15))

count = 0
size=16
def contract():
    global size, count

    if count <= 10  and count > 0:
        size -= 2

        e.config(font=('Times New Roman', size))

        count -= 1

        root.after(10, contract)

def expand():
    global size, count
    if count < 10:
        size += 2

        e.config(font=('Times New Roman', size))

        count += 1
        
        root.after(10, expand)
    elif count == 10:
        contract()

def search(e):
    
    
    q2 = q.get()
    query = " SELECT content, hscode FROM Tariff WHERE content LIKE '%"+q2+"%' OR hscode LIKE '"+q2+"%' "
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.commit()
    update(rows)
    
def get_row(e):
    
    row = trv.identify_row(e.y)
    item = trv.item(trv.focus())
    
    
    q.set(item['values'][1])
    
def update(rows):
    trv.delete(*trv.get_children())
    for i in rows:
        trv.insert('', 'end', values=i)

def copy(e=None):
    root.clipboard_clear()
	# Copy to clipboard
    root.clipboard_append(q.get())

root.bind('<Enter>', copy)

q = StringVar()

lblfrm1 = ttk.LabelFrame(root, text='                                               ژبو لێگه‌ریانێ جورێ كه‌رسته‌ی یان كودێ كه‌رسته‌ی بنڤێسه‌')
lblfrm1.place(relx=0.05, rely=0.04, width=780)

lblfrm2 = ttk.Labelframe(root, text='پێناسا گومركی')
lblfrm2.place(relx=0.05, rely=0.15, width=800, height=500)

e = ttk.Entry(lblfrm1, font=('Times New Roman', 15), textvariable=q, justify='right', width=850)

e.pack(pady=5,padx=5)

e.bind('<KeyRelease>', search, win32api.LoadKeyboardLayout('00000401',1))

e.focus()

scrollbar = ttk.Scrollbar(lblfrm2)
scrollbar.pack(side='right', fill=Y)

scrollbar1 = ttk.Scrollbar(lblfrm2, orient='horizontal')
scrollbar1.pack(side='bottom', fill=X)

trv = ttk.Treeview(lblfrm2, columns=(1,2), show='headings', height=27, style='style.Treeview', yscrollcommand=scrollbar.set, xscrollcommand=scrollbar.set)
scrollbar.config(command=trv.yview)
scrollbar1.config(command=trv.xview)
trv.heading(1, text='Description', anchor=E)
trv.heading(2, text='H.S Code', anchor=CENTER)
#trv.heading(3, text='Duties', anchor=E)
#trv.heading(4, text='Unit', anchor=CENTER)
trv.pack(pady=5, padx=5)

trv.bind('<<TreeviewSelect>>', get_row)



trv.column(1, anchor=E, width=650, stretch=False)
trv.column(2, anchor=CENTER, width=110, stretch=False)
#trv.column(3, anchor=CENTER, width=110, stretch=False)
#trv.column(4, anchor=CENTER, width=110, stretch=False)

#child_id = trv.get_children()[-1]

#trv.focus_set()
#trv.selection_set(child_id)
#trv.selection_set(100)

trv.selection_set()

conn = sqlite3.connect('tariff.db')
cursor = conn.cursor()
query = 'SELECT content, hscode FROM Tariff'
cursor.execute(query)
rows = cursor.fetchall()
update(rows)

ttk.Label(root, text='Developed By Hiwa Hossien', font=('Arial', 12)).place(relx=0, rely=0.96)




root.deiconify()
root.update()
root.mainloop()
