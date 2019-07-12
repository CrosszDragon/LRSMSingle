# -*- mode: python -*-
import sys
import os.path as osp

sys.setrecursionlimit(5000)

block_cipher = None
SETUP_DIR = u'D:\\学习文件\\python_learning\\LRSMSingleVersion'

a = Analysis(['UILayer\\MainWindow\\MainWindow.py',
              'UILayer\\MainWindow\\MainWindowUi.py',
              'UILayer\\CustomWidget\\ColorDockWidget.py',
              'UILayer\\CustomWidget\\DockWidget.py',
              'UILayer\\CustomWidget\\GadgetButton.py',
              'UILayer\\CustomWidget\\GadgetDockWidget.py',
              'UILayer\\CustomWidget\\LayerDockWidget.py',
              'UILayer\\CustomWidget\\NewProjectDialog.py',
              'UILayer\\CustomWidget\\ProjectTreeDockWidget.py',

              'ModelLayer\\AbstractFile.py',
              'ModelLayer\\AbstractFolder.py',
              'ModelLayer\\AbstractMarkItem.py',
              'ModelLayer\\Folder.py',
              'ModelLayer\\MarkFile.py',
              'ModelLayer\\MarkItem.py',
              'ModelLayer\\MarkProject.py',
              'ModelLayer\\Selection.py',
              
              'HistoryManage\\Command.py',
              
              'CONST\\CONST.py',
              
              'CommonHelper\\CommonHelper.py',
              
              'Application\\App.py',
              
              'Algorithm\\doubleArea_distinguish.py',

              'UILayer\\Workbench\\BorderItem.py',
              'UILayer\\Workbench\\GraphicsItem.py',
              'UILayer\\Workbench\\GraphicsView.py',
              'UILayer\\Workbench\\TextItem.py',
              'UILayer\\Workbench\\WorkbenchWidget.py',
              ],
             pathex=[u'D:\\学习文件\\python_learning\\LRSMSingleVersion'],
             binaries=[],
             datas=[("sources\\icons", "sources\\icons"), ("sources\\images", "sources\\images")],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
          cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='MainWindow',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False)
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='MainWindow')
