from app.services.database import get_supabase_client


def test_database_connection():
    """Test that we can connect to Supabase"""
    client = get_supabase_client()

    # Try to fetch categories (should exist from schema)
    result = client.table("categories").select("*").execute()

    assert len(result.data) == 8  # We inserted 8 default categories
    print("✅ Database connection successful!")
    print(f"Found {len(result.data)} categories")

    for cat in result.data:
        print(f"  - {cat['icon']} {cat['name']}")


if __name__ == "__main__":
    test_database_connection()
