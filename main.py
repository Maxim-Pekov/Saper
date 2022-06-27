import tkinter as tk

win = tk.Tk()
win.title('Сапёр')

ROW = 5
COLUMN = 5

buttons = []
for i in range(ROW):
    temp=[]
    for j in range(COLUMN):
        btn = tk.Button(win, font=('Arial', 15, 'bold'), width=3)
        btn.grid(row=i, column=j)
        temp.append(btn)
    buttons.append(temp)


win.mainloop()