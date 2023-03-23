
from enum import auto, Enum
from dataclasses import dataclass, field

class ChartDir(Enum):
    LR = auto()
    TD = auto()
    TB = auto()
    RL = auto()
    BT = auto()


class NodeShape(Enum):
    RECT_ROUND = "(VAL)"
    STADIUM = "([VAL])"
    SUBROUTINE = "[[VAL]]"
    CYLINDER = "[(VAL]]"
    CIRCLE = "((VAL))"
    ASSYMETRIC = ">VAL]"
    RHOMBUS = "{VAL}"
    HEXAGON = "{{VAL}}"

    def wrap(self, text: str) -> str:
        return self.value.replace('VAL', text)


def _short_hash(text: str) -> int:
    return abs(hash(text)) % (10 ** 8)

@dataclass
class Node:
    title: str = ''
    shape: NodeShape = NodeShape.RECT_ROUND
    id: str = ''

    def _ensure_id(self):
        if self.id == '' and self.title != '':
            self.id = str(_short_hash(self.title))

    def get_id(self):
        self._ensure_id()
        return self.id

    def __str__(self) -> str:
        self._ensure_id()
        print(self.id)
        print(self.shape)
        print(self.title)
        return f'{self.id}{self.shape.wrap(self.title)}'


class LinkType(Enum):
    ARROW = '-->'
    OPEN = '---'
    INVISIBLE = '~~~'


@dataclass
class Link:
    src: str
    dest: str
    text: str = None
    type: LinkType = LinkType.ARROW
    
    def __str__(self) -> str:
        link_text = ''
        if self.text:
            link_text = f'|{self.text}|'

        return f'{self.src} {self.type.value} {link_text}{self.dest}'



@dataclass
class Chart:
    title: str
    direction: ChartDir = ChartDir.TD
    nodes: list[Node] = field(default_factory=list)
 
    links: list[Link] = field(default_factory=list)
    subgraphs: list = field(default_factory=list)

    def __str__(self) -> str:
        return self.print('')

    def print(self, indent) -> str:
        current_indent = indent
        result = []
        if self.title:
            result.append(current_indent + '---')
            result.append(current_indent + f'title: {self.title}')
            result.append(current_indent + '---')
        result.append(current_indent + f'flowchart {self.direction.name}')
        current_indent += '  '
        for node in self.nodes:
            result.append(current_indent + str(node))
        for link in self.links:
            result.append(current_indent + str(link))
        for subgraph in self.subgraphs:
            result.append(subgraph.print(current_indent))
        return "\n".join(result)

    def add_node(self, node: Node):
        self.nodes.append(node)

    def add_link(self, link: Link):
        self.links.append(link)

    def add_subgraph(self, subgraph):
        self.subgraphs.append(subgraph)


class Subgraph(Chart):
    def __str__(self) -> str:
        return self.print('')

    def print(self, indent):
        current_indent = indent
        result = []
        result.append(current_indent + 'subgraph ' + self.title)
        # TODO: implement ID
        current_indent += '  '
        print(f'current_indent = "{current_indent}"')
        result.append(current_indent + f'direction {self.direction.name}')
        for node in self.nodes:
            result.append(current_indent + str(node))
        for link in self.links:
            result.append(current_indent + str(link))
        for subgraph in self.subgraphs:
            result.append(subgraph.print(current_indent))
        #current_indent -= '  '
        result.append(indent + 'end')
        return "\n".join(result)



if __name__ == '__main__':
    chart = Chart(title='Test', direction=ChartDir.TB)
    node1 = Node(title="this is my node", shape=NodeShape.HEXAGON)
    chart.add_node(node1)
    node2 = Node(title="this is my second node")
    chart.add_node(node2)
    link = Link(src=node1.get_id(), dest=node2.get_id(), text='this is my link')
    chart.add_link(link)
    subgraph = Subgraph(title='subgraph', direction=ChartDir.LR)
    subgraph.add_node(Node(title='i am a node inside subgraph'))
    
    subgraph2 = Subgraph(title='subgraph2', direction=ChartDir.LR)
    subgraph2.add_node(Node(title='subnode 2'))

    subgraph.add_subgraph(subgraph2)

    chart.add_subgraph(subgraph)
    print(chart)
