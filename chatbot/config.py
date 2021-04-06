#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os

""" Bot Configuration """


class DefaultConfig:
    """ Bot Configuration """

    PORT = 3978
    #APP_ID = os.environ.get("MicrosoftAppId", "") # for test with the emulator
    #APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "") # for test with the emulator
    APP_ID = os.environ.get("MicrosoftAppId", "ab78726f-f700-4ff0-b4b8-dbe453a8c949") # jpg-flightbooking-service
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "JPG_flightbooking_bot_1") # jpg-flightbooking-service
    
    LUIS_APP_ID = os.environ.get("LuisAppId", "2ab9cc99-4a8f-465e-8e5a-88356c84dc84") # FlightBooking-v13-SDK
    LUIS_API_KEY = os.environ.get("LuisAPIKey", "39e2caa19666427ebe7835c12e70fbd5") # jpg-luis-2-authoring
    INSTRUMENTATION_KEY = os.environ.get("INSTRUMENTATION_KEY", "51e36b9b-70cc-41c1-b656-4203b1d62b62") # jpg-flightbooking-v1

    # LUIS endpoint host name, ie "westus.api.cognitive.microsoft.com"
    LUIS_API_HOST_NAME = os.environ.get("LuisAPIHostName", "westeurope.api.cognitive.microsoft.com")

    
