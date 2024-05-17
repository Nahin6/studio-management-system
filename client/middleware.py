from django.shortcuts import redirect

class AuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path
        
        # Redirect unauthenticated users to the client login page
        # if  not request.user.is_authenticated:
        #     return redirect('client_login')

       # Check if the user is trying to access photographer-specific views
        # if 'photographer' in path and not request.user.is_photographer:
        #     return redirect('blocked')

        # Check if the user is trying to access admin-specific views
        if 'admin' in path and not request.user.is_admin:
            return redirect('blocked')

        # If the user passes all checks, continue to the view
        response = self.get_response(request)
        return response
