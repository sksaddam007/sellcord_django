# disputes/middleware.py
from django.shortcuts import redirect


class RoleBasedRedirectionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            if request.path == '/':
                if request.user.role == 'seller':
                    return redirect('item_list')
                elif request.user.role == 'customer':
                    return redirect('order_list')
        response = self.get_response(request)
        return response
