"""HTTP server receiving GSI payloads from the CS2 client."""

from __future__ import annotations

import hmac
import inspect
import json
from collections.abc import Awaitable, Callable, Mapping
from types import TracebackType
from typing import Any, TypeAlias

from aiohttp import web

from .exceptions import PayloadError
from .models import GameState
from .parser import GameStateParser

__all__ = ["GSIServer", "GameStateCallback"]

GameStateCallback: TypeAlias = Callable[[GameState], "Awaitable[None] | None"]
"""A sync or async callable invoked with every new :class:`GameState`."""


class GSIServer:
    """Receives GSI payloads over HTTP and notifies subscribers (observer pattern).

    Example::

        server = GSIServer(port=3000, auth_token="secret")

        @server.subscribe
        async def on_update(state: GameState) -> None:
            ...

        server.run()

    :param host: Interface to bind to.
    :param port: Port to listen on; must match the ``uri`` in the GSI ``.cfg`` file.
    :param auth_token: If set, payloads whose ``auth.token`` does not match are
        rejected with ``401``.
    :param path: URL path the game posts to.
    :param parser: Parser used to build :class:`GameState` objects.
    """

    def __init__(
        self,
        host: str = "127.0.0.1",
        port: int = 3000,
        *,
        auth_token: str | None = None,
        path: str = "/",
        parser: GameStateParser | None = None,
    ) -> None:
        self.host = host
        self.port = port
        self.path = path
        self._auth_token = auth_token
        self._parser = parser or GameStateParser()
        self._callbacks: list[GameStateCallback] = []
        self._game_state: GameState | None = None
        self._runner: web.AppRunner | None = None

    # ------------------------------------------------------------------ state

    @property
    def game_state(self) -> GameState | None:
        """The most recently received game state, ``None`` before the first payload."""
        return self._game_state

    @property
    def is_running(self) -> bool:
        """``True`` while started via :meth:`start` and not yet stopped."""
        return self._runner is not None

    # ------------------------------------------------------------------ observers

    def subscribe(self, callback: GameStateCallback) -> GameStateCallback:
        """Register ``callback`` to receive every new game state.

        Returns the callback unchanged, so this method can be used as a decorator.
        Callbacks are invoked sequentially in registration order.
        """
        if callback not in self._callbacks:
            self._callbacks.append(callback)
        return callback

    def unsubscribe(self, callback: GameStateCallback) -> None:
        """Remove a previously registered ``callback``.

        :raises ValueError: if ``callback`` was not registered.
        """
        self._callbacks.remove(callback)

    # ------------------------------------------------------------------ lifecycle

    def create_app(self) -> web.Application:
        """Create the :class:`aiohttp.web.Application`, e.g. for embedding or testing."""
        app = web.Application()
        app.router.add_post(self.path, self._handle_request)
        return app

    def run(self) -> None:
        """Run the server in the current thread, blocking until interrupted."""
        web.run_app(self.create_app(), host=self.host, port=self.port)

    async def start(self) -> None:
        """Start serving in the running event loop without blocking.

        :raises RuntimeError: if the server is already running.
        """
        if self._runner is not None:
            raise RuntimeError("GSIServer is already running")
        runner = web.AppRunner(self.create_app())
        await runner.setup()
        try:
            await web.TCPSite(runner, self.host, self.port).start()
        except BaseException:
            await runner.cleanup()
            raise
        self._runner = runner

    async def stop(self) -> None:
        """Stop a server started with :meth:`start`. Does nothing if not running."""
        if self._runner is None:
            return
        runner, self._runner = self._runner, None
        await runner.cleanup()

    async def __aenter__(self) -> GSIServer:
        await self.start()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        await self.stop()

    # ------------------------------------------------------------------ handling

    async def _handle_request(self, request: web.Request) -> web.Response:
        try:
            payload = json.loads(await request.text())
        except ValueError:
            return web.Response(status=400, text="Invalid JSON")

        if not isinstance(payload, Mapping):
            return web.Response(status=400, text="Payload must be a JSON object")

        if not self._is_authorized(payload):
            return web.Response(status=401, text="Invalid auth token")

        try:
            game_state = self._parser.parse(payload)
        except PayloadError as error:
            return web.Response(status=400, text=str(error))

        self._game_state = game_state
        await self._notify(game_state)
        return web.Response(status=200, text="OK")

    def _is_authorized(self, payload: Mapping[str, Any]) -> bool:
        if self._auth_token is None:
            return True
        auth = payload.get("auth")
        token = auth.get("token") if isinstance(auth, Mapping) else None
        if not isinstance(token, str):
            return False
        return hmac.compare_digest(token.encode(), self._auth_token.encode())

    async def _notify(self, game_state: GameState) -> None:
        for callback in tuple(self._callbacks):
            result = callback(game_state)
            if inspect.isawaitable(result):
                await result
