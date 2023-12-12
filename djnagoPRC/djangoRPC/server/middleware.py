from django.shortcuts import redirect

class RedirectToPageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if response.status_code == 404:
            # Если страница не найдена (404), выполняем перенаправление на вашу страницу
            return redirect('not_found')
        return response