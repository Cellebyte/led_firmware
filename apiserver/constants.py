import apiserver.objects.response

RGB_IS_REQUIRED = "RGB is required"
HSL_IS_REQUIRED = "HSL is required"
BODY_MISSING = apiserver.objects.response.Response({"error": "Body needs to be provided!"}, 400)


def EXCEPTION_ERROR(e: Exception):
    return apiserver.objects.response.Response({"error": "{}".format(e)}, 400)
