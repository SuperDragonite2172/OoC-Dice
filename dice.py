from argparse import ArgumentParser
from random import randint
import re
from typing import NamedTuple
from tkinter import *
from tkinter import ttk

parser = ArgumentParser()
parser.add_argument("dice", nargs="*")
inputs = parser.parse_args()
line_number = 1

def dice_roll(*args):
    if dice_text.get() == "":
        return
    else:
        rolls = dice_text.get().split()
        tokens = []
        for token in tokenize_dice(rolls):
            tokens.append(token)
        results = parse_roll(tokens)
        for i in range(len(rolls)):
            global line_number
            roll_output.insert("end", f"[{line_number}] {rolls[i]} => {results[i]}\n")
            line_number += 1
        dice_text.set("")

root = Tk()
root.title("OoC Dice Roller")

frame_input = ttk.Frame(root)
frame_output = ttk.Frame(root)

label_input = ttk.Label(frame_input, text="Input:")
dice_text = StringVar()
dice_input = ttk.Entry(frame_input, textvariable=dice_text)

button_roll = ttk.Button(root, text="Roll Dice", command=dice_roll)

roll_output = Text(frame_output, width = 40, height = 10)
roll_output_scrollbar = ttk.Scrollbar(frame_output, orient=VERTICAL, command=roll_output.yview)
roll_output['yscrollcommand'] = roll_output_scrollbar.set

frame_input.grid(row=0, column=0)
button_roll.grid(row=1, column=0, sticky=(E,W))
frame_output.grid(row=2, column=0)

label_input.grid(row=0, column=0, sticky=(E))
dice_input.grid(row=0, column=1, sticky=(E,W))
roll_output.grid(row=2, column=0, columnspan=2)
roll_output_scrollbar.grid(row=2, column=2, sticky=(N,S))

root.bind("<Return>", dice_roll)

# TODO(Draco): Implement logging for token output later.
ROLL_PARTS = [
    ("Die", r"(\d+)?[dD]\d+"),
    ("Operation", r"[+\-*/]+"),
    ("Number", r"\d+"),
    ("End", r"$"),
    ("Mismatch", r"."),
]


class Token(NamedTuple):
    type: str
    value: str


def tokenize_dice(dice: list) -> None:
    # TODO(Draco): Look into replacing print-f formatting with string literal.
    token_regex = "|".join("(?P<%s>%s)" % pair for pair in ROLL_PARTS)
    for die in dice:
        for match_object in re.finditer(token_regex, die):
            kind = match_object.lastgroup
            value = match_object.group()
            yield Token(kind, value)


def parse_roll(token_list) -> list:
    stack = ""
    output = []
    for token in token_list:
        match token.type:
            case "Die":
                register = None
                quantity, sides = token.value.split('d')
                if quantity:
                    # print(f"Quantity: {quantity}")
                    register = 0
                    for die in range(int(quantity)):
                        register2 = randint(1, int(sides))
                        # print(f"Die Roll: {register2}")
                        register += register2
                    # print(f"Total: {register}")
                    stack = stack + str(register)
                else:
                    register = randint(1, int(sides))
                    # print(f"Rolled {register}")
                    stack = stack + str(register)
            case "Operation":
                # print(f"Operation: {token.value}")
                stack = stack + token.value
            case "Number":
                # print(f"Number: {token.value}")
                stack = stack + token.value
            case "Mismatch":
                print(f"Mismatch: {token.value}")
            case "End":
                # print(f"End")
                # print(f"Final Result: {eval(stack)}")
                output.append(eval(stack))
                stack = ""
                # print("=" * 20)
            case _:
                print(f"Unhandled token: {token}")
    return output


def main() -> None:
    if len(inputs.dice) == 0:
        root.mainloop()
    else:
        tokens = []
        for token in tokenize_dice(inputs.dice):
            tokens.append(token)
        results = parse_roll(tokens)
        for i in range(len(inputs.dice)):
            # TODO(Draco): Add dice results to output
            print(f"{i + 1}. {inputs.dice[i]} => {results[i]}")


if __name__ == '__main__':
    main()
