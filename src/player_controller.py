```python
class PlayerController:
    def __init__(self, platform_creator):
        self.platform_creator = platform_creator

    def handle_input(self, input_event):
        if input_event.type == "PLATFORM_CREATE":
            x, y = input_event.position
            self.platform_creator.create_platform(x, y)
```