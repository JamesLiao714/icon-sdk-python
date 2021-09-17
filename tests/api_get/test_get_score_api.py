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

from iconsdk.exception import AddressException, JSONRPCException
from iconsdk.utils.validation import is_score_apis
from tests.api_send.test_send_super import TestSendSuper


@patch('iconsdk.providers.http_provider.HTTPProvider._make_id', return_value=1234)
class TestGetScoreApi(TestSendSuper):

    def test_get_score_api(self, _make_id):
        with requests_mock.Mocker() as m:
            governance_address = "cx0000000000000000000000000000000000000001"
            expected_request = {
                'id': 1234,
                'jsonrpc': '2.0',
                'method': 'icx_getScoreApi',
                'params': {
                    'address': governance_address
                }
            }

            m.post(self.matcher, json=response_governance_json)
            # case 0: when getting score apis successfully
            result = self.icon_service.get_score_api(governance_address)
            actual_request = json.loads(m._adapter.last_request.text)
            self.assertEqual(expected_request, actual_request)
            self.assertTrue(result)
            self.assertTrue(is_score_apis(result))

    def test_get_score_api_invalid(self, _make_id):
        # case 1: when address is wrong - wallet address
        self.assertRaises(AddressException, self.icon_service.get_score_api,
                          "hx882efc17c2f50e0d60142b9c0e746cbafb569d8c")
        # case 2: when address is wrong - too short
        self.assertRaises(AddressException, self.icon_service.get_score_api,
                          "cx882efc17c2f50e0d60142b9c0e746cbafb")

    def test_get_score_api_by_wrong_address(self, _make_id):
        with requests_mock.Mocker() as m:
            wrong_address = "cxb0776ee37f5b45bfaea8cff1d8232fbb6122ec32"
            expected_request = {
                'id': 1234,
                'jsonrpc': '2.0',
                'method': 'icx_getScoreApi',
                'params': {
                    'address': wrong_address
                }
            }

            response_json: dict = {
                "jsonrpc": "2.0",
                "error": {
                    "code": -32002,
                    "message": f"SCORE not found: {wrong_address}"
                },
                "id": 1234
            }
            m.post(self.matcher, json=response_json, status_code=400)
            # case 3: when the address is not score id
            self.assertRaises(JSONRPCException, self.icon_service.get_score_api, wrong_address)
            actual_request = json.loads(m._adapter.last_request.text)
            self.assertEqual(expected_request, actual_request)


