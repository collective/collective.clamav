from collective.clamav import _
from collective.clamav.interfaces import IAVScannerSettings
from plone.app.registry.browser import controlpanel


class ClamavControlPanelForm(controlpanel.RegistryEditForm):
    schema = IAVScannerSettings
    label = _('Clamav Plone Settings')
    description = _("""""")

    def updateFields(self):
        super().updateFields()

    def updateWidgets(self):
        super().updateWidgets()


class ClamavControlPanelView(controlpanel.ControlPanelFormWrapper):
    form = ClamavControlPanelForm
