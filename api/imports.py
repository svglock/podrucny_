import openpyxl

from warehouse.models import Product


def import_products_from_excel(path):

    workbook = openpyxl.load_workbook(path)

    sheet = workbook.active

    for row in sheet.iter_rows(
            min_row=2,
            values_only=True
    ):

        Product.objects.create(
            title=row[0],
            description=row[1],
            price=row[2],
            quantity=row[3]
        )