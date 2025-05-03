# FastAPI Project - Common HTTP Status Codes

This project uses **FastAPI** along with `starlette.status` to manage HTTP response codes in a clean and readable way.

Below is a list of commonly used HTTP status codes from the `starlette.status` module:

---

## ✅ 2xx: Success

| Code | Constant                 | Description |
|------|--------------------------|-------------|
| 200  | HTTP_200_OK              | The request was successful. |
| 201  | HTTP_201_CREATED         | The resource was successfully created. |
| 202  | HTTP_202_ACCEPTED        | The request has been accepted but not yet processed. |
| 204  | HTTP_204_NO_CONTENT      | The request succeeded but there's no content to return. |

---

## 🔁 3xx: Redirection

| Code | Constant                      | Description |
|------|-------------------------------|-------------|
| 300  | HTTP_300_MULTIPLE_CHOICES     | Multiple response options available. |
| 301  | HTTP_301_MOVED_PERMANENTLY    | Resource has been permanently moved. |
| 302  | HTTP_302_FOUND                | Temporary redirect to another URL. |
| 303  | HTTP_303_SEE_OTHER            | Response found under a different URL. |
| 304  | HTTP_304_NOT_MODIFIED         | Resource not modified since last request. |
| 307  | HTTP_307_TEMPORARY_REDIRECT   | Temporary redirection with same method. |
| 308  | HTTP_308_PERMANENT_REDIRECT   | Permanent redirection with same method. |

---

## ⚠️ 4xx: Client Errors

| Code | Constant                           | Description |
|------|------------------------------------|-------------|
| 400  | HTTP_400_BAD_REQUEST               | Invalid request from client. |
| 401  | HTTP_401_UNAUTHORIZED              | Authentication is required. |
| 402  | HTTP_402_PAYMENT_REQUIRED          | Reserved for future use. |
| 403  | HTTP_403_FORBIDDEN                 | Server refuses to authorize request. |
| 404  | HTTP_404_NOT_FOUND                 | Resource not found. |
| 405  | HTTP_405_METHOD_NOT_ALLOWED        | Method not allowed for this endpoint. |
| 406  | HTTP_406_NOT_ACCEPTABLE            | Requested response format not acceptable. |
| 407  | HTTP_407_PROXY_AUTHENTICATION_REQUIRED | Authentication with proxy required. |
| 408  | HTTP_408_REQUEST_TIMEOUT           | Request timeout. |
| 409  | HTTP_409_CONFLICT                  | Conflict with the current state of the resource. |
| 410  | HTTP_410_GONE                      | Resource is permanently gone. |
| 411  | HTTP_411_LENGTH_REQUIRED           | Missing `Content-Length` header. |
| 412  | HTTP_412_PRECONDITION_FAILED       | Precondition failed. |
| 413  | HTTP_413_PAYLOAD_TOO_LARGE         | Request payload is too large. |
| 414  | HTTP_414_URI_TOO_LONG              | Request URI is too long. |
| 415  | HTTP_415_UNSUPPORTED_MEDIA_TYPE    | Unsupported media type in request. |
| 416  | HTTP_416_RANGE_NOT_SATISFIABLE     | Requested range not satisfiable. |
| 417  | HTTP_417_EXPECTATION_FAILED        | Expectation in headers failed. |

---

## 🔥 5xx: Server Errors

| Code | Constant                          | Description |
|------|-----------------------------------|-------------|
| 500  | HTTP_500_INTERNAL_SERVER_ERROR    | Server encountered an unexpected error. |
| 501  | HTTP_501_NOT_IMPLEMENTED          | Server does not support the functionality. |
| 502  | HTTP_502_BAD_GATEWAY              | Invalid response from upstream server. |
| 503  | HTTP_503_SERVICE_UNAVAILABLE      | Server is currently unavailable. |
| 504  | HTTP_504_GATEWAY_TIMEOUT          | Timeout from upstream server. |
| 505  | HTTP_505_HTTP_VERSION_NOT_SUPPORTED | HTTP version not supported. |

---

## 📌 Example Usage in FastAPI

```python
from fastapi import FastAPI, HTTPException
from starlette import status

app = FastAPI()

@app.get("/user/{user_id}")
def get_user(user_id: int):
    # If user not found
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User not found"
    )
