import json

# Define valid options
Food_Item = ['milkshake', 'ice cream']
Milkshake_IceCream_Flavors = ['strawberry', 'chocolate', 'vanilla']
Milkshake_IceCream_Sizes = ['small', 'medium', 'large']
Store_Location = ['prosper', 'frisco', 'mckinney']

def validate_order(slots):
    # Validate Food_Item
    if not slots['Food_Item'] or not slots['Food_Item']['value']['originalValue']:
        return {
            'isValid': False,
            'invalidSlot': 'Food_Item'
        }
    if slots['Food_Item']['value']['originalValue'].lower() not in Food_Item:
        return {
            'isValid': False,
            'invalidSlot': 'Food_Item',
            'message': 'Please select a valid food item: {}'.format(", ".join(Food_Item))
        }

    # Validate Milkshake_IceCream_Flavors if Food_Item is valid
    if not slots['Milkshake_IceCream_Flavors'] or not slots['Milkshake_IceCream_Flavors']['value']['originalValue']:
        return {
            'isValid': False,
            'invalidSlot': 'Milkshake_IceCream_Flavors'
        }
    if slots['Milkshake_IceCream_Flavors']['value']['originalValue'].lower() not in Milkshake_IceCream_Flavors:
        return {
            'isValid': False,
            'invalidSlot': 'Milkshake_IceCream_Flavors',
            'message': 'Please select a valid flavor: {}'.format(", ".join(Milkshake_IceCream_Flavors))
        }

    # Validate Milkshake_IceCream_Sizes if Flavor is valid
    if not slots['Milkshake_IceCream_Sizes'] or not slots['Milkshake_IceCream_Sizes']['value']['originalValue']:
        return {
            'isValid': False,
            'invalidSlot': 'Milkshake_IceCream_Sizes'
        }
    if slots['Milkshake_IceCream_Sizes']['value']['originalValue'].lower() not in Milkshake_IceCream_Sizes:
        return {
            'isValid': False,
            'invalidSlot': 'Milkshake_IceCream_Sizes',
            'message': 'Please select a valid size: {}'.format(", ".join(Milkshake_IceCream_Sizes))
        }

    # Validate Store_Location if Size is valid
    if not slots['Store_Location'] or not slots['Store_Location']['value']['originalValue']:
        return {
            'isValid': False,
            'invalidSlot': 'Store_Location'
        }
    if slots['Store_Location']['value']['originalValue'].lower() not in Store_Location:
        return {
            'isValid': False,
            'invalidSlot': 'Store_Location',
            'message': 'Please select a valid store location: {}'.format(", ".join(Store_Location))
        }

    # If all validations pass
    return {'isValid': True}

def lambda_handler(event, context):
    print(event)

    bot = event['bot']['name']
    slots = event['sessionState']['intent']['slots']
    intent = event['sessionState']['intent']['name']

    # Validate the order
    order_validation_result = validate_order(slots)

    # Handle dialog actions
    if event['invocationSource'] == 'DialogCodeHook':
        if not order_validation_result['isValid']:
            response = {
                "sessionState": {
                    "dialogAction": {
                        "slotToElicit": order_validation_result['invalidSlot'],
                        "type": "ElicitSlot"
                    },
                    "intent": {
                        "name": intent,
                        "slots": slots
                    }
                }
            }
            if 'message' in order_validation_result:
                response["messages"] = [
                    {
                        "contentType": "PlainText",
                        "content": order_validation_result['message']
                    }
                ]
            return response
        else:
            # All slots are valid, delegate to Lex for further action
            return {
                "sessionState": {
                    "dialogAction": {
                        "type": "Delegate"
                    },
                    "intent": {
                        "name": intent,
                        "slots": slots
                    }
                }
            }

    # Handle fulfillment
    if event['invocationSource'] == 'FulfillmentCodeHook':
        return {
            "sessionState": {
                "dialogAction": {
                    "type": "Close"
                },
                "intent": {
                    "name": intent,
                    "slots": slots,
                    "state": "Fulfilled"
                }
            },
            "messages": [
                {
                    "contentType": "PlainText",
                    "content": "I've placed your order."
                }
            ]
        }
