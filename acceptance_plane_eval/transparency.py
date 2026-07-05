"""Small Merkle transparency helpers for public evaluation bundles."""
from __future__ import annotations

from .canonical import sha256_hex

LEAF_PREFIX = b"AP-MERKLE-LEAF-v1\x00"
NODE_PREFIX = b"AP-MERKLE-NODE-v1\x00"


def leaf_hash(data: bytes) -> str:
    return sha256_hex(LEAF_PREFIX + data)


def node_hash(left_hex: str, right_hex: str) -> str:
    return sha256_hex(NODE_PREFIX + bytes.fromhex(left_hex) + bytes.fromhex(right_hex))


def merkle_root(leaves: list[str]) -> str:
    if not leaves:
        return sha256_hex(b"AP-MERKLE-EMPTY-v1")
    level = leaves[:]
    while len(level) > 1:
        nxt: list[str] = []
        for i in range(0, len(level), 2):
            left = level[i]
            right = level[i + 1] if i + 1 < len(level) else left
            nxt.append(node_hash(left, right))
        level = nxt
    return level[0]


def inclusion_proof(leaves: list[str], index: int) -> list[dict[str, str]]:
    if index < 0 or index >= len(leaves):
        raise IndexError(index)
    proof: list[dict[str, str]] = []
    idx = index
    level = leaves[:]
    while len(level) > 1:
        if idx % 2 == 0:
            sib = idx + 1 if idx + 1 < len(level) else idx
            proof.append({"side": "right", "hash": level[sib]})
        else:
            proof.append({"side": "left", "hash": level[idx - 1]})
        idx //= 2
        nxt: list[str] = []
        for i in range(0, len(level), 2):
            left = level[i]
            right = level[i + 1] if i + 1 < len(level) else left
            nxt.append(node_hash(left, right))
        level = nxt
    return proof


def verify_inclusion(leaf: str, index: int, proof: list[dict[str, str]], expected_root: str) -> bool:
    cur = leaf
    idx = index
    for step in proof:
        side = step["side"]
        sibling = step["hash"]
        if side == "left":
            cur = node_hash(sibling, cur)
        elif side == "right":
            cur = node_hash(cur, sibling)
        else:
            return False
        idx //= 2
    return cur == expected_root
