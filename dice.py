from argparse import ArgumentParser
from random import randint
import re
from typing import NamedTuple

parser = ArgumentParser()
parser.add_argument("dice", nargs="+")
inputs = parser.parse_args()

DICE_SIDES = [2, 4, 6, 8, 10, 12, 20, 30, 100]

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
                # TODO(Draco): Replace usage of `eval` with something else.
                output.append(eval(stack))
                stack = ""
                # print("=" * 20)
            case _:
                print(f"Unhandled token: {token}")
    return output


def main() -> None:
    tokens = []
    for token in tokenize_dice(inputs.dice):
        tokens.append(token)
    results = parse_roll(tokens)
    for i in range(len(inputs.dice)):
        # TODO(Draco): Add dice results to output
        print(f"{i + 1}. {inputs.dice[i]} -> {results[i]}")


if __name__ == '__main__':
    main()
