"""Simple script to delete collections from Weaviate database.

Usage:
    python cleanup.py                  # Delete all collections (with confirmation)
    python cleanup.py <collection>     # Delete specific collection (with confirmation)
"""

import os
import sys
import weaviate
from dotenv import load_dotenv

load_dotenv()

# Connect to Weaviate
client = weaviate.connect_to_local(
    host=os.getenv("WEAVIATE_HOST"),
    port=os.getenv("WEAVIATE_HTTP_PORT"),
    grpc_port=os.getenv("WEAVIATE_GRPC_PORT"),
)

try:
    # Get all collections
    collections = client.collections.list_all()
    collection_names = list(collections.keys())

    if not collection_names:
        print("No collections found")
        sys.exit(0)

    # Check if specific collection is requested
    if len(sys.argv) > 1:
        target_collection = sys.argv[1]

        # Check if collection exists
        if target_collection not in collection_names:
            print(f"❌ Collection '{target_collection}' not found")
            print(f"\nAvailable collections:")
            for name in collection_names:
                print(f"  - {name}")
            sys.exit(1)

        # Delete specific collection
        print(f"\nTarget collection: {target_collection}")
        response = input(f"\n⚠️  Delete collection '{target_collection}'? (yes/no): ")

        if response.lower() in ["yes", "y"]:
            try:
                client.collections.delete(target_collection)
                print(f"✓ Deleted: {target_collection}")
                print("\n✅ Done!")
            except Exception as e:
                print(f"✗ Failed: {target_collection} - {e}")
                sys.exit(1)
        else:
            print("Cancelled")

    else:
        # Delete all collections
        print(f"\nFound {len(collection_names)} collection(s):")
        for name in collection_names:
            print(f"  - {name}")

        response = input(
            f"\n⚠️  Delete ALL {len(collection_names)} collections? (yes/no): "
        )

        if response.lower() in ["yes", "y"]:
            print("\nDeleting collections...")
            for name in collection_names:
                try:
                    client.collections.delete(name)
                    print(f"✓ Deleted: {name}")
                except Exception as e:
                    print(f"✗ Failed: {name} - {e}")
            print("\n✅ Done!")
        else:
            print("Cancelled")

finally:
    client.close()
