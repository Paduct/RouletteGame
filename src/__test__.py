# coding: utf-8
# Copyright 2020

"""Testing module."""

from unittest import TestCase, TestLoader, TestSuite

from bets import Bets
from purse import Purse


class Test(TestCase):

    """Testing rates and wallet."""

    def test_bets(self):
        """Bet management testing."""
        Bets.cash = 100.0
        Bets.min_bet = 1.0
        self.assertEqual(Bets().bets_display_form(),
                         ("bet:\n"
                          "\t№ 1 = 1.00 u.\n"
                          "\t№ 2 = 2.00 u.\n"
                          "\t№ 3 = 6.00 u.\n"
                          "\t№ 4 = 18.00 u.\n"
                          "\t№ 5 = 54.00 u.\n"
                          "balance:\n\t19.00 u.\n"))

    def test_purse(self):
        """Cash management testing."""
        purse: Purse = Purse()
        self.assertEqual(purse.cash, 0.0)

        purse.add(25.75)
        self.assertEqual(purse.balance, 25.75)

        purse.add(-75.25)
        self.assertEqual(purse.balance, 25.75)

        self.assertIsNone(purse.get(75.25))
        self.assertEqual(purse.balance, 25.75)

        self.assertIsNone(purse.get(-75.25))
        self.assertEqual(purse.balance, 25.75)

        self.assertEqual(purse.get(25.75), 25.75)
        self.assertEqual(purse.balance, 0.0)


def suite() -> TestSuite:
    """Return a test suite for execution."""
    tests: TestSuite = TestSuite()
    loader: TestLoader = TestLoader()
    tests.addTest(loader.loadTestsFromTestCase(Test))
    return tests
