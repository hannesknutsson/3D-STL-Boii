import StlToGif
import shutil

discordToken = "NjExMjg4Mjc5OTA3ODI3NzI1.XZUcYw.FDN44Of56bz7Xbtt8okr3rzHk04"


args = ["-i", "Yabbe_hallare.stl", "-o", "aaaaaaaa.gif", "--elevation", "45", "--duration", "0.01", "--nframes", "100"]

StlToGif.main(args)

shutil.rmtree('frames')
shutil.rmtree('__pycache__')

