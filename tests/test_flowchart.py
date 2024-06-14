import unittest

from mermaid_builder.flowchart import Chart, ClassDef, LinkStyle, Node, Link, NodeStyle, Subgraph, NodeShape, ChartDir
 
class TestStringMethods(unittest.TestCase):
    maxDiff = None
    def test_oop_style(self):
        chart = Chart(title='Test', direction=ChartDir.TB)
        node1 = Node(title="this is my node", id='my-node', shape=NodeShape.HEXAGON)
        node2 = Node(title="this is my second node")
        chart.add_node(node1).add_node(node2)
        link = Link(src=node1.get_id(), dest=node2.get_id(), text='this is my link')
        link.style = LinkStyle(color='red', stroke_width='2px')
        chart.add_link(link)
        subgraph = Subgraph(title='My Subgraph', direction=ChartDir.LR)
        subgraph.add_node(Node(title='i am a node inside subgraph'))
        
        subgraph2 = Subgraph(title='subgraph2', direction=ChartDir.LR)
        sn1 = Node(title='subnode 2', class_name='class1')
        sn2 = Node(title='subnode 3')
        (subgraph2
            .add_node(sn1)
            .add_node(sn2)
            .add_link(Link(src=sn1, dest=sn2, text='link between subnodes')))
        subgraph.add_subgraph(subgraph2)
        chart.add_subgraph(subgraph)
        chart.add_class_def(ClassDef(["class1"], "fill:#f9f,stroke:#333,stroke-width:2px;"))
        chart.add_class_def(ClassDef(["class2"], NodeStyle(fill='#300', stroke='#666', stroke_width='5px', color='red', stroke_dasharray=[5, 5])))
        chart.attach_class(sn2, 'class1')
        chart.attach_class(['my-node'], 'class1')
        chart.attach_class(node2, "class2")
        chart.add_link_between(node1, subgraph2.get_id())
        chart.add_link_style(2, LinkStyle(color='green', stroke_width='2px'))

        expected = """---
title: Test
---
flowchart TB
  my-node{{this is my node}}
  thisismysecondnode(this is my second node)
  my-node --> |this is my link|thisismysecondnode
  linkStyle 0 stroke-width:2px,color:red;
  my-node --> subgraph2
  subgraph MySubgraph [My Subgraph]
    direction LR
    iamanodeinsidesubgraph(i am a node inside subgraph)
    subgraph subgraph2 [subgraph2]
      direction LR
      subnode2(subnode 2):::class1
      subnode3(subnode 3)
      subnode2 --> |link between subnodes|subnode3
    end
  end
  classDef class1 fill:#f9f,stroke:#333,stroke-width:2px;
  classDef class2 fill:#300,stroke:#666,stroke-width:5px,color:red,stroke-dasharray:5 5
  class subnode3 class1;
  class my-node class1;
  class thisismysecondnode class2;
  linkStyle 2 stroke-width:2px,color:green;
"""
        self.assertEqual(expected, str(chart))

    def test_quick_style(self):
        chart = (Chart(title='test1')
          .add_node('user')
          .add_node('client')
          .add_node('server')
          .add_node('database')
          .add_link_between('user', 'client')
          .add_link_between('client', 'server')
          .add_link_between('server', 'database'))
        expected = """---
title: test1
---
flowchart TD
  user(user)
  client(client)
  server(server)
  database(database)
  user --> client
  client --> server
  server --> database
"""
        self.assertEqual(str(chart), expected)

if __name__ == '__main__':
    unittest.main()