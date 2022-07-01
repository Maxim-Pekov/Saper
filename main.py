import tkinter as tk
from random import shuffle
from tkinter.messagebox import showinfo

colors = {
    0: 'black',
    1: '#010575',
    2: '#0d6610',
    3: '#f70202',
    4: '#f70202',
    5: '#f70202',
    7: '#f70202',
    8: '#f70202',
}


class MyButton(tk.Button):
    def __init__(self, master, x, y, btn_number, *args, **kwargs):
        super(MyButton, self).__init__(master, *args, **kwargs)
        self.x = x
        self.y = y
        self.is_mine = False
        self.btn_number = btn_number
        self.count_mines = 0
        self.is_open = False

    def __repr__(self):
        return f'btn {self.x} {self.y} {self.btn_number} {self.is_mine}'


class MinesKeeper:
    win = tk.Tk()
    ROW = 10
    COLUMN = 10
    MINES = 15
    buttons = []
    first_click_t = True
    GAME_OVER = False

    def __init__(self):
        self.win.title('Сапёр')
        self.count = 1

        menubar = tk.Menu(self.win)
        self.win.config(menu=menubar)

        settings_menu = tk.Menu(menubar, tearoff=0)
        settings_menu.add_command(label='Играть', command=self.reload)
        settings_menu.add_command(label='Настройки')
        settings_menu.add_command(label='Выход', command=self.win.destroy)
        menubar.add_cascade(label='MENU', menu=settings_menu)

        for i in range(1, MinesKeeper.ROW + 1):
            tk.Grid.rowconfigure(self.win, i, weight=1)

        for i in range(1, MinesKeeper.COLUMN + 1):
            tk.Grid.columnconfigure(self.win, i, weight=1)

        for i in range(MinesKeeper.ROW):
            temp = []
            for j in range(MinesKeeper.COLUMN):
                btn = MyButton(MinesKeeper.win, i, j, self.count, font=('Arial', 15, 'bold'), width=3)
                btn.grid(row=i, column=j, stick='nwes')
                temp.append(btn)
                self.count += 1
            self.buttons.append(temp)

    def reload(self):
        [child.destroy() for child in self.win.winfo_children()]
        self.buttons = []
        self.__init__()
        self.click_button()
        self.first_click_t = True
        self.GAME_OVER = False

    def click_button(self):
        for i in range(MinesKeeper.ROW):
            for j in range(MinesKeeper.COLUMN):
                btn = self.buttons[i][j]
                btn.config(command=lambda button=btn: self.click(button))

                def rkm(event):
                    btn1 = event.widget
                    if btn1['state'] == 'normal':
                        btn1['state'] = 'disabled'
                        btn1['text'] = '🚩'
                        btn1['disabledforeground'] = 'red'
                    elif btn1['text'] == '🚩':
                        btn1['text'] = ''
                        btn1['state'] = 'normal'

                btn.bind('<Button-3>', rkm)

    def click(self, button: MyButton):
        if self.GAME_OVER:
            return None

        # print(button)
        if self.first_click_t:
            self.first_click_t = False
            self.insert_mines(button.btn_number)
            self.print_btn()

        if button.is_mine:
            button.config(text='*', state=tk.DISABLED, background='#820000', disabledforeground='black')
            button.is_open = True
            showinfo('Вы проиграли', 'Вы проиграли')
            self.GAME_OVER = True
            for i in range(MinesKeeper.ROW):
                for j in range(MinesKeeper.COLUMN):
                    btn = self.buttons[i][j]
                    if btn.is_mine: btn['text'] = '*'
                    # if not btn.is_mine: btn['text'] = btn.count_mines

        else:
            self.width_search(button)
        button.config(relief=tk.SUNKEN)

    def width_search(self, button: MyButton):
        queue = [button]
        while queue:
            cur_btn = queue.pop()
            cur_btn.count_mines = self.show_count_mines(cur_btn)
            if cur_btn.count_mines:
                color = colors.get(cur_btn.count_mines, 'black')
                cur_btn.config(text=cur_btn.count_mines, fg=color, disabledforeground=color)
            else:
                cur_btn.config(text='')
            cur_btn.is_open = True
            cur_btn.config(state=tk.DISABLED)
            cur_btn.config(relief=tk.SUNKEN)

            if cur_btn.count_mines == 0:
                x, y = cur_btn.x, cur_btn.y
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        # if not abs(dx - dy) == 1:
                        #     continue
                        new_i = x + dx
                        new_j = y + dy
                        if 0 <= new_i < self.ROW and 0 <= new_j < self.COLUMN:
                            next_btn = self.buttons[new_i][new_j]
                            if not next_btn.is_open and next_btn not in queue:
                                queue.append(next_btn)

    def print_btn(self):
        for i in range(self.ROW):
            for j in range(self.COLUMN):
                btn = self.buttons[i][j]
                if btn.is_mine:
                    print('*', end=' ')
                else:
                    btn.count_mines = self.show_count_mines(btn)
                    print(btn.count_mines, end=' ')
            print()

    def start(self):
        # self.first_click()
        # self.insert_mines()
        # self.print_btn()
        self.click_button()
        MinesKeeper.win.mainloop()

    def index_mines(self, number: int):
        index = list(range(1, self.ROW * self.COLUMN + 1))
        index.remove(number)
        shuffle(index)
        index = index[:self.MINES]
        print(index)
        return index

    def insert_mines(self, number: int):
        index = self.index_mines(number)
        for row_buttons in self.buttons:
            for buttons in row_buttons:
                if buttons.btn_number in index:
                    buttons.is_mine = True

    def show_count_mines(self, btn: MyButton):
        count_mines = 0
        z = [-1, 0, 1]
        for dx in z:
            for dy in z:
                neighbours_i = btn.x + dx
                neighbours_j = btn.y + dy
                if 0 <= neighbours_i < self.ROW and 0 <= neighbours_j < self.COLUMN:
                    neighbours = self.buttons[neighbours_i][neighbours_j]
                    if neighbours.is_mine:
                        count_mines += 1
        return count_mines


game = MinesKeeper()
game.start()
