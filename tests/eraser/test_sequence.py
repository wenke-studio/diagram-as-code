from diagrams.eraser import sequence as diagram


def test_node_properties():
    node = diagram.Node(name="node", icon="node-icon", color="node-color")

    assert node.properties.icon == "node-icon"
    assert node.properties.color == "node-color"

    content = node.render()

    assert "[icon: node-icon, color: node-color]" in content
