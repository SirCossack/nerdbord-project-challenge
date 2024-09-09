from . import auth
from supabase import create_client


url = auth.supabase_url
key = auth.supabase_key
supabase = create_client(url, key)
