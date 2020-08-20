from django.http import JsonResponse


class HTTPCode:
    ok = 200
    parameter_error = 400
    unauthorized = 401
    method_error = 405
    server_error = 500


def ok(message='', data=None, **kwargs):
    json_dict = {'code': HTTPCode.ok, 'message': message, 'data': data}

    if kwargs:
        json_dict.update(kwargs)

    return JsonResponse(json_dict)


def parameter_error(message='', data=None, **kwargs):
    json_dict = {'code': HTTPCode.parameter_error, 'message': message, 'data': data}

    if kwargs:
        json_dict.update(kwargs)

    return JsonResponse(json_dict)


def unauthorized(message='', data=None, **kwargs):
    json_dict = {'code': HTTPCode.unauthorized, 'message': message, 'data': data}

    if kwargs:
        json_dict.update(kwargs)

    return JsonResponse(json_dict)


def method_error(message='', data=None, **kwargs):
    json_dict = {'code': HTTPCode.method_error, 'message': message, 'data': data}

    if kwargs:
        json_dict.update(kwargs)

    return JsonResponse(json_dict)


def server_error(message='', data=None, **kwargs):
    json_dict = {'code': HTTPCode.server_error, 'message': message, 'data': data}

    if kwargs:
        json_dict.update(kwargs)

    return JsonResponse(json_dict)
