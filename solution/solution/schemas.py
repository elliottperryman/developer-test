# These schemas are used for validating json data correctness.
# All code should use these so that changes are minimized

empire_schema = {
    "type": "object",
    "properties": {
    "countdown": {
        "type": "integer",
        "minimum": 0
    },
    "bounty_hunters": {
        "type": "array",
        "items": {
        "type": "object",
        "properties": {
            "planet": {
            "type": "string"
            },
            "day": {
            "type": "integer",
            "minimum": 0
            }
        },
        "required": ["planet", "day"]
        }
    }
    },
    "required": ["countdown", "bounty_hunters"]
}

falcon_schema = {
    "type": "object",
    "properties": {
    "autonomy": {
        "type": "integer",
        "minimum": 0
    },
    "departure": {
        "type": "string"
    },
    "arrival": {
        "type": "string"
    },
    "routes_db": {
        "type": "string"
    }
    },
    "required": ["autonomy", "departure", "arrival", "routes_db"]
}