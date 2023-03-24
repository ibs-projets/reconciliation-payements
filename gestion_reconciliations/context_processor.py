from gestion_reconciliations.forms import AssocierCompteMagasinForm


def compteform(request):
    return {"compteform":AssocierCompteMagasinForm()}