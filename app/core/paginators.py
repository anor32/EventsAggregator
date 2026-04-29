from urllib.parse import urlencode

from httpx import AsyncClient, Response


class ApiPaginator:
    def __init__(
        self,
        count_objects: int,
        path: str,
        base_url: str,
        page=1,
        page_size=20,
    ):
        self._base_url = base_url
        self.page = page
        self.page_size = page_size
        self._next_url = ""
        self.previous_url = ""
        self.count_objects = count_objects
        self.max_pages = (count_objects + page_size - 1) // page_size
        self.path = path

    def get_next_url(self) -> str | None:
        if self.page >= self.max_pages:
            return None
        params = {"page": self.page + 1, "page_size": self.page_size}
        query = urlencode(params)
        self._next_url = f"{self._base_url}{self.path}?{query}"
        return self._next_url

    def get_previous_url(self) -> str | None:
        if self.page - 1 < 1:
            return None
        params = {"page": self.page - 1, "page_size": self.page_size}
        query = urlencode(params)
        self.previous_url = f"{self._base_url}{self.path}?{query}"
        return self.previous_url


class ClientEventsPaginator:
    def __init__(
        self,
        url: str,
        client: AsyncClient,
        headers: dict,
    ):
        self.headers = headers
        self.client = client
        self.url = url

    def __aiter__(self):
        return self

    async def __anext__(self) -> Response | None:
        if not self.url:
            raise StopAsyncIteration
        response = await self.client.get(
            url=self.url, headers=self.headers, follow_redirects=True
        )
        if response.json().get("next"):
            self.url = response.json().get("next")
        else:
            self.url = None

        return response
