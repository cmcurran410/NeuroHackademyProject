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
        self.toolbarView = viewMenu.AppendCheckItem(wx.ID_ANY, 'Toolbar')
        self.toolbarView.Check(check = True)
        menubar.Append(viewMenu, '&View')

        self.SetMenuBar(menubar)
        
        # Bind menu events
        self.Bind(wx.EVT_MENU, self.OnImport, importItem)
        self.Bind(wx.EVT_MENU, self.OnQuit, quitItem)
        self.Bind(wx.EVT_MENU, self.OnToggleToolbar, self.toolbarView)
        
        # Main panel
        panel = wx.Panel(self)
        mainSizer = wx.BoxSizer(wx.VERTICAL)

        # Query frame
        queryFrame = wx.Panel(panel)
        querySizer = wx.BoxSizer(wx.HORIZONTAL)
        self.queryString = wx.TextCtrl(queryFrame, value="Insert query here...", size=(500, -1))
        searchButton = wx.Button(queryFrame, label='Search', size=(100, -1))
        querySizer.Add(self.queryString, proportion=1, flag=wx.ALL | wx.EXPAND, border=5)
        querySizer.Add(searchButton, flag=wx.ALL, border=5)
        queryFrame.SetSizer(querySizer)

        # Viewer frame
        viewerFrame = wx.Panel(panel)
        viewerSizer = wx.BoxSizer(wx.VERTICAL)
        self.grid = gridlib.Grid(viewerFrame)
        self.grid.CreateGrid(0, 0)
        viewerSizer.Add(self.grid, proportion=1, flag=wx.ALL | wx.EXPAND, border=5)
        viewerFrame.SetSizer(viewerSizer)

        # Add frames to main sizer
        mainSizer.Add(viewerFrame, proportion=1, flag=wx.ALL | wx.EXPAND, border=10)
        mainSizer.Add(queryFrame, flag=wx.ALL | wx.EXPAND, border=10)
        panel.SetSizer(mainSizer)
        
        # Status bar
        self.CreateStatusBar()
        
        # Toolbar
        self.toolbar = self.CreateToolBar()
        self.toolbar.AddTool(wx.ID_OPEN, 'Sloth', wx.Bitmap("Project_dir/res/images/sloth_sleuth.png"))
        self.toolbar.SetToolBitmapSize(size=(32, 32))
        self.toolbar.Realize()

    def OnImport(self, event):
        with wx.FileDialog(self, "Open CSV file", wildcard="CSV files (*.csv)|*.csv",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return  # the user changed their mind

            path = fileDialog.GetPath()
            self.LoadData(path)

    def LoadData(self, path):
        df = pd.read_csv(path)
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

    def OnToggleToolbar(self, event):
        if self.toolbar.IsShown():
            self.toolbar.Hide()
        else:
            self.toolbar.Show()
        self.Layout()