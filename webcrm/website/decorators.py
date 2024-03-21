from django.shortcuts import redirect


def user_not_authenticated(function=None, redirect_url="/"):
    """
    Decorator to redirect authenticated users to a specified URL.

    Parameters:
    function (function): The view function to be decorated. Default is None.
    redirect_url (str): The URL to redirect to if the user is authenticated. Default is '/'.

    Returns:
    decorator (function): The decorated view function.
    """

    def decorator(view_func):
        """
        Inner decorator function.

        Parameters:
        view_func (function): The view function to be decorated.

        Returns:
        _wrapped_view (function): The wrapped view function.
        """

        def _wrapped_view(request, *args, **kwargs):
            """
            The actual wrapper function that checks if the user is authenticated.

            Parameters:
            request (HttpRequest): An instance of Django's HttpRequest.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

            Returns:
            HttpResponse: The response returned by the view function or a redirect response.
            """
            if request.user.is_authenticated:
                return redirect(redirect_url)
            return view_func(request, *args, **kwargs)

        return _wrapped_view

    if function:
        return decorator(function)
    return decorator
