class DescriptionMixin:
    """
    Mixin that defines the contract for classes that have
    a textual description.

    Classes that inherit from this mixin must implement
    the `get_description` method.
    """

    def get_description(self) -> str:
        raise NotImplementedError("Class must implement get_description()")
