from django import forms

from core.models import ContactMe

class ContactMeForm(forms.ModelForm):
    class Meta:
        model = ContactMe
        fields = ['name', 'email', 'subject', 'message']
        labels = {
            'name': 'Họ và Tên',
            'email': 'Email',
            'subject': 'Tiêu đề',
            'message': 'Nội dung',
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Họ và tên',
            }),
            'email': forms.TextInput(attrs={
                'placeholder': 'Email'
            }),
            'subject': forms.TextInput(attrs={
                'placeholder': 'Tiêu đề ',
            }),
            'message': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Nhập nội dung'
            })
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            css_class = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = f'{css_class} form-control'.strip()
            