class MyAntlrErrorTyping(Exception):
    def __init__(self, message: str, line: int = 1, column: int = 0, len = 1):
        super().__init__(message)
        self.line = line
        self.column = column
        self.len = len
