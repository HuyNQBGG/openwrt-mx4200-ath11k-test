from pathlib import Path
import sys

path = Path(sys.argv[1])
text = path.read_text()
assert text.count('PKG_RELEASE:=1\n') == 1, 'Unexpected mac80211 package release'
path.write_text(text.replace('PKG_RELEASE:=1\n', 'PKG_RELEASE:=2\n'), newline='\n')
