
class HTMLNode():
    def __init__(self, tag = None, value = None, children = None, props = None) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        res = ""
        if self.props is None:
            return res
        for k in self.props:
            res += f' {k}="{self.props[k]}"'
        return res

    def __repr__(self):
        return f"HTML Node data\ntag: {self.tag}\nvalue: {self.value}\nchildren: {self.children}\nprops: {self.props}\n"
    
    def __eq__(self, other):
        return self.tag == other.tag and self.value == other.value and self.children == other.children and self.props == other.props

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props = None) -> None:
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError
        elif self.tag is None:
            return self.value
        else:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"Leaf Node data\ntag: {self.tag}\nvalue: {self.value}\nprops: {self.props}\n"
    
class ParentNode(HTMLNode):
        def __init__(self, tag, children, props = None) -> None:
            super().__init__(tag, None, children, props)

        def to_html(self):
            if self.tag is None:
                raise ValueError("No tag")
            elif self.children is None:
                raise ValueError("No children")   
            else:
                children_html = ""
                for child in self.children:
                    children_html += child.to_html()

                return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"

        def __repr__(self):
            return f"Parent Node data\ntag: {self.tag}\nchildren: {self.children}\nprops: {self.props}\n"