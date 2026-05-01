from .registry_provider import PROVIDER_REGISTRY


def get_provider(provider):
    '''Factory function to retrieve and instantiate the appropriate email provider.

    This function uses the provider's `code` (stored in the database) to look up
    the corresponding provider class from the global PROVIDER_REGISTRY.

    Flow:
        1. Validate that the provider has a code.
        2. Look up the provider class in the registry using the code.
        3. Instantiate the provider class with the provider instance.
        4. Return the initialized provider object.

    Args:
        provider (Provider): Provider model instance containing code, credentials, region, etc.'''

    if not provider.code:
        raise ValueError("Provider code is not set")

    provider_class = PROVIDER_REGISTRY.get(provider.code)

    if not provider_class:
        raise ValueError(f"Unsupported provider: {provider.code}")

    return provider_class(provider)
