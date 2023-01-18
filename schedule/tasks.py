from celery import shared_task
from .models import Setup


@shared_task(name="computation_heavy_task_")
def computation_heavy_task(setup_id):
    setup = Setup.objects.get(id=setup_id)
    # Do heavy computation with variables in setup model here.
    print("Running Setup TASK++++++++++++++++++++++++++++++++++++")
    print(f'Running task for setup {setup.title} for id {setup.id}.')
    return 'Done'
