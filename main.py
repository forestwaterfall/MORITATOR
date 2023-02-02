#! env python
# -*- coding: utf-8 -*-

import os
import sys
import wx
from moritator_main_class import moritator_main_class

if __name__ == '__main__':
    app = wx.App(False)
    frame = moritator_main_class(None)
    frame.Show(True)
    app.MainLoop()
