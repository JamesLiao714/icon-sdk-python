# -*- coding: utf-8 -*-
# Copyright 2018 ICON Foundation
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

import json
from unittest import main
from unittest.mock import patch

import requests_mock

from iconsdk.builder.transaction_builder import DeployTransactionBuilder
from iconsdk.signed_transaction import SignedTransaction
from iconsdk.utils.validation import is_T_HASH
from tests.api_full_response.example_response import result_success_v3, result_error_v3
from tests.api_full_response.test_full_response_base import TestFullResponseBase


@patch('iconsdk.providers.http_provider.HTTPProvider._make_id', return_value=1234)
class TesFullResponseSendDeploy(TestFullResponseBase):
    def test_send_deploy(self, _make_id):
        deploy_transaction = DeployTransactionBuilder() \
            .from_(self.setting["from"]) \
            .to(self.setting["to_install"]) \
            .step_limit(self.setting["step_limit"]) \
            .nid(self.setting["nid"]) \
            .nonce(self.setting["nonce"]) \
            .content_type(self.setting["content_type"]) \
            .content(self.setting["content_install"]) \
            .params(self.setting["params_install"]) \
            .build()
        signed_transaction = SignedTransaction(deploy_transaction, self.wallet)

        with requests_mock.Mocker() as m:
            response_json = {
                "jsonrpc": "2.0",
                "id": 1234,
                "result": "0x4bf74e6aeeb43bde5dc8d5b62537a33ac8eb7605ebbdb51b015c1881b45b3aed"
            }

            m.post(self.matcher, json=response_json)
            result_dict = self.icon_service.send_transaction(signed_transaction, full_response=True)
            actual_request = json.loads(m._adapter.last_request.text)
            result_content = result_dict['result']

            self.assertEqual(result_success_v3.keys(), result_dict.keys())
            self.assertTrue(is_T_HASH(result_content))

    def test_deploy_wrong_address(self, _make_id):
        wrong_address = "hx5bfdb090f43a808005ffc27c25b213145e8"
        deploy_transaction = DeployTransactionBuilder() \
            .from_(self.setting["from"]) \
            .to(wrong_address) \
            .step_limit(self.setting["step_limit"]) \
            .nid(self.setting["nid"]) \
            .nonce(self.setting["nonce"]) \
            .content_type(self.setting["content_type"]) \
            .content(self.setting["content_install"]) \
            .params(self.setting["params_install"]) \
            .build()
        signed_transaction = SignedTransaction(deploy_transaction, self.wallet)

        with requests_mock.Mocker() as m:
            response_json = {
                'jsonrpc': '2.0',
                'id': 1234,
                'error': {
                    "code": -32600,
                    "message": f'Not a system SCORE {wrong_address}'
                }
            }

            m.post(self.matcher, json=response_json, status_code=400)
            result_dict = self.icon_service.send_transaction(signed_transaction, full_response=True)
            self.assertEqual(result_error_v3.keys(), result_dict.keys())


if __name__ == '__main__':
    main()
