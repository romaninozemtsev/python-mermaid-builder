
from enum import auto, Enum
from dataclasses import dataclass, field
import re
from typing import Union
import uuid

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
class NodeStyle:
    fill: str = None
    stroke: str = None
    stroke_width: str = None
    color: str = None
    stroke_dasharray: Union[str, list[int]] = None

    def __str__(self) -> str:
        result = []
        if self.fill:
            result.append(f'fill:{self.fill}')
        if self.stroke:
            result.append(f'stroke:{self.stroke}')
        if self.stroke_width:
            result.append(f'stroke-width:{self.stroke_width}')
        if self.color:
            result.append(f'color:{self.color}')
        if self.stroke_dasharray:
            if isinstance(self.stroke_dasharray, list):
                dasharray = " ".join(str(i) for i in self.stroke_dasharray)
            else:
                dasharray = self.stroke_dasharray
            result.append(f'stroke-dasharray:{dasharray}')
        return ",".join(result)

@dataclass
class Node:
    title: str = ''
    shape: NodeShape = NodeShape.RECT_ROUND
    id: str = ''
    class_name: str = None


    def _ensure_id(self):
        if self.id == '' and self.title != '':
            safe_title = re.sub(r'[^a-zA-Z0-9\-_!#\$]+', '', self.title)
            self.id = safe_title

    def get_id(self):
        self._ensure_id()
        return self.id

    def __str__(self) -> str:
        self._ensure_id()
        class_name_suffix = ':::' + self.class_name if self.class_name else '' 
        return f'{self.id}{self.shape.wrap(self.title)}{class_name_suffix}'

@dataclass
class LinkStyle:
    stroke: str = None
    stroke_width: str = None
    color: str = None

    def __str__(self) -> str:
        result = []
        if self.stroke:
            result.append(f'stroke:{self.stroke}')
        if self.stroke_width:
            result.append(f'stroke-width:{self.stroke_width}')
        if self.color:
            result.append(f'color:{self.color}')
        return ",".join(result)

@dataclass
class Link:
    src: Union[str, Node]
    dest: Union[str, Node]
    text: str = None
    type: LinkType = LinkType.ARROW
    style: LinkStyle = None
    
    def __str__(self) -> str:
        src_id = self.src
        if isinstance(self.src, Node):
            src_id = self.src.get_id()
        dest_id = self.dest
        if isinstance(self.dest, Node):
            dest_id = self.dest.get_id()
        link_text = ''
        if self.text:
            link_text = f'|{self.text}|'

        return f'{src_id} {self.type.value} {link_text}{dest_id}'

    def print_style(self, link_count: int) -> str:
        if self.style:
            return f"linkStyle {link_count} {self.style};"
        return ''


@dataclass
class ClassDef:
    class_names: Union[list[str], str]
    style: Union[str, NodeStyle]

    def __str__(self) -> str:
        cls_names = self.class_names
        if isinstance(cls_names, str):
            cls_names = [cls_names]
        return f'classDef {",".join(cls_names)} {self.style}'

@dataclass
class ClassAttachment:
    nodes: Union[list[Node], list[str], str, Node]
    class_name: str

    def __str__(self) -> str:
        nodes = self.nodes
        if isinstance(nodes, str):
            nodes = [nodes]
        elif isinstance(nodes, Node):
            nodes = [nodes.get_id()]
        elif isinstance(nodes[0], Node):
            nodes = [node.get_id() for node in nodes]
        return f'class {",".join(nodes)} {self.class_name};'


@dataclass
class Chart:
    title: str = None
    direction: ChartDir = ChartDir.TD
    nodes: list[Node] = field(default_factory=list)
 
    links: list[Link] = field(default_factory=list)
    subgraphs: list = field(default_factory=list)

    class_defs: list = field(default_factory=list)
    class_attachments: list = field(default_factory=list)

    positional_link_styles: list = field(default_factory=list)

    def __str__(self) -> str:
        return self.print('', 0)

    def print_body(self, indent: str, link_count: int) -> str:
        result = []
        for node in self.nodes:
            result.append(indent + str(node))
        for link in self.links:
            result.append(indent + str(link))
            if link.style:
                result.append(indent +link.print_style(link_count))
            link_count += 1
        for subgraph in self.subgraphs:
            result.append(subgraph.print(indent, link_count))
        for class_def in self.class_defs:
            result.append(indent + str(class_def))
        for class_attachment in self.class_attachments:
            result.append(indent + str(class_attachment))
        for link_pos, style in self.positional_link_styles:
            result.append(indent + f'linkStyle {link_pos} {style};')
        return "\n".join(result)

    def print(self, indent, link_count) -> str:
        current_indent = indent
        result = []
        if self.title:
            result.append(current_indent + '---')
            result.append(current_indent + f'title: {self.title}')
            result.append(current_indent + '---')
        result.append(current_indent + f'flowchart {self.direction.name}')
        
        result.append(self.print_body(current_indent + '  ', link_count))
        result.append('')
        return "\n".join(result)

    def add_node(self, node: Union[Node, str]):
        """Add a node to the chart
        
        Args:
            node (Union[Node, str]): Node or string
        
        Returns:
            Chart: self
        """
        if isinstance(node, str):
            node = Node(title=node)

        self.nodes.append(node)
        return self

    def add_nodes(self, nodes: list[Node]):
        self.nodes.extend(nodes)
        return self

    def add_link(self, link: Link):
        self.links.append(link)
        return self
    
    def add_class_def(self, class_def: ClassDef):
        self.class_defs.append(class_def)
        return self

    def attach_class(self, nodes: Union[list[Node], list[str], str, Node], class_name: str):
        self.class_attachments.append(ClassAttachment(nodes=nodes, class_name=class_name))

    def add_link_between(self, src: Union[str, Node], dest: Union[str, Node],
                         text: str = None):
        if isinstance(src, Node):
            src = src.get_id()
        if isinstance(dest, Node):
            dest = dest.get_id()
        self.add_link(Link(src=src, dest=dest, text=text))
        return self

    def add_link_style(self, link: Union[int, Link], style: Union[str, LinkStyle]):
        if isinstance(link, Link):
            link.style = style
        else:
            self.positional_link_styles.append((link, style))
        return self

    def add_subgraph(self, subgraph):
        self.subgraphs.append(subgraph)
        return self


class Subgraph(Chart):
    id: str = None

    def __str__(self) -> str:
        return self.print('', 0)

    def get_id(self):
        if not self.id:
            if self.title:
                self.id = re.sub(r'[^a-zA-Z0-9\-_]+', '', self.title)
            else:
                self.id = uuid.uuid4().hex
        return self.id

    def print(self, indent: str, link_count: int) -> str:
        current_indent = indent
        result = []
        result.append(current_indent + f'subgraph {self.get_id()} {"[" + self.title + "]" if self.title else ""}')
        current_indent += '  '
        result.append(current_indent + f'direction {self.direction.name}')
        result.append(self.print_body(current_indent, link_count))
        result.append(indent + 'end')
        return "\n".join(result)
