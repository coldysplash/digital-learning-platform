class HTMXMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Проверяем, является ли запрос HTMX-запросом
        is_htmx = request.headers.get("HX-Request") == "true"
        # Добавляем use_layout в объект request
        request.use_layout = not is_htmx
        response = self.get_response(request)
        return response
