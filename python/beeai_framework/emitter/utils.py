# Copyright 2025 © BeeAI a Series of LF Projects, LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import re
from typing import TYPE_CHECKING

from beeai_framework.emitter.errors import EmitterError

if TYPE_CHECKING:
    from beeai_framework.context import RunInstance
    from beeai_framework.emitter import EventMeta, Matcher


def assert_valid_name(name: str) -> None:
    if not name or not re.match("^[a-zA-Z0-9_]+$", name):
        raise EmitterError(
            f"Event name or a namespace part must contain only letters, numbers or underscores: {name}",
        )


def assert_valid_namespace(path: list[str]) -> None:
    for part in path:
        assert_valid_name(part)


def create_internal_event_matcher(name: str, instance: "RunInstance", *, parent_run_id: str | None = None) -> "Matcher":
    def matcher(event: "EventMeta") -> bool:
        if parent_run_id is not None and (not event.trace or event.trace.parent_run_id != parent_run_id):
            return False

        return (
            event.path == ".".join(["run", *instance.emitter.namespace, name])
            and bool(event.context.get("internal", False))
            and event.creator.instance is instance  # type: ignore
        )

    return matcher


def create_event_matcher(name: str, instance: "RunInstance", *, parent_run_id: str | None = None) -> "Matcher":
    def matcher(event: "EventMeta") -> bool:
        if parent_run_id is not None and (not event.trace or event.trace.parent_run_id != parent_run_id):
            return False

        return event.name == name and event.creator is instance

    return matcher