response_governance_json: dict = {
    "jsonrpc": "2.0",
    "result": [
        {
            "name": "Accepted",
            "type": "eventlog",
            "inputs": [
                {
                    "name": "txHash",
                    "type": "str",
                    "indexed": "0x1"
                }
            ]
        },
        {
            "name": "IRepChanged",
            "type": "eventlog",
            "inputs": [
                {
                    "name": "irep",
                    "type": "int",
                    "indexed": "0x1"
                }
            ]
        },
        {
            "name": "MaliciousScore",
            "type": "eventlog",
            "inputs": [
                {
                    "name": "address",
                    "type": "Address"
                },
                {
                    "name": "unfreeze",
                    "type": "int"
                }
            ]
        },
        {
            "name": "NetworkProposalApproved",
            "type": "eventlog",
            "inputs": [
                {
                    "name": "id",
                    "type": "bytes"
                }
            ]
        },
        {
            "name": "NetworkProposalCanceled",
            "type": "eventlog",
            "inputs": [
                {
                    "name": "id",
                    "type": "bytes"
                }
            ]
        },
        {
            "name": "NetworkProposalRegistered",
            "type": "eventlog",
            "inputs": [
                {
                    "name": "title",
                    "type": "str"
                },
                {
                    "name": "description",
                    "type": "str"
                },
                {
                    "name": "type",
                    "type": "int"
                },
                {
                    "name": "value",
                    "type": "bytes"
                },
                {
                    "name": "proposer",
                    "type": "Address"
                }
            ]
        },
        {
            "name": "NetworkProposalVoted",
            "type": "eventlog",
            "inputs": [
                {
                    "name": "id",
                    "type": "bytes"
                },
                {
                    "name": "vote",
                    "type": "int"
                },
                {
                    "name": "voter",
                    "type": "Address"
                }
            ]
        },
        {
            "name": "PRepDisqualified",
            "type": "eventlog",
            "inputs": [
                {
                    "name": "address",
                    "type": "Address"
                },
                {
                    "name": "success",
                    "type": "bool"
                },
                {
                    "name": "reason",
                    "type": "str"
                }
            ]
        },
        {
            "name": "Rejected",
            "type": "eventlog",
            "inputs": [
                {
                    "name": "txHash",
                    "type": "str",
                    "indexed": "0x1"
                },
                {
                    "name": "reason",
                    "type": "str"
                }
            ]
        },
        {
            "name": "RevisionChanged",
            "type": "eventlog",
            "inputs": [
                {
                    "name": "revisionCode",
                    "type": "int"
                },
                {
                    "name": "revisionName",
                    "type": "str"
                }
            ]
        },
        {
            "name": "StepPriceChanged",
            "type": "eventlog",
            "inputs": [
                {
                    "name": "stepPrice",
                    "type": "int",
                    "indexed": "0x1"
                }
            ]
        },
        {
            "name": "acceptScore",
            "type": "function",
            "inputs": [
                {
                    "name": "txHash",
                    "type": "bytes"
                }
            ],
            "outputs": []
        },
        {
            "name": "addAuditor",
            "type": "function",
            "inputs": [
                {
                    "name": "address",
                    "type": "Address"
                }
            ],
            "outputs": []
        },
        {
            "name": "cancelProposal",
            "type": "function",
            "inputs": [
                {
                    "name": "id",
                    "type": "bytes"
                }
            ],
            "outputs": []
        },
        {
            "name": "getIRep",
            "type": "function",
            "inputs": [],
            "outputs": [
                {
                    "type": "int"
                }
            ],
            "readonly": "0x1"
        },
        {
            "name": "getMaxStepLimit",
            "type": "function",
            "inputs": [
                {
                    "name": "contextType",
                    "type": "str"
                }
            ],
            "outputs": [
                {
                    "type": "int"
                }
            ],
            "readonly": "0x1"
        },
        {
            "name": "getProposal",
            "type": "function",
            "inputs": [
                {
                    "name": "id",
                    "type": "bytes"
                }
            ],
            "outputs": [
                {
                    "type": "{}"
                }
            ],
            "readonly": "0x1"
        },
        {
            "name": "getProposals",
            "type": "function",
            "inputs": [
                {
                    "name": "type",
                    "default": None,
                    "type": "int"
                },
                {
                    "name": "status",
                    "default": None,
                    "type": "int"
                }
            ],
            "outputs": [
                {
                    "type": "{}"
                }
            ],
            "readonly": "0x1"
        },
        {
            "name": "getRevision",
            "type": "function",
            "inputs": [],
            "outputs": [
                {
                    "type": "{}"
                }
            ],
            "readonly": "0x1"
        },
        {
            "name": "getScoreStatus",
            "type": "function",
            "inputs": [
                {
                    "name": "address",
                    "type": "Address"
                }
            ],
            "outputs": [
                {
                    "type": "{}"
                }
            ],
            "readonly": "0x1"
        },
        {
            "name": "getServiceConfig",
            "type": "function",
            "inputs": [],
            "outputs": [
                {
                    "type": "{}"
                }
            ],
            "readonly": "0x1"
        },
        {
            "name": "getStepCosts",
            "type": "function",
            "inputs": [],
            "outputs": [
                {
                    "type": "{}"
                }
            ],
            "readonly": "0x1"
        },
        {
            "name": "getStepPrice",
            "type": "function",
            "inputs": [],
            "outputs": [
                {
                    "type": "int"
                }
            ],
            "readonly": "0x1"
        },
        {
            "name": "getVersion",
            "type": "function",
            "inputs": [],
            "outputs": [
                {
                    "type": "str"
                }
            ],
            "readonly": "0x1"
        },
        {
            "name": "isDeployer",
            "type": "function",
            "inputs": [
                {
                    "name": "address",
                    "type": "Address"
                }
            ],
            "outputs": [
                {
                    "type": "bool"
                }
            ],
            "readonly": "0x1"
        },
        {
            "name": "isInImportWhiteList",
            "type": "function",
            "inputs": [
                {
                    "name": "importStmt",
                    "type": "str"
                }
            ],
            "outputs": [
                {
                    "type": "bool"
                }
            ],
            "readonly": "0x1"
        },
        {
            "name": "isInScoreBlackList",
            "type": "function",
            "inputs": [
                {
                    "name": "address",
                    "type": "Address"
                }
            ],
            "outputs": [
                {
                    "type": "bool"
                }
            ],
            "readonly": "0x1"
        },
        {
            "name": "registerProposal",
            "type": "function",
            "inputs": [
                {
                    "name": "title",
                    "type": "str"
                },
                {
                    "name": "description",
                    "type": "str"
                },
                {
                    "name": "type",
                    "type": "int"
                },
                {
                    "name": "value",
                    "type": "bytes"
                }
            ],
            "outputs": []
        },
        {
            "name": "rejectScore",
            "type": "function",
            "inputs": [
                {
                    "name": "txHash",
                    "type": "bytes"
                },
                {
                    "name": "reason",
                    "type": "str"
                }
            ],
            "outputs": []
        },
        {
            "name": "removeAuditor",
            "type": "function",
            "inputs": [
                {
                    "name": "address",
                    "type": "Address"
                }
            ],
            "outputs": []
        },
        {
            "name": "voteProposal",
            "type": "function",
            "inputs": [
                {
                    "name": "id",
                    "type": "bytes"
                },
                {
                    "name": "vote",
                    "type": "int"
                }
            ],
            "outputs": []
        }
    ],
    "id": 1234
}

if __name__ == "__main__":
    main()
