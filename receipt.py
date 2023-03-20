#! /usr/bin/python3

import tkinter as tk
from tkinter import ttk,Menu,messagebox
from tkinter.filedialog import asksaveasfile,askopenfilename
import pyautogui
import datetime

root = tk.Tk()
root.geometry("680x510")
root.title("Sales Receipt")
root.resizable(False,False)

time_entry = tk.Entry(root, state="disabled", justify="center")
time_entry.grid(row=0, column=0, columnspan=4, sticky="nsew")

def get_time():
    time_entry.configure(state="normal")
    time_entry.delete(0, tk.END)
    time_entry.insert(0,datetime.datetime.now().strftime('%a %Y/%m/%d %H:%M:%S'))
    time_entry.configure(state="disabled")
get_time()

columns = ("Item Name", "Amount", "Price", "Discount", "Total Price")
table = ttk.Treeview(root, columns=columns, show="headings", height=10)
vsb = ttk.Scrollbar(orient="vertical",command=table.yview)
table.column("Item Name", width=224, anchor="center")
table.column("Amount", width=84, anchor="center")
table.column("Price", width=124, anchor="center")
table.column("Discount", width=83, anchor="center")
table.column("Total Price", width=143, anchor="center")
table.heading("Item Name", text="Item Name")
table.heading("Amount", text="Amount")
table.heading("Price", text="Price")
table.heading("Discount", text="Discount")
table.heading("Total Price", text="Total Price")
table.grid(row=1, column=0, columnspan=4)
vsb.grid(row=1, column=6, sticky="nsew")
table.configure(yscrollcommand=vsb.set)

def get_total():
    total = 0
    for child in table.get_children():
        total += float(table.item(child)["values"][4])
    return total
total_label = tk.Label(root, text="Total: 0")
def update_total():
    total_label.config(text=f"Total: {get_total():.2f}")
total_label.grid(row=2, column=3)

def exist_check(item_name,amount,price,discount,total):
    done=0
    for child in table.get_children():
        if item_name == str(table.item(child)["values"][0]):
            if float(price_entry.get()) == float(table.item(child)["values"][2]) and discount == int(table.item(child)["values"][3]):
                amount = amount+float(table.item(child)["values"][1])
                total = (amount*price)-(amount*price*discount/100)
                table.item(child, values=(item_name, amount, price, discount, total))
                done=1
                break
            else:
                done=0
        else:
            done=0
    if done==0:
        table.insert("", tk.END, values=(item_name, amount, price, discount, total))


def add_item():
    item_name = item_entry.get()
    amount = float(amount_entry.get())
    price = float(price_entry.get())
    discount = discount_entry.get()
    press=3
    if discount=='':
        discount=0
        press=2
    elif int(discount)<=100:
        discount=int(discount)
    else:
        discount=0
    total = (amount*price)-(amount*price*discount/100)
    exist_check(item_name,amount,price,discount,total)
    item_entry.delete(0, tk.END)
    amount_entry.delete(0, tk.END)
    price_entry.delete(0, tk.END)
    discount_entry.delete(0, tk.END)
    update_total()
    pyautogui.keyDown("shift")
    pyautogui.press("tab", presses=press)
    pyautogui.keyUp("shift")
root.bind('<Return>', lambda e: add_item())

def clear_all():
    box_stat = tk.messagebox.askquestion(title="Warning", message='Are you sure you want to clear all?')
    if box_stat == 'yes':
        item_entry.delete(0, tk.END)
        amount_entry.delete(0, tk.END)
        price_entry.delete(0, tk.END)
        discount_entry.delete(0, tk.END)
        for item in table.get_children():
            table.delete(item)
    
def exit_app():
    box_stat = tk.messagebox.askquestion(title="Warning", message='Are you sure you want to exit the application?')
    if box_stat == 'yes':
        root.destroy()
        
def delete_item():
   selected_item = table.selection()[0]
   table.delete(selected_item)
   update_total()


#set the entries, add & delete & quit button
table2 = ttk.Treeview(root, columns=("Item Name", "Amount", "Price", "Discount"), show="headings", height=0)
table2.column("Item Name", width=160, anchor="center")
table2.column("Amount", width=160, anchor="center")
table2.column("Price", width=160, anchor="center")
table2.column("Discount", width=160, anchor="center")
table2.heading("Item Name", text="Item Name")
table2.heading("Amount", text="Amount")
table2.heading("Price", text="Price")
table2.heading("Discount", text="Discount")
table2.grid(row=4, column=0, columnspan=4, sticky="nsew")
tk.Label(root).grid(row=3,pady=20)

item_entry = tk.Entry(root)
item_entry.grid(row=5, column=0)
amount_entry = tk.Entry(root)
amount_entry.grid(row=5, column=1)
price_entry = tk.Entry(root)
price_entry.grid(row=5, column=2)
discount_entry = tk.Entry(root)
discount_entry.grid(row=5, column=3)
tk.Label(root).grid(row=8)
add_button = tk.Button(root, text="Add", command=add_item, background="green")
add_button.grid(row=6, column=0, columnspan=4, sticky="nsew")
quit_button = tk.Button(root, text="Quit", command=exit_app, background='red')
quit_button.grid(row=11, column=0, columnspan=6, sticky="nsew")       
delete_button = tk.Button(root, text="Delete", command=delete_item, background="black", foreground="white")
delete_button.grid(row=7, column=0, columnspan=4, sticky="nsew")

