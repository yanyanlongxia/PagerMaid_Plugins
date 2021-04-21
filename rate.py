""" Pagermaid currency exchange rates plugin. Plugin by @fruitymelon and @xtaodada"""

import asyncio, json, time
from json.decoder import JSONDecodeError
import urllib.request
from pagermaid.listener import listener
from pagermaid import log

API = "https://cdn.jsdelivr.net/gh/fawazahmed0/currency-api@1/latest/currencies.json"
currencies = []
data = {}

inited = False


def init():
  with urllib.request.urlopen(API) as response:
    result = response.read()
    try:
      global data
      data = json.loads(result)
      for key in list(enumerate(data)):
        currencies.append(key[1].upper())
      currencies.sort()
    except JSONDecodeError as e:
      raise e
    global inited
    inited = True


init()
last_init = time.time()

@listener(incoming=True, ignore_edited=True)
async def refresher(context):
  if time.time() - last_init > 24 * 60 * 60:
    # we'd better do this to prevent ruining the log file with massive fail logs
    # as this `refresher` would be called frequently
    last_init = time.time()
    try:
      init()
    except Exception as e:
      await log(f"Warning: plugin rate failed to refresh rates data. {e}")

@listener(is_plugin=True, outgoing=True, command="rate",
          description="Currency exchange rate plugin.",
          parameters="<FROM> <TO> <NUM>")
async def rate(context):
  if not inited:
    init()
  if not inited:
    return
  if not context.parameter:
    await context.edit(
      f"This is the currency exchange rate plugin.\n\nUsage: `-rate <FROM> <TO> <NUM>` where `<NUM>` is optional\n\nAvailable currencies: \n`{', '.join(currencies)}`\n\nData are updated daily, for encrypted currencies we recommend to use the `bc` plugin.")
    return
  NB = 1.0
  if len(context.parameter) != 3:
    if len(context.parameter) != 2:
      await context.edit(f"Usage: `-rate <FROM> <TO> <NUM>` where `<NUM>` is optional\n\nAvailable currencies: \n`{', '.join(currencies)}`\n\nData are updated daily, for encrypted currencies we recommend to use the `bc` plugin.")
      return
  FROM = context.parameter[0].upper().strip()
  TO = context.parameter[1].upper().strip()
  try:
    NB = NB if len(context.parameter) == 2 else float(context.parameter[2].strip())
  except:
    NB = 1.0
  if currencies.count(FROM) == 0:
    await context.edit(f"Currency type {FROM} is not supported. Choose one among `{', '.join(currencies)}` instead.")
    return
  if currencies.count(TO) == 0:
    await context.edit(f"Currency type {TO} is not supported. Choose one among `{', '.join(currencies)}` instead.")
    return
  endpoint = f"https://cdn.jsdelivr.net/gh/fawazahmed0/currency-api@1/latest/currencies/{FROM.lower()}/{TO.lower()}.json"
  with urllib.request.urlopen(endpoint) as response:
    result = response.read()
    try:
      rate_data = json.loads(result)
      await context.edit(f'`{FROM} : {TO} = {NB} : {round(NB * rate_data[TO.lower()], 4)}`\n\nData are updated daily.')
    except Exception as e:
      await context.edit(str(e))
