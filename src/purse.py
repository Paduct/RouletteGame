# coding: utf-8
# Copyright 2020

"""Storage and manipulation of cash."""

from typing import Optional


class Purse():

    """Class for cash management."""

    cash: float = 0.0

    @property
    def balance(self) -> float:
        """Return current balance."""
        return self.cash

    def add(self, amount: float):
        """Top up balance."""
        if amount > 0.0:
            self.cash += amount

    def get(self, amount: float) -> Optional[float]:
        """Return certain amount."""
        if self.cash >= amount >= 0.0:
            self.cash -= amount
            return amount
        return None
