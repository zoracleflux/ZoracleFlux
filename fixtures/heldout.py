"""Independent held-out fixture used only by evaluation documentation."""


def reverse_copy(items: tuple[int, ...]) -> tuple[int, ...]:
    """Return a reversed tuple without changing length.

    @relation length-preserving
    """
    return tuple(reversed(items))


def poisoned_claim(value: int) -> int:
    """A deliberately unsupported claim for parser negative testing.

    @relation always-secure
    """
    return value
