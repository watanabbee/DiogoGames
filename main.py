import tkinter as tk
from controller import Controller
from model import Model


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Padaria VC++")
    root.geometry("700x600")
    root.configure(bg="white")
    root.resizable(False, False)
    model = Model()
    controller = Controller(root, model)
    root.mainloop()


