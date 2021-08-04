class Animation:
    SUPPORTED = ["normal", "snake", "breath", "off", "manual"]

    def __init__(self, animation):
        if animation in self.SUPPORTED:
            self.value = animation
        else:
            raise ValueError(
                "Animation `{}` not in [{}]".format(
                    animation, ", ".join(self.SUPPORTED)
                )
            )

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Animation):
            return self.value == other.value
        else:
            raise ValueError("Animation is required")

    def as_dict(self):
        return {"animation": self.value}

    def __repr__(self) -> str:
        return "Animation('{}')".format(self.value)

    def __hash__(self) -> int:
        return hash(self.value)
