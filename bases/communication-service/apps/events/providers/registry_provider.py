PROVIDER_REGISTRY = {}


def register_provider(name):
    '''Decorator to register a provider class in the global PROVIDER_REGISTRY.

    This enables dynamic provider resolution using a string identifier (`name`),
    allowing the system to map database-stored provider codes to their
    corresponding implementation classes.

    When a provider class is decorated with this, it is automatically added
    to the registry at import time.

    Args:
        name (str): Unique identifier for the provider (e.g., "google_smtp").

    Returns:
        function: A decorator that registers the class in the registry.

    Example:
        @register_provider("google_smtp")
        class SMTPProvider(BaseEmailProvider):'''

    def wrapper(cls):
        PROVIDER_REGISTRY[name] = cls
        return cls

    return wrapper
