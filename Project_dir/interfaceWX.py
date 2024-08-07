import wx
import wx.grid as gridlib
import pandas as pd

#non-wx vars (global)
path = ""

class SlothSleuth(wx.Frame):

    def __init__(self, parent, title):
        super(SlothSleuth, self).__init__(parent, title=title, size=(800, 500))

        self.InitUI()
        self.Centre()
        self.Show()

    def InitUI(self):
        # Menu bar
        menubar = wx.MenuBar()
        
        # File menu
        fileMenu = wx.Menu()
        importItem = fileMenu.Append(wx.ID_OPEN, 'Import')
        fileMenu.AppendSeparator()
        quitItem = fileMenu.Append(wx.ID_EXIT, 'Exit')
        menubar.Append(fileMenu, '&File')
        
        # View menu
        viewMenu = wx.Menu()
        dfViewItem = viewMenu.AppendCheckItem(wx.ID_ANY, 'DataFrame View')
        chatViewItem = viewMenu.AppendCheckItem(wx.ID_ANY, 'AI Chat View')
        toolbarView = viewMenu.AppendCheckItem(wx.ID_ANY, 'Toolbar')
        dfViewItem.Check(check=True)
        chatViewItem.Check(check=True)
        toolbarView.Check(check = True)
        menubar.Append(viewMenu, '&View')

        self.SetMenuBar(menubar)
        
        # Bind menu events
        self.Bind(wx.EVT_MENU, self.OnImport, importItem)
        self.Bind(wx.EVT_MENU, self.OnQuit, quitItem)
        self.Bind(wx.EVT_MENU, self.OnToggleDFView, dfViewItem)
        self.Bind(wx.EVT_MENU, self.OnToggleChatView, chatViewItem)

        # Main panel
        self.panel = wx.Panel(self)
        self.vbox = wx.BoxSizer(wx.VERTICAL)

        #Initial background panel
        self.backgroundPanel = wx.Panel(self.panel)
        self.backgroundImage = wx.Image("Project_dir/res/images/sloth_background.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.backgroundBitmap = wx.StaticBitmap(self.backgroundPanel, -1, self.backgroundImage)
        self.vbox.Add(self.backgroundPanel, 1, wx.EXPAND)
        
        self.panel.SetSizer(self.vbox)

        #Status bar
        self.CreateStatusBar()

        #Create Toolbar
        self.toolbar = self.CreateToolBar()
        self.dfViewTool = self.toolbar.AddTool(wx.ID_ANY, 'DataFrame View', wx.Bitmap("Project_dir/res/images/dficon.png"))
        self.chatViewTool = self.toolbar.AddTool(wx.ID_ANY, 'AI Chat View', wx.Bitmap("Project_dir/res/images/chaticon.png"))
        self.toolbar.SetToolBitmapSize(size=(32, 32))
        self.toolbar.Realize()

        #Bind toolbar functions
        self.Bind(wx.EVT_TOOL, self.OnToggleChatView, self.chatViewTool)
        self.Bind(wx.EVT_TOOL, self.OnToggleDFView, self.dfViewTool)

    def OnImport(self, event):
        with wx.FileDialog(self, "Open CSV file", wildcard="CSV files (*.csv)|*.csv", style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return  # the user changed their mind

            path = fileDialog.GetPath()
            self.LoadData(path)
            self.DisplayViews()

    def LoadData(self, path):
        self.df = pd.read_csv(path)

    def DisplayViews(self):
        self.vbox.Clear(True)
        
        # Search bar at the top (shared across views)
        self.queryString = wx.TextCtrl(self.panel, value="Insert query here...", size=(500, -1))
        searchButton = wx.Button(self.panel, label='Search', size=(100, -1))
        searchButton.Bind(wx.EVT_BUTTON, self.OnSearch)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(self.queryString, 1, wx.EXPAND | wx.ALL, 5)
        hbox.Add(searchButton, 0, wx.ALL, 5)
        self.vbox.Add(hbox, 0, wx.EXPAND)
        
        # Splitter window for different views
        self.splitter = wx.SplitterWindow(self.panel)
        
        # DataFrame view
        self.dfPanel = wx.Panel(self.splitter)
        self.dfSizer = wx.BoxSizer(wx.VERTICAL)
        self.grid = gridlib.Grid(self.dfPanel)
        self.grid.CreateGrid(0, 0)
        self.dfSizer.Add(self.grid, 1, wx.EXPAND)
        self.dfPanel.SetSizer(self.dfSizer)
        
        # AI Chat view
        self.chatPanel = wx.Panel(self.splitter)
        self.chatSizer = wx.BoxSizer(wx.VERTICAL)
        self.chatBox = wx.TextCtrl(self.chatPanel, style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.chatSizer.Add(self.chatBox, 1, wx.EXPAND)
        self.inputBox = wx.TextCtrl(self.chatPanel, style=wx.TE_PROCESS_ENTER)
        self.inputBox.Bind(wx.EVT_TEXT_ENTER, self.OnChatEnter)
        self.chatSizer.Add(self.inputBox, 0, wx.EXPAND)
        self.chatPanel.SetSizer(self.chatSizer)
        
        self.splitter.SplitVertically(self.dfPanel, self.chatPanel)
        self.splitter.SetSashGravity(0.5)
        self.vbox.Add(self.splitter, 1, wx.EXPAND)
        
        # Load data into the DataFrame view
        self.LoadGridData()

        self.panel.SetSizer(self.vbox)
        self.Layout()

    def LoadGridData(self):
        df = self.df
        self.grid.ClearGrid()

        if self.grid.GetNumberRows() > 0:
            self.grid.DeleteRows(0, self.grid.GetNumberRows())
        
        if self.grid.GetNumberCols() > 0:
            self.grid.DeleteCols(0, self.grid.GetNumberCols())

        self.grid.AppendCols(len(df.columns))
        self.grid.AppendRows(len(df.index))

        for col_idx, col_name in enumerate(df.columns):
            self.grid.SetColLabelValue(col_idx, col_name)
            for row_idx, value in enumerate(df[col_name]):
                self.grid.SetCellValue(row_idx, col_idx, str(value))

    def OnQuit(self, event):
        self.Close()

    def OnSearch(self, event):
        query = self.queryString.GetValue()
        wx.MessageBox(f'Searching for: {query}', 'Search', wx.OK | wx.ICON_INFORMATION)

    def OnChatEnter(self, event):
        message = self.inputBox.GetValue()
        self.chatBox.AppendText(f'You: {message}\n')
        self.inputBox.Clear()
    
    def OnToggleToolbar(self, event):
        if self.toolbar.IsShown():
            self.toolbar.Hide()
        else:
            self.toolbar.Show()
        self.Layout()
    
    def OnToggleDFView(self, event):
        if self.dfPanel.IsShown():
            self.dfPanel.Hide()
        else:
            self.dfPanel.Show()
        self.Layout()
    
    def OnToggleChatView(self, event):
        if self.chatPanel.IsShown():
            self.chatPanel.Hide()
        else:
            self.chatPanel.Show()
        self.Layout()