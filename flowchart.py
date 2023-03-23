
from enum import auto, Enum
from dataclasses import dataclass, field
import re

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

class LinkType(Enum):
    ARROW = '-->'
    OPEN = '---'
    INVISIBLE = '~~~'

@dataclass
class Node:
    title: str = ''
    shape: NodeShape = NodeShape.RECT_ROUND
    id: str = ''

    def _ensure_id(self):
        if self.id == '' and self.title != '':
            safe_title = re.sub(r'[^a-zA-Z0-9]+', '', self.title)
            self.id = safe_title

    def get_id(self):
        self._ensure_id()
        return self.id

    def __str__(self) -> str:
        self._ensure_id()
        return f'{self.id}{self.shape.wrap(self.title)}'

    def link_to(self, dest_id: str, text: str = None, type: LinkType = LinkType.ARROW):
        # TODO: see how can we implement it.
        pass



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

    def print_body(self, indent) -> str:
        result = []
        for node in self.nodes:
            result.append(indent + str(node))
        for link in self.links:
            result.append(indent + str(link))
        for subgraph in self.subgraphs:
            result.append(subgraph.print(indent))
        return "\n".join(result)

    def print(self, indent) -> str:
        current_indent = indent
        result = []
        if self.title:
            result.append(current_indent + '---')
            result.append(current_indent + f'title: {self.title}')
            result.append(current_indent + '---')
        result.append(current_indent + f'flowchart {self.direction.name}')
        
        result.append(self.print_body(current_indent + '  '))
        return "\n".join(result)

    def add_node(self, node: Node):
        self.nodes.append(node)
        return self

    def add_node_str(self, node_id: str):
        self.add_node(Node(id=node_id, title=node_id))

    def add_nodes(self, nodes: list[Node]):
        self.nodes.extend(nodes)
        return self

    def add_link(self, link: Link):
        self.links.append(link)
        return self

    def add_link_str(self, src: str, dest: str):
        self.add_link(Link(src=src, dest=dest))

    def add_subgraph(self, subgraph):
        self.subgraphs.append(subgraph)
        return self


class Subgraph(Chart):
    def __str__(self) -> str:
        return self.print('')
    

    def print(self, indent):
        current_indent = indent
        result = []
        result.append(current_indent + 'subgraph ' + self.title)
        current_indent += '  '
        result.append(current_indent + f'direction {self.direction.name}')
        result.append(self.print_body(current_indent))
        result.append(indent + 'end')
        return "\n".join(result)