def get_save():
    file = asksaveasfile(mode='w', initialfile = f'print-{datetime.datetime.now().strftime("%Y/%m/%d-%H:%M:%S")}.txt',defaultextension=".txt",filetypes=[("All Files","*.*"),("Text Documents","*.txt")])
    file.write(time_entry.get()+'\n')
    file.write("Item\t\tAmount\t\tPrice\t\tDiscount\t\tTotal\n")
    for child in table.get_children():
        for i in table.item(child)["values"]:
            file.write(str(i)+'\t\t')
        file.write('\n')
    file.write(str(f'{get_total():.2f}'))
    file.close()

def get_open():
    file = open(askopenfilename(initialfile = 'print.txt', defaultextension=".txt",filetypes=[("All Files","*.*"),("Text Documents","*.txt")]), mode='r')
    item_entry.delete(0, tk.END)
    amount_entry.delete(0, tk.END)
    price_entry.delete(0, tk.END)
    discount_entry.delete(0, tk.END)
    for item in table.get_children():
        table.delete(item)
    time_entry.configure(state="normal")
    time_entry.delete(0, tk.END)
    time_entry.insert(0,file.readline().replace('\n',''))
    time_entry.configure(state="disabled")
    for i in file.readlines():
        if i!="Item\t\tAmount\t\tPrice\t\tDiscount\t\tTotal\n":
            new_item_list=[]
            item_list = i.split("\t\t")
            for x in item_list:
                new_item_list.append(x.replace('\n',''))
            if len(new_item_list)>1:
                table.insert("", tk.END, values=(new_item_list))
    file.close()
    update_total()

def create_new():
    box_stat = tk.messagebox.askquestion(title="Warning", message='Do you want to save this receipt?')
    if box_stat == 'yes':
        get_save()
        item_entry.delete(0, tk.END)
        amount_entry.delete(0, tk.END)
        price_entry.delete(0, tk.END)
        discount_entry.delete(0, tk.END)
        for item in table.get_children():
            table.delete(item)
        get_time()
    else:
        clear_all()
        get_time()

def get_print():
    box_stat = tk.messagebox.askquestion(title="Warning", message='Do you want to print this receipt?')
    if box_stat == 'yes':
        from prettytable import PrettyTable
        print_table = PrettyTable(["Item Name", "Amount", "Price", "Discount", "Total"])
        for child in table.get_children():
            print_table.add_row(table.item(child)["values"][:5])
        print_time = datetime.datetime.now().strftime('%H%M%S')
        file=open(f'PrintTemplate{print_time}.txt', 'w')
        file.write(time_entry.get()+'\n')
        file.write(str(print_table))
        file.write(f"\nTotal: {get_total():.2f}")
        file.close()
        import subprocess
        import platform
        if platform.system() == "Windows":
            subprocess.call(["notepad.exe", "/p", f'PrintTemplate{print_time}.txt'])
        else:
            import cups
            conn = cups.Connection()
            printers = conn.getPrinters()
            printer_name = list(printers.keys())[0]
            subprocess.call(["lpr", f'PrintTemplate{print_time}.txt'])
        import os
        os.remove(f'PrintTemplate{print_time}.txt')

def about_page():
    import webbrowser
    message = "This program was created by Mobin Babaee using Python and the Tkinter library.\n\nThank you for using this program!\n\nPlease check out the GitHub repository for the latest updates and to report issues:\n\n"
    link = "https://github.com/mobinbabaee/sales-receipt"
    result = messagebox.askquestion("About", message+"Would you like to go to the GitHub repository?", icon="info")
    if result == "yes":
        webbrowser.open_new(link)
    
#set the menu bar
menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="New", command=create_new)
root.bind('<Control-n>', lambda e: create_new())
filemenu.add_command(label="Open", command=get_open)
root.bind('<Control-o>', lambda e: get_open())
filemenu.add_command(label="Save", command=get_save)
root.bind('<Control-s>', lambda e: get_save())
filemenu.add_command(label="Print", command=get_print)
root.bind('<Control-p>', lambda e: get_print())
filemenu.add_separator()
filemenu.add_command(label="Exit", command=exit_app)
root.bind("<Escape>", lambda e: exit_app())
root.bind("<Alt-x>", lambda e: exit_app())
root.bind("<Control-q>", lambda e: exit_app())
menubar.add_cascade(label="File", menu=filemenu)

editmenu = Menu(menubar, tearoff=0)
editmenu.add_command(label="Clear all", command=clear_all)
root.bind('<Control-l>', lambda e: clear_all())
editmenu.add_command(label="Update time", command=get_time)
root.bind('<Control-r>', lambda e: get_time())
editmenu.add_command(label="Delete", command=delete_item)
root.bind('<Delete>', lambda e: delete_item())
menubar.add_cascade(label="Edit", menu=editmenu)

helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="About...", command=about_page)
menubar.add_cascade(label="Help", menu=helpmenu)

root.config(menu=menubar)


# Start the Tkinter event loop
root.mainloop()
