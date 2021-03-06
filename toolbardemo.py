#!/usr/bin/env python2.5

# Note that I use python2.4 above because my system has 2.4 and 2.4 installed


"""

This is demo of a number of things that can be done with toolbars. When
run from a console, it writes messages to indicate toolbar events

This includes:
-Having it managed by a frame: the most basic way of creating a toolbar

-Placing a toolbar in a wxPanel with a sizer so that you can have a
 custom panel with a toolbar attached, rather than a frame

-Placing multiple toolbars in a Panel (could be done with a frame as well)

-Using a wxStaticBitmap on a toolbar: can be used a custom separator, if
 you don't like the one that comes with the stock widget, or want the
 same thing on all platforms.

-Making a set of buttons on a toolbar act like radio buttons: that is,
 only one is pressed at a time.

A few things in the demo that are not strictly about toolbars:

-A simple sizer layout of multiple panels on a frame

-Using code generated by img2py.py to imbed icons into Python code.

Please send Comments, suggestions, etc to:

Chris.Barker@noaa.gov

"""
import wx

ID_ZOOM_IN_BUTTON = wx.NewId()
ID_ZOOM_OUT_BUTTON = wx.NewId()
ID_TEST_BUTTON = wx.NewId()
ID_MOVE_MODE_BUTTON = wx.NewId()

ID_ZOOM_IN_BUTTON2 = wx.NewId()
ID_ZOOM_OUT_BUTTON2 = wx.NewId()
ID_TEST_BUTTON2 = wx.NewId()
ID_MOVE_MODE_BUTTON2 = wx.NewId()

ID_TOOLBAR = wx.NewId()


class TestPanel(wx.Panel):
    """
    A Panel class with one or two attached toolbars

    """
    
    def __init__(self, parent, id = -1, size = wx.DefaultSize,color = "BLUE",NumToolbars = 1):
        
        wx.Panel.__init__(self, parent, id, wx.Point(0, 0), size, wx.SUNKEN_BORDER)

        self.WindowColor = color

        ## Create the vertical sizer for the toolbar and Panel
        box = wx.BoxSizer(wx.VERTICAL)
        tb = self.BuildToolbar1()
        box.Add(tb,0,wx.ALL | wx.ALIGN_LEFT | wx.EXPAND,4) # add the toolbar to the sizer
        if NumToolbars == 2: # Do we want the second toolbar?
            tb = self.BuildToolbar2()
            box.Add(tb,0,wx.ALL | wx.ALIGN_RIGHT ,4)# This one gets aligned to the right

        #Now add a Window to draw stuff to (this could be any wx.Window derived control) 
        self.DrawWindow = wx.Window(self,-1,wx.DefaultPosition,wx.DefaultSize,wx.SUNKEN_BORDER)
        box.Add(self.DrawWindow,1,wx.EXPAND)

        box.Fit(self)
        self.SetAutoLayout(True)
        self.SetSizer(box)

        # this connects the OnPaint handler to when the DrawWindow needs to be re-painted
        wx.EVT_PAINT(self.DrawWindow, self.OnPaint)
        

    def BuildToolbar1(self):

        """
        creates one of the toolbars

        The buttons act like radio buttons, setting a mode for the Panel
        Only one of them is pressed at a time. The SetMOde() method handles this

        """
        
        tb = wx.ToolBar(self,-1)
        self.ToolBar = tb
        tb.SetToolBitmapSize((21,21))# this required for non-standard size buttons on MSW
        
        tool = tb.AddTool(wx.ID_ANY, bitmap=GetPlusBitmap(), isToggle=True)
        self.Bind(wx.EVT_TOOL, self.SetMode, tool)
      
        tb.AddTool(ID_ZOOM_OUT_BUTTON, GetMinusBitmap(),isToggle=True)
        wx.EVT_TOOL(self, ID_ZOOM_OUT_BUTTON, self.SetMode)
      
        tb.AddTool(ID_MOVE_MODE_BUTTON, GetHandBitmap(),isToggle=True)
        wx.EVT_TOOL(self, ID_MOVE_MODE_BUTTON, self.SetMode)
      
        tb.AddSeparator()
      
        tb.AddControl(wx.Button(tb, ID_TEST_BUTTON, "Button",wx.DefaultPosition, wx.DefaultSize))
        wx.EVT_BUTTON(self, ID_TEST_BUTTON, self.ButtonAction)
                
        tb.Realize()

        return tb

    def BuildToolbar2(self):

        """
        Creates another toolbar. It looks the same, but acts a little different:
        The buttons are independent, rather than acting like radio buttons

        It also has a custom separator, created by adding a tall skinny bitmap.

        """
        
        tb = wx.ToolBar(self,-1)
        self.ToolBar2 = tb
        tb.SetToolBitmapSize((21,21))# this required for non-standard size buttons on MSW

        tb.AddTool(ID_ZOOM_IN_BUTTON2, GetPlusBitmap(),isToggle=True)
        wx.EVT_TOOL(self, ID_ZOOM_IN_BUTTON2, self.ButtonPress2)
      
        tb.AddTool(ID_ZOOM_OUT_BUTTON2, GetMinusBitmap(),isToggle=True)
        wx.EVT_TOOL(self, ID_ZOOM_OUT_BUTTON2, self.ButtonPress2)
      
        tb.AddTool(ID_MOVE_MODE_BUTTON2, GetHandBitmap(),isToggle=True)
        wx.EVT_TOOL(self, ID_MOVE_MODE_BUTTON2, self.ButtonPress2)
      
        # a way to do a custom separator
        tb.AddControl(wx.StaticBitmap(tb, -1, GetSeparatorBitmap(), wx.DefaultPosition, wx.DefaultSize))
      
        tb.AddControl(wx.Button(tb, ID_TEST_BUTTON2, "Button",wx.DefaultPosition, wx.DefaultSize))
        wx.EVT_BUTTON(self, ID_TEST_BUTTON2, self.ButtonPress2)

        tb.Realize()

        return tb

    def ButtonPress2(self,event):
        print "A button was pressed on the second toolbar of the %s Panel"%self.WindowColor

    def SetMode(self,event):
        for id in [ID_ZOOM_IN_BUTTON,ID_ZOOM_OUT_BUTTON,ID_MOVE_MODE_BUTTON]:
            self.ToolBar.ToggleTool(id,0)
        self.ToolBar.ToggleTool(event.GetId(),1)
        if event.GetId() == ID_ZOOM_IN_BUTTON:
            print "mode set to Zoom In in the %s Canvas"%self.WindowColor
        elif event.GetId() == ID_ZOOM_OUT_BUTTON:
            print "mode set to Zoom Out in the %s Canvas"%self.WindowColor
        elif event.GetId() == ID_MOVE_MODE_BUTTON:
            print "mode set to Move in the %s Canvas"%self.WindowColor

    def ButtonAction(self,event):
        print "Button clicked in the %s Canvas"%self.WindowColor
        pass

    def OnPaint(self,event):
        dc = wx.PaintDC(self.DrawWindow)
        dc.SetBackground(wx.Brush(wx.NamedColour(self.WindowColor)))
        dc.BeginDrawing()
        dc.Clear()
        dc.EndDrawing()

