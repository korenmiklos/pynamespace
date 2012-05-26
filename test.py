# -*- coding: utf-8 -*-
import unittest as ut 
import namespace as np

class TestInterface(ut.TestCase):
	def test_node_returns_string(self):
		node = np.Node(5)
		self.assertEqual(str(node),str(5))

	def test_get_data_and_string(self):
		node = np.Node(5)
		self.assertEqual(node.get_data(),int(unicode(node)))

class TestExceptions(ut.TestCase):
	def test_parent_accepts_no_data(self):
		node = np.Node()
		node.a = 1
		node.b = 2
		node.c = 3
		self.assertRaises(TypeError,node.set_data,5)

	def test_parent_returns_no_data(self):
		node = np.Node()
		node.a = 1
		node.b = 2
		node.c = 3
		self.assertRaises(LookupError,node.get_data)

	def test_nodes_with_data_cannot_have_children(self):
		node = np.Node(5)
		def callable():
			node.a = 1
		self.assertRaises(TypeError,callable)

	def test_nodes_with_data_cannot_have_grandchildren(self):
		node = np.Node(5)
		def callable():
			node.a.b = 1
		self.assertRaises(TypeError,callable)

	def test_cannot_call_node_reserved_word(self):
		RESERVED_WORDS = ['__init__','__data__',
							'get_tree','get_data','set_data',
							'children_as_dictionary']
		node = np.Node()
		def callable(word):
			node.__setattr__(word,1)
		for word in RESERVED_WORDS:
			self.assertRaises(NameError,callable,word)

class TestIteration(ut.TestCase):
	def test_node_is_iterable(self):
		node = np.Node()
		try:
			for point in node:
				pass
		except TypeError:
			self.fail('Node is not iterable.')

	def test_iterates_over_nodes(self):
		node = np.Node()
		node.a = 1
		node.b = 2
		node.c = 3
		for subnode in node:
			self.assertIsInstance(subnode,np.Node)

	def test_node_returns_all_attributes(self):
		node = np.Node()
		node.a = 1
		node.b = 2
		node.c = 3
		halmaz = set([])
		for point in node: 
			halmaz.add(point)
		self.assertSetEqual(set([node.a,node.b,node.c]),halmaz)

	def test_iterable_does_not_return_self(self):
		node = np.Node()
		node.a = 1
		node.b = 2
		node.c = 3
		halmaz = set([])
		for point in node: 
			halmaz.add(point)
		self.assertNotIn(node,halmaz)

	def test_number_of_children(self):
		node = np.Node()
		node.a = 1
		node.b = 2
		node.c = 3
		self.assertEqual(len(node),3)

	def test_no_child_returns(self):
		node = np.Node(5)
		for child in node:
			self.fail('this node should not have a child')

	def test_zero_child(self):
		node = np.Node(5)
		self.assertEqual(len(node),0)

	def test_children_as_dictionary(self):
		node = np.Node()
		node.a = 1
		node.b = 2
		node.c = 3
		self.assertDictEqual(node.children_as_dictionary(),{'a': node.a, 'b': node.b, 'c': node.c})

class TestTree(ut.TestCase):
	def test_children_belong_to_same_parent(self):
		root = np.Node()
		root.parent1.child1 = 1
		root.parent1.child2 = 2
		root.parent2 = 3

		children = [root.parent1.child1, root.parent1.child2]
		for child in root.parent:
			self.assertIn(child,children)

	def test_tree_can_be_walked(self):
		root = np.Node()
		root.parent1.child1 = 1
		root.parent1.child2 = 2
		root.parent2 = 3

		def walk(parent):
			children = []
			if parent:
				for child in parent:
					children.extend(walk(child))
				return children
			else:
				return [str(parent)]

		walk(root) 

	def test_get_tree(self):
		root = np.Node()
		root.parent1.child1 = 1
		root.parent1.child2 = 2
		root.parent2 = 3
		self.assertDictEqual(root.get_tree(),{'parent1': {'child1': 1, 'child2': 2}, 'parent2': 3})
		import yaml
		print yaml.dump(root.get_tree(),default_flow_style=False)

class TestAssignment(ut.TestCase):
	def test_set_data(self):
		node = np.Node('test')
		node.set_data('other data')
		self.assertEqual(node.get_data(),'other data')

	def test_new_attribute(self):
		node = np.Node()
		node.a = 5

	def test_attribute_is_node(self):
		node = np.Node()
		node.a = 5
		self.assertIsInstance(node.a,np.Node)

	def test_multiple_attributes(self):
		node = np.Node()
		try:
			node.a.b = 5
		except:
			self.fail('node.a.b cannot be assigned')

	def test_numerical_value_returned(self):
		node = np.Node(5)
		self.assertEqual(node.get_data(),5)

	def test_string_value_returned(self):
		node = np.Node(u'árvíztűrő')
		self.assertEqual(node.get_data(),u'árvíztűrő')

	def test_attribute_value_returned(self):
		node = np.Node()
		node.a = 5
		self.assertEqual(node.a.get_data(),5)

if __name__=='__main__':
	ut.main()
