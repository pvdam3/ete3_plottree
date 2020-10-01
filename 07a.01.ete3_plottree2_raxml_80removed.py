# Call script using python2: python 07a.01.ete3_plottree2_raxml_<80removed.py [infolder containing files ending with .raxml_hc]
# A pdf file of the phylogenetic tree with colored nodes will be created of all files in the infolder that end with .raxml_hc
# Nodes will be colored according to colors indicated in the colordict in fsp_to_color.py
# Nodes with low bootstrap values (below 80) will be collapsed
# Leaves with nodename F-nonpath-Barmshour are detached

import sys
from ete3 import *
from fsp_to_color import CheckColor

infolder = sys.argv[1]
for file in os.listdir(infolder):
	if file.endswith('.raxml_hc'):
		print file
		infile = infolder+'/'+file
		try:
			t = Tree(infile)
		except:
			continue
		ts = TreeStyle()
		#ts.mode = "c" #circular tree
		ts.show_leaf_name = False
		ts.margin_top = 10
		ts.margin_left = 10
		ts.margin_right = 10
		ts.margin_bottom = 10
		ts.show_branch_support = True
		# to increase branch length
		ts.scale = 300000
		# to increase node seperation
		ts.branch_vertical_margin = 10
		# # To draw guiding lines if you align isolate names
		ts.draw_guiding_lines = True	

		nameFace = AttrFace("name", fsize=35)
		
		R = t.get_midpoint_outgroup()
		t.set_outgroup(R)
		t.ladderize(direction=1)

		# remove nodes with low bootstrap support (<80)
		for n in t.get_descendants():
			if not n.is_leaf() and n.support < 80:
				n.delete()
		
		# remove F-nonpath-Barmshour
		for n in t.get_descendants():
			if n.is_leaf() and n.name == "F-nonpath-Barmshour":
				n.detach()

		for n in t.traverse():
			nstyle = NodeStyle()
			nstyle["fgcolor"] = "black"
			nstyle["size"] = 4
			if n.is_leaf():
				nstyle["fgcolor"] = CheckColor(n.name[:3])
				nstyle["size"] = 20
				nstyle["hz_line_width"] = 4
				n.up.sort_descendants(attr="name")
				# to align isolate names
				n.add_face(nameFace, column = 0, position = "aligned")	
			else:
				BranchSupportValues= TextFace(n.support, fsize=20, fgcolor="DarkRed")
				#n.add_face(BranchSupportValues, column=0, position = "branch-top")
				if float(n.support) > float(90):
					nstyle["hz_line_width"] = 4
					nstyle["vt_line_width"] = 4
					nstyle["hz_line_color"] = "black"
				else:
					nstyle["hz_line_width"] = 4
					nstyle["vt_line_width"] = 4
					nstyle["hz_line_color"] = "black"
			n.set_style(nstyle)

		t.render(infile+'<80removed.pdf', tree_style=ts, w=297, units="mm")
	