import requests

class TornApi:
  def __init__(self, key):
    self.__base_url = "https://api.torn.com"
    self.__key = key

  def user(self, user_id=None, fields=None, since=None, until=None):
    """Fetch user information.

If user ID is unspecified, the user related to the API key is used.

UNIX epoch timestamps `since` and `until` work for some fields.

Fields: ammo, attacks, attacksfull, bars, basic, battlestats, bazaar, cooldowns, crimes, discord,
display, education, events, gym, hof, honors, icons, inventory, jobpoints, log, medals, merits,
messages, money, networth, notifications, perks, personalstats, profile, properties, receivedevents,
refills, reports, revives, revivesfull, skills, stocks, timestamp, travel, weaponexp, workstats
    """
    fields = fields or []
    params = {
      "key": self.__key,
      "selections": ",".join(fields),
    }
    if since:
      params["from"] = str(int(since))
    if until:
      params["to"] = str(int(until))
    url = "{}/user/".format(self.__base_url)
    if user_id:
      url += user_id
    resp = requests.get(url, params=params)
    return resp.json()

  def property(self, property_id=None, fields=None):
    """Fetch property information.

If property ID is unspecified, the property related to the API key is used.

Fields: property, timestamp
    """
    fields = fields or []
    params = {
      "key": self.__key,
      "selections": ",".join(fields),
    }
    url = "{}/property/".format(self.__base_url)
    if property_id:
      url += property_id
    resp = requests.get(url, params=params)
    return resp.json()

  def faction(self, faction_id=None, fields=None, since=None, until=None):
    """Fetch faction information.

If faction ID is unspecified, the faction related to the API key is used.

UNIX epoch timestamps `since` and `until` work for some fields.

Fields: applications, armor, armorynews, attacknews, attacks, attacksfull, basic, boosters, cesium,
chain, chains, contributors, crimenews, crimes, currency, donations, drugs, fundsnews, mainnews,
medical, membershipnews, reports, revives, revivesfull, stats, temporary, territory, timestamp,
upgrades, weapons
    """
    fields = fields or []
    params = {
      "key": self.__key,
      "selections": ",".join(fields),
    }
    if since:
      params["from"] = str(int(since))
    if until:
      params["to"] = str(int(until))
    url = "{}/faction/".format(self.__base_url)
    if faction_id:
      url += faction_id
    resp = requests.get(url, params=params)
    return resp.json()

  def company(self, company_id=None, fields=None):
    """Fetch company information.

If company ID is unspecified, the company related to the API key is used.

Fields: applications, detailed, employees, news, newsfull, profile, stock, timestamp
    """
    fields = fields or []
    params = {
      "key": self.__key,
      "selections": ",".join(fields),
    }
    url = "{}/company/".format(self.__base_url)
    if company_id:
      url += company_id
    resp = requests.get(url, params=params)
    return resp.json()

  def market(self, item_id=None, fields=None):
    """Fetch item market information.

Fields: bazaar, itemmarket, pointsmarket, timestamp
    """
    fields = fields or []
    params = {
      "key": self.__key,
      "selections": ",".join(fields),
    }
    url = "{}/market/".format(self.__base_url)
    if item_id:
      url += item_id
    resp = requests.get(url, params=params)
    return resp.json()

  def torn(self, fields, user_id=None):
    """Fetch TORN information.

If user ID is unspecified, the user related to the API key is used.

Fields: bank, cards, companies, competition, education, factiontree, gyms, honors, items,
logcategories, logtypes, medals, organisedcrimes, pawnshop, properties, rackets, raids, stats,
stocks, territory, territorywars, timestamp
    """
    params = {
      "key": self.__key,
      "selections": ",".join(fields),
    }
    url = "{}/torn/".format(self.__base_url)
    if user_id:
      url += user_id
    resp = requests.get(url, params=params)
    return resp.json()
