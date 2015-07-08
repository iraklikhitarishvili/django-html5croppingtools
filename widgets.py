from django.contrib.staticfiles.templatetags.staticfiles import static
from django.core.exceptions import ImproperlyConfigured


__author__ = 'irakli'
from django.forms import FileInput


class CropImageWidget(FileInput):
    def __init__(self, width_ratio, height_ratio, url='undefined', *args, **kwargs):
        kwargs.update(
            {
                'attrs': {
                    'class': 'jcrop_image_input',
                    'jcrop_width_ratio': width_ratio,
                    'jcrop_height_ratio': height_ratio,
                    'jcrop_url': url
                }
            }
        )
        super().__init__(*args, **kwargs)

    class Media:
        try:
            css = {
                'all': ('html5croppingtools/jcrop/css/jquery.Jcrop.min.css',),
            }

            js = (
                static('html5croppingtools/jcrop/js/jquery.min.js'),
                static('html5croppingtools/jcrop/js/jquery.Jcrop.min.js'),
                static('html5croppingtools/html5crop.js'),
            )

        except AttributeError:
            raise ImproperlyConfigured("error")


