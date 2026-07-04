from allauth.account.forms import SignupForm

class CustomSignupForm(SignupForm):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        
        self.fields["email"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Email",
            "autocomplete": "email",
            "autofocus": True,
            "spellcheck": "false",
            "maxlength": 100,
        })
        
        self.fields["password1"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Password",
            "autocomplete": "current-password"
        })
        
        self.fields["password2"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Re-Password",
            "autocomplete": "current-password"
        })