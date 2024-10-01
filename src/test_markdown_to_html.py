import unittest

from markdown_to_html import markdown_to_html_node
from htmlnode import ParentNode, LeafNode

class TestMarkdownToHTML(unittest.TestCase):

    def test_paragraph(self):
        
        markdown = "Testito bonito"
        p_node = markdown_to_html_node(markdown)
        comparenode = ParentNode("div",children=
                                 [ParentNode("p", children=
                                             [LeafNode(
                                                 tag= None,value="Testito bonito")
                                                 ])])

        self.assertEqual(p_node, comparenode)

    def test_heading1(self):
        
        markdown = "# Testito bonito"
        p_node = markdown_to_html_node(markdown)
        comparenode = ParentNode("div",children=
                                 [ParentNode("h1", children=
                                             [LeafNode(
                                                 tag= None,value="Testito bonito")
                                                 ])])

        self.assertEqual(p_node, comparenode)

    def test_heading6(self):
        
        markdown = "###### Testito bonito"
        p_node = markdown_to_html_node(markdown)
        comparenode = ParentNode("div",children=
                                 [ParentNode("h6", children=
                                             [LeafNode(
                                                 tag= None,value="Testito bonito")
                                                 ])])

        self.assertEqual(p_node, comparenode)

    def test_heading7(self):
        
        markdown = "####### Testito bonito"
        p_node = markdown_to_html_node(markdown)
        comparenode = ParentNode("div",children=
                                 [ParentNode("p", children=
                                             [LeafNode(
                                                 tag= None,value="####### Testito bonito")
                                                 ])])
        self.assertEqual(p_node, comparenode)

    def test_code(self):
        
        markdown = "```esto\nes codigo```"
        p_node = markdown_to_html_node(markdown)
        comparenode = ParentNode("div",children=
                                 [ParentNode("pre", children=
                                             [LeafNode(tag= "code",value="esto\nes codigo")
                                            ])
                                 ])
        self.assertEqual(p_node, comparenode)

    def test_quote(self):
        
        markdown = ">esto\n>es\n>una\n>cita"
        p_node = markdown_to_html_node(markdown)
        comparenode = ParentNode("div",children=
                                 [ParentNode("blockquote", children=
                                             [LeafNode(
                                                 tag= None,value="esto\nes\nuna\ncita")
                                                 ])])
        self.assertEqual(p_node, comparenode)

    def test_unordered_list_star(self):
        
        markdown = "* esto\n* es\n* una\n* lista\n* desordenada"
        p_node = markdown_to_html_node(markdown)
        comparenode = ParentNode("div",children=
                                 [ParentNode("ul", children=
                                             [ParentNode("li",[LeafNode(tag= None,value="esto")]),
                                              ParentNode("li",[LeafNode(tag= None,value="es")]),
                                              ParentNode("li",[LeafNode(tag= None,value="una")]),
                                              ParentNode("li",[LeafNode(tag= None,value="lista")]),
                                              ParentNode("li",[LeafNode(tag= None,value="desordenada")])
                                             ])
                                 ])

        self.assertEqual(p_node, comparenode)

    def test_unordered_list_hyphen(self):
        
        markdown = "- esto\n- es\n- una\n- lista\n- desordenada"
        p_node = markdown_to_html_node(markdown)
        comparenode = ParentNode("div",children=
                                 [ParentNode("ul", children=
                                             [ParentNode("li",[LeafNode(tag= None,value="esto")]),
                                              ParentNode("li",[LeafNode(tag= None,value="es")]),
                                              ParentNode("li",[LeafNode(tag= None,value="una")]),
                                              ParentNode("li",[LeafNode(tag= None,value="lista")]),
                                              ParentNode("li",[LeafNode(tag= None,value="desordenada")])
                                             ])
                                 ])
                                                 
        self.assertEqual(p_node, comparenode)

    def test_full_case(self):
        
        file = open("md_file.md","r")
        markdown = file.read()
        p_node = markdown_to_html_node(markdown)
        # print("\n--REF NODE--\n")
        # print(p_node)
        comparenode = ParentNode("div",children=
                                 [ParentNode("h1",[LeafNode(tag=None, value="Titulo 1")]),
                                  ParentNode("pre", children=
                                             [LeafNode(tag= "code",value="todo parte con un buen codigo\na = 1 + b")
                                            ]),
                                  ParentNode("p",[LeafNode(tag= None, value="con "),
                                                  LeafNode(tag="b", value="unas"),
                                                  LeafNode(tag= None, value=" cosas para "),
                                                  LeafNode(tag="i", value="decir"),
                                                  LeafNode(tag= None, value=" que incluyen una "),
                                                  LeafNode(tag="img", value=None, props={"src": "LGV.jpg", "alt": "foto"}),
                                                  LeafNode(tag= None, value="\ny una lista:")
                                            ]),
                                  ParentNode(tag="ul",children=
                                             [ParentNode("li",[LeafNode(tag= None,value="de")]),
                                              ParentNode("li",[LeafNode(tag= None,value="otras")]),
                                              ParentNode("li",[LeafNode(tag= None,value="cosas")])
                                             ]),
                                  ParentNode("h3",[LeafNode(tag=None, value="Categoria 3")]),
                                  ParentNode(tag="ol",children=
                                             [ParentNode("li",[LeafNode(tag= None,value="importante")]),
                                              ParentNode("li",[LeafNode(tag= None,value="es")]),
                                              ParentNode("li",[LeafNode(tag= None,value="que podemos manejar "),
                                                               LeafNode(tag="a", value="enlaces", props={"href": "https://boot.dev"})
                                                              ])
                                             ]),
                                  ParentNode("blockquote",children=[LeafNode(tag= None,value="y responder a\ncitas\nde otras personas")]),
                                  ParentNode("p",children=[LeafNode(tag=None, value="Fin")])
                                ])
        file.close()
        # print("\n--COMPARE NODE--\n")
        # print(comparenode)
        self.assertEqual(p_node, comparenode)