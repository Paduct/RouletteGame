# coding: utf-8
# Copyright 2020

"""Bet generation module."""

from argparse import ArgumentParser, Namespace
from sys import stderr, stdout
from typing import List


class Bets():

    """Bets management."""

    FRS: str = "{0:.2f}"
    ZERO: float = 0.0
    U_STR: str = "u.\n"
    MINIMUM_BET_STR: str = "minimum bet"
    CURRENT_BALANCE_STR: str = "current balance"
    DESCRIPTION: str = "Roulette with increasing rates system."

    cash: float
    min_bet: float
    bets: List[float] = []
    red: str = '{0}'
    blue: str = '{0}'
    yellow: str = '{0}'
    bold: str = '{0}'

    def check_data(self) -> bool:
        """Return the sign of correct input."""
        if not self.cash >= self.min_bet > self.ZERO:
            stderr.write(self.red.format(
                f"Should be {self.CURRENT_BALANCE_STR} "
                f">= {self.MINIMUM_BET_STR} > {self.ZERO}\n"
            ))
            return False
        return True

    def generate_bets(self):
        """Calculate bets."""
        self.bets.clear()
        if not self.check_data():
            return
        self.bets.append(self.min_bet)
        self.cash -= self.min_bet

        bet: float = self.min_bet * 2
        if self.cash < bet:
            return
        self.bets.append(bet)
        self.cash -= bet

        bet *= 3
        while self.cash >= bet:
            self.bets.append(bet)
            self.cash -= bet
            bet *= 3

    def bets_display_form(self) -> str:
        """Return the result for display."""
        self.generate_bets()

        bets_lines: str = \
            f"{self.blue.format(self.MINIMUM_BET_STR.split()[1])}:\n"

        for number, bet in enumerate(self.bets, 1):
            bets_lines = "{0}\t№ {1} = {2} {3}".format(
                bets_lines, self.bold.format(number),
                self.yellow.format(self.FRS.format(bet)), self.U_STR
            )

        bets_lines = "{0}{1}:\n\t{2} {3}".format(
            bets_lines, self.blue.format(self.CURRENT_BALANCE_STR.split()[1]),
            self.red.format(self.FRS.format(self.cash)), self.U_STR
        )

        return bets_lines


if __name__ == "__main__":
    parser: ArgumentParser = ArgumentParser(description=Bets.DESCRIPTION)
    parser.add_argument("cash", type=float, help=Bets.CURRENT_BALANCE_STR)
    parser.add_argument("min_bet", type=float, help=Bets.MINIMUM_BET_STR)
    parser.add_argument("-c", dest="colors", help="turn color design",
                        action="store_true")

    args: Namespace = parser.parse_args()
    Bets.cash = args.cash
    Bets.min_bet = args.min_bet

    if args.colors:
        Bets.red = "\x1b[31m{0}\x1b[0m"
        Bets.blue = "\x1b[34;1m{0}\x1b[0m"
        Bets.yellow = "\x1b[33m{0}\x1b[0m"
        Bets.bold = "\x1b[0;1m{0}\x1b[0m"

    stdout.write(Bets().bets_display_form())
