from App.config import getConfiguration
from collective.clamav.interfaces import IAVScanner
from collective.clamav.interfaces import IAVScannerSettings
from collective.clamav.scanner import ScanError
from plone.registry.interfaces import IRegistry
from Products.validation.interfaces.IValidator import IValidator
from z3c.form.interfaces import NOT_CHANGED
from zope.component import getUtility
from zope.interface import implementer
from zope.interface import Invalid

import logging


logger = logging.getLogger("collective.clamav")


def _scanBuffer(buffer):
    if getConfiguration().debug_mode:  # pragma: no cover
        logger.warning("Skipping virus scan in development mode.")
        return ""

    registry = getUtility(IRegistry)
    settings = registry.forInterface(IAVScannerSettings)  # noqa: P001
    if settings is None:
        return ""
    scanner = getUtility(IAVScanner)

    if settings.clamav_connection == "net":
        result = scanner.scanBuffer(
            buffer,
            "net",
            host=settings.clamav_host,
            port=int(settings.clamav_port),
            timeout=float(settings.clamav_timeout),
        )
    else:
        result = scanner.scanBuffer(
            buffer,
            "socket",
            socketpath=settings.clamav_socket,
            timeout=float(settings.clamav_timeout),
        )

    return result


@implementer(IValidator)
class ClamavValidator:
    """Dexterity content types validator to confirm a file upload
    is virus-free."""

    def __init__(self, name):
        self.name = name

    def __call__(self, value, *args, **kwargs):
        if hasattr(value, "seek"):  # noqa: P002
            # when submitted a new file 'value' is a
            # 'ZPublisher.HTTPRequest.FileUpload'

            if getattr(value, "_validate_isVirusFree", False):
                # validation is called multiple times for the same file upload
                return True

            value.seek(0)
            # TODO this reads the entire file into memory, there should be  # noqa: T000,E501
            # a smarter way to do this
            content = value.read()
            result = ""
            try:
                result = _scanBuffer(content)
            except ScanError as e:
                logger.error(f"ScanError {e} on {value.filename}.")
                return (
                    "There was an error while checking the file for "
                    "viruses: Please contact your system administrator."
                )

            if result:
                return f"Validation failed, file is virus-infected. ({result})"  # noqa: E501
            else:
                # mark the file upload instance as already checked
                value._validate_isVirusFree = True
                return True
        else:
            # if we kept existing file
            return True


try:
    from plone.formwidget.namedfile.interfaces import INamedFileWidget
    from plone.formwidget.namedfile.validator import NamedFileWidgetValidator
    from plone.namedfile.interfaces import INamedField
    from z3c.form import validator
except ImportError:
    pass
else:

    class Z3CFormclamavValidator(NamedFileWidgetValidator):
        """z3c.form validator to confirm a file upload is virus-free."""

        def validate(self, value):
            super().validate(value)

            if getattr(value, "_validate_isVirusFree", False) or value is None:
                # validation is called multiple times for the same file upload
                return

            if value is NOT_CHANGED:
                return

            # TODO this reads the entire file into memory, there should be  # noqa: T000,E501
            # a smarter way to do this
            result = ""
            try:
                result = _scanBuffer(value.data)
            except ScanError as e:
                logger.error(f"ScanError {e} on {value.filename}.")
                raise Invalid(
                    "There was an error while checking "
                    "the file for viruses: Please "
                    "contact your system administrator."
                )

            if result:
                raise Invalid(
                    f"Validation failed, file is virus-infected. (i{result})"
                )  # noqa: E501
            else:
                # mark the file instance as already checked
                value._validate_isVirusFree = True

    validator.WidgetValidatorDiscriminators(
        Z3CFormclamavValidator, field=INamedField, widget=INamedFileWidget
    )
