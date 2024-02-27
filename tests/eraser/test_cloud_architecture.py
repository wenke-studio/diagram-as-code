from diagrams.eraser import cloud_architecture as diagram


def teardown_function():
    diagram.CloudArchitecture.reset()


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


def test_default_arrow_connect(stdout):
    diagram.CloudArchitecture.reset()

    proxy = diagram.Node(name="proxy", icon="aws-ec2")
    service = diagram.Node(name="service", icon="aws-ec2")
    proxy.connect(service)

    diagram.CloudArchitecture.draw(stdout)

    assert stdout.length == 3, "should display two nodes and one relation"
    assert "proxy > service" in stdout, "default arrow should be `>`"


def test_anthor_arrow_connect(stdout):
    proxy = diagram.Node(name="proxy", icon="aws-ec2")
    service = diagram.Node(name="service", icon="aws-ec2")
    service.connect(proxy, arrow=diagram.ArrowType.RIGHT_TO_LEFT_ARROW)

    diagram.CloudArchitecture.draw(stdout)

    assert stdout.length == 3, "should display two nodes and one relation"
    assert "service < proxy" in stdout, "specified arrow should be `<`"


def test_relations_must_be_drawn_last(stdout):

    gw = diagram.Node(name="gw", icon="aws-internet-gateway")
    vpc = diagram.Group(name="vpc", icon="aws-vpc")
    vpc.connect(gw, diagram.ArrowType.RIGHT_TO_LEFT_ARROW)  # vpc < gw

    public_subnet = diagram.Group(name="public", icon="aws-public-subnet")
    private_subnet = diagram.Group(name="private", icon="aws-private-subnet")
    public_subnet.connect(private_subnet)  # public > private
    vpc.append(public_subnet, private_subnet)

    proxy = diagram.Node(name="proxy", icon="aws-ec2")
    public_subnet.append(proxy)

    service = diagram.Node(name="service", icon="aws-ec2")
    proxy.connect(service)  # proxy > service
    private_subnet.append(service)

    diagram.CloudArchitecture.draw(stdout)

    invalid_message = "should exist and be positioned at the end of the list"
    for conn in ["vpc < gw", "public > private", "proxy > service"]:
        assert conn in stdout[-3:], invalid_message
