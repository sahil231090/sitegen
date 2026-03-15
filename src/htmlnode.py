from textnode import TextNode, TextType

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
            raise ValueError("value of LeafNode is set to None!")
        if self.tag is None:
            return self.value
        if self.props is None:
            return f"<{self.tag}>{self.value}</{self.tag}>"
        else:
            return f"<{self.tag} {self.props_to_html()}>{self.value}</{self.tag}>"
    
    def __repr__(self):
        return f"""HTMLNode(
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
        return LeafNode(tag='img', value=None, props={'src': text_node.url, 'alt': text_node.text})
    
