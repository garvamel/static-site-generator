
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
        for k,v in self.props.items():
            res += f' {k}="{v}"'
        return res

    def __repr__(self):
        return f"HTML Node data\ntag: {self.tag}\nvalue: {self.value}\nchildren:  {self.children}\nprops: {self.props}\n"

class LeafNode(HTMLNode):
    def __init__(self, value, tag = None, props = None) -> None:
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value in [None, '']:
            raise ValueError
        elif self.tag in [None, '']:
            return self.value
        else:
            return f"<{self.tag}{self.props_to_html()}>{self.value}<\{self.tag}>"

    def __repr__(self):
        return f"Leaf Node data\ntag: {self.tag}\nvalue: {self.value}\nprops: {self.props}\n"
    
class ParentNode(HTMLNode):
        def __init__(self, tag, children, props = None) -> None:
            super().__init__(tag, None, children, props)

        def to_html(self):
            if self.tag in [None, '']:
                raise ValueError("No tag")
            elif self.children is None or self.children == 0:
                raise ValueError("No children")   
            else:
                return f"<{self.tag}{self.props_to_html()}>{self.value}<\{self.tag}>"

        def __repr__(self):
            return f"Parent Node data\ntag: {self.tag}\nchildren: {self.children}\nprops: {self.props}\n"