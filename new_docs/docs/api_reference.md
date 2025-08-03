# API 参考

Proxy Pool 通过一个轻量级的 Flask Web 应用提供 HTTP API，方便你快速地获取和管理代理。

## 获取一个代理

-   **URL**: `/get/`
-   **Method**: `GET`
-   **Description**: 随机从代理池中获取一个可用代理。
-   **URL Params**:
    -   `type` (optional): `https` 或空。如果设置为 `https`，则只返回支持 HTTPS 的代理。
-   **Success Response**:
    -   **Code**: `200`
    -   **Content**:
        ```json
        {
          "proxy": "123.45.67.89:8080",
          "https" : true,
          "source": "freeProxy01",
          "region": "中国 上海",
          "fail_count": 0,
          "last_time": "2025-08-03 09:10:00"
        }
        ```
-   **Error Response (无可用代理)**:
    -   **Code**: `200`
    -   **Content**: `{"code": 0, "src": "no proxy"}`

## 获取并删除一个代理

-   **URL**: `/pop/`
-   **Method**: `GET`
-   **Description**: 从代理池中获取一个代理，并立即将其删除，以确保该代理只被使用一次。
-   **URL Params**:
    -   `type` (optional): `https` 或空。
-   **Success Response**: 同 `/get/`。
-   **Error Response (无可用代理)**: 同 `/get/`。

## 删除一个代理

-   **URL**: `/delete/`
-   **Method**: `GET`
-   **Description**: 当你发现一个代理不可用时，可以通过这个接口将其从代理池中删除。
-   **URL Params**:
    -   `proxy` (required): 需要删除的代理，格式为 `ip:port`。例如: `127.0.0.1:8080`。
-   **Success Response**:
    -   **Code**: `200`
    -   **Content**: `{"code": 0, "src": "delete proxy success"}`

## 获取所有代理

-   **URL**: `/all/`
-   **Method**: `GET`
-   **Description**: 获取代理池中的所有代理信息。
-   **URL Params**:
    -   `type` (optional): `https` 或空。
-   **Success Response**:
    -   **Code**: `200`
    -   **Content**:
        ```json
        [
          {
            "proxy": "123.45.67.89:8080",
            "https": true,
            "source": "freeProxy01",
            "region": "中国 上海",
            "fail_count": 0,
            "last_time": "2025-08-03 09:10:00"
          },
          {
            "proxy": "98.76.54.32:443",
            "https": false,
            "source": "freeProxy02",
            "region": "美国 加州",
            "fail_count": 1,
            "last_time": "2025-08-03 09:05:30"
          }
        ]
        ```

## 获取代理数量统计

-   **URL**: `/count/`
-   **Method**: `GET`
-   **Description**: 返回代理池中代理的总数、按类型（HTTP/HTTPS）和来源的详细统计信息。
-   **Success Response**:
    -   **Code**: `200`
    -   **Content**:
        ```json
        {
          "count": 120,
          "http_type": {
            "http": 80,
            "https": 40
          },
          "source": {
            "freeProxy01": 50,
            "freeProxy02": 70
          }
        }