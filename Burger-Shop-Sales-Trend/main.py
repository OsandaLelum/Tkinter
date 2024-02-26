import tkinter as tk
from order import BurgerOrderingSystem

def main():
    root = tk.Tk()
    app = BurgerOrderingSystem(root)
    root.mainloop()

if __name__ == "__main__":
    main()
