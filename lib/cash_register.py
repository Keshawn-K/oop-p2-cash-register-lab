#!/usr/bin/env python3

class CashRegister:
  def __init__(self, discount=0):
    self.total = 0
    # validate discount: must be integer between 0 and 100 inclusive
    if not isinstance(discount, int) or discount < 0 or discount > 100:
      print("Not valid discount")
      self.discount = 0
    else:
      self.discount = discount
    self.items = []
    # keep a history of previous transactions (each is a dict with title, price, quantity, amount)
    self.previous_transactions = []
    self.last_transaction = 0

  def add_item(self, title, price, quantity=1):
    amount = price * quantity
    self.total += amount
    for _ in range(quantity):
      self.items.append(title)
    self.last_transaction = amount
    # record the transaction
    self.previous_transactions.append({
      'title': title,
      'price': price,
      'quantity': quantity,
      'amount': amount
    })

  def apply_discount(self):
    if not self.previous_transactions:
      print("There is no discount to apply.")
      return

    # apply discount to the current total
    if self.discount:
      self.total = self.total * (100 - self.discount) / 100
      try:
        if float(self.total).is_integer():
          print(f"After the discount, the total comes to ${int(self.total)}.")
        else:
          print(f"After the discount, the total comes to ${self.total}.")
      except Exception:
        print(f"After the discount, the total comes to ${self.total}.")
    else:
      print("There is no discount to apply.")

    # remove the last transaction record from previous_transactions and update items accordingly
    if self.previous_transactions:
      last = self.previous_transactions.pop()
      qty = last.get('quantity', 1)
      title = last.get('title')
      for _ in range(qty):
        for i in range(len(self.items)-1, -1, -1):
          if self.items[i] == title:
            self.items.pop(i)
            break

  def void_last_transaction(self):
    if not self.previous_transactions:
      return
    last = self.previous_transactions.pop()
    self.total -= last.get('amount', 0)
    # remove the last N items matching the title from the end
    qty = last.get('quantity', 1)
    title = last.get('title')
    for _ in range(qty):
      # only remove if present
      for i in range(len(self.items)-1, -1, -1):
        if self.items[i] == title:
          self.items.pop(i)
          break
    if self.total < 0:
      self.total = 0.0
