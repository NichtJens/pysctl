#!/usr/bin/env python

import wx


class nTextCtrl(wx.Panel):

    def __init__(self,
                 parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.DefaultSize, name=wx.TextCtrlNameStr,
                 number=None, value=None,
                 style=0, validator=wx.DefaultValidator,
                 orient=wx.HORIZONTAL,
                 debug=False):

        wx.Panel.__init__(self, parent=parent, id=id, pos=pos, size=size, name=name)

        self.sizer = wx.BoxSizer(orient=orient)
        self.SetSizer(self.sizer)

        if isinstance(value, str):
            value = value.split()
        number, value = correct(number, value)

        if debug:
            value = ["{name}: {number}-{index}".format(name=name, number=number, index=i+1) for i in xrange(number)]

        self._textctrls = []
        for i, v in enumerate(value):
            t = wx.TextCtrl(self, value=v,
                            style=style, validator=validator,
                            name="{}[{}]".format(name, i))

            self._textctrls.append(t)
            self.sizer.Add(t, 1)

        self._setup_forwarders()


    def _setup_forwarders(self):
        EVENTS = (wx.EVT_TEXT, wx.EVT_TEXT_ENTER)
        for e in EVENTS:
            self._bind_event_forwarder(e)

        METHODS = ("SetWindowStyleFlag", "ToggleWindowStyle")
        for f in METHODS:
            self._add_method_fowarder(f)


    def _bind_event_forwarder(self, event):
        for t in self._textctrls:
            t.Bind(event, self._event_forwarder)

    def _event_forwarder(self, event):
        event.SetEventObject(self)
        self.GetEventHandler().ProcessEvent(event)


    def _add_method_fowarder(self, function_name):
        setattr(self, function_name, self._method_fowarder(function_name))

    def _method_fowarder(self, function_name):
        return lambda *args, **kwargs: self._method_loop(function_name, *args, **kwargs)

    def _method_loop(self, function_name, *args, **kwargs):
        for t in self._textctrls:
            getattr(t, function_name)(*args, **kwargs)


    def GetValue(self):
        return "\t".join(tc.GetValue() for tc in self._textctrls)

    def SetValue(self, value):
        if isinstance(value, str):
            value = value.split()
        for v, tc in zip(value, self._textctrls):
            tc.SetValue(v)

    Value = property(GetValue, SetValue)





def correct(number=None, value=None):

    if value is None:
        if number is None:
            number = 1
        value  = [wx.EmptyString] * number
    else:
        if number is None:
            number = len(value)
        else:
            assert number == len(value)

    return number, value


def test_correct():
    n = 10
    L = range(n)

    assert correct()                  == (1, [wx.EmptyString])
    assert correct(number=n)          == (n, [wx.EmptyString] * n)
    assert correct(value=L)           == (n, L)
    assert correct(number=n, value=L) == (n, L)

    try:
        correct(number=1, value=L)
        print "This was supposed to fail!"
    except AssertionError:
        pass







class MainFrame(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, "My Frame")
        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)

        t = wx.TextCtrl(panel, wx.ID_ANY, "a standard wx.TextCtrl")
        sizer.Add(t, 0, wx.ALL|wx.EXPAND)

        ntxts = []
        for i in xrange(10):
            t = nTextCtrl(panel, value=["a"*i]*i, style=wx.TE_PROCESS_ENTER)
            ntxts.append(t)
            sizer.Add(t, 0, wx.ALL|wx.EXPAND)

        for t in ntxts:
            print t.GetValue()
#            t.SetValue("m "*len(t.GetValue()))
#            print t.Value
#            t.Value = "n "*len(t.GetValue())

        panel.SetSizer(sizer)
        sizer.Fit(self)

        self.Show()



if __name__ == '__main__':
    test_correct()
    app = wx.App()
    MainFrame()
    app.MainLoop()

