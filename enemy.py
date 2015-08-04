#!/usr/bin/env python

from math import *

import pysctl
import wx
from wx.lib.scrolledpanel import ScrolledPanel


TITLE = "Network Memory Editor"

FIELDS = [
"net.core.rmem_default",
"net.core.rmem_max",
"net.core.wmem_default",
"net.core.wmem_max"
]



class wxPysctl(wx.Frame):

    def __init__(self, debug=False, actually_write=True):
        wx.Frame.__init__(self, None, wx.ID_ANY, title=TITLE)

        self.debug = debug
        self.actually_write = actually_write
        self.orig_value = {} # filled in make_all_widgets()

        self.icons = {}
        self.icons["idle"]  = wx.ArtProvider.GetBitmap(wx.ART_TICK_MARK, wx.ART_OTHER)
        self.icons["warn"]  = wx.ArtProvider.GetBitmap(wx.ART_WARNING,   wx.ART_OTHER)
        self.icons["error"] = wx.ArtProvider.GetBitmap(wx.ART_ERROR,     wx.ART_OTHER)
        self.icons["info"]  = wx.ArtProvider.GetBitmap(wx.ART_TIP,       wx.ART_OTHER)
        self.set_icon("info")

        self.panel = wx.Panel(self, wx.ID_ANY)
        mainSizer = self.make_all_widgets()
        self.panel.SetSizer(mainSizer)

        self.Show()


    def make_widget_set(self, name, value):
        ico = wx.StaticBitmap(self.panel, wx.ID_ANY, name="ico::"+name, bitmap=self.icons["idle"])
        lbl = wx.StaticText  (self.panel, wx.ID_ANY, name="lbl::"+name, label=name)
        txt = wx.TextCtrl    (self.panel, wx.ID_ANY, name="txt::"+name, value=value, style=wx.TE_PROCESS_ENTER)
        btn = wx.Button      (self.panel, wx.ID_ANY, name="btn::"+name, label="set")

        ico.Bind(wx.EVT_LEFT_DOWN,  self.onIconClick)
        lbl.Bind(wx.EVT_LEFT_DOWN,  self.onLabelClick)
        txt.Bind(wx.EVT_TEXT,       self.onTextChange)
        txt.Bind(wx.EVT_TEXT_ENTER, self.onButtonClick)
        btn.Bind(wx.EVT_BUTTON,     self.onButtonClick)

        lbl.SetToolTipString(value)
        self.set_idle(name)

        return ico, lbl, txt, btn


    def make_all_widgets(self):
        sizer = wx.FlexGridSizer(len(FIELDS), 4)
        sizer.AddGrowableCol(2)

        for name in FIELDS:
            value = pysctl.read(name)
            self.orig_value[name] = value
            ws = self.make_widget_set(name, value)
            for w in ws:
                style = wx.ALL|wx.ALIGN_CENTER_VERTICAL
                if isinstance(w, wx.TextCtrl):
                    style |= wx.EXPAND
                sizer.Add(w, 0, style, 5)

        sizer.Fit(self)
        return sizer



    def set_idle(self, name, message=""):
        self.set_status("idle", name, message)


    def set_warn(self, name, message="Change made!"):
        self.set_status("warn", name, message)


    def set_error(self, name, message="An Error occurred!"):
        self.set_status("error", name, message)


    def set_status(self, status, name, message):
        ico = self.find_ico(name)
        btn = self.find_btn(name)
        txt = self.find_txt(name)

        ico.SetBitmap(self.icons[status])
        ico.SetToolTipString(message)

        if status is "warn":
            btn.Enable()
            txt.SetWindowStyleFlag(wx.TE_PROCESS_ENTER)
        else:
            btn.Disable()
            txt.SetWindowStyleFlag(wx.TE_PROCESS_ENTER)
            txt.ToggleWindowStyle(wx.TE_PROCESS_ENTER)



    def set_icon(self, name):
        icon = wx.EmptyIcon()
        icon.CopyFromBitmap(self.icons[name])
        self.SetIcon(icon)



    get_name = lambda self, event: event.GetEventObject().GetName()[5:]
    find_ico = lambda self, name: self.FindWindowByName("ico::" + name)
    find_txt = lambda self, name: self.FindWindowByName("txt::" + name)
    find_btn = lambda self, name: self.FindWindowByName("btn::" + name)



    def evaluate(self, value):
        return str(eval(value, {'__builtins__': {}}))



    def onIconClick(self, event):
        name = self.get_name(event)

        if self.debug:
            print "icon clicked:\t", name

        txt = self.find_txt(name)
        txt.SetValue(pysctl.read(name))


    def onLabelClick(self, event):
        name = self.get_name(event)

        if self.debug:
            print "label clicked:\t", name

        txt = self.find_txt(name)
        txt.SetValue(self.orig_value[name])


    def onTextChange(self, event):
        name = self.get_name(event)

        if self.debug:
            print "text changed:\t", name

        txt = self.find_txt(name)
        value = txt.GetValue()
        orig = pysctl.read(name)
        if value != orig:
            self.set_warn(name, str(orig))
        else:
            self.set_idle(name)

        try:
            evaluated = self.evaluate(value)
        except (SyntaxError, NameError):
            return

        btn = self.find_btn(name)
        if value == evaluated:
            btn.SetLabel("set")
        else:
            btn.SetLabel("calc")


    def onButtonClick(self, event):
        name = self.get_name(event)

        if self.debug:
            print "button clicked:", name

        txt = self.find_txt(name)
        value = txt.GetValue()

        try:
            evaluated = self.evaluate(value)
        except (SyntaxError, NameError) as e:
            self.set_error(name, e.message)
            return

        if value != evaluated:
            txt.SetValue(evaluated)
            return

        if self.debug or not self.actually_write:
            print "write \"{}\" to: {}".format(value, name)

        if self.actually_write:
            pysctl.write(name, value)

        self.set_idle(name)





if __name__ == '__main__':
    app = wx.App()
    wxPysctl(debug=True, actually_write=False)
    app.MainLoop()


