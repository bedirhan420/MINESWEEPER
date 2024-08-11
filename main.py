import tkinter as tk
from tkinter import messagebox
import random

class MineSweeper:
    def __init__(self, root):
        self.root = root
        self.root.title("Mayın Tarlası")

        self.colors = {
            1: 'blue',
            2: 'green',
            3: 'red',
            4: 'purple',
            5: 'maroon',
            6: 'turquoise',
            7: 'black',
            8: 'gray'
        }

        self.board = None
        self.rows = 0
        self.columns = 0
        self.mines = 0
        self.buttons = []
        self.game_over = False
        self.flags_left = 0
        self.flagged_positions = set()

        self.info_frame = tk.Frame(self.root)
        self.info_frame.pack(side=tk.TOP, anchor=tk.NE)
        
        self.flag_label = tk.Label(self.info_frame, text="🚩: 0",fg="red")
        self.flag_label.pack()

        self.menu_bar = tk.Menu(root)
        self.root.config(menu=self.menu_bar)
        self.create_menu()

    def create_menu(self):
        difficulty_menu = tk.Menu(self.menu_bar, tearoff=0)
        difficulty_menu.add_command(label="Kolay", command=lambda: self.new_game(9, 9, 10))
        difficulty_menu.add_command(label="Orta", command=lambda: self.new_game(16, 16, 40))
        difficulty_menu.add_command(label="Zor", command=lambda: self.new_game(16, 30, 100))
        self.menu_bar.add_cascade(label="Zorluk Seviyesi", menu=difficulty_menu)

        self.new_game(9, 9, 10)

    def new_game(self, rows, columns, mines):
        self.rows = rows
        self.columns = columns
        self.mines = mines
        self.flags_left = mines
        self.flagged_positions.clear()
        self.game_over = False

        if self.board:
            self.board.destroy()

        self.buttons = []

        self.create_board()
        self.update_flag_count()

    def create_board(self):
        self.board = tk.Frame(self.root)
        self.board.pack()

        self.mine_positions = random.sample(range(self.rows * self.columns), self.mines)

        for row in range(self.rows):
            button_row = []
            for col in range(self.columns):
                button = tk.Button(self.board, width=2, padx=5, pady=5,
                                   command=lambda r=row, c=col: self.on_click(r, c))
                button.bind("<Button-3>", lambda e, r=row, c=col: self.toggle_flag(r, c))
                button.grid(row=row, column=col)
                button_row.append(button)
            self.buttons.append(button_row)

    def on_click(self, row, col):
        if self.game_over or (row, col) in self.flagged_positions:
            return

        button = self.buttons[row][col]
        if row * self.columns + col in self.mine_positions:
            button.config(text='*', relief=tk.SUNKEN, state=tk.DISABLED, disabledforeground='red')
            self.game_over = True
            messagebox.showinfo("Oyun Bitti!", "Maalesef! Mayına tıkladınız. Tekrar deneyin.")
            self.new_game(9, 9, 10)
            return

        self.open_adjacent(row, col)
        self.check_win_condition()

    def open_adjacent(self, row, col):
        stack = [(row, col)]
        visited = set(stack)

        while stack:
            r, c = stack.pop()
            button = self.buttons[r][c]
            count = self.count_adjacent_mines(r, c)
            if count > 0:
                button.config(text=str(count), relief=tk.SUNKEN, state=tk.DISABLED, disabledforeground=self.colors[count], bg='light gray')
            else:
                button.config(relief=tk.SUNKEN, state=tk.DISABLED, bg='light gray')
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < self.rows and 0 <= nc < self.columns and (nr, nc) not in visited:
                            visited.add((nr, nc))
                            if self.count_adjacent_mines(nr, nc) == 0:
                                stack.append((nr, nc))
                                self.buttons[nr][nc].config(relief=tk.SUNKEN, state=tk.DISABLED, bg='light gray')
                            else:
                                self.buttons[nr][nc].config(text=str(self.count_adjacent_mines(nr, nc)), relief=tk.SUNKEN, state=tk.DISABLED, disabledforeground=self.colors[self.count_adjacent_mines(nr, nc)], bg='light gray')

    def toggle_flag(self, row, col):
        if self.game_over:
            return
        
        button = self.buttons[row][col]
        if (row, col) in self.flagged_positions:
            button.config(text='', relief=tk.RAISED, state=tk.NORMAL)
            self.flagged_positions.remove((row, col))
            self.flags_left += 1
        else:
            if self.flags_left > 0 and button.cget("background") != "light gray":
                button.config(text='🚩', relief=tk.RAISED, state=tk.NORMAL,fg="red")
                self.flagged_positions.add((row, col))
                self.flags_left -= 1
        self.update_flag_count()

    def update_flag_count(self):
        self.flag_label.config(text=f"🚩: {self.flags_left}", fg="black")

    def check_win_condition(self):
        non_mine_buttons = set((r, c) for r in range(self.rows) for c in range(self.columns) if (r * self.columns + c) not in self.mine_positions)
        opened_buttons = set()
        for r in range(self.rows):
            for c in range(self.columns):
                button = self.buttons[r][c]
                if button.cget('state') == tk.DISABLED:
                    opened_buttons.add((r, c))

        if len(opened_buttons) == len(non_mine_buttons):
            self.game_over = True
            messagebox.showinfo("Kazandınız!", "Tebrikler! Tüm mayınları buldunuz.")

    def count_adjacent_mines(self, row, col):
        count = 0
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                nr, nc = row + dr, col + dc
                if 0 <= nr < self.rows and 0 <= nc < self.columns:
                    if nr * self.columns + nc in self.mine_positions:
                        count += 1
        return count

if __name__ == "__main__":
    root = tk.Tk()
    minesweeper = MineSweeper(root)
    root.mainloop()
