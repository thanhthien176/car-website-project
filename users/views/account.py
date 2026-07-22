from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect
from django.views import View
from allauth.account.models import EmailAddress


class ResendConfirmationEmailView(View):
    
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "Bạn cần đăng nhập để thực hiện thao tác này.")
            return redirect('account_login')
        
        email_address = EmailAddress.objects.filter(
            user=request.user, verified=False
        ).first()
        
        if email_address:
            email_address.send_confirmation(request)
            messages.success(request, "Đã gửi lại email xác nhận, vui lòng kiểm tra hộp thư.")
        else:
            messages.info(request, "Email của bạn đã được xác nhận rồi")
            
        return redirect('cars:home')