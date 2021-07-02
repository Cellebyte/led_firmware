def code_to_message(code):
    if code == 100:
        return "Continue"
    if code == 101:
        return "Switching Protocols"
    if code == 200:
        return "OK"
    if code == 201:
        return "Created"
    if code == 202:
        return "Accepted"
    if code == 203:
        return "Non-Authoritative Information"
    if code == 204:
        return "No Content"
    if code == 205:
        return "Reset Content"
    if code == 300:
        return "Multiple Choices"
    if code == 301:
        return "Moved Permanently"
    if code == 302:
        return "Found"
    if code == 303:
        return "See Other"
    if code == 305:
        return "Use Proxy"
    if code == 306:
        return "(Unused)"
    if code == 307:
        return "Temporary Redirect"
    if code == 308:
        return "Permanent Redirect"
    if code == 400:
        return "Bad Request"
    if code == 401:
        return "Unauthorized"
    if code == 402:
        return "Payment Required"
    if code == 403:
        return "Forbidden"
    if code == 404:
        return "Not Found"
    if code == 405:
        return "Method Not Allowed"
    if code == 406:
        return "Not Acceptable"
    if code == 408:
        return "Request Timeout"
    if code == 409:
        return "Conflict"
    if code == 410:
        return "Gone"
    if code == 411:
        return "Length Required"
    if code == 413:
        return "Payload Too Large"
    if code == 414:
        return "URI Too Long"
    if code == 415:
        return "Unsupported Media Type"
    if code == 417:
        return "Expectation Failed"
    if code == 426:
        return "Upgrade Required"
    if code == 500:
        return "Internal Server Error"
    if code == 501:
        return "Not Implemented"
    if code == 502:
        return "Bad Gateway"
    if code == 503:
        return "Service Unavailable"
    if code == 504:
        return "Gateway Timeout"
    if code == 505:
        return "HTTP Version Not Supported"
