# Authors (Alphabetical by last name):
# Cristian Curran
# Magdalena Martinez-Garcia
# Keerthi Stanley
# Loreta Sutkus
# Aydin Tasevac

# NeuroHackademy Hackathon, 2024

#main.py puts everything together and runs the program!

from interfaceWX import SlothSleuth
import wx

if __name__ == '__main__':
    app = wx.App(False)
    frame = SlothSleuth(None, title='Sloth Sleuth')
    frame.SetIcon(wx.Icon("Project_dir/res/images/sloth_sleuth.png"))
    app.MainLoop()