#  Installation
    run  pip install django-html5croppingtools

#  Configure settings.py:
     Add html5croppingtools to INSTALLED_APPS


#  manage.py
     run manage.py collectstatic

# Examples

### Admin example without saving original image

``` python
        #models.py
        class MyModel(models.Model):
            ...
            image = models.ImageField(upload_to='<upload path>')
            ...

        #admin.py
        ....
        from html5croppingtools.fields import CropImageField
        from html5croppingtools.forms import CropImageFormMixin
        ....

        class MyModelForm(CropImageFormMixin, ModelForm):
            """
            :param max_size maximum size of image width or height(depends on which is greater) in pixels
            :param width_ratio and height_ratio using this two parameters code calculates ratio
                   between width and height of image and helps when selecting cropping area in admin by fixing ratio between sides
            """
            image = CropImageField(max_size=900, width_ratio=500,height_ratio=300)
            ....


        @admin.register(MyModel)
        class MyModelAdmin(admin.ModelAdmin):
            form = MyModel
            ....
```

### Admin example with saving original image
``` python 
        ...
        class MyModel(models.Model):
                ...
                image = models.ImageField(upload_to='<upload path>')
                original_image = models.ImageField(upload_to='<upload path>')
                ...
        ...
        class MyModelForm(CropImageFormMixin, ModelForm):
            """
            :param original_field name of corresponding model's field where you want to save original image
            """
            image = CropImageField(
                original_field='original_image', max_size=900,
                width_ratio=500, height_ratio=300,
            )
            ....
````
# On the fly cropping
### Add html5croppingtools.imagecrop.ImageCropMiddleware to MIDDLEWARE_CLASSES
    after adding html5croppingtools.imagecrop.ImageCropMiddleware to MIDDLEWARE_CLASSES
    you can add "quality=<int>&dimensions=<int x1 >x<int y1 >x<int x2 >x<int y2>" this parameters to GET querystring
    and middleware will serve corresponding image cropped and resized

### Middleware working steps:
1.  If "quality" is supplied, image will be resized
1.  If crop "dimensions" are supplied, image will be cropped

**Note:** "dimensions" and "quality" parameters are optional

#    Example
/media/image/my_image_guid.jpeg?quality=1200&dimensions=300x200x900x800

1. middleware will  resize image proportionally making It's bigger side equal to 1200 pixels
1. after shrinking it will crop out a rectangle with coordinates:  **x1=300 y1=200 x2=900 y2=800** rectangle

#    Template example
```html
{% load croppingtools_extra %}
<img src="{% html5crop MyModel.image dimensions='100x100x300x300' quality=500 %}">
```

takes "ImageFiled", "dimensions" and "quality" parameters and
returns url "/media/image/my_image_guid.jpeg?quality=500&dimensions=100x100x300x300"
after which middleware will serve cropped and resized image

**Note:** "dimensions" and "quality" parameters are optional