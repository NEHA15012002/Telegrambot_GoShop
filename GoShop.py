import os
import telebot
import telegram.ext

API_KEY = "6203147275:AAEPwwA83mm_N5ZQ-CpqhUhjaOi-HWKnUHg"
bot= telebot.TeleBot(API_KEY)
OWNER_CHAT_ID="8840874334"

def get_inventory():
    inventory = {
        'Milk': {'price': 20, 'quantity': 100, 'weight': 1.0, 'type': 'Dairy', 'brand': 'Amul'},
        'Butter': {'price': 50, 'quantity': 100, 'weight': 1.0, 'type': 'Dairy', 'brand': 'Amul'},
        'Apple': {'price': 200, 'quantity': 50, 'weight': 1.0, 'type': 'Fruits', 'brand': 'Himalchal'},
        'Mango': {'price': 250, 'quantity': 50, 'weight': 1.0, 'type': 'Fruits', 'brand': 'Mangro'},
        'Potato': {'price': 25, 'quantity': 30, 'weight': 4.0, 'type': 'Vegetable', 'brand': 'Mr Sharmas'},
        'Tomato': {'price': 15, 'quantity': 30, 'weight': 3.0, 'type': 'Food', 'brand': 'Personal Care'},
        'Bread': {'price': 20, 'quantity': 10, 'weight': 1.3, 'type': 'Bakery', 'brand': 'Britania'},
        'Shampoo': {'price': 350, 'quantity': 10, 'weight': 1.1, 'type': 'Personal Care', 'brand': 'Wow'},
        'Soap': {'price': 50, 'quantity': 4, 'weight': 2.5, 'type': 'Personal Care', 'brand': 'Pears'},
        'Chips': {'price': 20, 'quantity': 500, 'weight': 5.0, 'type': 'Food', 'brand': 'Snacks'}
    }
    return inventory

order_items=[]

@bot.message_handler(commands=['hello'])
def hello(message):
    bot.send_message(message.chat.id, "hello!")

# Define command handlers
@bot.message_handler(commands=['start'])
def start(message):
    """Send a welcome message when the /start command is issued."""
    bot.send_message(message.chat.id,"Welcome to our store! How can we assist you today? Type /help to see available commands.")

@bot.message_handler(commands=['help'])
def help(message):
    """Provide a list of available commands when the /help command is issued."""
    help_text = "Available commands:\n"
    help_text += "/menu - View our inventory\n"
    help_text += "/order - Place an order\n"
    help_text += "/recommendations - Product recommendations\n"
    help_text += "/loyalty - Check your loyalty points\n"
    help_text += "/delivery - View delivery options\n"
    help_text += "/specials - View special offers\n"
    help_text += "/reviews - View and leave user reviews\n"
    help_text += "/exit - Exit\n"
    bot.send_message(message.chat.id,help_text)



@bot.message_handler(commands=['menu'])
def menu(message):
    inventory = get_inventory()
    inventory_text = "Inventory:\n"
    for item in inventory:
        item_info = inventory[item]
        inventory_text += f"{item}:\n- Price: {item_info['price']}\n- Quantity: {item_info['quantity']}\n- Weight: {item_info['weight']}\n- Type: {item_info['type']}\n- Brand: {item_info['brand']}\n\n"
    bot.reply_to(message, inventory_text)


@bot.message_handler(commands=['order'])
def order(message):
    inventory = get_inventory()
    order_text = "Please enter the item you would like to order:\n"
    for item in inventory:
        order_text += f"{item}\n"
    bot.reply_to(message, order_text)
    bot.register_next_step_handler(message, process_order)

def process_order(message):
    inventory = get_inventory()
    order_item = message.text
    if order_item in inventory:
        order_quantity_text = f"How many {order_item}s would you like to order?"
        bot.reply_to(message, order_quantity_text)
        bot.register_next_step_handler(message, process_quantity, order_item)
    else:
        error_text = "Sorry, that item is not in our inventory. Please try again."
        bot.reply_to(message, error_text)
        order(message)

