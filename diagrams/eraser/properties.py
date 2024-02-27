import attrs


class NotSupportedError(Exception):
    pass


@attrs.define(kw_only=True)
class Properties:
    """Supported properties for a diagram node in Eraser

    Args:
        icon (str, optional):
            The icon of the graph. Defaults to None.
            https://docs.eraser.io/docs/icons
        color (str, optional):
            The color name or hex code. Defaults to None.
        label (str, optional):
            [FLOW CHARTS ONLY]
            The label of the graph. Defaults to None.
        shape (str, optional):
            [FLOW CHARTS ONLY]
            The shape of the graph. Defaults to None.

    Refs:
        cloud architecture diagrams: https://docs.eraser.io/docs/syntax#properties
        entity relationship diagrams: https://docs.eraser.io/docs/syntax-1#properties
        sequence diagrams: https://docs.eraser.io/docs/syntax-2#properties
        flow charts (NOT YET SUPPORTED): https://docs.eraser.io/docs/syntax-3#properties
    """

    icon: str | None = None
    color: str | None = None
    label: str | None = None
    shape: str | None = None

    def render(self) -> str:
        """Render the properties as a string

        Properties are key-value pairs enclosed in `[ ]` brackets that can be appended to
        definitions of nodes and groups.

        Returns:
            A string representation of the properties. There are key-value pairs enclosed in `[ ]`
            brackets or an empty string if no properties are set.
        """
        filtered_fields = attrs.asdict(self, filter=lambda _, v: v is not None)
        serialized_items = [f"{key}: {value}" for key, value in filtered_fields.items()]
        if serialized_items:
            return f"[{', '.join(serialized_items)}]"
        return ""
