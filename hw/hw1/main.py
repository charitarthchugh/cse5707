import jax.numpy as jnp
from dataclasses import dataclass

@dataclass 
class Items:
    count: int
    items: dict[int,dict[str,int]] 
    capacity: int

def parser(input_text: str) -> Items:
    lines = input_text.split('\n')
    count = int(lines[0])

    item_map = {}
    for i in range(1, count + 1):
        parts = lines[i].split()
        item_id = int(parts[0])
        item_map[item_id] = {
            'value': int(parts[1]),
            'weight': int(parts[2])
        }

    capacity = int(lines[count + 1])

    return Items(count=count, items=item_map, capacity=capacity)