from __future__ import absolute_import, unicode_literals
import logging

from products.models import MainProductsCategorie, ProductsSubCategorie, Product
 
from django.urls import reverse
from celery import shared_task

import telebot
 
 
@shared_task
def telegramRegister(token):
    bot = telebot.TeleBot(token)
    
    @bot.message_handler(commands=['start'])
    def send_welcome(message):
        mpc = MainProductsCategorie.objects.all()
        psc = ProductsSubCategorie.objects.all()
        
        output = 'Доступные категории:\n'
        
        for mc in mpc:
            output += mc.name + "\n\n"
            for sc in psc:
                if sc.parent == mc:
                    output += sc.name + "\n"
        
        bot.reply_to(message, output)
        
    @bot.message_handler(commands=['category'])
    def send_products_by_category(message):
        cat = message.text.split('/category ')

        try:
            psc = ProductsSubCategorie.objects.get(name = cat[1])
        except ProductsSubCategorie.DoesNotExist:
            bot.reply_to(message, "Такую категорию ещё не придумали:(")
            return
        
        products = Product.objects.filter(category = psc)
        
        output = 'Вот что я нашёл:\n\n'
        
        for product in products:
            output+= product.name + "\n" + product.description + "\n" + str(product.price) + "\n\n"
        
        bot.reply_to(message, output)
    
    bot.polling()
