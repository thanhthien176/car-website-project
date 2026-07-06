from django import forms
from users.models import User


class ProfileUpdateForm(forms.ModelForm):
    """
    Form for a user to edit their own public profile.
    Deliberately excludes  sensitive fields (phone, address, cccd) - 
    those go through separate forms with explicit confirmation later.
    """
    class Meta:
        model = User
        fields = ['bio', 'avatar', 'province', 'birth_year']
        widgets = {
            'bio': forms.Textarea(attrs={
                'rows': 4,
                'class': 'form-control',
            })
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for name, field in self.fields.items():
            if name == 'bio':
                continue
            field.widget.attrs.setdefault('class', 'form-control')