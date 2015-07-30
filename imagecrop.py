import os
from PIL import Image
from django.conf import settings
from django.http.request import HttpRequest
from django.http.response import HttpResponse


class ImageCropMiddleware:
    def process_response(self, request: 'HttpRequest', response: 'HttpResponse'):
        # todo check if media root exists
        if request.path.startswith(settings.MEDIA_URL):
            try:
                file = open(os.path.join(settings.MEDIA_ROOT, request.path.replace(settings.MEDIA_URL, '')), mode='rb')
                response = HttpResponse(content_type="image/jpeg")
                """:type:Image"""
                image = Image.open(file).convert('RGB')

                if request.GET.get('quality', None):
                    quality = request.GET.get('quality')
                    image.thumbnail((int(quality), int(quality)), Image.ANTIALIAS)
                if request.GET.get('dimensions', None):
                    x, y, x2, y2 = [int(d) for d in request.GET.get('dimensions').split('x')]
                    x2 = image.size[0] if image.size[0] < x2 else x2
                    y2 = image.size[1] if image.size[1] < y2 else y2
                    image = image.crop((x, y, x2, y2))
                image.save(response, "jpeg")
            except BaseException as ex:
                print(ex)
                raise ex  # todo exception handling
        return response
