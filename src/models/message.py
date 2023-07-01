class Message:
    def __init__(self, date: str, time: str, sender: str, content: str):
        self.date = date
        self.time = time
        self.sender = sender
        self.content = content

    def __str__(self):
        return f"[{self.date} {self.time}] {self.sender}: {self.content}"
