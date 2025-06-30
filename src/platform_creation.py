```python
class PlatformCreator:
    def __init__(self, world):
        self.world = world

    def create_platform(self, x, y):
        # Simplified platform creation logic
        self.world.add_platform(x, y, temporary=True)
        print(f"Platform created at {x}, {y}")
```