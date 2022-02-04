from __future__ import annotations

class Ownership:
    """Class to handle ..."""
    owners:list(str) = []

    def add(self, metadata:dict) -> None:
        """Try to add owner data from meta data to service_teams"""
        self.owners.extend(metadata.get("owners", []))


