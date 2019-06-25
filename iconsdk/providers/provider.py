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

from abc import ABCMeta, abstractmethod


class Provider(metaclass=ABCMeta):
    """The provider defines how the IconService connects to Loopchain."""

    @abstractmethod
    def make_request(self, method, params=None):
        raise NotImplementedError("Providers must implement this method")

    @abstractmethod
    def is_connected(self):
        raise NotImplementedError("Providers must implement this method")
