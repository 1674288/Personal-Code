# Sense cicle
a, b, c = ListNode(1), ListNode(2), ListNode(3)
a.next, b.next = b, c
assert hasCycle(a) is False

# Cicle a la posició 1
c.next = b
assert hasCycle(a) is True

# Casos límit
assert hasCycle(None) is False
x = ListNode(1); x.next = x
assert hasCycle(x) is True
