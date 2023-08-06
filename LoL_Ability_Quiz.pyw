import random
import tkinter as tk
from tkinter import messagebox

class RandomSpell:
    def __init__(self, master):
        self.master = master
        master.title("Random Abilities Game")

        # VARIABLES
        self.champ_dict = {}
        self.champ = ""
        self.ability = ""
        self.ability_name = ""
        self.timeleft = 20
        self.running = False
        self.action = None

        # LABELS
        self.header = tk.Label(master, text="Random Abilities Game", font=("Arial", 24), bg="#121212", fg="#FAFAFA")
        self.header.place(x=50, y=20, width=700, height=50)

        self.timer = tk.Label(master, text="20 s", font=("Arial", 20), borderwidth=2, relief="groove", bg="#121212", fg="#FAFAFA")
        self.timer.place(x=300, y=500, width=200, height=50)

        self.labelAbility = tk.Label(master, text="", font=("Arial", 16), borderwidth=2, relief="groove", bg="#121212", fg="#FAFAFA")
        self.labelAbility.place(x=200, y=100, width=400, height=50)

        self.labelReveal = tk.Label(master, text="", font=("Arial", 16), borderwidth=2, relief="groove", bg="#121212", fg="#FAFAFA")
        self.labelReveal.place(x=200, y=160, width=400, height=50)

        # BUTTONS
        self.next_button = tk.Button(master, text="Show next ability", command=self.next, font=("Arial", 12), bg="#222222", fg="#FAFAFA")
        self.next_button.place(x=200, y=250, height=45, width=400)

        self.reveal_button = tk.Button(master, text="Reveal champion and ability", command=self.reveal, font=("Arial", 12), bg="#222222", fg="#FAFAFA")
        self.reveal_button.place(x=200, y=300, height=45, width=400)

        self.close_button = tk.Button(master, text="Close", command=master.quit, font=("Arial", 12), bg="#222222", fg="#FAFAFA")
        self.close_button.place(x=200, y=350, height=45, width=400)

        self.load_data()

    def load_data(self):
        try:
            with open("ChampData.json", "r") as file:
                self.champ_dict = eval(file.read())
        except FileNotFoundError:
            messagebox.showerror("Error", "ChampData.json file not found!")
            self.master.quit()

    def remove_item(self):
        del self.champ_dict[self.champ][self.ability]
        if not self.champ_dict[self.champ]:
            del self.champ_dict[self.champ]

    def next(self):
        if self.action:
            self.master.after_cancel(self.action)
            self.action = None
        self.running = False

        if not self.champ_dict:
            self.labelAbility.configure(text="No abilities left.")
            self.labelReveal.configure(text="Wind's howling...")
            self.timer.configure(text="GGWP")
            return

        self.champ = random.choice(list(self.champ_dict.keys()))
        self.ability = random.choice(list(self.champ_dict[self.champ].keys()))
        self.ability_name = self.champ_dict[self.champ][self.ability]
        self.full_info = f"{self.champ} {self.ability}"
        self.remove_item()
        self.labelAbility.configure(text=self.ability_name)
        self.labelReveal.configure(text="")
        self.timeleft = 21
        self.running = True

        if not self.action:
            self.update_clock()

    def reveal(self):
        self.running = False
        if self.action:
            self.labelReveal.configure(text=self.full_info)
            self.action = None

    def update_clock(self):
        if self.timeleft > 1 and self.running:
            self.timeleft -= 1
            self.timer.configure(text=f"{self.timeleft} s")
            self.action = self.master.after(1000, self.update_clock)
        elif self.running:  # Only update text when running
            self.timer.configure(text="OUT OF TIME")

if __name__ == "__main__":
    root = tk.Tk()
    my_gui = RandomSpell(root)
    root.geometry("800x600")
    root.configure(bg='#121212')
    root.mainloop()
