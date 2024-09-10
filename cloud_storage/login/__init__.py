import os
from supabase import create_client

url = os.getenv("supabase_url")
key = os.getenv("supabase_key")
supabase = create_client(url, key)
