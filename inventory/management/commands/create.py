from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
from inventory.models import Product, ProductLot, Warehouse, InventoryBay, InventoryBayLot


class Command(BaseCommand):

    def print_help(self, prog_name, subcommand):
        help_message = """
        Create Help Menu
        ===================

        Create a new Product, ProductLot, Warehouse, InventoryBay, or
        InventoryBayLot with history tracking.

        Usage:
          python manage.py create [model] [args] --username=[user]

        Models:

          product:
            Usage:
              python manage.py create product [name] [description] \\
                      --username=[user]
            Arguments:
              name                  Name of the product being created.
              description           Short description of the product.

          lot:
            Usage:
              python manage.py create lot [lot number] [internal reference] \\
                    --product=[product] --quantity=[quantity] --username=[user]
            Arguments:
              lot number            Name of lot
              internal reference    Internal reference of lot
              product               Product tied to lot
              quantity              Quantity (defaults to 0)

          warehouse:
            Usage:
              python manage.py create warehouse [name] --active=[active]
            Arguments:
              name                  Name of the warehouse
              active                Active status of the warehouse (defaults to True)

          bay:
            Usage:
              python manage.py create bay [name] [warehouse] \\
                      --max_unique_lots=[max_unique_lots] --active=[active] \\
                      --user=[user]
            Arguments:
              name                  Name of the bay
              warehouse             Name of the warehouse
              max_unique_lot        Maximum number of unique lots per bay (defaults to 1)
              active                Active status of the bay (defaults to True)

          bay_lot:
            Usage:
              python manage.py create bay_lot [lot number] [bay] \\
                      --quantity=[quantity] --user=[user]
            Arguments:
              lot number            Name of lot
              bay                   Name of the destination bay
              quantity              Quantity of lot in bay (defaults to 0)

        """
        self.stdout.write(help_message)

    def add_arguments(self, parser):
        parser.add_argument('model', type=str)
        parser.add_argument('name_or_lot', type=str)
        parser.add_argument('description_or_internal_ref', type=str, nargs='?')
        parser.add_argument('--product', type=str)
        parser.add_argument('--quantity', type=int, default=0)
        parser.add_argument('--active', type=bool, default=True)
        parser.add_argument('--warehouse_name', type=str)
        parser.add_argument('--friendly_name', type=str)
        parser.add_argument('--max_unique_lots', type=int, default=1)
        parser.add_argument('--inventory_bay_name', type=str)
        parser.add_argument('--product_lot_number', type=str)
        parser.add_argument('--user', type=str, required=True)

    def handle(self, *args, **kwargs):
        model = kwargs['model'].lower()
        name_or_lot = kwargs['name_or_lot']
        description_or_internal_ref = kwargs.get('description_or_internal_ref')
        username = kwargs['user']

        User = get_user_model()
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(
                f'User "{username}" does not exist'))
            return

        if model == 'product':
            product = Product.objects.create(
                name=name_or_lot,
                description=description_or_internal_ref
            )
            product._history_user = user
            product.save()

            self.stdout.write(self.style.SUCCESS(
                f"Product '{name_or_lot}' created successfully!"))

        elif model == 'lot':
            product_name = kwargs.get('product')
            quantity = kwargs.get('quantity', 0)
            if not product_name:
                raise CommandError(
                    "The '--product' argument is required for creating a ProductLot.")
            try:
                product = Product.objects.get(name=product_name)
            except Product.DoesNotExist:
                raise CommandError(f"Product with name '{
                                   product_name}' does not exist.")
            if ProductLot.objects.filter(
                lot_number=name_or_lot,
                internal_reference=description_or_internal_ref
            ).exists():
                product_lot = ProductLot.objects.get(
                    lot_number=name_or_lot,
                    internal_reference=description_or_internal_ref
                )
                product_lot.quantity += quantity
                product_lot._history_user = user
                product_lot.save()

                self.stdout.write(self.style.SUCCESS(
                    f"ProductLot '{name_or_lot}' created successfully!"))
            else:
                if ProductLot.objects.filter(lot_number=name_or_lot).exists():
                    raise CommandError(f"A lot with the number '{
                                       name_or_lot}' already exists.")
                if ProductLot.objects.filter(internal_reference=description_or_internal_ref).exists():
                    raise CommandError(f"A lot with the internal reference '{
                                       description_or_internal_ref}' already exists.")

                product_lot = ProductLot(
                    lot_number=name_or_lot,
                    internal_reference=description_or_internal_ref,
                    product_name=product,
                    quantity=quantity,
                )
                product_lot._history_user = user
                product_lot.save()

                self.stdout.write(self.style.SUCCESS(
                    f"ProductLot '{name_or_lot}' created successfully!"))

        elif model == 'warehouse':
            active = kwargs.get('active', True)
            if Warehouse.objects.filter(name=name_or_lot).exists():
                raise CommandError(f"A warehouse with the name '{
                                   name_or_lot}' already exists.")

            warehouse = Warehouse(name=name_or_lot, active=active)
            warehouse._history_user = user
            warehouse.save()

            self.stdout.write(self.style.SUCCESS(
                f"Warehouse '{name_or_lot}' created successfully!"))

        elif model == 'bay':
            friendly_name = kwargs.get('friendly_name', f'x-{name_or_lot}')
            max_unique_lots = kwargs.get('max_unique_lots', 1)
            active = kwargs.get('active', True)

            if not description_or_internal_ref:
                raise CommandError(
                    "The 'warehouse' argument is required for creating an InventoryBay.")
            try:
                warehouse = Warehouse.objects.get(
                    name=description_or_internal_ref)
            except Warehouse.DoesNotExist:
                raise CommandError(f"Warehouse with name '{
                                   description_or_internal_ref}' does not exist.")
            if InventoryBay.objects.filter(name=name_or_lot).exists():
                raise CommandError(f"An InventoryBay with the name '{
                                   name_or_lot}' already exists.")
            if InventoryBay.objects.filter(friendly_name=friendly_name).exists():
                raise CommandError(f"An InventoryBay with the friendly name '{
                                   friendly_name}' already exists.")
            inventory_bay = InventoryBay(
                name=name_or_lot,
                warehouse_name=warehouse,
                max_unique_lots=max_unique_lots,
                friendly_name=friendly_name,
                active=active,
            )
            inventory_bay._history_user = user
            inventory_bay.save()
            self.stdout.write(self.style.SUCCESS(
                f"InventoryBay '{name_or_lot}' created successfully!"))

        elif model == 'bay_lot':
            quantity = kwargs.get('quantity', 0)
            try:
                inventory_bay = InventoryBay.objects.get(
                    name=name_or_lot)
            except InventoryBay.DoesNotExist:
                raise CommandError(f"InventoryBay with name '{
                                   name_or_lot}' does not exist.")
            try:
                product_lot = ProductLot.objects.get(
                    lot_number=description_or_internal_ref)
            except ProductLot.DoesNotExist:
                raise CommandError(f"ProductLot with lot number '{
                                   description_or_internal_ref}' does not exist.")
            if InventoryBayLot.objects.filter(inventory_bay=inventory_bay, product_lot=product_lot).exists():
                inventory_bay_lot = InventoryBayLot.objects.get(inventory_bay=inventory_bay, product_lot=product_lot)
                inventory_bay_lot.quantity += quantity
                inventory_bay_lot._history_user = user
                inventory_bay_lot.save()
            else:
                inventory_bay_lot = InventoryBayLot(
                    inventory_bay=inventory_bay,
                    product_lot=product_lot,
                    quantity=quantity,
                )
                inventory_bay_lot._history_user = user
                inventory_bay_lot.save()
            self.stdout.write(self.style.SUCCESS(f"InventoryBayLot with '{
                              description_or_internal_ref}' in '{name_or_lot}' created successfully!"))

        else:
            raise CommandError(
                "Invalid model. Use 'product', 'lot', 'warehouse', 'inventory_bay', or 'inventory_bay_lot'.")
