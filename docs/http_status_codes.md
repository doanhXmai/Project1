# HTTP Status Codes

## 1xx – Informational
| Status | Message             | Ý nghĩa                        |
|--------|---------------------|--------------------------------|
| 100    | Continue            | Máy khách tiếp tục gửi request |
| 101    | Switching Protocols | Chuyển giao thức theo yêu cầu  |
| 102    | Processing          | Server đang xử lý              |
| 103    | Early Hints         | Header preload                 |

## 2xx – Success
| Status  | Message                       | Ý nghĩa                  |
|---------|-------------------------------|--------------------------|
| 200     | OK                            | Thành công               |
| 201     | Created                       | Tạo mới thành công       |
| 202     | Accepted                      | Đã nhận nhưng chưa xử lý |
| 203     | Non-Authoritative Information | Thông tin từ nguồn khác  |
| 204     | No Content                    | Không trả body           |
| 205     | Reset Content                 | Reset form               |
| 206     | Partial Content               | Trả một phần dữ liệu     |

## 3xx – Redirection
| Status  | Message            | Ý nghĩa                        |
|---------|--------------------|--------------------------------|
| 300     | Multiple Choices   | Nhiều lựa chọn                 |
| 301     | Moved Permanently  | Chuyển hướng vĩnh viễn         |
| 302     | Found              | Chuyển hướng tạm               |
| 303     | See Other          | Điều hướng đến tài nguyên khác |
| 304     | Not Modified       | Cache                          |
| 307     | Temporary Redirect | Chuyển hướng tạm, giữ method   |
| 308     | Permanent Redirect | Chuyển hướng vĩnh viễn         |

## 4xx – Client Errors
| Status  | Message                | Ý nghĩa                  |
|---------|------------------------|--------------------------|
| 400     | Bad Request            | Request sai định dạng    |
| 401     | Unauthorized           | Thiếu hoặc sai token     |
| 403     | Forbidden              | Không có quyền           |
| 404     | Not Found              | Không tìm thấy           |
| 405     | Method Not Allowed     | Sai method               |
| 406     | Not Acceptable         | Không trả format yêu cầu |
| 408     | Request Timeout        | Hết thời gian chờ        |
| 409     | Conflict               | Xung đột dữ liệu         |
| 410     | Gone                   | Không còn tồn tại        |
| 413     | Payload Too Large      | File quá lớn             |
| 414     | URI Too Long           | URL quá dài              |
| 415     | Unsupported Media Type | Sai content-type         |
| 422     | Unprocessable Entity   | Không xử lý được dữ liệu |
| 429     | Too Many Requests      | Quá nhiều request        |

## 5xx – Server Errors
| Status  | Message               | Ý nghĩa                   |
|---------|-----------------------|---------------------------|
| 500     | Internal Server Error | Lỗi server                |
| 501     | Not Implemented       | Chưa hỗ trợ               |
| 502     | Bad Gateway           | Gateway nhận response lỗi |
| 503     | Service Unavailable   | Bảo trì / quá tải         |
| 504     | Gateway Timeout       | Gateway hết thời gian chờ |