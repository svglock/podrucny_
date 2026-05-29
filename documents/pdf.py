from reportlab.pdfgen import canvas


def generate_invoice_pdf(invoice, filepath):
    c = canvas.Canvas(filepath)
    c.drawString(100, 750, f'Invoice {invoice.number}')
    c.drawString(100, 720, f'Order #{invoice.order.id}')
    c.drawString(100, 690, f'Total {invoice.order.total_price}')
    c.save()


def generate_shipping_pdf(
        shipping_document,
        filepath
):
    pdf = canvas.Canvas(
        filepath
    )

    pdf.drawString(
        100,
        750,
        'Transport Waybill'
    )

    pdf.drawString(
        100,
        720,
        f'Order #{shipping_document.order.id}'
    )

    pdf.drawString(
        100,
        690,
        f'Route: {shipping_document.route}'
    )

    pdf.save()


def generate_offer_pdf(
        offer,
        filepath
):
    pdf = canvas.Canvas(
        filepath
    )

    pdf.drawString(
        100,
        750,
        'Commercial Offer'
    )

    pdf.drawString(
        100,
        720,
        f'Order #{offer.order.id}'
    )

    pdf.drawString(
        100,
        690,
        f'Amount: {offer.order.total_price}'
    )

    pdf.save()
