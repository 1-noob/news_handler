import hashlib
from urllib.parse import urlsplit, urlunsplit

class HashGenerator:
    """
    Generates SHA 256 hash string for given URL.
    """

    @staticmethod
    def get_hash_str(url: str) -> str:
        """
        Generates SHA 256 hash for the given URL after normalizing it.

        Params:
            url (str): The URL to hash.
        Returns:
            str: The SHA 256 hash of the normalized URL.
        """

        
        if not isinstance(url, str):
            raise ValueError("URL must be a string")
            
        # Encode exactly as-is
        data = url.encode('utf-8')

        # Generate SHA 256 hash
        hash_str = hashlib.sha256(data).hexdigest()

        return hash_str


if __name__ == "__main__":
    test_url = "https://example.com/news/article?id=123&ref=homepage"
    hash_value = HashGenerator.get_hash_str(test_url)
    print(f"SHA 256 Hash: {hash_value}")