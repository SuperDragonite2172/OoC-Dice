from argparse import ArgumentParser
from random import randint
import re
from typing import NamedTuple
from tkinter import *
from tkinter import ttk

parser = ArgumentParser()
parser.add_argument("dice", nargs="*")
inputs = parser.parse_args()


ROLL_PARTS = [
    ("Die", r"(\d+)?[dD]\d+"),
    ("Operation", r"[+\-*/]+"),
    ("Number", r"\d+"),
    ("End", r"$"),
    ("Mismatch", r"."),
]


class Gui(Tk):
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.title("OoC Dice Roller")

        self.frame_input = ttk.Frame(self)
        self.frame_input.grid(row=0, column=0)
        self.frame_output = ttk.Frame(self)
        self.frame_output.grid(row=2, column=0)
        
        self.label_input = ttk.Label(self.frame_input, text="Input:")
        self.label_input.grid(row=0, column=0, sticky=(E))
        self.dice_text = StringVar()
        self.dice_input = ttk.Entry(self.frame_input, textvariable=self.dice_text)
        self.dice_input.grid(row=0, column=1, sticky=(E,W))
        
        self.button_roll = ttk.Button(self, text="Roll Dice", command=self.dice_roll)
        self.button_roll.grid(row=1, column=0, sticky=(E,W))
        
        self.roll_output = Text(self.frame_output, width = 40, height = 10)
        self.roll_output_scrollbar = ttk.Scrollbar(self.frame_output, orient=VERTICAL, command=self.roll_output.yview)
        self.roll_output['yscrollcommand'] = self.roll_output_scrollbar.set
        self.roll_output.grid(row=2, column=0, columnspan=2)
        self.roll_output_scrollbar.grid(row=2, column=2, sticky=(N,S))

        self.bind("<Return>", self.dice_roll)

        self.line_number = 1

    def dice_roll(self, *args):
        if self.dice_text.get() == "":
            return
        else:
            rolls = self.dice_text.get().split()
            tokens = []
            for token in tokenize_dice(rolls):
                tokens.append(token)
            results, dice_results = parse_roll(tokens)
            print(results)
            for i in range(len(rolls)):
                self.roll_output.insert("end", f"[{self.line_number}] {rolls[i]} {dice_results[i].rstrip()} => {results[i]}\n")
                self.line_number += 1
            self.dice_text.set("")


class Token(NamedTuple):
    type: str
    value: str


def tokenize_dice(dice: list) -> None:
    token_regex = "|".join([f"(?P<{pair[0]}>{pair[1]})" for pair in ROLL_PARTS])
    for die in dice:
        for match_object in re.finditer(token_regex, die):
            kind = match_object.lastgroup
            value = match_object.group()
            if kind == "Die" and int(value.split('d')[1]) == 0:
                kind = "Number"
                value = "0"
            yield Token(kind, value)


def parse_roll(token_list) -> list:
    dice = ""
    stack = ""
    output = []
    output_dice = []
    for token in token_list:
        match token.type:
            case "Die":
                register = None
                quantity, sides = token.value.split('d')
                if quantity:
                    register = 0
                    die_list = []
                    for die in range(int(quantity)):
                        register2 = randint(1, int(sides))
                        die_list.append(register2)
                        register += register2
                    dice = dice + f"{die_list}"
                    stack = stack + str(register)
                else:
                    register = randint(1, int(sides))
                    stack = stack + str(register)
                    dice = dice + f"[{register}] "
            case "Operation":
                stack = stack + token.value
            case "Number":
                stack = stack + token.value
            case "Mismatch":
                print(f"Mismatch: {token.value}")
            case "End":
                output.append(eval(stack))
                output_dice.append(dice)
                stack = ""
                dice = ""
            case _:
                print(f"Unhandled token: {token}")
    return output, output_dice


def main() -> None:
    if len(inputs.dice) == 0:
        gui = Gui()
        gui.mainloop()
    else:
        tokens = []
        for token in tokenize_dice(inputs.dice):
            tokens.append(token)
        results, dice_results = parse_roll(tokens)
        for i in range(len(inputs.dice)):
            print(f"{i + 1}. {inputs.dice[i]} {dice_results[i].rstrip()} => {results[i]}")


if __name__ == '__main__':
    main()
