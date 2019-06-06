# -*- mode: python -*-

import sys
from os import path
site_packages = next(p for p in sys.path if 'site-packages' in p)
block_cipher = None

a = Analysis(['c:\\users\\ma3339\\documents\\#develop\\#viga_mista\\python\\VM_GUI_003.pyw'],
             pathex=['C:\\Users\\ma3339\\AppData\\Local\\Programs\\Python\\Python36\\Scripts'],
             binaries=[],
             datas=[(path.join(site_packages,"docx","templates"), 
"docx/templates")],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='VM_GUI_003',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True )
