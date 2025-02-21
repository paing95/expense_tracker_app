from django.core.management.base import BaseCommand
from expense_tracker import models
import log_helper

logger = log_helper.getLogger('Setup Initial Data')

def setup_expense_types(expense_types):
    expense_type_objects = []
    for expense_type in expense_types:
        if not models.ExpenseType.objects.filter(name=expense_type).exists():
            expense_type_object = models.ExpenseType()
            expense_type_object.name = expense_type
            expense_type_objects.append(expense_type_object)
    if expense_type_objects:
        logger.debug(f'Bulk inserting {len(expense_type_objects)} Expense Type records')
        models.ExpenseType.objects.bulk_create(expense_type_objects)
    
def setup_income_types(income_types):
    income_type_objects = []
    for income_type in income_types:
        if not models.IncomeType.objects.filter(name=income_type).exists():
            income_type_object = models.IncomeType()
            income_type_object.name = income_type
            income_type_objects.append(income_type_object)
    if income_type_objects:
        logger.debug(f'Bulk inserting {len(income_type_objects)} Income Type records')
        models.IncomeType.objects.bulk_create(income_type_objects)
    
def setup_places(places):
    place_objects = []
    for place in places:
        if not models.Place.objects.filter(name=place).exists():
            place_object = models.Place()
            place_object.name = place
            place_objects.append(place_object)
    if place_objects:
        logger.debug(f'Bulk inserting {len(place_objects)} Place records')
        models.Place.objects.bulk_create(place_objects)

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        try:
            logger.debug('Running setup init data script...')
            # Setup Expense Types
            data = []
            setup_expense_types(data)

            # Setup Income Types
            data = []
            setup_income_types(data)

            # Setup Places
            data = []
            setup_places(data)

        except Exception as e:
            logger.error(f'Error running setup init data script: {e}')

        finally:
            logger.debug('Finished running setup init data script...')