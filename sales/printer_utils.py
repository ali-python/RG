# printer_utils.py

from escpos.printer import Usb

def print_receipt(invoice):
    try:
        # Replace with your printer's Vendor ID and Product ID
        p = Usb(0x0416, 0x5011, 0, timeout=0, in_ep=0x82, out_ep=0x01)

        p.set(align='center', width=2)
        p.text("RadiGull Traders\n")
        p.text("--------- Invoice ---------\n\n")

        p.set(align='left', width=1)

        if invoice.customer:
            p.text(f"Customer: {invoice.customer.name}\n")
            p.text(f"Mobile: {invoice.customer.mobile}\n")
            p.text(f"CNIC: {invoice.customer.cnic}\n")

        p.text(f"Date: {invoice.date.strftime('%d-%m-%Y')}\n")
        p.text(f"Payment: {invoice.payment_type}\n")
        p.text(f"Receipt #: {str(invoice.id).zfill(7)}\n")
        p.text("-" * 32 + "\n")

        for item in invoice.invoice_purchased.all():
            name = f"{item.item.name} {item.item.category}"
            qty = item.quantity
            total = item.purchase_amount
            p.text(f"{name[:24]}\n")
            p.text(f"  Qty: {qty}  Total: {total:.2f}\n")

        p.text("-" * 32 + "\n")
        p.text(f"Total Qty: {invoice.total_quantity}\n")
        p.text(f"Grand Total: {invoice.grand_total:.2f}\n")
        p.text(f"Cash: {invoice.cash_payment:.2f}\n")
        p.text(f"Returned: {invoice.returned_payment:.2f}\n")
        p.text(f"Received: {invoice.paid_amount:.2f}\n")
        p.text(f"Remaining: {invoice.remaining_payment:.2f}\n")
        p.text("\n")

        if invoice.barcode:
            p.barcode(invoice.barcode, 'EAN13', width=2, height=60)

        p.text("\nThank you for your business\n\n")

        p.cut()

    except Exception as e:
        print(f"[ERROR] Print failed: {e}")
