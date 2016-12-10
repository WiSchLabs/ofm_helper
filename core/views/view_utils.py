from django.core.exceptions import MultipleObjectsReturned


def validate_filtered_field(field):
    if len(field) > 1:
        raise MultipleObjectsReturned
    elif field:
        field = field[0]
    return field
