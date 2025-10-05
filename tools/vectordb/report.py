"""Simple script to generate a report of all Weaviate collections and their record counts."""

import os
import sys
import weaviate
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# Connect to Weaviate
print("Connecting to Weaviate...", flush=True)
try:
    client = weaviate.connect_to_local(
        host=os.getenv("WEAVIATE_HOST"),
        port=os.getenv("WEAVIATE_HTTP_PORT"),
        grpc_port=os.getenv("WEAVIATE_GRPC_PORT"),
    )
    print("✓ Connected successfully", flush=True)
except Exception as e:
    print(f"✗ Failed to connect: {e}", flush=True)
    sys.exit(1)

try:
    # Get all collections
    print("Fetching collections...", flush=True)
    collections = client.collections.list_all()
    collection_names = list(collections.keys())
    print(f"Found {len(collection_names)} collections", flush=True)

    # Generate report
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    report_filename = f"weaviate_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

    print(f"Generating report: {report_filename}", flush=True)

    total_objects = 0

    with open(report_filename, "w", encoding="utf-8") as f:
        # Header
        f.write("=" * 60 + "\n")
        f.write("Weaviate Collections Report\n")
        f.write(f"Generated: {timestamp}\n")
        f.write("=" * 60 + "\n\n")

        if not collection_names:
            f.write("No collections found\n")
            print("No collections found", flush=True)
        else:
            f.write(f"Total Collections: {len(collection_names)}\n\n")

            # List each collection with object count
            for i, name in enumerate(collection_names, 1):
                try:
                    collection = client.collections.get(name)
                    # Get total count using aggregate
                    result = collection.aggregate.over_all(total_count=True)
                    count = result.total_count
                    total_objects += count

                    f.write(f"{i}. {name}\n")
                    f.write(f"   Objects: {count:,}\n\n")

                    print(f"✓ {name}: {count:,} objects", flush=True)

                except Exception as e:
                    f.write(f"{i}. {name}\n")
                    f.write(f"   Error: {e}\n\n")
                    print(f"✗ {name}: Error - {e}", flush=True)

            # Summary
            f.write("-" * 60 + "\n")
            f.write(f"Total Objects: {total_objects:,}\n")
            f.write("=" * 60 + "\n")

    print(f"\n✅ Report saved to: {report_filename}", flush=True)
    print(f"Total collections: {len(collection_names)}", flush=True)
    print(f"Total objects: {total_objects:,}", flush=True)

except Exception as e:
    print(f"\n✗ Error: {e}", flush=True)
    import traceback

    traceback.print_exc()
finally:
    print("Closing connection...", flush=True)
    client.close()
    print("Done!", flush=True)
