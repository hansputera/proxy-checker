import requests
from bs4 import BeautifulSoup
from random import choice

proxiesArray = []

listTargets = [
	"https://google.com",
	"https://microsoft.com",
	"https://duckduckgo.com",
	"https://discord.com",
	"https://whoer.net"
]

# check proxy function.
def checkProxy(targetHost: str, proxy: str) -> bool:
	proxies = { "https": f"http://{proxy}" }
	try:
		response = requests.get(targetHost, proxies=proxies, timeout=7)
		if response.reason != "OK":
			return False
		else:
			return True
	except:
		return False


# List proxy function
def proxies():
	url = "https://sslproxies.org/";
	response = requests.get(url)
	
	html = response.text
	soup = BeautifulSoup(html, "html5lib")

	rows = soup.find('table').findNext('tbody').find_all('tr')
	for row in rows:
		data = row.find_all('td')

		proxy_ = f"{data[0].text.strip()}:{data[1].text.strip()}"
		
		print(f"Found {proxy_}")
		target = choice(listTargets)
		print(f"Checking {proxy_} to {target}")
		goodProxy = checkProxy(target, proxy_)
		if goodProxy is False:
			print(f"{proxy_} is bad, [{target}]\n")
		else:
			print(f"{proxy_} is good, [{target}]")
			fl = open("proxies.txt", "a+")
			fl.write(f"\n{proxy_}")
			fl.close()
			country = data[3].text.strip()
			lastCheck = data[-1].text.strip()

			print(f"{proxy_}, country: {country} {lastCheck}\n\n")
			
			proxiesArray.append({
				"proxy": proxy_,
				"country": country,
				"last_check": lastCheck
			})
	return proxiesArray

proxies()