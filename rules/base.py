class ClassificationRule:
    category: str

    def match(self, title: str) -> bool:
        raise NotImplementedError

    def extract_title(self, title: str) -> str:
        raise NotImplementedError
