import threading
import queue
from typing import Optional
from sqlalchemy.orm import Session
from .db import get_session
from .processing_worker import process_insight


_q: "queue.Queue[str]" = queue.Queue()
_worker_started = False


def _worker_loop():
    while True:
        insight_id = _q.get()
        try:
            session: Session = next(get_session())
            process_insight(session, insight_id)
        except Exception:
            pass
        finally:
            _q.task_done()


def start_worker_once():
    global _worker_started
    if _worker_started:
        return
    t = threading.Thread(target=_worker_loop, daemon=True)
    t.start()
    _worker_started = True


def enqueue_insight(insight_id: str):
    _q.put(insight_id)

