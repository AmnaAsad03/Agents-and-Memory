from app.agentt.data_extractor import extract_data
from app.agentt.intent_checker import check_intent
from app.agentt.missing_info import find_missing_fields


def check_request(user_request: str) -> dict:
    intent = check_intent(user_request)

    extracted_data = extract_data(
        user_request,
        intent,
    )

    missing_fields = find_missing_fields(
        intent,
        extracted_data,
    )

    return {
        "intent": intent,
        "data": extracted_data,
        "missing_fields": missing_fields,
    }
    
    
if __name__ == "__main__":
    request = input("Enter request: ")

    result = check_request(request)

    print(f"Intent: {result['intent']}")
    print(f"Data: {result['data']}")
    print(f"Missing fields: {result['missing_fields']}")    