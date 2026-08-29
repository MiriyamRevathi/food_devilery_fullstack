"""HTML & Text Printable Tax Invoice Generator for Orders."""

def generate_order_invoice_html(order):
    """Generate printable HTML Tax Invoice document string."""
    items_rows = ""
    for idx, item in enumerate(order.get('items', []), 1):
        items_rows += f"""
        <tr>
            <td>{idx}</td>
            <td><strong>{item.get('name')}</strong> {f"<small>({item.get('variant')})</small>" if item.get('variant') else ""}</td>
            <td>₹{float(item.get('price', 0.0)):,.2f}</td>
            <td>{item.get('quantity', 1)}</td>
            <td style="text-align: right;">₹{(float(item.get('price', 0.0)) * int(item.get('quantity', 1))):,.2f}</td>
        </tr>
        """

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Invoice - {order.get('order_number')}</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; color: #333; }}
            .invoice-box {{ max-width: 800px; margin: auto; border: 1px solid #eee; padding: 30px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.15); }}
            .flex-between {{ display: flex; justify-content: space-between; align-items: center; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
            th, td {{ padding: 10px; border-bottom: 1px solid #ddd; text-align: left; }}
            th {{ background: #f8f9fa; }}
            .text-right {{ text-align: right; }}
            .total-row {{ font-size: 1.2em; font-weight: bold; color: #fc8019; }}
        </style>
    </head>
    <body>
        <div class="invoice-box">
            <div class="flex-between">
                <div>
                    <h2>🚴‍♂️ FoodFlow Technologies Pvt. Ltd.</h2>
                    <p>Official Tax Invoice & Delivery Bill</p>
                </div>
                <div class="text-right">
                    <h3>{order.get('order_number')}</h3>
                    <p>Date: {order.get('created_at')}</p>
                </div>
            </div>

            <hr>

            <div class="flex-between" style="margin-top: 20px;">
                <div>
                    <strong>Billed To:</strong><br>
                    {order.get('customer_name')}<br>
                    {order.get('customer_phone')}<br>
                    {order.get('delivery_address')}
                </div>
                <div class="text-right">
                    <strong>Restaurant:</strong><br>
                    {order.get('restaurant_name')}<br>
                    GSTIN: 36AAACF1029F1Z4
                </div>
            </div>

            <table>
                <thead>
                    <tr>
                        <th>#</th>
                        <th>Item Description</th>
                        <th>Unit Price</th>
                        <th>Qty</th>
                        <th class="text-right">Amount</th>
                    </tr>
                </thead>
                <tbody>
                    {items_rows}
                </tbody>
            </table>

            <div style="margin-top: 20px; width: 300px; margin-left: auto;">
                <div class="flex-between"><p>Subtotal:</p><p>₹{float(order.get('subtotal', 0.0)):,.2f}</p></div>
                {"<div class='flex-between' style='color: green;'><p>Discount:</p><p>-₹" + f"{float(order.get('discount', 0.0)):,.2f}</p></div>" if float(order.get('discount', 0.0)) > 0 else ""}
                <div class="flex-between"><p>Delivery Fee:</p><p>₹{float(order.get('delivery_fee', 0.0)):,.2f}</p></div>
                <div class="flex-between"><p>GST Tax (5%):</p><p>₹{float(order.get('tax', 0.0)):,.2f}</p></div>
                <hr>
                <div class="flex-between total-row"><p>Total Paid:</p><p>₹{float(order.get('total', 0.0)):,.2f}</p></div>
            </div>

            <div style="margin-top: 40px; text-align: center; font-size: 0.85em; color: #777;">
                <p>Payment Method: {order.get('payment_method')} ({order.get('payment_status')})</p>
                <p>Thank you for ordering with FoodFlow! This is a computer-generated tax invoice.</p>
            </div>
        </div>
    </body>
    </html>
    """
    return html
