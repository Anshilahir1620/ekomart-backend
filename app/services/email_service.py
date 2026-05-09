import smtplib
from email.mime.text import MIMEText
import os

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")

# def send_order_email(to_email: str, name: str, order_id: int):
#     print("📧 Sending email to:", to_email, "Order:", order_id)
#     msg = MIMEText(f"""
#     <h2>Hello {name}</h2>
#     <p>Your order <b>#{order_id}</b> is confirmed.</p>
#     """, "html")

#     msg["Subject"] = "Order Confirmed"
#     msg["From"] = EMAIL
#     msg["To"] = to_email

#     with smtplib.SMTP("smtp.gmail.com", 587) as server:
#         server.starttls()
#         server.login(EMAIL, PASSWORD)

#         try:
#             server.send_message(msg)
#             print("✅ Email sent successfully to:", to_email)

#         except Exception as e:
#             print("❌ Email failed:", str(e))


def send_order_email(to_email: str, name: str, order):

    print("📧 Sending email to:", to_email)

    # 🧾 Build product table rows
    items_html = ""
    for item in order.items:
        items_html += f"""
        <tr>
            <td>{item.product_name}</td>
            <td>{item.quantity}</td>
            <td>₹{item.price}</td>
            <td>₹{item.price * item.quantity}</td>
        </tr>
        """

    payment_method = ""
    if order.payments and len(order.payments) > 0:
        payment_method = order.payments[0].payment_method

    # 📨 HTML Email
    html_content = f"""
    <html>
    <body style="font-family: Arial; background:#f5f5f5; padding:20px;">
        <div style="max-width:600px;margin:auto;background:white;padding:20px;border-radius:10px;">
            
            <h2 style="color:#28a745;">✅ Order Confirmed</h2>
            <p>Hello <b>{name}</b>,</p>
            <p>Your order has been successfully placed.</p>

            <h3>📦 Order Summary</h3>
            <table width="100%" border="1" cellspacing="0" cellpadding="8" style="border-collapse:collapse;">
                <tr style="background:#eee;">
                    <th>Product</th>
                    <th>Qty</th>
                    <th>Price</th>
                    <th>Total</th>
                </tr>
                {items_html}
            </table>

            <h3>💰 Payment Details</h3>
            <p><b>Method:</b> {payment_method}</p>
            <p><b>Total Amount:</b> ₹{order.total_amount}</p>
            <p><b>Discount:</b> ₹{order.discount_amount}</p>
            <p><b>Final Amount:</b> ₹{order.final_amount}</p>

            <h3>🚚 Shipping Details</h3>
            <p>
                {order.shipping_name}<br>
                {order.shipping_phone}<br>
                {order.shipping_address}, {order.shipping_city}<br>
                {order.shipping_state} - {order.shipping_pincode}
            </p>

            <hr>
            <p style="font-size:12px;color:gray;">
                Thank you for shopping with Ekomart ❤️
            </p>
        </div>
    </body>
    </html>
    """

    msg = MIMEText(html_content, "html")
    msg["Subject"] = "Your Order is Confirmed 🛒"
    msg["From"] = EMAIL
    msg["To"] = to_email

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(EMAIL, PASSWORD)

        try:
            server.send_message(msg)
            print("✅ Email sent successfully")
        except Exception as e:
            print("❌ Email failed:", str(e))