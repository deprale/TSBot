from __future__ import annotations

from dataclasses import dataclass
from typing import Generator, TypeVar

from tsbot import utils

_T = TypeVar("_T", bound="TSResponse")


@dataclass(slots=True, frozen=True)
class TSResponse:
    """
    Class to represent the response to a query from a Teamspeak server.
    """

    data: list[dict[str, str]]
    error_id: int
    msg: str

    def __iter__(self) -> Generator[dict[str, str], None, None]:
        yield from self.data

    @property
    def first(self) -> dict[str, str]:
        """First datapoint from the response"""
        return self.data[0]

    @property
    def last(self) -> dict[str, str]:
        """Last datapoint from the response"""
        return self.data[-1]

    @classmethod
    def from_server_response(cls: type[_T], raw_data: list[str]) -> _T:
        response_info = utils.parse_line(raw_data[-1].removeprefix("error "))
        data = utils.parse_data("".join(raw_data[:-1]))

        error_id = int(response_info.pop("id"))
        msg = response_info.pop("msg")

        if response_info:
            data.append(response_info)

        return cls(data=data, error_id=error_id, msg=msg)
