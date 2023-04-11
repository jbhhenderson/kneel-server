DATABASE = {
    "metals": [
        {
            "id": 1,
            "metal": "Sterling Silver",
            "price": 12.42
        },
        {
            "id": 2,
            "metal": "14K Gold",
            "price": 736.4
        },
        {
            "id": 3,
            "metal": "24K Gold",
            "price": 1258.9
        },
        {
            "id": 4,
            "metal": "Platinum",
            "price": 795.45
        },
        {
            "id": 5,
            "metal": "Palladium",
            "price": 1241
        }
    ],
    "orders": [
        {
            "id": 1,
            "metalId": 3,
            "sizeId": 2,
            "styleId": 3,
            "jewelryTypeId": 2,
            "timestamp": 1614659931693
        }
    ],
    "sizes": [
        {
            "id": 1,
            "carets": 0.5,
            "price": 405
        },
        {
            "id": 2, 
            "carets": 0.75, 
            "price": 782
        },
        {
            "id": 3, 
            "carets": 1, 
            "price": 1470
        },
        {
            "id": 4, 
            "carets": 1.5, 
            "price": 1997
        },
        {
            "id": 5, 
            "carets": 2, 
            "price": 3638
        }
    ],
    "styles": [
        {
            "id": 1, 
            "style": "Classic", 
            "price": 500 
        },
        {
            "id": 2, 
            "style": "Modern", 
            "price": 710 
        },
        {
            "id": 3, 
            "style": "Vintage", 
            "price": 965 
        }
    ]
}

def all(resource):
    """For GET requests to collection"""
    response = DATABASE[resource]
    return response

def retrieve(resources, id, query_params):
    """For GET requests to a single resource"""
    response = None
    if resources == "orders":
        requested_order = None

        for order in DATABASE["orders"]:
            if order["id"] == id:
                requested_order = order.copy()

                if "metal" in query_params:
                    matching_metal = retrieve("metals", requested_order["metalId"], "")
                    requested_order["metal"] = matching_metal
                    del order["metalId"]
                if "style" in query_params:
                    matching_style = retrieve("styles", requested_order["styleId"], "")
                    requested_order["style"] = matching_style
                    del order["styleId"]
                if "size" in query_params:
                    matching_size = retrieve("sizes", requested_order["sizeId"], "")
                    requested_order["size"] = matching_size
                    del order["sizeId"]
                requested_order["total_price"] = requested_order["metal"]["price"] + requested_order["size"]["price"] + requested_order["style"]["price"]

        response = requested_order

    else:
        for resource in DATABASE[resources]:
            if resource["id"] == id:
                response = resource

    return response

def create(type, resource):
    """For POST requests to a collection"""
    max_id = DATABASE[type][-1]["id"]

    new_id = max_id + 1

    resource["id"] = new_id

    DATABASE[type].append(resource)

    return resource


def update(id, type, new_resource):
    """For PUT requests to a single resource"""
    for index, resource in enumerate(DATABASE[type]):
        if resource["id"] == id:
            # Found the resource. Update the value.
            DATABASE[type][index] = new_resource
            break


def delete(id, type):
    """For DELETE requests to a single resource"""
    # Initial -1 value for resource index, in case one isn't found
    resource_index = -1

    # Iterate the type list, but use enumerate() so that you
    # can access the index value of each item
    for index, resource in enumerate(DATABASE[type]):
        if resource["id"] == id:
            # Found the resource. Store the current index.
            resource_index = index

    # If the resource was found, use pop(int) to remove it from list
    if resource_index >= 0:
        DATABASE[type].pop(resource_index)
