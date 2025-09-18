from concurrent.futures import ThreadPoolExecutor, as_completed
import asyncio
from typing import Iterable, List
import math
from .db import get_db
from .models import Account


def _sum_batch(accounts):
    # accounts: list of Account
    return sum(a.balance for a in accounts)


def _partition(seq: List, size: int):
    for i in range(0, len(seq), size):
        yield seq[i:i + size]


def total_balance_thread(batch_size: int = 10) -> float:
    db = get_db()
    accounts = db.query(Account).all()
    batches = list(_partition(accounts, batch_size))
    total = 0.0
    with ThreadPoolExecutor(max_workers=min(8, len(batches))) as ex:
        futures = [ex.submit(_sum_batch, b) for b in batches]
        for f in as_completed(futures):
            total += f.result()
    return float(total)


async def total_balance_async(batch_size: int = 10, concurrency: int = 4) -> float:
    # read accounts synchronously then process batches with async tasks
    db = get_db()
    accounts = db.query(Account).all()
    batches = list(_partition(accounts, batch_size))
    sem = asyncio.Semaphore(concurrency)

    async def worker(batch):
        async with sem:
            # CPU-light sum; run in thread to avoid blocking if heavy.
            loop = asyncio.get_running_loop()
            return await loop.run_in_executor(None, _sum_batch, batch)

    results = await asyncio.gather(*(worker(b) for b in batches))
    return float(sum(results))
