import re
from textnode import TextNode, TextType, markdown_to_blocks, text_to_textnodes
from block import block_to_block_type, BlockType

class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        return " ".join( [f'{k}="{v}"' for k,v in self.props.items()] )
    
    def __repr__(self):
        return f"""HTMLNode(
    tag={self.tag}, 
    value={self.value}, 
    children={self.children},
    props={self.props})
    """


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(
            tag=tag,
            value=value,
            children=None,
            props=props
            )
    
    def to_html(self):
        if self.value is None:
            raise ValueError(f"value of LeafNode is set to None! tag ={self.tag} ")
        if self.tag is None:
            return self.value
        if self.props is None:
            return f"<{self.tag}>{self.value}</{self.tag}>"
        else:
            return f"<{self.tag} {self.props_to_html()}>{self.value}</{self.tag}>"
    
    def __repr__(self):
        return f"""LeafNode(
    tag={self.tag}, 
    value={self.value}, 
    props={self.props})
    """

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(
            tag=tag,
            value=None,
            children=children,
            props=props
            )
    def to_html(self):
        if self.tag is None:
            raise ValueError("tag of ParentNode is set to None!")
        if self.children is None:
            raise ValueError("children of ParentNode is set to None!")
        

        if self.props is None:
            output = f"<{self.tag}>"
        else:
            output = f"<{self.tag} {self.props_to_html()}>"

        for child in self.children:
            output += child.to_html()
        
        output += f"</{self.tag}>"
        return output

    def __repr__(self):
        return f"""ParentNode(
    tag={self.tag}, 
    children={self.children}, 
    props={self.props})
    """
    
def text_node_to_html_node(text_node):
    if text_node.text_type not in list(TextType):
        raise IndexError('text_node.text_type is not valid')
    
    elif text_node.text_type == TextType.TEXT:
        return LeafNode(tag=None, value=text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode(tag='b', value=text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode(tag='i', value=text_node.text)
    elif text_node.text_type == TextType.CODE:
        return LeafNode(tag='code', value=text_node.text)
    elif text_node.text_type == TextType.LINK:
        return LeafNode(tag='a', value=text_node.text, props={'href': text_node.url})
    elif text_node.text_type == TextType.IMAGE:
        return LeafNode(tag='img', value='', props={'src': text_node.url, 'alt': text_node.text})
    

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.HEADING:
            children.append(heading_to_html_node(block))
        elif block_type == BlockType.CODE:
            children.append(code_to_html_node(block))
        elif block_type == BlockType.QUOTE:
            children.append(quote_to_html_node(block))
        elif block_type == BlockType.UNORDERED_LIST:
            children.append(unordered_list_to_html_node(block))
        elif block_type == BlockType.ORDERED_LIST:
            children.append(ordered_list_to_html_node(block))
        else:
            children.append(paragraph_to_html_node(block))
    return ParentNode("div", children)



def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(node) for node in text_nodes]


def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    text = block[level + 1:]
    return ParentNode(f"h{level}", text_to_children(text))


def code_to_html_node(block):
    # strip the ```\n and ``` delimiters
    text = block[4:-3]
    code_node = text_node_to_html_node(TextNode(text, TextType.CODE))
    return ParentNode("pre", [code_node])


def quote_to_html_node(block):
    lines = block.split("\n")
    stripped = [line.lstrip(">").strip() for line in lines]
    text = "\n".join(stripped)
    return ParentNode("blockquote", text_to_children(text))


def unordered_list_to_html_node(block):
    items = block.split("\n")
    li_nodes = []
    for item in items:
        text = item[2:]
        li_nodes.append(ParentNode("li", text_to_children(text)))
    return ParentNode("ul", li_nodes)


def ordered_list_to_html_node(block):
    items = block.split("\n")
    li_nodes = []
    for item in items:
        text = re.sub(r"^\d+\. ", "", item)
        li_nodes.append(ParentNode("li", text_to_children(text)))
    return ParentNode("ol", li_nodes)


def paragraph_to_html_node(block):
    lines = block.split("\n")
    text = " ".join(lines)
    return ParentNode("p", text_to_children(text))