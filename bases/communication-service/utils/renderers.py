from rest_framework import renderers


class CustomRenderer(renderers.JSONRenderer):
    charset = 'utf-8'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = renderer_context.get('response')

        if response.status_code >= 400:
            return super().render(data, accepted_media_type, renderer_context)

        formatted_data = {
            'status': 'success',
            'message': 'Request processed successfully',
            'data': data
        }

        return super().render(formatted_data, accepted_media_type, renderer_context)
