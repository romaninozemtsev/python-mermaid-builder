import unittest

from flowchart import Chart, Node, Link, Subgraph, NodeShape, ChartDir

class TestStringMethods(unittest.TestCase):
    def test_oop_style(self):
        chart = Chart(title='Test', direction=ChartDir.TB)
        node1 = Node(title="this is my node", id='my-node', shape=NodeShape.HEXAGON)
        node2 = Node(title="this is my second node")
        chart.add_node(node1).add_node(node2)
        link = Link(src=node1.get_id(), dest=node2.get_id(), text='this is my link')
        chart.add_link(link)
        subgraph = Subgraph(title='subgraph', direction=ChartDir.LR)
        subgraph.add_node(Node(title='i am a node inside subgraph'))
        
        subgraph2 = Subgraph(title='subgraph2', direction=ChartDir.LR)
        sn1 = Node(title='subnode 2')
        sn2 = Node(title='subnode 3')
        (subgraph2
            .add_node(sn1)
            .add_node(sn2)
            .add_link(Link(src=sn1, dest=sn2, text='link between subnodes')))
        subgraph.add_subgraph(subgraph2)
        chart.add_subgraph(subgraph)
        

        expected = """---
title: Test
---
flowchart TB
  my-node{{this is my node}}
  thisismysecondnode(this is my second node)
  my-node --> |this is my link|thisismysecondnode
  subgraph subgraph
    direction LR
    iamanodeinsidesubgraph(i am a node inside subgraph)
    subgraph subgraph2
      direction LR
      subnode2(subnode 2)
      subnode3(subnode 3)
      subnode2 --> |link between subnodes|subnode3
    end
  end"""
        self.assertEqual(chart.print(''), expected)

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
  server --> database"""
        self.assertEqual(str(chart), expected)

if __name__ == '__main__':
    unittest.main()