import os
import random
import time
from turtle import color
try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk


class RandomSpell:
    def __init__(self, master):

        self.master = master
        master.title("Random Abilities Game")

        # VARIABLES

        self.champ = ""
        self.ability = ""
        self.ability_name = ""
        self.timeleft = 21
        self.running = False
        self.action = None

        # LABELS

        self.header = tk.Label(
            master, text="Random Abilities Game", font=("Arial", 24), bg="#121212", fg="#FAFAFA")
        self.header.place(x=50, y=20, width=700, height=50)

        self.timer = tk.Label(master, text="20 s", font=(
            "Arial", 20), borderwidth=2, relief="groove", bg="#121212", fg="#FAFAFA")
        self.timer.place(x=300, y=500, width=200, height=50)

        self.labelAbility = tk.Label(master, text="", font=(
            "Arial", 16), borderwidth=2, relief="groove", bg="#121212", fg="#FAFAFA")
        self.labelAbility.place(x=200, y=100, width=400, height=50)

        self.labelReveal = tk.Label(master, text="", font=(
            "Arial", 16), borderwidth=2, relief="groove", bg="#121212", fg="#FAFAFA")
        self.labelReveal.place(x=200, y=160, width=400, height=50)

        # BUTTONS

        self.next_button = tk.Button(
            master, text="Show next ability", command=self.next, font=("Arial", 12), bg="#222222", fg="#FAFAFA")
        self.next_button.place(x=200, y=250, height=45, width=400)

        self.reveal_button = tk.Button(
            master, text="Reveal champion and ability", command=self.reveal, font=("Arial", 12), bg="#222222", fg="#FAFAFA")
        self.reveal_button.place(x=200, y=300, height=45, width=400)

        self.close_button = tk.Button(
            master, text="Close", command=master.quit, font=("Arial", 12), bg="#222222", fg="#FAFAFA")
        self.close_button.place(x=200, y=350, height=45, width=400)

    # METHODS

    def next(self):
        if self.action:
            root.after_cancel(self.action)
            self.action = None
        self.running = False
        self.champ = random.choice(list(champ_dict.keys()))
        self.ability = random.choice(list(champ_dict[self.champ].keys()))
        self.ability_name = champ_dict[self.champ][self.ability]
        self.labelAbility.configure(text=self.ability_name)
        self.labelReveal.configure(text="")
        self.timeleft = 21
        self.running = True
        if not self.action:
            self.update_clock()

    def reveal(self):
        self.labelReveal.configure(text=self.champ + " " + self.ability)
        self.running = False

    def update_clock(self):
        if self.timeleft > 1 and self.running == True:
            self.timeleft -= 1
            self.timer.configure(text=str(self.timeleft) + " s")
            self.action = self.timer.after(1000, self.update_clock)
        elif self.timeleft > 1 and self.running == False:
            if self.action:
                root.after_cancel(self.action)
                self.action = None
                self.timer.configure(text=str(self.timeleft) + " s")
        else:
            if self.action:
                root.after_cancel(self.action)
                self.action = None
                self.timer.configure(text="OUT OF TIME")


file_name = "ChampData.json"
champ_dict = open(file_name, "r")
champ_dict = champ_dict.read()
champ_dict = eval(champ_dict)

if __name__ == "__main__":
    root = tk.Tk()
    my_gui = RandomSpell(root)
    root.geometry("800x600")
    root.configure(bg='#121212')
    root.mainloop()
