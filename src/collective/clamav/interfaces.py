"""Module where all interfaces, events and exceptions live."""

from collective.clamav import _
from zope import schema
from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


class ICollectiveClamavLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


clamdConnectionType = SimpleVocabulary(
    [SimpleTerm(title='Unix Socket', value='socket'),
     SimpleTerm(title='Network', value='net')],
)


class IAVScannerSettings(Interface):
    """ Schema for the clamav settings
    """
    clamav_connection = schema.Choice(
        title=_('Connection type to clamd'),
        description=_('Choose whether clamd is accessible through local '
                      'UNIX sockets or network.'),
        vocabulary=clamdConnectionType)

    clamav_socket = schema.ASCIILine(
        title=_('Clamd local socket file'),
        description=_('If connected to clamd through local UNIX sockets, '
                      'the path to the local socket file.'),
        default='/var/run/clamd',
        required=True)

    clamav_host = schema.ASCIILine(title=_('Scanner host'),
                                   description=_('If connected to clamd '
                                                 'through the network, '
                                                 'the host running clamd.'),
                                   default='localhost',
                                   required=True)

    clamav_port = schema.Int(title=_('Scanner port'),
                             description=_('If connected to clamd '
                                           'through the network, the '
                                           'port on which clamd listens.'),
                             default=3310,
                             required=True)

    clamav_timeout = schema.Int(title=_('Timeout'),
                                description=_('The timeout in seconds for '
                                              'communication with clamd.'),
                                default=120,
                                required=True)


class IAVScanner(Interface):
    def ping():
        pass

    def scanBuffer(buffer):
        pass
