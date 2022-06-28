import tkinter as tk

class MyButton(tk.Button):
    def __init__(self, master, x, y, btn_number, *args, **kwargs):
        super(MyButton, self).__init__(master, *args, **kwargs)
        self.x = x
        self.y = y
        self.is_mine = False
        self.btn_number = btn_number
    def __repr__(self):
        return f'btn {self.x} {self.y} {self.btn_number} {self.is_mine}'

class MinesKeeper:

    win = tk.Tk()
    ROW = 5
    COLUMN = 5

    def __init__(self):
        self.win.title('Сапёр')
        self.buttons = []
        self.count = 1
        self.mines
        for i in range(MinesKeeper.ROW):
            temp = []
            for j in range(MinesKeeper.COLUMN):
                btn = MyButton(MinesKeeper.win, i, j, self.count, font=('Arial', 15, 'bold'), width=3)
                btn.grid(row=i, column=j)
                temp.append(btn)
                self.count += 1
            self.buttons.append(temp)

    # def create_button(self):
    #     for i in range(MinesKeeper.ROW):
    #         for j in range(MinesKeeper.COLUMN):
    #             btn = self.buttons[i][j]
    #             btn.grid(row=i, column=j)

    def print_btn(self):
        for i in self.buttons:
            print(i)

    def start(self):
        # self.create_button()
        self.print_btn()
        MinesKeeper.win.mainloop()


game = MinesKeeper()
game.start()
