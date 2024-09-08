import auth
from supabase import create_client


url = auth.supabase_url
key = auth.supabase_key
supabase = create_client(url, key)
response = supabase.table("test").select("*").execute()
print(response)