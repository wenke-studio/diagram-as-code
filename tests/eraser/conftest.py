import pytest


class StdoutMock(list):

    def __call__(self, out: str) -> None:
        self.append(out)

    @property
    def length(self) -> int:
        return len(self)


@pytest.fixture(scope="function")
def stdout():
    yield StdoutMock()
