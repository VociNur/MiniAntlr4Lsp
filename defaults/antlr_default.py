class DefaultLoader:
    def __init__(self) -> None:
        self.already_init_variable = ["EOF"]
        self.can_be_initialized = {
            "STAR": "*",
            "COL": ":",
            "SCOL": ";",
            "OPAR": "(",
            "CPAR": ")",
            "OBRACE": "{",
            "CBRACE": "}",
            "RETURN": "return",
            "TRUE": "true",
            "FALSE": "false",
            "IF": "if",
            "THEN": "then",
            "ELSE": "else",
            "WHILE": "while",
            "FOR": "for",
            

        }
