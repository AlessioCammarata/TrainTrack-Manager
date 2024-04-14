import tkinter as tk
from tkinter import ttk
import GUI_refactored


def main():
    root = tk.Tk()
    gui = GUI_refactored.GUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()