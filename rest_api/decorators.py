from rest_framework.response import Response
from rest_framework.views import status


def validate_request_inputs(func):
    def decorated(*args, **kwargs):
        # TODO: change this here, it does not do what you think it does
        # args[0] == GenericView Object
        data_dict = args[0].request.data
        # empty_params = tuple(map(lambda item: item[0], filter(lambda kwarg: kwarg[1] == '', kwargs.items())))
        empty_params = tuple(item[0] for item in data_dict.items() if item[1] == '')
        if empty_params:
            message = f"The following parameters were missing from your request: {', '.join(empty_params)}"
            return Response(data={'message': message}, status=status.HTTP_400_BAD_REQUEST)
        return func(*args, **kwargs)
    return decorated
