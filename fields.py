import json
from io import BytesIO
import uuid

from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.forms import ImageField

from html5croppingtools.widgets import CropImageWidget


class CropImageField(ImageField):
    def __init__(self, max_size=2000, width_ratio=500, height_ratio=300, dimension=None, initial=None,
                 original_field=None, *args, **kwargs):
        self.dimension = dimension
        self.initial = initial
        self.max_size = max_size
        self.width_ratio = width_ratio
        self.height_ratio = height_ratio
        self.original_field = original_field
        self.original_field_data = None
        kwargs.update(
            {
                'widget': CropImageWidget(
                    width_ratio=width_ratio,
                    height_ratio=height_ratio,
                )
            }
        )
        super().__init__(*args, **kwargs)

    def validate(self, value):
        super().validate(value)
        if self.dimension is None:
            raise TypeError("dimensions can't be None")

    def clean(self, data, initial=None):
        super().clean(data, initial=initial)
        if data is None and initial is not None:
            data = open(initial.path, 'rb')
        if data:
            dimensions = json.loads(self.dimension)
            image = Image.open(data).convert('RGB')  # type:Image

            width, height = image.size
            width_coefficient = width / dimensions.get('actual_width')
            height_coefficient = height / dimensions.get('actual_height')
            x = dimensions.get('x') * width_coefficient
            y = dimensions.get('y') * height_coefficient
            x2 = dimensions.get('x2') * width_coefficient
            y2 = dimensions.get('y2') * height_coefficient
            quality = (dimensions.get('quality') / 100) * self.max_size

            cropped_example = image.crop((int(x), int(y), int(x2), int(y2)))
            cropped_example.thumbnail((quality, quality), Image.ANTIALIAS)
            if hasattr(self, 'form'):
                self.form.base_fields['image'].original_field_data = image
                self.form.cropping_tool_has_original = True

            return get_in_memory_file(cropped_example)


def get_in_memory_file(image: 'Image'):
    temp_file_io = BytesIO()

    image.save(temp_file_io, 'jpeg', optimize=True)
    temp_file_io.seek(0)

    image_file = InMemoryUploadedFile(temp_file_io, None, str(uuid.uuid4()) + '.jpeg', 'jpeg', None, None)
    image_file.seek(0)
    return image_file
