import requests
import json
from datetime import datetime, timezone
from os.path import exists

class TornApi:
  def __init__(self, key, cache_file=None):
    if not isinstance(key, str):
      raise Exception("API key must be a string! " + str(key))
    self.__base_url = "https://api.torn.com"
    self.__key = key
    self.__cache_file = cache_file
    self.__cache = dict()  # (url, params json) -> (expire timestamp, json result)
    self.__load_cache()

  def __enter__(self):
    return self

  def __exit__(self, exc_type, exc_value, traceback):
    self.__save_cache()

  @staticmethod
  def today():
    return datetime.now(timezone.utc)

  @staticmethod
  def during_today(timestamp):
    return TornApi.today().date() == datetime.fromtimestamp(timestamp, timezone.utc).date()

  def user(self, user_id=None, fields=None, since=None, until=None, ttl=60):
    """Fetch user information.

If user ID is unspecified, the user related to the API key is used.

UNIX epoch timestamps `since` and `until` work for some fields.

Fields: ammo, attacks, attacksfull, bars, basic, battlestats, bazaar, cooldowns, crimes, discord,
display, education, events, gym, hof, honors, icons, inventory, jobpoints, log, medals, merits,
messages, money, networth, notifications, perks, personalstats, profile, properties, receivedevents,
refills, reports, revives, revivesfull, skills, stocks, timestamp, travel, weaponexp, workstats
    """
    return self.__get("user", user_id, fields, since, until, ttl=ttl)

  def property(self, property_id=None, fields=None, ttl=60):
    """Fetch property information.

If property ID is unspecified, the property related to the API key is used.

Fields: property, timestamp
    """
    return self.__get("property", property_id, fields, ttl=ttl)

  def faction(self, faction_id=None, fields=None, since=None, until=None, ttl=60):
    """Fetch faction information.

If faction ID is unspecified, the faction related to the API key is used.

UNIX epoch timestamps `since` and `until` work for some fields.

Fields: applications, armor, armorynews, attacknews, attacks, attacksfull, basic, boosters, cesium,
chain, chains, contributors, crimenews, crimes, currency, donations, drugs, fundsnews, mainnews,
medical, membershipnews, reports, revives, revivesfull, stats, temporary, territory, timestamp,
upgrades, weapons
    """
    return self.__get("faction", faction_id, fields, since, until, ttl=ttl)

  def company(self, company_id=None, fields=None, ttl=60):
    """Fetch company information.

If company ID is unspecified, the company related to the API key is used.

Fields: applications, detailed, employees, news, newsfull, profile, stock, timestamp
    """
    return self.__get("company", company_id, fields, ttl=ttl)

  def market(self, item_id=None, fields=None, ttl=60):
    """Fetch item market information.

Fields: bazaar, itemmarket, pointsmarket, timestamp
    """
    return self.__get("market", item_id, fields, ttl=ttl)

  def torn(self, fields, user_id=None, ttl=60):
    """Fetch TORN information.

If user ID is unspecified, the user related to the API key is used.

Fields: bank, cards, companies, competition, education, factiontree, gyms, honors, items,
logcategories, logtypes, medals, organisedcrimes, pawnshop, properties, rackets, raids, stats,
stocks, territory, territorywars, timestamp
    """
    return self.__get("torn", user_id, fields, ttl=ttl)

  def __get(self, name, id=None, fields=None, since=None, until=None, ttl=60):
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
    result = self.__get_cache(url, params)
    if result is None:
      result = requests.get(url, params=params).json()
      if isinstance(ttl, int) and ttl > 0:
        self.__add_cache(url, params, result, ttl)
    return result

  def __cache_key(self, url, params):
    return (url, json.dumps(params))

  def __get_cache(self, url, params):
    """Return cached value for `(url, params)` if cached and not expired. Remove from cache if
expired."""
    key = self.__cache_key(url, params)
    if key in self.__cache:
      (exp_ts, result) = self.__cache[key]
      if datetime.now().timestamp() < exp_ts:
        return result
      else:
        del(self.__cache[key])
    return None

  def __add_cache(self, url, params, result, ttl):
    self.__add_cache_raw(url, params, datetime.now().timestamp() + ttl, result)

  def __add_cache_raw(self, url, params, exp_ts, result):
    self.__cache[self.__cache_key(url, params)] = (exp_ts, result)

  def __save_cache(self):
    if self.__cache_file is not None:
      with open(self.__cache_file, mode="w") as fp:
        data = []
        for (url, params) in self.__cache.keys():
          (exp_ts, result) = self.__cache[(url, params)]
          data.append((url, json.loads(params), exp_ts, result))
        json.dump(data, fp)

  def __load_cache(self):
    if self.__cache_file is not None and exists(self.__cache_file):
      with open(self.__cache_file, mode="r") as fp:
        data = json.load(fp)
        for (url, params, exp_ts, result) in data:
          self.__add_cache_raw(url, params, exp_ts, result)
