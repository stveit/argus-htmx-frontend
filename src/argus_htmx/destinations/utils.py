from argus.notificationprofile.models import Media
from argus.notificationprofile.media import api_safely_get_medium_object


def get_settings_key_for_media(media: Media) -> str:
    """Returns the required settings key for the given media,
    e.g. "email_address", "phone_number"
    """
    medium = api_safely_get_medium_object(media.slug)
    return medium.MEDIA_JSON_SCHEMA["required"][0]
