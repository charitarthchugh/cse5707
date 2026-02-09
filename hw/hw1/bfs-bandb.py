import argparse
from dataclasses import dataclass
from collections import deque

@dataclass
class Items:
    count: int
    values: list[float]
    weights: list[float]
    capacity: int


def parser(input_text: str) -> Items:
    lines = input_text.strip().split('\n')
    count = int(lines[0])
    capacity = int(lines[count + 1])

    data = [list(map(float, line.split())) for line in lines[1:count + 1]]
    values = [row[1] for row in data]
    weights = [row[2] for row in data]

    return Items(
        count=count,
        values=values,
        weights=weights,
        capacity=capacity
    )

def knapsack_bfs(items: Items) -> tuple[float, list[int]]:
    def upper_bound(level, curr_weight, curr_value):
        """Calculate upper bound using fractional """
        if level >= items.count:
            return curr_value

        bound = curr_value
        remaining_capacity = items.capacity - curr_weight

        for i in range(level, items.count):
            if items.weights[i] <= remaining_capacity:
                bound += items.values[i]
                remaining_capacity -= items.weights[i]
            else:
                # Take fractional part of the item
                bound += items.values[i] * (remaining_capacity / items.weights[i])
                break

        return bound

    # State: (level, current_weight, current_value, selected_items)
    queue = deque([(0, 0, 0, [])])
    max_value = 0
    best_selection = []

    while queue:
        level, curr_weight, curr_value, selected = queue.popleft()

        # If we've processed all items
        if level == items.count:
            if curr_value > max_value:
                max_value = curr_value
                best_selection = selected
            continue

        # Option 1: Don't include the current item
        if upper_bound(level + 1, curr_weight, curr_value) > max_value:
            queue.append((level + 1, curr_weight, curr_value, selected))

        # Option 2: Include the current item (if it fits)
        item_weight = items.weights[level]
        item_value = items.values[level]

        if curr_weight + item_weight <= items.capacity:
            new_value = curr_value + item_value
            new_weight = curr_weight + item_weight
            new_selected = selected + [level]

            # Update the best solution if this is better
            if new_value > max_value:
                max_value = new_value
                best_selection = new_selected

            # Check if this branch is promising
            if upper_bound(level + 1, new_weight, new_value) > max_value:
                queue.append((level + 1, new_weight, new_value, new_selected))

    return max_value, best_selection


def main():
    arg_parser = argparse.ArgumentParser(description="Build Simplex tableau for Knapsack problem.")
    arg_parser.add_argument("input_file", help="Path to the input file.")
    args = arg_parser.parse_args()

    with open(args.input_file, "r") as f:
        items = parser(f.read())

    max_value, selected_items = knapsack_bfs(items)

    print(f"Maximum value: {max_value}")
    print(f"Selected items (0-indexed): {selected_items}")
    print(f"Number of items selected: {len(selected_items)}")


if __name__ == "__main__":
    main()
