import apiserver.objects.response


BODY_MISSING = apiserver.objects.response.Response({"error": "Body needs to be provided!"}, 400)


def EXCEPTION_ERROR(e: Exception):
    return apiserver.objects.response.Response({"error": "{}".format(e)}, 400)
