#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 19 07:51:56 2023

@author: vipin
"""

from smartapi import SmartConnect
from smartapi.smartWebSocketV2 import SmartWebSocketV2
import os
import urllib
import json
from pyotp import TOTP

from flask import Flask, jsonify, request

app = Flask(__name__)

# Sample data (can be replaced with a database)
books = [
    {"id": 1, "title": "Book 1", "author": "Author 1"},
    {"id": 2, "title": "Book 2", "author": "Author 2"},
    {"id": 3, "title": "Book 3", "author": "Author 3"}
]

# GET /books - Get all books
@app.route('/getToken', methods=['POST'])
def get_books():
   new_book = request.get_json()
   obj=SmartConnect(api_key=new_book["API_KEY"])

   data = obj.generateSession(new_book["USER_ID"],new_book["PIN"],TOTP(new_book["TOKEN"]).now())
   feed_token = obj.getfeedToken()
   sessionToken = data["data"]["jwtToken"]
   return jsonify({ feed_token :feed_token, sessionToken  :sessionToken  })


@app.route('/placeOrder', methods=['POST'])
def placeOrder():
   params = request.get_json()
   obj=SmartConnect(api_key=params["API_KEY"])

  
  # data = obj.generateSession(params["USER_ID"],params["PIN"],TOTP(params["TOKEN"]).now())
   # feed_token = obj.getfeedToken()
   #placeParams = request.get_json()
 
   params = {
                "variety":"NORMAL",
                "tradingsymbol":params["STOCK_NAME"],
                "symboltoken":params["STOCK_TOKEN"],
                "transactiontype":params["TRADE_TYPE"],
                "exchange":"NSE",
                "ordertype":"LIMIT",
                "producttype":"INTRADAY",
                "duration":"DAY",
                "price":params["PRICE"],
                "quantity":params["qnty"],
    }
   
   response = obj.placeOrder(params)


   #placeParams = request.get_json()
   return jsonify("response"), 200

# POST /books - Add a new book
@app.route('/books', methods=['POST']) 
def add_book():
    new_book = request.get_json()
    if new_book:
        new_book['id'] = len(books) + 1
        books.append(new_book)
        return jsonify(new_book), 201
    else:
        return jsonify({"message": "Invalid data"}), 400
    
@app.route('/getStockToken', methods=['POST'])
def getToken():
   new_book = request.get_json()
   stock_name =new_book["STOCK_NAME"]
   

   instrument_url = "https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json"
   response = urllib.request.urlopen(instrument_url)
   instrument_list = json.loads(response.read())
   data = []
   for instrument in instrument_list:
       if instrument["name"].find(stock_name) != -1 and instrument["exch_seg"] == "NSE" and instrument["symbol"].split('-')[-1] == "EQ":
           data.append(instrument)
    
   return jsonify({"msg" :data })


# GET /books/:id - Get a specific book
@app.route('/books/<int:book_id>', methods=['POST'])
def get_book(book_id):
    new_book = request.get_json()
    book = next((book for book in books if book['id'] == book_id), None)
    if book:
        print(book)
        return jsonify(book)
    else:
        return jsonify({"message": "Book not found"}), 404



# PUT /books/:id - Update a book
@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    updated_book = request.get_json()
    if updated_book:
        book = next((book for book in books if book['id'] == book_id), None)
        if book:
            book.update(updated_book)
            return jsonify(book)
        else:
            return jsonify({"message": "Book not found"}), 404
    else:
        return jsonify({"message": "Invalid data"}), 400

# DELETE /books/:id - Delete a book
@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = next((book for book in books if book['id'] == book_id), None)
    if book:
        books.remove(book)
        return jsonify({"message": "Book deleted"})
    else:
        return jsonify({"message": "Book not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
