# -*- coding: utf-8 -*-
default_profile = 'profile-collective.clamav:default'


def upgrade_site(setup):
    setup.runImportStepFromProfile(default_profile, 'plone.app.registry')
