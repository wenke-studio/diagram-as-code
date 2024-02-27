from diagrams.eraser import sequence as diagram


def teardown_function():
    diagram.Sequence.reset()


def test_node_properties():
    node = diagram.Node(name="node", icon="node-icon", color="node-color")

    assert node.properties.icon == "node-icon"
    assert node.properties.color == "node-color"

    content = node.render()

    assert "[icon: node-icon, color: node-color]" in content


def test_node_request(stdout):
    client = diagram.Node(name="client")
    server = diagram.Node(name="server")

    client.request("request", server)

    diagram.Sequence.draw(stdout)

    assert "client > server : request" in stdout[-1]


def test_node_response(stdout):
    client = diagram.Node(name="client")
    server = diagram.Node(name="server")

    server.request("response", client)

    diagram.Sequence.draw(stdout)

    assert "server > client : response" in stdout[-1]


def test_start_session_between_nodes(stdout):
    client = diagram.Node(name="client")
    server = diagram.Node(name="server")

    client.start_session("session", server)

    diagram.Sequence.draw(stdout)

    assert "client <> server : session" in stdout[-1]


def test_do_something(stdout):
    node = diagram.Node(name="node")

    node.do("do something")

    diagram.Sequence.draw(stdout)

    assert "node --> node : do something" in stdout[-1]


def test_relations_must_be_drawn_after_nodes(stdout):
    client = diagram.Node(name="client", icon="monitor")
    service = diagram.Node(name="service", icon="service")

    client.request("SYN", service)
    service.response("SYN-ACK", client)
    client.request("ACK", service)
    client.start_session("ESTABLISHED", service)
    client.do("do something (unnecessary)")
    client.request("FIN", service)
    service.do("...")

    diagram.Sequence.draw(stdout)

    # draws nodes first
    assert "client [icon: monitor]" in stdout[:2]
    assert "service [icon: service]" in stdout[:2]
