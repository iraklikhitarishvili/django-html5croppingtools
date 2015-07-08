add to installed_apps

run manage.py collectstatic


admin example

from croppingtools.fields import CropImageField
from croppingtools.forms import CropImageFormMixin

class ImageForm(CropImageFormMixin, ModelForm):
    image = CropImageField(max_size=2200, width_ratio=500, height_ratio=300)


requirements pillow 
