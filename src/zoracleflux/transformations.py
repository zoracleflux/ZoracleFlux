"""Small deterministic reference functions used by the release-candidate fixture."""


def normalize_whitespace(text: str) -> str:
    """Collapse runs of whitespace and trim ends.

    @relation idempotent
    @relation whitespace-free
    @relation token-preserving
    """
    return " ".join(text.split())


def clamp(value: float, low: float, high: float) -> float:
    """Bound value inclusively between low and high.

    @relation idempotent
    @relation bounded
    @relation endpoint-preserving
    """
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(value, high))


def rotate_left(items: tuple[int, ...], amount: int) -> tuple[int, ...]:
    """Rotate a tuple left without changing its length.

    @relation composition
    @relation length-preserving
    """
    if not items:
        return items
    shift = amount % len(items)
    return items[shift:] + items[:shift]


def stable_unique(items: tuple[int, ...]) -> tuple[int, ...]:
    """Remove duplicates while retaining first-occurrence order.

    @relation idempotent
    @relation membership
    @relation tuple-output
    """
    seen: set[int] = set()
    result: list[int] = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return tuple(result)


def chunk(items: tuple[int, ...], size: int) -> tuple[tuple[int, ...], ...]:
    """Split items into non-empty chunks of at most size.

    @relation flatten-roundtrip
    @relation chunk-size
    """
    if size <= 0:
        raise ValueError("size must be positive")
    return tuple(items[index:index + size] for index in range(0, len(items), size))
