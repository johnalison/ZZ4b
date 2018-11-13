from analysis import *
import optparse
parser = optparse.OptionParser()
parser.add_option('-i', '--inFileName',           dest="inFileName",         default="", help="")
parser.add_option('-o', '--outFileName',          dest="outFileName",        default="", help="")
parser.add_option('-n', '--nEvents',              dest="nEvents",            default=None, help="Number of events to process")
parser.add_option('-d', '--debug',                dest="debug",    action="store_true", default=False, help="Debug")
o, a = parser.parse_args()


f=ROOT.TFile(o.inFileName)
tree=f.Get("LHEF")

a = analysis(tree, o.outFileName, o.debug)
a.lumi = 24.3e3
if o.nEvents: a.eventLoop(range(int(o.nEvents)))
else:         a.eventLoop()

f.Close()
a.Write()
