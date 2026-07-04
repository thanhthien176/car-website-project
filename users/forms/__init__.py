# users/forms/__init__.py

from .login_form import CustomLoginForm
from .signup_form import CustomSignupForm
# from .password_forms import MyCustomChangePasswordForm, MyCustomResetPasswordForm

# (Tùy chọn) Định nghĩa __all__ để làm sạch package (nếu muốn)
__all__ = [
    'CustomLoginForm',
    'CustomSignupForm',
    # 'MyCustomChangePasswordForm',
    # 'MyCustomResetPasswordForm',
]