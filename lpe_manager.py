"""
AOV Light Groups are stored in an attributed named "aiAov"
Get all lights in the scene
Loop through the lights to generate a set of all the aiAov's (light groups)
Show a list of all light groups
Create an AOV with LPE for each group and desired channel

Class structure:
LPEManager_UI
|-LPEManager
|--AOV
"""
import pymel.core as pm
import re
from aov import AOV


class LPEManager(object):
	"""Class for managing Arnold AOV light groups and light path expressions"""

	def __init__(self):
		super(LPEManager, self).__init__()
		self.aov_list = []

		for group in self.getSceneLightGroups():
			self._initialize_group_list(group)

	def getSceneLights(self):
		return pm.ls(type=["aiAreaLight", "aiSkyDomeLight"])

	def getSceneLightGroups(self):
		groups = set()
		for light in self.getSceneLights():
			groups.add(light.getAttr("aiAov"))
		return groups

	def aov_exists(self, group_name, render_pass):
		for aov in self.aov_list:
			if(aov.light_group == group_name and aov.render_pass == render_pass):
				return True
		return False

	def add_aov(self, group_name, render_pass, make_node=True):
		if(self.aov_exists(group_name, render_pass)):
			return None
		new_aov = AOV(group_name, render_pass, make_node)
		self.aov_list.append(new_aov)
		return new_aov

	def add_aovs(self, group_name, render_pass_list):
		aov_list = []
		for render_pass in render_pass_list:
			aov = self.add_aov(group_name, render_pass)
			aov_list.append(aov)
		return aov_list

	def get_aov(self, search_name):
		for aov in self.aov_list:
			if aov.nice_name() == search_name:
				return aov
		return None

	def get_aov_list(self, group_name=None):
		if group_name is None:
			return self.aov_list

		return_list = []
		for aov in self.aov_list:
			if aov.light_group == group_name:
				return_list.append(aov)
		return return_list

	def delete_aov(self, group_name, render_pass=None):
		to_delete = None

		if render_pass is None:
			for index, aov in enumerate(self.aov_list):
				if(group_name == aov.nice_name()):
					to_delete = aov
					break
		else:
			for index, aov in enumerate(self.aov_list):
				if(aov.light_group == group_name and aov.render_pass == render_pass):
					to_delete = aov
					break
		to_delete.delete_node()
		self.aov_list.remove(to_delete)

	def delete_aovs(self, group_name):
		list_to_delete = self.get_aov_list(group_name)

		for aov in list_to_delete:
			self.delete_aov(aov.light_group, aov.render_pass)

	def _initialize_group_list(self, group_name):
		existing_list = pm.ls(type="aiAOV")
		search_string = "aiAOV_{}_".format(group_name)
		for item in existing_list:
			item_string = str(item)
			if re.search(search_string, item_string):
				split_string = re.split(search_string, item_string)[1]
				self.add_aov(group_name, split_string, False)
