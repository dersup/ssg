class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        if not self.tag:
            return f"{self.value}"
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def props_to_html(self):
        ret_str = ""
        if self.props:
            for k, v in self.props.items():
                ret_str += f" {k}=\"{v}\""
        return ret_str

    def __repr__(self):
        return f"HTMLNode({self.tag},{self.value},{self.children},{self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag, value, None, props)
        if self.value is None:
            raise ValueError("all leaf nodes must have a value!")

    def to_html(self):

        if self.tag is None:
            return f"{self.value}"
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
        if self.tag is None:
            raise ValueError("Parent Node needs a tag")
        if self.children is None:
            raise ValueError("Parent Node needs children")

    def to_html(self):
        if self.children is None:
            return None
        child_str = ""
        for child in self.children:
            child_str += child.to_html()
        if not self.tag:
            return f"{child_str}"
        return f"<{self.tag}{self.props_to_html()}>{child_str}</{self.tag}>"
