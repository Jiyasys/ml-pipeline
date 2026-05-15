# db/client.py
# ============================================================
# Supabase client — single instance reused across all requests
# ============================================================

import os
from functools import lru_cache

from supabase import Client, create_client
from dotenv import load_dotenv

load_dotenv()


@lru_cache(maxsize=1)
def get_supabase() -> Client:
    """
    Returns a cached Supabase client.
    Called once on first use, reused for every subsequent request.

    Usage in routers:
        from db.client import get_supabase
        sb = get_supabase()
        sb.table("insight_feedback").insert({...}).execute()
    """
    url  = os.environ.get("SUPABASE_URL")
    key  = os.environ.get("SUPABASE_ANON_KEY")

    if not url or not key:
        raise RuntimeError(
            "Missing SUPABASE_URL or SUPABASE_ANON_KEY in environment. "
            "Check your .env file."
        )

    return create_client(url, key)