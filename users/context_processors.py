# users/context_processors.py
def email_verification_status(request):
    if request.user.is_authenticated:
        is_verified = request.user.emailaddress_set.filter(verified=True).exists()
        return {"email_verified": is_verified}
    return {}