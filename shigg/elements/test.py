from enum import Enum, auto
from button import ButtonReleased

if __name__ == "__main__":

    class Tag(Enum):
        Settings = auto()

    a = ButtonReleased(Tag.Settings)
    print(a.tag)

    # check the tag type enforcement
    try:
        a = ButtonReleased("settings")
        raise AssertionError("ButtonReleased did not raise TypeError")
    except TypeError:
        print(
            "Passed: Creating a ButtonReleased with a non enum tag raised Type error."
        )
    except Exception as e:
        # If an unexpected error type was raised, raise an AssertionError
        raise AssertionError(f"Unexpected exception type: {type(e).__name__}") from e
