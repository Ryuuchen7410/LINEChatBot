target = "漢堡蛋"
targetSet = set(target)
print(targetSet)

order1 = "老闆，我要一個漢堡加蛋!"
order1Set = set(order1)
print(order1Set)

order2 = "我想想，我要一個漢堡，然後要加蛋。"
order2Set = set(order2)
print(order2Set)

print(targetSet & order1Set)
print(targetSet & order2Set)

def similar(target, order, threshold=0.6):
    target_set = set(target)
    order_set = set(order)

    intersect = target_set & order_set

    return (len(intersect) / len(target_set)) >= threshold

print(similar(target, order1))
print(similar(target, order2))

