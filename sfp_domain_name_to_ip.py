# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:         sfp_domain_name_to_ip
# Purpose:      SpiderFoot plug-in for creating new modules.
#
# Author:      Luis Sánchez Mateos
# Based on the template: 	Daniel García Baameiro <dagaba13@gmail.com>
# Created:     04/09/2023
# Copyright:   (c) Luis Sánchez Mateos 2023
# Licence:     GPL
# -------------------------------------------------------------------------------

# Importamos el módulo socket de Python
import socket
from spiderfoot import SpiderFootEvent, SpiderFootPlugin


class sfp_new_module(SpiderFootPlugin):

    meta = {
        'name': "New Module",
        'summary': "Perform a <¿what this module do?>",
        'flags': [""],
        'useCases': [""],
        'categories': ["Passive DNS"]
    }

    # Default options
    opts = {
    }

    # Option descriptions
    optdescs = {
    }

    results = None

    def setup(self, sfc, userOpts=dict()):
        self.sf = sfc
        self.results = self.tempStorage()

        for opt in list(userOpts.keys()):
            self.opts[opt] = userOpts[opt]

    # What events is this module interested in for input
    def watchedEvents(self):
        return ["DOMAIN_NAME", "DOMAIN_NAME_PARENT", "CO_HOSTED_SITE_DOMAIN", 
                "AFFILIATE_DOMAIN_NAME", "SIMILARDOMAIN"]

    # What events this module produces
    # This is to support the end user in selecting modules based on events
    # produced.
    def producedEvents(self):
        return ["IP_ADDRESS"]

    # Handle events sent to this module
    def handleEvent(self, event):
        eventName = event.eventType
        srcModuleName = event.module
        eventData = event.data

        if eventData in self.results:
            return

        self.results[eventData] = True

        self.sf.debug(f"Received event, {eventName}, from {srcModuleName}")

	data = None

        try:
            self.sf.debug(f"We use the data: {eventData}")
            print(f"We use the data: {eventData}")

            # Traducimos el nombre de dominio a su correspondiente dirección IP con un método
            # del módulo socket de Python que importamos al inicio del archivo
            data = socket.gethostbyname(eventData)

            if not data:
                self.sf.error("Unable to perform <ACTION MODULE> on " + eventData)
                return
        except Exception as e:
            self.sf.error("Unable to perform the <ACTION MODULE> on " + eventData + ": " + str(e))
            return

        typ = "IP_ADDRESS"

        evt = SpiderFootEvent(typ, data, self.__name__, event)
        self.notifyListeners(evt)

# End of sfp_new_module class