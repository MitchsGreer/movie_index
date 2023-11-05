"""Enhanced JSON encoder ripped from stack overflow."""
import dataclasses
import json
from typing import Any, Dict


class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o) -> Dict[str, Any]:
        """Default decoder.

        Args:
            o: Object to decode.

        Returns:
            The object in dictionary form.
        """
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        return super().default(o)
