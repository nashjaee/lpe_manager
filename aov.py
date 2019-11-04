import mtoa as arnold
import pymel.core as pm

# TODO: add all scatter events
SCATTER_EVENTS = {
	"background": "B",
	"beauty": ".*",
	"coat": "<RS'coat'>.*",
	"diffuse": "<RD>.*",
	"diffuse_direct": "<RD>",
	"diffuse_indirect": "<RD>[DSVOB].*",
	"direct": "[DSV]",
	"emission": "[LO]",
	"indirect": "[DSV][DSVOB].*",
	"transmission": "<TS>.*",
	"specular": "<RS>.*",
	"specular_direct": "<RS[^'coat']>",
	"specular_indirect": "<RS[^'coat']>[DSVOB].*",
	"sss": "<TD>.*",
	"volume": "V.*"
}


class AOV(object):
	"""Arnold AOV objects"""

	def __init__(self, light_group, render_pass, make_node=True):
		super(AOV, self).__init__()
		self.light_group = light_group
		self.render_pass = render_pass
		self.lpe = AOV.format_lpe(self.light_group, self.render_pass)
		self._interface = arnold.aovs.AOVInterface()
		self._aov_node = None
		if(make_node):
			self.make_aov_node()
		else:
			self._find_node()

	@staticmethod
	def format_lpe(group, renderPass):
		if renderPass not in SCATTER_EVENTS.keys():
			renderPass = "beauty"
		events = SCATTER_EVENTS[renderPass.lower()]
		return "C{}<L.'{}'>".format(events, group)

	def delete_node(self):
		if(self._aov_node):
			pm.delete(self._aov_node)

	def make_aov_node(self):
		aov_name = self.nice_name()
		self._aov_node = pm.PyNode(self._interface.addAOV(aov_name).node)
		self._aov_node.lightPathExpression.set(self.lpe)

	def nice_name(self):
		return "{}_{}".format(self.light_group, self.render_pass)

	def _find_node(self):
		search_name = "aiAOV_{}_{}".format(self.light_group, self.render_pass)
		search_results = pm.ls(search_name, type="aiAOV")
		if(search_results):
			self._aov_node = search_results[0]
			return True
		return False
