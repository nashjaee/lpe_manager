"""
A full beauty pass can be represented by a few different combinations of AOVs
- RGBA (beauty)
- direct, indirect, emission, background.
- diffuse, specular, coat, transmission, sss, volume, emission, background.
- diffuse_direct, diffuse_indirect, specular_direct, specular_indirect,
	coat, transmission, sss, volume, emission, background.

Each light group should have the option of which combination to use.
"""
from functools import partial
import pymel.core as pm
from lpe_manager import LPEManager

AOV_PASSES = {
	"coarse": ["direct", "indirect", "emission", "background"],
	"medium": ["diffuse", "specular", "coat", "transmission", "sss", "volume", "emission", "background"],
	"fine": ["diffuse_direct", "diffuse_indirect", "specular_direct", "specular_indirect", "coat", "transmission", "sss", "volume", "emission", "background"]
}


class LPEManagerUI(object):
	"""LPEManagerUI: manages UI for interacting with LPEManager"""

	def __init__(self):
		super(LPEManagerUI, self).__init__()
		self._manager = LPEManager()
		self._VERSION = "0.9"
		self._WINNAME = "lpe_win"
		self._TITLE = "LPE Manager v{}".format(self._VERSION)
		self.widgets = {}
		self.build_UI()

	def build_UI(self):
		if(pm.window(self._WINNAME, exists=True)):
			pm.deleteUI(self._WINNAME)

		windowWidth = 300
		columnSpacing = 5
		tripleColumnWidth = windowWidth / 3 - columnSpacing

		self.widgets["mainWindow"] = pm.window(self._WINNAME, t=self._TITLE, rtf=True)
		with self.widgets["mainWindow"]:
			self.widgets["mainLayout"] = pm.columnLayout(w=windowWidth)
			self.widgets["mainLayout"].adjustableColumn()
			with self.widgets["mainLayout"]:
				pm.text("Light Groups")
				self.widgets["lightGroupList"] = pm.textScrollList(w=windowWidth, h=100)
				self.widgets["lightGroupList"].setAllowMultiSelection(False)
				self.widgets["lightGroupList"].selectCommand(self.clicked_light_group)

				pm.text("Light Group AOVs")
				self.widgets["aovList"] = pm.textScrollList(w=windowWidth, h=100)
				self.widgets["aovList"].setAllowMultiSelection(False)
				self.widgets["aovList"].selectCommand(self.clicked_aov)

				self.update_light_groups()

				with pm.rowColumnLayout(numberOfColumns=2, columnWidth=[(1, 120), (2, 160)]):
					pm.text("Light Path Expression: ")
					self.widgets["lpeField"] = pm.textField()
					self.widgets["lpeField"].setEnable(False)

				pm.text("Build AOVs")
				with pm.rowColumnLayout(numberOfColumns=3,
										columnSpacing=[(2, columnSpacing), (3, columnSpacing)],
										columnWidth=[(1, tripleColumnWidth), (2, tripleColumnWidth), (3, tripleColumnWidth)]):
					pm.button("Coarse", c=partial(self.build_aovs, "coarse"))
					pm.button("Medium", c=partial(self.build_aovs, "medium"))
					pm.button("Fine", c=partial(self.build_aovs, "fine"))
				with pm.rowColumnLayout(numberOfColumns=1):
					pm.button("Remove Existing AOVs", c=self.remove_aovs,
								w=windowWidth - columnSpacing)
					pm.button("Remove Selected AOV", c=self.remove_aov,
								w=windowWidth - columnSpacing)

	def add_list_entry(self, label, parent):
		self.widgets[parent].append(label)

	def build_aovs(self, level, *args):
		selection = self.widgets["lightGroupList"].getSelectItem()
		if not selection:
			pm.warning("Please make a selection before building AOVs")
			return

		group = selection[0]
		self._manager.add_aovs(group, AOV_PASSES[level])
		self.update_aovs(group)

	def clear_lpe(self):
		self.widgets["lpeField"].setText("")

	def clear_text_list(self, list_name):
		self.widgets[list_name].removeAll()

	def clicked_aov(self):
		aov_name = self.widgets["aovList"].getSelectItem()[0]
		aov = self._manager.get_aov(aov_name)
		self.widgets["lpeField"].setText(aov.lpe)
		pm.select(aov._aov_node)

	def clicked_light_group(self):
		item = self.widgets["lightGroupList"].getSelectItem()[0]
		self.update_aovs(item)

	def remove_aov(self, *args):
		selected_group = self.widgets["lightGroupList"].getSelectItem()[0]
		selected_aov = self.widgets["aovList"].getSelectItem()[0]

		self._manager.delete_aov(selected_aov)
		self.update_aovs(selected_group)

	def remove_aovs(self, *args):
		selection = self.widgets["lightGroupList"].getSelectItem()
		if not selection:
			pm.warning("Please make a selection before deleting AOVs")
			return

		group = selection[0]
		self._manager.delete_aovs(group)
		self.update_aovs(group)

	def update_aovs(self, group):
		self.clear_text_list("aovList")
		self.clear_lpe()

		group = self.widgets["lightGroupList"].getSelectItem()[0]
		aov_list = self._manager.get_aov_list(group)

		self.widgets["aovList"].setEnable(True)
		if not aov_list:
			self.widgets["aovList"].append("No AOVs for this group")
			self.widgets["aovList"].setEnable(False)

		for aov in aov_list:
			self.add_list_entry(aov.nice_name(), "aovList")

	def update_light_groups(self):
		self.clear_text_list("lightGroupList")
		self.clear_text_list("aovList")

		light_groups = self._manager.getSceneLightGroups()
		for group in light_groups:
			self.add_list_entry(group, "lightGroupList")
