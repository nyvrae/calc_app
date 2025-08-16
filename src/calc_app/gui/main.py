import tkinter as tk
import pygame

from ..core.parser import Parser
from ..core.evaluator import Evaluator


class Calc:
    def __init__(self, master):
        self.master = master
        master.title("Calculator")
        master.geometry("400x600")
        master.resizable(False, False)

        self.expression = ""
        self.sound_enabled = False
        self.parser = Parser()
        self.evaluator = Evaluator()

        pygame.mixer.init()
        try:
            self.shot_sound = pygame.mixer.Sound("tank_shot.wav")
        except Exception:
            self.shot_sound = None

        self.display = tk.Entry(master, font=('Arial', 18), justify='right')
        self.display.pack(padx=10, pady=10, fill="x")
        self.display.bind("<Return>", self.on_enter_pressed)

        self.backspace_frame = tk.Frame(master)
        self.backspace_frame.pack(fill="x", padx=10, pady=0)

        self.backspace_btn = tk.Button(
            self.backspace_frame,
            text='← Backspace',
            font=('Arial', 14),
            bg='lightblue',
            command=self.backspace
        )
        self.backspace_btn.pack(fill="x")

        self.buttons_frame = tk.Frame(master)
        self.buttons_frame.pack(expand=True, fill="both", padx=10, pady=0)

        self.create_buttons()
        self.create_sound_button()
    
    def on_enter_pressed(self, event):
        self.expression = self.display.get()
        self.calculate()


    def create_buttons(self):
        buttons = [
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            '0', '.', '=', '+',
            'C', '(', ')', '^',
            'sin', 'cos', 'tan', 'exp',
            'log', 'sqrt', 'pi', 'e'
        ]

        row = 0
        col = 0
        for button_text in buttons:
            action = lambda text=button_text: self.on_button_click(text)

            color = 'lightgrey'
            if button_text in '+-*/^':
                color = 'orange'
            elif button_text == 'C':
                color = 'salmon'
            elif button_text == '=':
                color = 'green'
            elif button_text in ['sin', 'cos', 'tan', 'exp', 'log', 'sqrt', 'pi', 'e', '(', ')']:
                color = 'skyblue'

            btn = tk.Button(
                self.buttons_frame,
                text=button_text,
                font=('Arial', 14),
                bg=color,
                command=action
            )
            btn.grid(row=row, column=col, sticky="nsew", padx=2, pady=2)

            col += 1
            if col > 3:
                col = 0
                row += 1

        for i in range(4):
            self.buttons_frame.columnconfigure(i, weight=1)
        for i in range(row + 1):
            self.buttons_frame.rowconfigure(i, weight=1)

    def create_sound_button(self):
        self.sound_btn = tk.Button(
            self.master,
            text='🔊 Sound',
            font=('Arial', 14),
            bg='yellow',
            command=self.toggle_sound
        )
        self.sound_btn.pack(pady=5, fill='x')

    def toggle_sound(self):
        self.sound_enabled = not self.sound_enabled
        self.display.delete(0, tk.END)
        self.display.insert(tk.END, "Sound ON" if self.sound_enabled else "Sound OFF")

    def backspace(self):
        self.expression = self.display.get()[:-1]
        self.display.delete(0, tk.END)
        self.display.insert(tk.END, self.expression)

    def on_button_click(self, char: str):
        self.expression = self.display.get()

        if char == 'C':
            self.expression = ""
            self.display.delete(0, tk.END)
        elif char == '=':
            self.calculate()
        else:
            self.expression += char
            self.display.delete(0, tk.END)
            self.display.insert(tk.END, self.expression)

        if self.sound_enabled:
            self.play_tank_shot()

    def calculate(self):
        try:
            expression_clean = self.expression.replace(" ", "")
            tokens = self.parser.parse(expression_clean)
            result = self.evaluator.evaluate(tokens)
            self.display.delete(0, tk.END)
            self.display.insert(tk.END, str(result))
            self.expression = str(result)
        except Exception as e:
            self.display.delete(0, tk.END)
            self.display.insert(tk.END, f"Error: {e}")
            self.expression = ""

    def play_tank_shot(self):
        if self.shot_sound:
            self.shot_sound.play()


if __name__ == "__main__":
    root = tk.Tk()
    app = Calc(root)
    root.mainloop()
