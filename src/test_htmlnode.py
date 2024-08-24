from htmlnode import HTMLNode, LeafNode, ParentNode
html_node = HTMLNode("one","two",["three","four"],{"href":"google.com","target": "_blank"})
print(html_node)
html_prop = html_node.props_to_html()
print(html_prop)
leaf_node = LeafNode("a","hello",{"href":"mysight.com"})
print(leaf_node.to_html())

a1 = ParentNode( "body",
	[
		LeafNode("p","a paragraph"),
		LeafNode("p","another paragraph")
	]
	)

a2 =LeafNode("a", "Click me!", {"href": "https://www.google.com"})
print(a1.to_html())
print(a2.to_html())

node = ParentNode(
    "head",
    [
        LeafNode("b", "Bold text"),
        LeafNode(None, "Normal text"),
        LeafNode("i", "italic text"),
        LeafNode(None, "Normal text"),
        a1,
        a2
    ],
    {"href":"boot.dev"}
)

print(node.to_html())