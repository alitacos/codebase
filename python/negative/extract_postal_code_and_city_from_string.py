def extract_postal_code_and_city_from_string(location: str) -> tuple[str, str]:
    """
    Parses a mixed location input like '70197 Stuttgart' or 'Stuttgart 70197',
    and returns (postal_code, city) after validation.
    """
    location = str(location).strip()
    if not location:
        return '', ''

    parts = location.split()
    postal_code = ''
    city_parts = []

    for part in parts:
        if part.isdigit() and len(part) == 5:
            postal_code = part
        else:
            city_parts.append(part)

    city_input = ' '.join(city_parts).strip()

    # Validate postal code
    suggested_city_for_plz = get_city_name_via_autocomplete_suggestions(postal_code) if postal_code else ''
    
    # If we have both a postal code and city, validate the match
    if postal_code and city_input:
        if suggested_city_for_plz and city_input.lower() not in suggested_city_for_plz.lower():
            print(f"Input mismatch: '{postal_code}' does not belong to '{city_input}'.")
            print(f"Suggested city for {postal_code}: {suggested_city_for_plz}")
            return '', ''  # Return empty to signal error
        return postal_code, suggested_city_for_plz

    # If only postal code
    if postal_code:
        if not suggested_city_for_plz:
            print(f"Invalid postal code: {postal_code}. No matching city found.")
            return '', ''
        return postal_code, suggested_city_for_plz

    # If only city
    if city_input:
        validated_city = validate_city_name_via_autocomplete_suggestions(city_input)
        if not validated_city:
            print(f"Invalid city: '{city_input}'. No matching suggestion found.")
            return '', ''
        print(f"Missing postal code. Did you mean: {validated_city}?")
        return '', ''  # Could be extended to reverse lookup
    return '', ''
