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
        subgraph2.add_node(Node(title='subnode 2'))

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
    end
  end"""
        self.assertEqual(chart.print(''), expected)

    def test_quick_style(self):
        chart = Chart(title='test1')
        chart.add_node_str('user')
        chart.add_node_str('client')
        chart.add_node_str('server')
        chart.add_node_str('database')

        chart.add_link_str('user', 'client')
        chart.add_link_str('client', 'server')
        chart.add_link_str('server', 'database')
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
        self.assertEqual(chart.print(''), expected)

if __name__ == '__main__':
    unittest.main()