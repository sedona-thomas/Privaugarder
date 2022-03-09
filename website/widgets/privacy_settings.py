#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Sedona Thomas"
__date__ = "03/08/2022"
__version__ = "1.0.1"
__maintainer__ = "Sedona Thomas"
__links__ = ["https://github.com/sedona-thomas/Navagetur"]
__email__ = "sedona.thomas@columbia.edu"

from privacy_settings.AccountData import *
from privacy_settings.AccountSecurity import *


def test():
    data = AccountData("../data/test.json")
    data.askForAccounts()
    security = AccountSecurity(data)
    security.makeHtml()


if __name__ == "__main__":
    test()
