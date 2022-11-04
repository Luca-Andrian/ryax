import asyncio
import inspect
import os
from pathlib import Path
from typing import Callable
from unittest.mock import AsyncMock

import pytest
import yaml

from ryax_execution.ryax_source_protocol import RyaxSourceProtocol


@pytest.fixture(scope="function")
def module_outputs():
    class ModuleOutputDict(dict):
        def __init__(self, metadata: dict):
            self.outputs_values_keys = [
                out["name"] for out in metadata["spec"].get("outputs", [])
            ]

        def __eq__(self, other):
            if all(k in self.outputs_values_keys for k in other.keys()):
                return True
            return False

    return ModuleOutputDict


@pytest.fixture(scope="function")
def module_metadata():
    def get_metadata(module_caller: Callable):
        metadata_search_loc = Path(inspect.getfile(module_caller)).parent
        for base, dirs, files in os.walk(metadata_search_loc):
            if "ryax_metadata.yaml" in files or "ryax_metadata.yml" in files:
                metadata_path = os.path.join(base, "ryax_metadata.yaml")
                with open(metadata_path, "r") as f:
                    return yaml.safe_load(f)

    return get_metadata


@pytest.fixture(scope="function")
def service_mock():
    return AsyncMock(RyaxSourceProtocol)


@pytest.fixture(scope="function")
def runtime_error_after_n_seconds(n):
    asyncio.sleep(n)
    raise RuntimeError