class TestFrame(wx.Frame):
    def __init__(self,parent, id,title,position,size):
        wx.Frame.__init__(self,parent, id,title,position, size)
        

        wx.EVT_CLOSE(self, self.OnCloseWindow)


        Canvas1 = TestPanel(self,color = "RED")
        Canvas2 = TestPanel(self,color = "BLUE",NumToolbars = 2)

        #Build the Toolbar
        tb = self.CreateToolBar(wx.TB_HORIZONTAL|wx.NO_BORDER)
        self.ToolBar = tb
        tb.SetToolBitmapSize((21,21))# this required for non-standard size buttons on MSW
      
        tb.AddTool(ID_ZOOM_IN_BUTTON, GetPlusBitmap(),isToggle=True)
        wx.EVT_TOOL(self, ID_ZOOM_IN_BUTTON, self.SetMode)
      
        tb.AddTool(ID_ZOOM_OUT_BUTTON, GetMinusBitmap(),isToggle=True)
        wx.EVT_TOOL(self, ID_ZOOM_OUT_BUTTON, self.SetMode)
      
        tb.AddTool(ID_MOVE_MODE_BUTTON, GetHandBitmap(),isToggle=True)
        wx.EVT_TOOL(self, ID_MOVE_MODE_BUTTON, self.SetMode)
      
        tb.AddSeparator()
      
        tb.AddControl(wx.Button(tb, ID_TEST_BUTTON, "Button",wx.DefaultPosition, wx.DefaultSize))
        wx.EVT_BUTTON(self, ID_TEST_BUTTON, self.ButtonAction)

        tb.AddSeparator()
      
        tb.AddControl(wx.StaticText(tb, -1, "A Frame Managed Toolbar", wx.DefaultPosition, wx.DefaultSize))
                
        tb.Realize()


        ## Create the horizontal sizer for the two panels
        box = wx.BoxSizer(wx.HORIZONTAL)

        box.Add(Canvas1,1,wx.EXPAND)
        box.Add(Canvas2,2,wx.EXPAND)

        #box.Fit(self)
        self.SetAutoLayout(True)
        self.SetSizer(box)

        self.Show(True)

    def SetMode(self,event):
        for id in [ID_ZOOM_IN_BUTTON,ID_ZOOM_OUT_BUTTON,ID_MOVE_MODE_BUTTON]:
            self.ToolBar.ToggleTool(id,0)
        self.ToolBar.ToggleTool(event.GetId(),1)
        if event.GetId() == ID_ZOOM_IN_BUTTON:
            print "mode set to Zoom In in the Frame"
        elif event.GetId() == ID_ZOOM_OUT_BUTTON:
            print "mode set to Zoom Out in the Frame"
        elif event.GetId() == ID_MOVE_MODE_BUTTON:
            print "mode set to Move in the Frame"

    def ButtonAction(self,event):
        print "Button clicked in the Frame"
        pass

    def OnCloseWindow(self, event):
        self.Destroy()
    