def process_quantity(message, order_item):
    inventory = get_inventory()
    order_quantity = message.text
    if not order_quantity.isdigit():
        error_text = "Sorry, that is not a valid quantity. Please enter a number."
        bot.reply_to(message, error_text)
        bot.register_next_step_handler(message, process_quantity, order_item)
    elif int(order_quantity) > inventory[order_item]['quantity']:
        error_text = f"Sorry, we only have {inventory[order_item]['quantity']} {order_item}s in stock. Please enter a smaller quantity."
        bot.reply_to(message, error_text)
        bot.register_next_step_handler(message, process_quantity, order_item)
    else:
        total_price = int(order_quantity) * inventory[order_item]['price']
        order_summary = f"Order Confirmation\nYou have ordered {order_quantity} {order_item}s for a total of {total_price} INR\n. Thank you for your order it will be delivered within an hour!"
        bot.reply_to(message, order_summary)


@bot.message_handler(commands=['owner'])
def owner(order_summary):
    order_text = "\n".join([f"{item['name']} ({item['quantity']} x {item['price']})" for item in order_summary])
    order_details_text = f"New order received:\n{order_text}\nTotal cost: {calculate_total_cost(order_summary)}\nWould you like to accept this order? Please reply with 'accept' or 'reject'."
    bot.send_message(OWNER_CHAT_ID, order_details_text)
    bot.register_next_step_handler_by_chat_id(OWNER_CHAT_ID, process_order_confirmation, order_summary)

def process_order_confirmation(message, order_summary):
    confirmation = message.text.lower()
    if confirmation == 'accept':
        bot.send_message(OWNER_CHAT_ID, "Order accepted. Please process the order and ship the items.")
    elif confirmation == 'reject':
        bot.send_message(OWNER_CHAT_ID, "Order rejected. Please contact the customer to discuss the issue.")
    else:
        error_text = "Sorry, we did not recognize your response. Please reply with 'accept' or 'reject'."
        bot.send_message(OWNER_CHAT_ID, error_text)
        bot.register_next_step_handler_by_chat_id(OWNER_CHAT_ID, process_order_confirmation, order_summary)




@bot.message_handler(commands=['recommendations'])
def recommendations(message):
    """Provide product recommendations when the /recommendations command is issued."""
    recommendations_text = "Based on your purchase history, we recommend: Milk\n"
    # Insert code to provide product recommendations based on user purchase history
    bot.send_message(message.chat.id,recommendations_text)

@bot.message_handler(commands=['loyalty'])
def loyalty(message):
    """Display the user's loyalty points when the /loyalty command is issued."""
    loyalty_points = 5 # Insert code to retrieve the user's loyalty points here
    loyalty_text = "You have earned {} loyalty points for this order.".format(loyalty_points)
    bot.send_message(message.chat.id,loyalty_text)

@bot.message_handler(commands=['delivery'])
def delivery(message):
    """Display available delivery options when the /delivery command is issued."""
    delivery_text = "We offer the following delivery options:\n"
    delivery_text += "- Local pickup\n"
    delivery_text += "- Same-day delivery within a 10-mile radius\n"
    delivery_text += "- Standard shipping\n"
    bot.send_message(message.chat.id,delivery_text)


@bot.message_handler(commands=['specials'])
def specials(message):
    """Display available special offers when the /specials command is issued."""
    specials_text = "Our current special offers:\n"
    specials_text += "- Buy one, get one free on snacks items in store\n"
    specials_text += "- 10% off your first online order\n"
    bot.send_message(message.chat.id,specials_text)


@bot.message_handler(commands=['reviews'])
def reviews(message):
    """Display user reviews and allow users to leave reviews when the /reviews command is issued."""
    reviews_text = "User reviews: Excellent Service\n"
    # Insert code to retrieve user reviews and display them here
    bot.send_message(message.chat.id,reviews_text)

@bot.message_handler(commands=['exit'])
def exit(message):
    """Send a exit message when the /exit command is issued."""
    bot.send_message(message.chat.id,"Thankyou, hope you are satisfied by our service!")



bot.polling()
