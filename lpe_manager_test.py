import os
import unittest
import pymel.core as pm
from lpe_manager import LPEManager
from aov import AOV
from aov import arnold

# Test scene has 2 lights:
# warmLightShape
# coldLightShape
TEST_SCENE_PATH = "General\\scripts\\lpe_manager\\test_scene.mb"


def openMayaFile(sceneName):
	pm.system.openFile(sceneName, force=True)


class LPEManagerTest(unittest.TestCase):
	"""Test class for LPEManager"""

	def setUp(self):
		self.manager = LPEManager()
		dirPath = os.getcwd()
		filePath = os.path.join(dirPath, TEST_SCENE_PATH)
		openMayaFile(filePath)

	def test_gets_lights_in_scene(self):
		lights = self.manager.getSceneLights()
		self.assertEqual(len(lights), 2)
		self.assertTrue("warmLightShape" in lights)
		self.assertTrue("coldLightShape" in lights)

	def test_get_light_groups(self):
		groups = self.manager.getSceneLightGroups()
		self.assertEqual(len(groups), 2)
		self.assertTrue("warm" in groups)
		self.assertTrue("cold" in groups)

	def test_adds_an_AOV(self):
		new_aov = self.manager.add_aov("group_name", "diffuse")
		self.assertTrue(type(new_aov) is AOV)

	def test_adds_list_of_AOVs(self):
		name = "group_name"
		render_pass_list = ["beauty", "direct", "indirect"]
		self.manager.add_aovs(name, render_pass_list)
		self.assertEqual(len(self.manager.get_aov_list()), 3)

	def test_add_list_returns_array(self):
		name = "group_name"
		render_pass_list = ["beauty", "direct", "indirect"]
		return_value = self.manager.add_aovs(name, render_pass_list)
		self.assertEqual(len(return_value), 3)

	def test_maintains_list_of_AOVs(self):
		self.manager.add_aov("group_1", "diffuse")
		self.manager.add_aov("group_2", "diffuse")
		self.manager.add_aov("group_3", "diffuse")
		aov_list = self.manager.get_aov_list()

		self.assertEqual(len(aov_list), 3)
		self.assertTrue(type(aov_list[0]), AOV)

	def test_returns_list_by_light_group(self):
		self.manager.add_aov("group_1", "beauty")
		self.manager.add_aov("group_1", "direct")
		self.manager.add_aov("group_1", "indirect")
		self.manager.add_aov("group_2", "direct")
		self.manager.add_aov("group_3", "diffuse")

		aov_list = self.manager.get_aov_list("group_1")
		self.assertEqual(len(aov_list), 3)
		aov_list = self.manager.get_aov_list("group_2")
		self.assertEqual(len(aov_list), 1)

	def test_returns_specific_aov(self):
		group_name = "test_name"
		pass_name = "test_pass"
		search_name = "{}_{}".format(group_name, pass_name)
		self.manager.add_aov(group_name, pass_name)
		aov_object = self.manager.get_aov(search_name)

		self.assertEqual(type(aov_object), AOV)
		self.assertEqual(aov_object.nice_name(), search_name)

	def test_delete_aov(self):
		group_name = "group_1"
		render_pass = "beauty"
		self.manager.add_aov(group_name, render_pass)
		self.assertEqual(len(self.manager.get_aov_list()), 1)
		self.manager.delete_aov(group_name, render_pass)

		test_list = self.manager.get_aov_list()
		self.assertEqual(len(test_list), 0)

		# check the actual Maya scene file
		aov_list = pm.ls(type="aiAOV")
		self.assertEqual(len(aov_list), 0)

	def test_delete_aovs_of_group(self):
		group_name = "group_1"
		render_pass_list = ["beauty", "diffuse", "indirect"]
		self.manager.add_aovs(group_name, render_pass_list)
		self.assertEqual(len(self.manager.get_aov_list()), 3)

		self.manager.delete_aovs(group_name)

		test_list = self.manager.get_aov_list()
		self.assertEqual(len(test_list), 0)

	def test_deletes_aov_from_nice_name(self):
		group_name = "group_1"
		render_pass = "beauty"
		delete_name = "{}_{}".format(group_name, render_pass)
		self.manager.add_aov(group_name, render_pass)
		self.assertEqual(len(self.manager.get_aov_list()), 1)

		self.manager.delete_aov(delete_name)

		test_list = self.manager.get_aov_list()
		self.assertEqual(len(test_list), 0)

	def test_dont_create_duplicate_aov(self):
		group_name = "group_1"
		render_pass = "beauty"
		self.manager.add_aov(group_name, render_pass)
		self.manager.add_aov(group_name, render_pass)

		aov_list = self.manager.get_aov_list()
		self.assertEqual(len(aov_list), 1)

	def test_gets_existing_aov_nodes(self):
		aov_name = "test_group_test_pass"
		arnold.aovs.AOVInterface().addAOV(aov_name)
		self.manager._initialize_group_list("test_group")
		self.assertEqual(len(self.manager.get_aov_list()), 1)
