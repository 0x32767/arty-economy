from aiosqlite import connect, Cursor, Connection
from typing import Tuple, Union, overload
from enum import StrEnum, auto
from types_ import user_id


class Account(StrEnum):
    USER_ID = auto()
    BALANCE = auto()


@overload
async def query_account(
    uid: user_id, shards: Tuple[Union[Account.BALANCE, Account.USER_ID]]
) -> bool:
    ...


@overload
async def query_account(
    uid: user_id,
    shards: Tuple[Union[Account.BALANCE, Account.USER_ID]],
    conn: Connection,
) -> bool:
    ...


@overload
async def query_account(
    uid: user_id,
    shards: Tuple[Union[Account.BALANCE, Account.USER_ID]],
    conn: Connection,
    curr: Cursor,
) -> bool:
    ...


async def query_account(
    uid: user_id,
    shards: Tuple[Union[Account.BALANCE, Account.USER_ID]],
    # If we already have a connection then we don't want to make another one
    conn: Connection,
    curr: Cursor,
) -> Tuple[int] | None:
    if conn == None and curr == None:
        with connect("./account.db") as conn:
            with conn.cursor() as curr:
                await curr.execute(
                    "SELECT ? FROM accounts WHERE uid = ?",
                    (
                        ", ".join(shards),
                        uid,
                    ),
                )
                return await curr.fetchone()

    elif curr == None and isinstance(conn, Connection):
        with conn.cursor() as curr:
            await curr.execute(
                "SELECT ? FROM accounts WHERE uid = ?",
                (
                    ", ".join(shards),
                    uid,
                ),
            )
            return await curr.fetchone()

    elif curr == None and conn == None:
        with connect("./accounts.db") as conn:
            with conn.cursor() as curr:
                await conn.execute(
                    "SELECT ? FROM accounts WHERE uid = ?",
                    (
                        ", ".join(shards),
                        uid,
                    ),
                )
                return await curr.fetchone()

    else:
        return None
