import wx
import wx.grid as gridlib
import pandas as pd
from datetime import datetime
import visualization.plotter as pl

#non-wx vars (global)
path = ""
toolbar_bool = True
nextyear = int(datetime.now().year) + 1
dataLoaded = False

class SlothSleuth(wx.Frame):

    def __init__(self, parent, title):
        super(SlothSleuth, self).__init__(parent, title=title, size=(800, 500))

        self.dfPanel = None
        self.chatPanel = None
        self.splitter = None

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
        self.visualizeItem = viewMenu.Append(wx.ID_ANY, 'Visualize Data')
        dfViewItem.Check(check=toolbar_bool)
        chatViewItem.Check(check=toolbar_bool)
        toolbarView.Check(check = toolbar_bool)
        menubar.Append(viewMenu, '&View')

        #Filter menu
        filtermenu = wx.Menu()
        datefilter = filtermenu.Append(wx.ID_ANY, 'Date', "Filter by: Date")
        keywordfilter = filtermenu.Append(wx.ID_ANY, 'Keyword', "Filter by: Keyword")
        menubar.Append(filtermenu, '&Filter')

        self.SetMenuBar(menubar)

        # Bind menu events
        self.Bind(wx.EVT_MENU, self.OnImport, importItem)
        self.Bind(wx.EVT_MENU, self.OnQuit, quitItem)
        self.Bind(wx.EVT_MENU, self.OnToggleDFView, dfViewItem)
        self.Bind(wx.EVT_MENU, self.OnToggleChatView, chatViewItem)
        self.Bind(wx.EVT_MENU, self.OnToggleToolbar, toolbarView)
        self.Bind(wx.EVT_MENU, self.filterByDate, datefilter)
        self.Bind(wx.EVT_MENU, self.easterEgg, keywordfilter) #make a filterByKeyword function

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
        self.toolbar.SetBackgroundColour((150, 150, 220, 50))
        self.toolbar.SetToolBitmapSize(size=(32, 32))
        self.toolbar.Realize()

        #Bind toolbar functions
        self.Bind(wx.EVT_TOOL, self.OnToggleDFView, self.dfViewTool)
        self.Bind(wx.EVT_TOOL, self.OnToggleChatView, self.chatViewTool)

        #New keybinds
        ctrl_s_id = wx.NewId()
        ctrl_i_id = wx.NewId()
        ctrl_j_id = wx.NewId()

        # Accelerator Table for Key Bindings
        entries = [wx.AcceleratorEntry() for i in range(4)]

        entries[0].Set(wx.ACCEL_CTRL, ord('S'), ctrl_s_id)
        entries[1].Set(wx.ACCEL_CTRL, ord('X'), wx.ID_EXIT)
        entries[2].Set(wx.ACCEL_CTRL, ord('I'), ctrl_i_id)
        entries[3].Set(wx.ACCEL_CTRL, ord('J'), ctrl_j_id)
        accel = wx.AcceleratorTable(entries)
        self.SetAcceleratorTable(accel)

        self.Bind(wx.EVT_MENU, self.OnShowSearchQuery, id=ctrl_s_id)
        self.Bind(wx.EVT_MENU, self.OnImport, id=ctrl_i_id)
        self.Bind(wx.EVT_KEY_DOWN, self.OnQuit, id=wx.ID_EXIT)
        self.Bind(wx.EVT_MENU, self.easterEgg, id=ctrl_j_id)

    def OnShowSearchQuery(self, event):
        if not hasattr(self, 'queryString'):
            self.queryString = wx.TextCtrl(self.panel, value="Insert query here...", size=(500, -1), style=wx.TE_PROCESS_ENTER)
            searchButton = wx.Button(self.panel, label='Search', size=(100, -1))
            searchButton.Bind(wx.EVT_BUTTON, self.OnSearch)
            self.queryString.Bind(wx.EVT_TEXT_ENTER, self.OnSearch)
            hbox = wx.BoxSizer(wx.HORIZONTAL)
            hbox.Add(self.queryString, 1, wx.EXPAND | wx.ALL, 5)
            hbox.Add(searchButton, 0, wx.ALL, 5)
            self.vbox.Add(hbox, 0, wx.EXPAND)
            self.panel.Layout()
        self.queryString.SetFocus()

    def OnImport(self, event):
        with wx.FileDialog(self, "Open Excel file", wildcard="Excel File (*.xlsx) | *.xlsx", style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return  # the user changed their mind

            path = fileDialog.GetPath()
            self.LoadData(path)
            self.Bind(wx.EVT_MENU, pl.plot_charts(self.df), self.visualizeItem)
            self.DisplayViews()
            self.Refresh()

    def LoadData(self, path):
        self.df = pd.read_excel(path)
        print(len(self.df))
        for index, row in self.df.iterrows():
            print(type(row['Date']))
        dataLoaded = True
        self.column_names = self.df.columns
        print(self.column_names)
        return self.df

    def DisplayViews(self):
        self.vbox.Clear(True)
        
        # Search bar at the top (shared across views)
        self.queryString = wx.TextCtrl(self.panel, value="Insert query here...", size=(500, -1), style=wx.TE_PROCESS_ENTER)
        searchButton = wx.Button(self.panel, label='Search', size=(100, -1))
        searchButton.Bind(wx.EVT_BUTTON, self.OnSearch)
        self.queryString.Bind(wx.EVT_TEXT_ENTER, self.OnSearch)
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
        self.splitter.Refresh()
        self.panel.Layout()
        self.vbox.Layout()
        self.panel.Refresh()
        self.panel.Update()
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
        if query.strip():  # Check if there's text in the search bar
            wx.MessageBox(f'Searching for: {query}', 'Search', wx.OK | wx.ICON_INFORMATION)
        else:
            wx.MessageBox('Please enter a search query.', 'Search', wx.OK | wx.ICON_WARNING)


    def OnChatEnter(self, event):
        message = self.inputBox.GetValue()
        self.chatBox.AppendText(f'You: {message}\n')
        self.inputBox.Clear()
    
    def easterEgg(self, event):
        wx.MessageBox(f'This is an Easter Egg :-)', 'Egg', wx.OK | wx.ICON_ASTERISK)

    def OnToggleToolbar(self, event):
        if self.toolbar.IsShown():
            self.toolbar.Hide()
            toolbar_bool = False
        else:
            self.toolbar.Show()
            toolbar_bool = True
        self.Layout()
        self.Refresh()
    
    def OnToggleDFView(self, event):
        if self.dfPanel:
            if self.dfPanel.IsShown():
                self.dfPanel.Hide()
                toolbar_bool = False
            else:
                self.dfPanel.Show()
                toolbar_bool = True
    
    def OnToggleChatView(self, event):
        if self.chatPanel:
            if self.chatPanel.IsShown():
                self.chatPanel.Hide()
                toolbar_bool = False
            else:
                self.chatPanel.Show()
                toolbar_bool = True
    
    def getFilterByDate(self):
        filterentry = wx.TextEntryDialog(self, "Enter a minimum year value to filter by.")
        return filterentry.GetValue()
    
    def filterByDate(self, event):
        self.dateval = self.getFilterByDate()
        print(type(self.dateval))
        self.dateval = int(self.dateval)
        print(type(self.dateval))
        for index, row in self.df.iterrows():
            print(type(row['Date']))
            if isinstance(row['Date'], int):
                if self.dateval > nextyear or self.dateval < 1:
                    wx.MessageBox(f'Please enter a real year.', 'Error: nonexistent year', wx.OK | wx.ICON_ERROR)
                else: 
                    filtereddate = self.df.loc[row['Date'] >= self.dateval]
            else:
                continue