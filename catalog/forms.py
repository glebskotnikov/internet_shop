from django import forms

from catalog.models import Product, Version

forbidden_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != 'is_published':
                field.widget.attrs['class'] = 'form-control'


class ProductForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Product
        exclude = ('date_of_creation', 'date_last_modified', 'owner')

    def clean_name(self):
        cleaned_data = self.cleaned_data['name']

        for word in forbidden_words:
            if word in cleaned_data.lower():
                raise forms.ValidationError('Вы использовали запрещенное слово в названии')

        return cleaned_data

    def clean_description(self):
        cleaned_data = self.cleaned_data['description']

        for word in forbidden_words:
            if word in cleaned_data.lower():
                raise forms.ValidationError('Вы использовали запрещенное слово в описании')

        return cleaned_data


class ProductModeratorForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Product
        fields = ('description', 'category', 'is_published')

    def clean_description(self):
        cleaned_data = self.cleaned_data['description']

        for word in forbidden_words:
            if word in cleaned_data.lower():
                raise forms.ValidationError('Вы использовали запрещенное слово в описании')

        return cleaned_data


class VersionForm(forms.ModelForm):
    class Meta:
        model = Version
        exclude = ('product',)
