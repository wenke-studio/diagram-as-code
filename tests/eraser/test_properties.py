from diagrams.eraser.properties import Properties


def test_properties():
    assert hasattr(Properties, "render"), "Properties class should have render method"

    props = Properties()

    assert props.icon is None
    assert props.color is None
    assert props.label is None
    assert props.shape is None

    assert props.render() == "", "a empty properties should render to empty string"


def test_properties_render_icon():
    props = Properties(icon="any-icon")

    assert props.icon == "any-icon"
    assert props.render() == "[icon: any-icon]"


def test_properties_render_color():
    props = Properties(color="#color")

    assert props.color == "#color"
    assert props.render() == "[color: #color]"


def test_properties_render_icon_color():
    props = Properties(icon="any-icon", color="#color")

    assert props.icon == "any-icon"
    assert props.color == "#color"
    assert props.render() == "[icon: any-icon, color: #color]"
