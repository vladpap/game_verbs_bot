# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START apikeys_create_api_key]

import json

from environs import Env
from google.cloud import api_keys_v2
from google.cloud.api_keys_v2 import Key


def create_api_key(project_id: str, suffix: str) -> Key:
    """
    Creates and restrict an API key. Add the suffix for uniqueness.

    TODO(Developer):
    1. Before running this sample,
      set up ADC as described
      in https://cloud.google.com/docs/authentication/external/set-up-adc
    2. Make sure you have the necessary permission to create API keys.

    Args:
        project_id: Google Cloud project id.

    Returns:
        response: Returns the created API Key.
    """
    # Create the API Keys client.
    client = api_keys_v2.ApiKeysClient()

    key = api_keys_v2.Key()
    key.display_name = f"My first API key - {suffix}"

    # Initialize request and set arguments.
    request = api_keys_v2.CreateKeyRequest()
    request.parent = f"projects/{project_id}/locations/global"
    request.key = key

    # Make the request and wait for the operation to complete.
    response = client.create_key(request=request).result()

    print(f"Successfully created an API key: {response.name}")
    # For authenticating with the API key,
    # use the value in "response.key_string".
    # To restrict the usage of this API key, use the value in "response.name".
    return response

# [END apikeys_create_api_key]


if __name__ == '__main__':
    env = Env()
    env.read_env()

    project_id = env.str('DIALOGFLOW_PROJECT_ID')

    google_app_credential_file_name = env.str('GOOGLE_APPLICATION_CREDENTIALS')

    google_api_key_response = create_api_key(
        project_id=project_id,
        suffix=f'PVG {project_id}')

    print(f'-=-=-=-=-=-=\n\n\n{google_api_key_response}')
    google_api_key = {
        'key_string': google_api_key_response.key_string,
        'uid': google_api_key_response.uid
    }

    with open(google_app_credential_file_name, "w") as google_file:
        google_file.write(json.dumps(google_api_key))
