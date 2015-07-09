from django.forms import ModelForm

from html5croppingtools.fields import CropImageField, get_in_memory_file

__author__ = 'irakli'


class CropImageFormMixin(ModelForm):
    def __init__(self, *args, **kwargs):
        jcrop_fields = [(key, value) for (key, value) in self.base_fields.items() if
                        isinstance(value, CropImageField)]  # type:list[(str,CropImageField)]
        for key, value in jcrop_fields:  # type: str,CropImageField
            dimension = args[0].get(key + '_jcrop', None) if len(args) > 0 else None
            try:
                initial = getattr(kwargs['instance'], key)
            except:
                pass
            if value.original_field and isinstance(value.original_field, str):
                value.form = self
            value.dimension = dimension
            try:
                url = initial.url
            except:
                url = 'undefined'

            value.widget.attrs.update({'jcrop_url': url})

        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit=False)
        if hasattr(self, 'cropping_tool_has_original'):
            jcrop_fields = [(key, value) for (key, value) in self.base_fields.items() if
                            isinstance(value, CropImageField)]  # type:list[(str,CropImageField)]
            for key, value in jcrop_fields:  # type: str,CropImageField
                setattr(
                    instance,
                    value.original_field,
                    get_in_memory_file(value.original_field_data)
                )

        if commit:
            instance.save()
        return instance
