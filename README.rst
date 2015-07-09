1 Configure settings.py:
    a) Add html5croppingtools to INSTALLED_APPS


2 manage.py
    a) run manage.py collectstatic

3 Examples

    a) Admin example without saving original image
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
                   between width and height of image and helps when selecting cropping area in admin by fixing ratio
                   between sides
            """
            image = CropImageField(max_size=900, width_ratio=500,height_ratio=300)
            ....


        @admin.register(MyModel)
        class MyModelAdmin(admin.ModelAdmin):
            form = MyModel
            ....

    b) Admin example with saving original image
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
4 On fly cropping
    a) Add html5croppingtools.imagecrop.ImageCropMiddleware to MIDDLEWARE_CLASSES

    after adding html5croppingtools.imagecrop.ImageCropMiddleware to MIDDLEWARE_CLASSES
    you can add "quality=<int>&dimensions=<int>x<int>x<int>x<int>" this parameters to GET querystring
    and middleware will serve corresponding image cropped and resized
    middleware working steps:
        1 if quality is supplied then resize image
        2 if crop dimensions ar supplied crop image
        3 return image

    Note: "dimensions" and "quality" parameters are optional

    Example
        /media/image/9f925601-cf3e-4acb-b16c-e3d475343192.jpeg?quality=1200&dimensions=300x200x900x800
        1 middleware will shrink image and it's biggest side will be 1200 pixel
        2 after shrinking it will crop  x1=300 y1=200 x2=900 y2=800 rectangle
        3 return image

    Template example
        {% load croppingtools_extra %}
        <img src="{% html5crop MyModel.image dimensions='100x100x300x300' quality=500 %}">
        takes ImageFiled dimensions and quality and
        returns url "/media/image/3ec7e4e5-c303-4339-bcf5-b70048978e91.jpeg?quality=500&dimensions=100x100x300x300"
        after what middleware will serve cropped and resized image

        Note: "dimensions" and "quality" parameters are optional


requirements pillow 
