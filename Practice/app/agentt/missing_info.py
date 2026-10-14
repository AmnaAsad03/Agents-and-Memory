from app.agentt.requirements import get_required_fields


def find_missing_fields(intent: str, extracted_data: dict) -> list[str]:
    required_fields = get_required_fields(intent)

    missing_fields = []

    for field in required_fields:
        if not extracted_data.get(field):
            missing_fields.append(field)

    return missing_fields