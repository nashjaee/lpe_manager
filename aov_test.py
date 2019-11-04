import unittest
import pymel.core as pm
from aov import AOV
from aov import arnold


class AOVTest(unittest.TestCase):
	"""Test class for AOV"""

	def setUp(self):
		self.clean_environment()
		self.dummy_aov = AOV("test_name", "test_pass")

	def clean_environment(self):
		# Open a new file to clear out any AOVs created by the tests
		pm.newFile(force=True)
		# defaultArnoldDriver (among other objects) doesn't load until needed.
		# The following 2 lines will force them to load to avoid runtime errors.
		from mtoa.core import createOptions
		createOptions()

	def test_saves_a_lightgroup_name(self):
		self.assertEqual(self.dummy_aov.light_group, "test_name")

	def test_saves_a_renderpass_name(self):
		self.assertEqual(self.dummy_aov.render_pass, "test_pass")

	def test_saves_an_lpe(self):
		self.assertEqual(type(self.dummy_aov.lpe), str)

	def test_creates_an_aov_node(self):
		AOV("test_aov", "test_pass")
		aov_list = pm.ls(type="aiAOV")
		self.assertEqual(len(aov_list), 2)  # 2, because one is created in setUp()
		self.assertTrue("aiAOV_test_aov_test_pass" in aov_list)

	def test_optionally_does_not_create_node(self):
		AOV("test_aov", "test_lpe", False)
		aov_list = pm.ls(type="aiAOV")
		self.assertEqual(len(aov_list), 1)

	def test_formats_background_lpe_expression(self):
		expression = AOV.format_lpe("group_name", "background")
		self.assertEqual(expression, "CB<L.'group_name'>")

	def test_formats_beauty_lpe_expression(self):
		expression = AOV.format_lpe("group_name", "beauty")
		self.assertEqual(expression, "C.*<L.'group_name'>")

	def test_formats_coat_lpe_expression(self):
		expression = AOV.format_lpe("group_name", "coat")
		self.assertEqual(expression, "C<RS'coat'>.*<L.'group_name'>")

	def test_formats_diffuse_lpe_expression(self):
		expression = AOV.format_lpe("group_name", "diffuse")
		self.assertEqual(expression, "C<RD>.*<L.'group_name'>")

	def test_formats_diffuse_direct_lpe_expression(self):
		expression = AOV.format_lpe("group_name", "diffuse_direct")
		self.assertEqual(expression, "C<RD><L.'group_name'>")

	def test_formats_diffuse_indirect_lpe_expression(self):
		expression = AOV.format_lpe("group_name", "diffuse_indirect")
		self.assertEqual(expression, "C<RD>[DSVOB].*<L.'group_name'>")

	def test_formats_direct_lpe_expression(self):
		expression = AOV.format_lpe("group_name", "direct")
		self.assertEqual(expression, "C[DSV]<L.'group_name'>")

	def test_formats_emission_lpe_expression(self):
		expression = AOV.format_lpe("group_name", "emission")
		self.assertEqual(expression, "C[LO]<L.'group_name'>")

	def test_formats_indirect_lpe_expression(self):
		expression = AOV.format_lpe("group_name", "indirect")
		self.assertEqual(expression, "C[DSV][DSVOB].*<L.'group_name'>")

	def test_formats_specular_lpe_expression(self):
		expression = AOV.format_lpe("group_name", "specular")
		self.assertEqual(expression, "C<RS>.*<L.'group_name'>")

	def test_formats_specular_direct_lpe_expression(self):
		expression = AOV.format_lpe("group_name", "specular_direct")
		self.assertEqual(expression, "C<RS[^'coat']><L.'group_name'>")

	def test_formats_specular_indirect_lpe_expression(self):
		expression = AOV.format_lpe("group_name", "specular_indirect")
		self.assertEqual(expression, "C<RS[^'coat']>[DSVOB].*<L.'group_name'>")

	def test_formats_sss_lpe_expression(self):
		expression = AOV.format_lpe("group_name", "sss")
		self.assertEqual(expression, "C<TD>.*<L.'group_name'>")

	def test_formats_transmission_lpe_expression(self):
		expression = AOV.format_lpe("group_name", "transmission")
		self.assertEqual(expression, "C<TS>.*<L.'group_name'>")

	def test_formats_volume_lpe_expression(self):
		expression = AOV.format_lpe("group_name", "volume")
		self.assertEqual(expression, "CV.*<L.'group_name'>")

	def test_format_defaults_to_beauty(self):
		expression = AOV.format_lpe("group_name", "fake pass")
		self.assertEqual(expression, "C.*<L.'group_name'>")

	def test_saves_lpe_to_maya_node(self):
		test_aov = pm.ls(type="aiAOV")[0]
		expectedExpression = "C.*<L.'test_name'>"

		self.assertEqual(test_aov.lightPathExpression.get(), expectedExpression)

	def test_deletes_node_when_explicitly_requested(self):
		new_aov = AOV("group_name", "direct")
		aov_list = pm.ls(type="aiAOV")
		self.assertEqual(len(aov_list), 2)
		new_aov.delete_node()
		aov_list = pm.ls(type="aiAOV")
		self.assertEqual(len(aov_list), 1)

	def test_does_not_delete_node_on_destruction(self):
		new_aov = AOV("group_name", "direct")
		aov_list = pm.ls(type="aiAOV")
		self.assertEqual(len(aov_list), 2)
		del(new_aov)
		aov_list = pm.ls(type="aiAOV")
		self.assertEqual(len(aov_list), 2)

	def test_finds_existing_aov_node(self):
		# Make an AOV directly through arnold, and verify it exists
		aov_name = "test_group_test_pass"
		arnold.aovs.AOVInterface().addAOV(aov_name)
		aov_list = pm.ls("aiAOV_" + aov_name)
		self.assertEqual(len(aov_list), 1)

		# Ensure that the AOV instance found the node
		new_aov = AOV("test_group", "test_pass", False)
		self.assertTrue(new_aov._aov_node.type() == "aiAOV")

	def test_returns_nice_name(self):
		expected_return = "test_name_test_pass"
		self.assertEqual(self.dummy_aov.nice_name(), expected_return)
