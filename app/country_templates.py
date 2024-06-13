country_templates = {
    "IN": ["business_name", "PAN", "GSTIN"],
    "US": ["business_name", "registration_number", "extra_detail"],
    "CA": ["business_name","business_number","province","industry_type"]    # Add other country templates as needed
}



def validate_configuration(country_code: str, data: dict):
    template = country_templates.get(country_code)
    if not template:
        raise ValueError(f"No template found for country code {country_code}")
    missing_fields = [field for field in template if field not in data]
    if missing_fields:
        raise ValueError(f"Missing fields for country {country_code}: {', '.join(missing_fields)}")
