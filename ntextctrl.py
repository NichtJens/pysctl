#!/usr/bin/env python

import wx


class nTextCtrl(wx.Panel):
    """
    Widget containing an array of wx.TextCtrl widgets
    Trys to mimic the behavior of the contained widgets
    """

    def __init__(self,
                 parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.DefaultSize, name=wx.TextCtrlNameStr,
                 number=None, value=None,
                 style=0, validator=wx.DefaultValidator,
                 orient=wx.HORIZONTAL,
                 debug=False):
        """
        The number of TextCtrl widgets is either given by number or by the length of value
        Other parameters are forwarded to the TextCtrl widgets or the panel/sizer containing them
        If debug is True, the TextCtrl widgets will be filled with a counting string instead
        """

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


    def _setup_forwarders(self,
                          events = (wx.EVT_TEXT, wx.EVT_TEXT_ENTER),
                          methods = ("SetWindowStyleFlag", "ToggleWindowStyle")):
        """
        Calls _bind_event_forwarder and _add_method_forwarder
        for the given events and methods, respectively
        """

        for e in events:
            self._bind_event_forwarder(e)

        for f in methods:
            self._add_method_forwarder(f)


    def _bind_event_forwarder(self, event):
        """Bind _event_forwarder to event for all _textctrls"""
        for t in self._textctrls:
            t.Bind(event, self._event_forwarder)

    def _event_forwarder(self, event):
        """Replace the EventObject by self and re-emit event"""
        event.SetEventObject(self)
        self.GetEventHandler().ProcessEvent(event)


    def _add_method_forwarder(self, function_name):
        """Add _method_forwarder to self for given function_name"""
        setattr(self, function_name, self._method_forwarder(function_name))

    def _method_forwarder(self, function_name):
        """Curry a _method_loop with function_name"""
        return lambda *args, **kwargs: self._method_loop(function_name, *args, **kwargs)

    def _method_loop(self, function_name, *args, **kwargs):
        """Call function_name(*args, **kwargs) for all _textctrls"""
        for t in self._textctrls:
            getattr(t, function_name)(*args, **kwargs)


    def GetValue(self):
        """Return the joined Values of all _textctrls"""
        return "\t".join(t.GetValue() for t in self._textctrls)

    def SetValue(self, value):
        """If necessary split value, set its items as Value to the _textctrls"""
        if isinstance(value, str):
            value = value.split()
        for v, tc in zip(value, self._textctrls):
            tc.SetValue(v)

    Value = property(GetValue, SetValue)





def correct(number=None, value=None):
    """Make the content of number and value consistent"""

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
    """A simple test for correct()"""

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
    """A small test for nTextCtrl"""

    def __init__(self):
        """
        Create this frame, a panel, and a sizer
        Add a standard wx.TextCtrl and several nTextCtrl widgets
        Read and print their Values
        """

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

