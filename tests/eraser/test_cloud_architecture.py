from diagrams.eraser import cloud_architecture as diagram


def test_node_properties():
    node = diagram.Node(name="node", icon="node-icon", color="node-color")

    assert node.properties.icon == "node-icon"
    assert node.properties.color == "node-color"

    content = node.render()

    assert "[icon: node-icon, color: node-color]" in content


def test_group_properties():
    group = diagram.Group(name="group", icon="group-icon", color="group-color")

    assert group.properties.icon == "group-icon"
    assert group.properties.color == "group-color"

    content = group.render()

    assert "[icon: group-icon, color: group-color]" in content
