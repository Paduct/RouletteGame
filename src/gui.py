# coding: utf-8
# Copyright 2020

"""Implementing the graphical interface."""

from glob import glob
from os import path
from random import choices
from typing import List

from kivy.app import App
from kivy.core.window import Window
from kivy.factory import Factory
from kivy.lang import Builder
from kivy.uix.togglebutton import ToggleButton
from widgetskv import WKV_ABOUT_DIALOG, WKV_PANEL_MENU, WKV_SEPARATOR_LINE

from .bets import Bets
from .purse import Purse


class Gui(App):

    """Class of the main window and runing of the application."""

    RED: str = "[color=#ff0000]-{0}[/color]"
    GREEN: str = "[color=#00ff00]+{0}[/color]"
    RED_SECTOR: int = -1
    GREEN_SECTOR: int = 0
    BLACK_SECTOR: int = 1
    RED_SECTOR_AMOUNT: int = 18
    GREEN_SECTOR_AMOUNT: int = 1
    BLACK_SECTOR_AMOUNT: int = RED_SECTOR_AMOUNT
    INITIAL_AMOUNT: float = 10.0

    bets: Bets = Bets()
    purse: Purse = Purse()
    title: str = "Roulette game"
    version: str = "0.1.0"
    create_year: int = 2017
    license_link: str = "https://www.gnu.org/licenses/gpl-3.0"
    project_link: str = "https://github.com/Paduct/roulette_game"
    description: str = bets.DESCRIPTION
    bet_sector: int = GREEN_SECTOR

    def build(self):
        """Accumulate of resources and the start of the main window."""
        project_path: str = path.split(path.dirname(__file__))[0]
        kv_files_path: str = path.join(project_path, "uix", "*.kv")
        kv_file_names: List[str] = glob(kv_files_path)
        kv_file_names.extend(
            (WKV_PANEL_MENU, WKV_SEPARATOR_LINE, WKV_ABOUT_DIALOG)
        )

        for file_name in kv_file_names:
            Builder.load_file(file_name)

        Window.clearcolor = (0.2, 0.2, 0.2, 1)

        self.icon = path.join(project_path, "data", "zero.png")
        self.root = Factory.RootWindow()

        self.bets.yellow = "{0}_"
        self.bets.red = self.bets.yellow
        self.bets.bold = "**{0}**"

        self.reset()

    def reset(self):
        """Return to initial values."""
        self.purse.cash = self.INITIAL_AMOUNT

        self.root.ids.result_status.text = str(self.bets.ZERO)
        self.root.ids.cur_balance.text = str(self.purse.balance)
        self.root.ids.min_bet.text = f"{self.GREEN_SECTOR_AMOUNT:.1f}"

        self.bet_sector = self.GREEN_SECTOR
        for toggle in ToggleButton.get_widgets("zero"):
            toggle.state = "normal"

        self.show_bets()

    def show_bets(self):
        """Calculate and display bets."""
        self.bets.cash = self.purse.balance
        self.bets.min_bet = round(float(self.root.ids.min_bet.text), 2) \
            if self.root.ids.min_bet.text else self.bets.ZERO

        self.root.ids.bets.text = self.bets.bets_display_form() \
            .replace(":", "\n-------") \
            .replace(self.bets.U_STR, f"{self.bets.U_STR}\n")

    def play_bets(self):
        """Play bet sequence."""
        bet: float = self.bets.ZERO
        for number, bet in enumerate(self.bets.bets):
            croupier_ball: int = choices((self.RED_SECTOR,
                                          self.GREEN_SECTOR,
                                          self.BLACK_SECTOR),
                                         (self.RED_SECTOR_AMOUNT,
                                          self.GREEN_SECTOR_AMOUNT,
                                          self.BLACK_SECTOR_AMOUNT))[0]
            if croupier_ball == self.bet_sector:
                if number > self.bets.ZERO:
                    bet /= 2
                self.bets.bets.clear()
                break

        if self.bets.bets:
            self.root.ids.result_status.text = self.RED.format(
                self.bets.FRS.format(self.purse.get(sum(self.bets.bets)))
            )
        else:
            self.root.ids.result_status.text = \
                self.GREEN.format(self.bets.FRS.format(bet))
            self.purse.add(bet)

        self.root.ids.cur_balance.text = \
            self.bets.FRS.format(self.purse.balance)
        self.show_bets()

    def on_pause(self) -> bool:
        """Return the sign of switching to pause mode."""
        return True
