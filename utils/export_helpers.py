"""Data Export Helpers for CSV/JSON Reports Generation."""
import csv
import io
import json

def export_orders_to_csv(orders):
    """Convert orders list to CSV formatted string for download."""
    output = io.StringIO()
    writer = csv.writer(output)

    # Header
    writer.writerow([
        'Order Number', 'Date', 'Customer Name', 'Customer Phone',
        'Restaurant Name', 'Item Count', 'Subtotal', 'Discount',
        'Delivery Fee', 'Tax', 'Total Amount', 'Status', 'Payment Method'
    ])

    for o in orders:
        writer.writerow([
            o.get('order_number'),
            o.get('created_at'),
            o.get('customer_name'),
            o.get('customer_phone'),
            o.get('restaurant_name'),
            len(o.get('items', [])),
            o.get('subtotal'),
            o.get('discount'),
            o.get('delivery_fee'),
            o.get('tax'),
            o.get('total'),
            o.get('status'),
            o.get('payment_method')
        ])

    return output.getvalue()

def export_menu_to_json(foods):
    """Export food menu items to formatted JSON string."""
    return json.dumps(foods, indent=2)
