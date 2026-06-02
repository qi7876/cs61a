from tree import tree, label, branches, is_leaf, is_tree

def only_paths(t, n):
    """Return a tree with only the nodes of t along paths from the root to a leaf of t for which the node labels of the path sum to n. If no paths sum to n, return None.

    >>> t = tree(3, [tree(4), tree(1, [tree(3, [tree(2)]), tree(2, [tree(1)]), tree(5), tree(3)])])
    >>> print_tree(only_paths(t, 7))
    3
      4
      1
        2
          1
        3
    >>> print_tree(only_paths(t, 9))
    3
      1
        3
          2
        5
    >>> print(only_paths(t, 3))
    None
    """
    if is_leaf(t) and n == label(t):
        return t
    new_branches = [only_paths(b, n - label(t)) for b in branches(t)]
    if any(new_branches):
        return tree(label(t), [b for b in new_branches if b is not None])

