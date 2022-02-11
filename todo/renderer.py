from rest_framework.renderers import JSONRenderer
from rest_framework.views import exception_handler


class CustomJSONRenderer(JSONRenderer):
   def render(self, data, accepted_media_type=None, renderer_context=None):
       # reformat the response
       response_data = {"message": "", "errors": [], "data": data, "status": "success"}
       # call super to render the response
       response = super(CustomJSONRenderer, self).render(
           response_data, accepted_media_type, renderer_context
       )

       return response