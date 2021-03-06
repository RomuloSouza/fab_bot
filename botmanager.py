#!/usr/bin/env python3.6.7
# -*- coding: utf-8 -*-
import logging
import db
import constants
from util import isfloat, isinteger, tobool
from db import Product
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ForceReply
from keyboardmanager import KeyboardManager
from dbmanager import DbManager


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


class BotManager:
    """
    Define all commands used in the bot
    """
    keyboard_manager = KeyboardManager()
    db_manager = DbManager()

    def call_back(self, bot, update):
        """
        Represents an incoming callback query from a callback button in an inline keyboard.
        """

        query = update.callback_query
        method, option = query.data.split(" ")
        if(option == "all"):
            reply_markup = self.keyboard_manager.confirm(method)
            bot.edit_message_text(text="Are you sure?", 
                    chat_id=query.message.chat.id, 
                    message_id=query.message.message_id, 
                    reply_markup=reply_markup)
        elif(option.isnumeric() == False):
            if(tobool(option) and method == "rm"):
                self.db_manager.remove_products(query.message.chat.id)
                bot.edit_message_text(text="All products successfully removed.",
                        chat_id=query.message.chat.id,
                        message_id=query.message.message_id)
            elif(tobool(option) and method == "rm_debt"):
                self.db_manager.pay_debt(query.message.chat.id)
                bot.edit_message_text(text="Debt successfully paid.",
                        chat_id=query.message.chat.id,
                        message_id=query.message.message_id)
            else:
                bot.edit_message_text(text="Operation cancelled",
                        chat_id=query.message.chat.id,
                        message_id=query.message.message_id)
        elif(method == "add"):
            """
            Increases the quantity of an specific product in database
            """
            query_db = db.SESSION.query(Product).filter_by(id=int(option))
            product = query_db.one()
            product.quantity = product.quantity + 1
            db.SESSION.commit()

            bot.edit_message_text(text="{} successfully added. You owe {}".format(product.name, product.quantity),
                    chat_id=query.message.chat.id,
                    message_id=query.message.message_id)
        elif(method == "rm"):
            """
            Removes a product from database
            """
            query_db = db.SESSION.query(Product).filter_by(id=int(option))
            product = query_db.one()
            db.SESSION.delete(product)
            db.SESSION.commit()

            bot.edit_message_text(text="{} successfully removed.".format(product.name),
                    chat_id=query.message.chat.id,
                    message_id=query.message.message_id)
        elif(method == "rm_debt"):
            """
            Decreases the quantity of an specific product in database
            """
            query_db = db.SESSION.query(Product).filter_by(id=int(option))
            product = query_db.one()
            product.quantity = product.quantity - 1
            db.SESSION.commit()

            bot.edit_message_text(text="A paid {}. You owe {}".format(product.name, product.quantity),
                    chat_id=query.message.chat.id,
                    message_id=query.message.message_id)

    def list_product(self, bot, update):
        """
        Lists all products linked to chat
        """

        query = db.SESSION.query(Product).filter_by(chat=update.message.chat.id)
        product = query.all()
        text = "*Products*\n"
        for i in product:
            text += i.name + " - " + i.price + "\n"

        update.message.reply_markdown(text)

    def new_product(self, bot, update):
        """
        Inserts a product into the database linked to chat
        """

        text = update.message.text
        commands = text.split(" ")
        commands[-1] = commands[-1].replace(",",".")
        if(isinteger(commands[-1]) and commands[-1].find(".") == -1):
            commands[-1] += ".00"
        if(len(commands) >= 3 and isfloat(commands[-1])):
            name = " ".join(commands[1:-1])
            price = commands[-1]

            product = Product(chat=update.message.chat.id, name=name, price=price, quantity=0)
            db.SESSION.add(product)
            db.SESSION.commit()
            update.message.reply_text("Procuct succesfully added")
        else:
            update.message.reply_markdown("To add a new product, type:\n*/newProd* <name of product> <price>")

    def remove_product(self, bot, update):
        """
        Removes a product into the database linked to chat
        """

        keyboard = self.keyboard_manager.create_rm_buttons(update.message.chat.id)
        reply_markup = InlineKeyboardMarkup(keyboard)

        update.message.reply_text("Please choose a product:", reply_markup=reply_markup)

    def fab_config(self, bot, update):
        """
        Adds all products used in FSW
        """
        
        product = Product(chat=update.message.chat.id, name="Guaraná", price="1.50", quantity=0)
        db.SESSION.add(product)
        product = Product(chat=update.message.chat.id, name="Coca-Cola", price="1.50", quantity=0)
        db.SESSION.add(product)
        product = Product(chat=update.message.chat.id, name="Fanta", price="2.50", quantity=0)
        db.SESSION.add(product)
        product = Product(chat=update.message.chat.id, name="Schweppes", price="2.50", quantity=0)
        db.SESSION.add(product)
        product = Product(chat=update.message.chat.id, name="Sprite", price="2.50", quantity=0)
        db.SESSION.add(product)
        product = Product(chat=update.message.chat.id, name="Suco Maçã", price="2.00", quantity=0)
        db.SESSION.add(product)
        product = Product(chat=update.message.chat.id, name="Suco Goiaba", price="2.00", quantity=0)
        db.SESSION.add(product)
        product = Product(chat=update.message.chat.id, name="Suco Caju", price="2.00", quantity=0)
        db.SESSION.add(product)
        product = Product(chat=update.message.chat.id, name="Suco Uva", price="2.00", quantity=0)
        db.SESSION.add(product)
        product = Product(chat=update.message.chat.id, name="Paçoquinha", price="0.50", quantity=0)
        db.SESSION.add(product)
        product = Product(chat=update.message.chat.id, name="Pé de Moça", price="1.00", quantity=0)
        db.SESSION.add(product)
        product = Product(chat=update.message.chat.id, name="Oreo", price="2.50", quantity=0)
        db.SESSION.add(product)
        product = Product(chat=update.message.chat.id, name="Teens Chocolate", price="1.50", quantity=0)
        db.SESSION.add(product)
        product = Product(chat=update.message.chat.id, name="Bolinho Cenoura", price="1.00", quantity=0)
        db.SESSION.add(product)
        product = Product(chat=update.message.chat.id, name="Bolinho Brigadeiro", price="1.00", quantity=0)
        db.SESSION.add(product)
        db.SESSION.commit()
        update.message.reply_text("Products successfully added")

    def add_to_product(self, bot, update):
        """
        Adds a product to the account
        """
        
        keyboard = self.keyboard_manager.create_add_buttons(update.message.chat.id)
        reply_markup = InlineKeyboardMarkup(keyboard)

        update.message.reply_text("Please choose a product:", reply_markup=reply_markup)

    def remove_from_product(self, bot, update):
        """
        Removes a product from the account
        """

        keyboard = self.keyboard_manager.create_rm_debt_buttons(update.message.chat.id)
        reply_markup = InlineKeyboardMarkup(keyboard)

        update.message.reply_text("Please choose a product:", reply_markup=reply_markup)

    def show_debt(self, bot, update):
        """
        Shows the total debt in product
        """
        
        query = db.SESSION.query(Product).filter_by(chat=update.message.chat.id)
        products = query.all()
        response = "*Product   Price    Quantity    Value*\n"
        response +="----------------------------------------------------------\n"
        debt = 0
        for i in products:
            value = float(i.price) * float(i.quantity)
            debt += value
            formatted_name = self.format_names(i.name)
            formatted_price = self.format_price(i.price)
            formatted_quantity = self.format_quantity(i.quantity)
            if(value > 0):
                formatted_value = self.format_float(value)
                formatted_value = self.format_price(formatted_value)
                response += "{}  R${}      {}     R${}\n".format(formatted_name[0], formatted_price,
                            formatted_quantity, formatted_value)
                for i in range(1, len(formatted_name)):
                    response += formatted_name[i] + "\n"
                response +="----------------------------------------------------------\n"
            
        
        response += '\nTotal debt = {}'.format(debt)
        update.message.reply_markdown(response)

    def format_price(self, price):
        """
        Formats spaces for better apresentation
        """
        price = self.format_float(price)
        if (float(price) < 10):
            price = " {}".format(price)

        return price
    
    def format_quantity(self, quantity):
        """
        Formats spaces for better apresentation
        """

        if (int(quantity) < 10):
            quantity = "{}   ".format(quantity)
        
        return quantity

    def format_float(self, old_value):
        """
        Formats the 0s in the number's decimal part
        """

        value = str(old_value).split(".")
        while (len(value[1]) < 2):
            value[1] += "0"
        new_value = value[0] + "." + value[1]

        return new_value

    def format_names(self, name):
        names_list = []
        while(len(name) > 8):
            names_list.append(name[0:8])
            name = name[8:]
        for i in range(len(name),8):
            name += "  "
        names_list.append(name)

        return names_list

    def help(self, bot, update):
        """
        Replies to user all commands used in the bot 
        """

        update.message.reply_text(constants.HELP)


    def error(self, bot, update, error):
        """
        Log Errors caused by Updates.
        """

        logger.warning('Update "%s" caused error "%s"', update, error)

    
