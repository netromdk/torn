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
