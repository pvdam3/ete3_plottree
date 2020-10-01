
def CheckColor(nodename):
	colordict={
	"F-n":"#8D99AE",
	"Fo-":"#8D99AE",
	"Fol":"#D72638",
	"Foc":"#7FB069",
	"For":"#034732",
	"Fom":"#F3A712",
	"Fon":"#2F6690"
	}
	if colordict.has_key(nodename):
		return colordict[nodename]
	else:
		return "black"