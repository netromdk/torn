import requests

class TornApi:
  def __init__(self, key):
    if not isinstance(key, str):
      raise Exception("API key must be a string! " + str(key))
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
    return self.__get("user", user_id, fields, since, until)

  def property(self, property_id=None, fields=None):
    """Fetch property information.

If property ID is unspecified, the property related to the API key is used.

Fields: property, timestamp
    """
    return self.__get("property", property_id, fields)

  def faction(self, faction_id=None, fields=None, since=None, until=None):
    """Fetch faction information.

If faction ID is unspecified, the faction related to the API key is used.

UNIX epoch timestamps `since` and `until` work for some fields.

Fields: applications, armor, armorynews, attacknews, attacks, attacksfull, basic, boosters, cesium,
chain, chains, contributors, crimenews, crimes, currency, donations, drugs, fundsnews, mainnews,
medical, membershipnews, reports, revives, revivesfull, stats, temporary, territory, timestamp,
upgrades, weapons
    """
    return self.__get("faction", faction_id, fields, since, until)

  def company(self, company_id=None, fields=None):
    """Fetch company information.

If company ID is unspecified, the company related to the API key is used.

Fields: applications, detailed, employees, news, newsfull, profile, stock, timestamp
    """
    return self.__get("company", company_id, fields)

  def market(self, item_id=None, fields=None):
    """Fetch item market information.

Fields: bazaar, itemmarket, pointsmarket, timestamp
    """
    return self.__get("market", item_id, fields)

  def torn(self, fields, user_id=None):
    """Fetch TORN information.

If user ID is unspecified, the user related to the API key is used.

Fields: bank, cards, companies, competition, education, factiontree, gyms, honors, items,
logcategories, logtypes, medals, organisedcrimes, pawnshop, properties, rackets, raids, stats,
stocks, territory, territorywars, timestamp
    """
    return self.__get("torn", user_id, fields)

  def __get(self, name, id=None, fields=None, since=None, until=None):
    fields = fields or []
    params = {
      "key": self.__key,
      "selections": fields if isinstance(fields, str) else ",".join(fields),
    }
    if since:
      params["from"] = str(int(since))
    if until:
      params["to"] = str(int(until))
    url = "{}/{}/".format(self.__base_url, name)
    if id:
      url += str(id)
    resp = requests.get(url, params=params)
    return resp.json()
