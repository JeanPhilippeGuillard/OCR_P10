#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os

""" Bot Configuration """


class DefaultConfig:
    """ Bot Configuration """

    PORT = 3978
    APP_ID = os.environ.get("MicrosoftAppId", "")
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "")
    #LUIS_APP_ID = os.environ.get("LuisAppId", "536910f3-7d68-4ec9-b0d8-d8f4bdf46f4f") # FlightBooking-v5
    LUIS_APP_ID = os.environ.get("LuisAppId", "631685be-cc61-45bc-b327-ee93bf1cdeca") # FlightBooking-v5-SDK
    LUIS_API_KEY = os.environ.get("LuisAPIKey", "726d4526485546eea8d2331a5e017ac8") # jpg-cognitive-predicion
    # LUIS endpoint host name, ie "westus.api.cognitive.microsoft.com"
    LUIS_API_HOST_NAME = os.environ.get("LuisAPIHostName", "westeurope.api.cognitive.microsoft.com")