class App(wx.App):
    def OnInit(self):
        frame = TestFrame(None, -1, "Toolbar Test",wx.DefaultPosition,(550,200))
        self.SetTopWindow(frame)
        return True

# The data for the icons. These functions were generated by img2py,
# which comes with the wxPython distribution, in the tools directory.
# It is a pretty handy way to imbed icons in your Python code.

import cPickle, zlib

def GetHandData():
    return cPickle.loads(zlib.decompress(
'x\xda\xd3\xc8)0\xe4\nV72T\x00!\x05Cu\xae\xc4`u=\x85d\x05\xa7\x9c\xc4\xe4l0O\
\x01\xc8S\xb6t\x06A(\x1f\x0b\xa0\xa9\x8c\x9e\x1e6\x19\xa0\xa8\x1e\x88\xd4C\
\x97\xd1\x83\xe8\x80 \x9c2zh\xa6\xc1\x11X\n\xab\x8c\x02\x8a\x0cD!\x92\x12\
\x98\x8c\x1e\x8a\x8b\xd1d\x14\xf4\x90%\x90LC\xf6\xbf\x1e\xba\xab\x91%\xd0\
\xdc\x86C\x06\xd9m\xe8!\xaa\x87S\x86\x1a1\xa7\x07\x00v\x0f[\x17' ))

def GetHandBitmap():
    return wx.BitmapFromXPMData(GetHandData())

def GetHandImage():
    return wx.ImageFromBitmap(GetHandBitmap())

#----------------------------------------------------------------------
def GetPlusData():
    return cPickle.loads(zlib.decompress(
'x\xda\xd3\xc8)0\xe4\nV72T\x00!\x05Cu\xae\xc4`u=\x85d\x05\xa7\x9c\xc4\xe4l0O\
\x01\xc8S\xb6t\x06A(\x1f\x0b RF\x0f\x08\xb0\xc9@D\xe1r\x08\x19\xb8j=l2`\r\
\xe82HF\xe9a\xc8\xe8\xe9A\x9c@\x8a\x0c\x0e\xd3p\xbb\x00\x8f\xab\xe1>\xd5\xd3\
\xc3\x15:P)l!\n\x91\xc2\x1a\xd6`)\xec\xb1\x00\x92\xc2\x11?\xb8e\x88\x8fSt\
\x19=\x00\x82\x16[\xf7' ))

def GetPlusBitmap():
    return wx.BitmapFromXPMData(GetPlusData())

def GetPlusImage():
    return wx.ImageFromBitmap(GetPlusBitmap())

#----------------------------------------------------------------------
def GetMinusData():
    return cPickle.loads(zlib.decompress(
'x\xda\xd3\xc8)0\xe4\nV72T\x00!\x05Cu\xae\xc4`u=\x85d\x05\xa7\x9c\xc4\xe4l0O\
\x01\xc8S\xb6t\x06A(\x1f\x0b RF\x0f\x08\xb0\xc9@D\xe1r\x08\x19\xb8j=\xa2e\
\x10\x16@\x99\xc82zz\x10\'\x90"\x83\xc34r\xdc\x86\xf0\xa9\x9e\x1e\xae\xd0\
\x81Ja\x0bQ\x88\x14\xd6\xb0\x06Ka\x8f\x05\x90\x14\x8e\xf8\xc1-C|\x9c\xa2\xcb\
\xe8\x01\x00\xed\x0f[\x87' ))

def GetMinusBitmap():
    return wx.BitmapFromXPMData(GetMinusData())

def GetMinusImage():
    return wx.ImageFromBitmap(GetMinusBitmap())

def GetSeparatorData():
    return cPickle.loads(zlib.decompress(
'x\xda\xd3\xc8)0\xe4\nV74P02T0R0T\xe7J\x0cV\xd7SHVPvs3\x00\x020_\x01\xc8\xf7\
\xcb\xcfK\x85r\x14\x14\xf4\xf4@\xe4(\x97$\xae\x1e\x00S\xca=4' ))

def GetSeparatorBitmap():
    return wx.BitmapFromXPMData(GetSeparatorData())

def GetSeparatorImage():
    return wx.ImageFromBitmap(GetSeparatorBitmap())
     
if __name__ == "__main__":
    app = App(0)
    app.MainLoop()














