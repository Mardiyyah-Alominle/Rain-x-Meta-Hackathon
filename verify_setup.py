import sys
import os

# Add current directory to path
sys.path.append(os.getcwd())

print("Verifying imports...")

try:
    from utils.db import db
    print("✅ utils.db imported")
except ImportError as e:
    print(f"❌ utils.db import failed: {e}")

try:
    from tools.shop_ops import product_lookup_tool
    print("✅ tools.shop_ops imported")
except ImportError as e:
    print(f"❌ tools.shop_ops import failed: {e}")

try:
    from tools.order_ops import signal_order_finalization
    print("✅ tools.order_ops imported")
except ImportError as e:
    print(f"❌ tools.order_ops import failed: {e}")

try:
    from agents.sales_agent import sales_associate_node
    print("✅ agents.sales_agent imported")
except ImportError as e:
    print(f"❌ agents.sales_agent import failed: {e}")

try:
    from workflows.shop_flow import app
    print("✅ workflows.shop_flow imported")
except ImportError as e:
    print(f"❌ workflows.shop_flow import failed: {e}")

print("Verification complete.")
