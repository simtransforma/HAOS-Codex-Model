"""Safe YAML frontmatter with duplicate/alias rejection, including nested data."""

from __future__ import annotations

import yaml


class UniqueLoader(yaml.SafeLoader):
    def compose_node(self, parent, index):
        if self.check_event(yaml.AliasEvent) or self.peek_event().anchor is not None:
            raise ValueError("frontmatter")
        return super().compose_node(parent, index)

    def construct_mapping(self, node, deep=False):
        if not isinstance(node, yaml.MappingNode):
            raise ValueError("frontmatter")
        result = {}
        for key_node, value_node in node.value:
            key = self.construct_object(key_node, deep=deep)
            if not isinstance(key, str) or key in result or key == "<<":
                raise ValueError("frontmatter")
            result[key] = self.construct_object(value_node, deep=deep)
        return result


def document(text: str) -> tuple[dict, str]:
    lines = text.lstrip("\ufeff").splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        raise ValueError("frontmatter")
    end = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), None)
    if end is None:
        raise ValueError("frontmatter")
    try:
        data = yaml.load("".join(lines[1:end]), Loader=UniqueLoader)
    except (yaml.YAMLError, TypeError, RecursionError, ValueError):
        raise ValueError("frontmatter") from None
    if not isinstance(data, dict) or any(
        not isinstance(data.get(key), str) or not data[key].strip()
        for key in ("name", "description")
    ):
        raise ValueError("frontmatter")
    return data, "".join(lines[end + 1:])


def frontmatter(text: str) -> dict[str, str]:
    data, _ = document(text)
    return {key: data[key] for key in ("name", "description")}
