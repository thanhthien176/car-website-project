from allauth.account.forms import LoginForm

class CustomLoginForm(LoginForm):
    
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        
        self.fields["login"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Email",
            "autocomplete": "email",
            "autofocus": True,
            "spellcheck": "false",
            "maxlength": 100,
        })
        
        self.fields["password"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "password",
            "autocomplete": "current-password"
        })
        
        if "remember" in self.fields:
            self.fields["remember"].widget.attrs.update({
                "class": "form-check-input"
            })
            
            
