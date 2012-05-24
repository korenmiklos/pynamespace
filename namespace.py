'''
Create a namespace of nodes. Examples:

	root = Node()

Nodes can have be assigned values of any python type.

	root = 'Root of namespace'

Subnodes are declared implicitly.

	root.complex = 'Data from Complex'
	root.complex.rovat_0.ceg_id = [1,2,3]
	root.complex.rovat_1.ceg_id = [1,2,3]
	root.complex.rovat_1.name = ['Firm A', 'Firm B', 'Firm C']
	root.output.frame = {}

Nodes are iterable. To iterate over subnodes,

	for rovat in root.complex:
		print rovat.ceg_id

	for field in root.complex.rovat_1:
		print field

The length of a node is the number of its children, which can also be used as Truthism:

	if root:
		print len(root)

To access the data stored in the node, use get_data():

	ceg_id_list = root.complex.rovat_0.ceg_id.get_data()

There is a dictionary representation of the whole tree:

	print root.get_tree()

	{'complex': {'rovat_0': {'ceg_id': None
							},
				 'rovat_1': {'ceg_id': None,
							 'name': None
							},
				},
	 'output':	{'frame': None}
	}
'''

class Node(object):
	def __init__(self,value=None):
		'''
		Store value directly.
		'''
		object.__setattr__(self, '__data__', value)

	def get_data(self):
		return self.__data__

	def set_data(self,value):
		'''
		Store value directly.
		'''
		object.__setattr__(self, '__data__', value)

	def __unicode__(self):
		return unicode(self.get_data())

	def __str__(self):
		return self.__unicode__()

	def __setattr__(self,name,value):
		'''
		Store value in a node, not directly.
		'''
		node = Node(value)
		object.__setattr__(self, name, node)

	def __getattr__(self,name):
		'''
		If attribute is not found, create one.
		'''
		node = Node()
		object.__setattr__(self, name, node)
		return node 

	def __iter__(self):
		'''
		To ensure that nodes are iterable. 
		'''
		# manually copy subnodes to list
		lst = []
		for name, subnode in self.__dict__.items():
			if not name == '__data__':
				lst.append(subnode) 
		return iter(lst)

	def __len__(self):
		'''
		Return number of child nodes.
		'''
		return len(self.__dict__)-1

	def children_as_dictionary(self):
	# manually copy subnodes to list
		dct = {}
		for name, subnode in self.__dict__.items():
			if not name == '__data__':
				dct[name] =  subnode 
		return dct 

	def get_tree(self):
		'''
		Return a tree of children
		'''
		if not self:
			# no children
			return None
		else:
			dct = {}
			for name, value in self.children_as_dictionary().items():
				dct[name] = value.get_tree()
			return dct
