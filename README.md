# python-mermaid-builder


### WIP

Next tasks:
1. styling for flowchart (adding classes and styles)
2. "clone with prefix" (creates a clone of a node or a subgraph but adds a prefix to ID, so the don't conflict)
3. class diagrams
4. package for distribution



## Examples:

### Flow chart

#### untyped version
```python
chart = (Chart(title='test1')
    .add_node('user')
    .add_node('client')
    .add_node('server')
    .add_node('database')
    .add_link_between('user', 'client')
    .add_link_between('client', 'server')
    .add_link_between('server', 'database'))
```

#### OOP (more complicated version)
```python
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
```


## Sequence diagram
```python
        diagram = SequenceDiagram()
        client = Participant(id='C', label='Client')
        server = Participant(id='S', label='Server')
        database = Participant(id='D', label='Database')
        (diagram
          .add_participant(client)
          .add_participant(server)
          .add_participant(database)
          .add_message(Message(src=client, dest=server, text='HTTP Request', activation_mode=ActivationMode.ACTIVATE))
          .add_message(Message(src=server, dest=database, text='SQL Query'))
          .add_message(Message(src=database, dest=server, text='Result', arrow=ArrowType.DOTTED_LINE_NO_ARROW))        
          .add_message(Message(src=server, dest=client, text='HTTP Response', activation_mode=ActivationMode.DEACTIVATE))
          .add_note(Note(participants=[client], text='This is a note', position=NotePosition.LEFT_OF)))
```



see `flowchart_test.py` and `sequence_diagram_test.py ` for examples.


## Run tests
```bash
python3 flowchart_test.py
python3 sequence_diagram_test.py 
```

to preview - paste results to 
https://www.devtoolsdaily.com/diagrams/mermaidjs/playground/


## Develop
this library doesn't have any dependencies, no need to do virtual env etc.
just use python3.5+ , as it's using `types` and `Union`





