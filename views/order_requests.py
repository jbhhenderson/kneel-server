from .metal_requests import get_single_metal
from .size_requests import get_single_size
from .style_requests import get_single_style

ORDERS = [
    {
        "id": 1,
        "metalId": 3,
        "sizeId": 2,
        "styleId": 3,
        "jewelryTypeId": 2,
        "timestamp": 1614659931693
    }
]

def get_all_orders():
    return ORDERS

def get_single_order(id):
    requested_order = None

    for order in ORDERS:
        if order["id"] == id:
            requested_order = order
            matching_metal = get_single_metal(requested_order["metalId"])
            requested_order["metal"] = matching_metal
            del order["metalId"]
            matching_style = get_single_style(requested_order["styleId"])
            requested_order["style"] = matching_style
            del order["styleId"]
            matching_size = get_single_size(requested_order["sizeId"])
            requested_order["size"] = matching_size
            del order["sizeId"]

    return requested_order

def create_order(order):
    # Get the id value of the last order in the list
    max_id = ORDERS[-1]["id"]

    # Add 1 to whatever that number is
    new_id = max_id + 1

    # Add an `id` property to the order dictionary
    order["id"] = new_id

    # Add the order dictionary to the list
    ORDERS.append(order)

    # Return the dictionary with `id` property added
    return order

def delete_order(id):
    "Test"
    # Initial -1 value for order index, in case one isn't found
    order_index = -1

    # Iterate the ORDERS list, but use enumerate() so that you
    # can access the index value of each item
    for index, order in enumerate(ORDERS):
        if order["id"] == id:
            # Found the order. Store the current index.
            order_index = index

    # If the order was found, use pop(int) to remove it from list
    if order_index >= 0:
        ORDERS.pop(order_index)

def update_order(id, new_order):
    "Test"
    # Iterate the ORDERS list, but use enumerate() so that
    # you can access the index value of each item.
    for index, order in enumerate(ORDERS):
        if order["id"] == id:
            # Found the order. Update the value.
            ORDERS[index] = new_order
            break

