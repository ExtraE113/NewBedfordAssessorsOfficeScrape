# parse each file in /html and extract the data
import csv
import os
import bs4
from tqdm import tqdm

template = {
	"Location": "",
	"ParcelID": "",
	"Zoning": "",
	"Fiscal Year": "",
	"Account Number": "",
	"Current Owner": "",
	"Current Sales info": {
		"Sale Date": "",
		"Sale Price": "",
		"Legal Reference": "",
		"Grantor": "",
	},
	"Text Description": "",
	"Building Value": "",
	"Land Value": "",
	"Yard Items Value": "",
	"Total Value": "",
	"Fiscal data": {
		"2022": {
			"Tax Rate Res.:": "",
			"Tax rate Com.:": "",
			"Property Code": "",
			"Total Bldg Value": "",
			"Total Yard Value": "",
			"Land Value": "",
			"Tax": "",
		},
		"2021": {
			"Tax Rate Res.:": "",
			"Tax rate Com.:": "",
			"Property Code": "",
			"Total Bldg Value": "",
			"Total Yard Value": "",
			"Land Value": "",
			"Tax": "",
		},
		"2020": {
			"Tax Rate Res.:": "",
			"Tax rate Com.:": "",
			"Property Code": "",
			"Total Bldg Value": "",
			"Total Yard Value": "",
			"Land Value": "",
			"Tax": "",
		},
	},
	"Ezra's Notes": "",
}

properties = []


def flatten_dict(dd, separator='_', prefix=''):
	return {prefix + separator + k if prefix else k: v
			for kk, vv in dd.items()
			for k, v in flatten_dict(vv, separator, kk).items()
			} if isinstance(dd, dict) else {prefix: dd}


for filename in tqdm(os.listdir('./html/')):
	with open(os.path.join('./html', filename)) as f:
		# parse
		f_contents = f.read()

		soup = bs4.BeautifulSoup(f_contents, 'html.parser')

		# skip if title is 500 Internal Server Error
		if soup.title.text == "500 - Internal server error.":
			continue

		# extract
		data = soup.find_all('td')
		try:
			# fill template
			active = template.copy()

			i = 0
			active['Location'] = data[0].text.split(":")[-1].strip()
			active['ParcelID'] = data[1].text.split(":")[-1].strip()
			active['Zoning'] = data[2].text.split(":")[-1].strip()
			active['Fiscal Year'] = data[3].text.split(":")[-1].strip()
			active['Account Number'] = data[4].text.split(":")[-1].strip()
			active['Current Owner'] = data[5].text.split(":")[-1].strip()

			if "Card #:" in f_contents:
				active["Ezra's Notes"] += "Has multiple cards, may be missing data."
				# remove card label
				data.pop(6)

			sales_info = data[6].text.split(":")
			active['Current Sales info']['Sale Date'] = sales_info[2].split('\n')[0].strip()
			active['Current Sales info']['Sale Price'] = sales_info[3].split('\n')[0].strip()
			active['Current Sales info']['Legal Reference'] = sales_info[4].split('\n')[0].strip()
			active['Current Sales info']['Grantor'] = sales_info[5].split('\n')[0].strip()

			active['Text Description'] = data[8].text
			active['Building Value'] = data[9].text.split(':')[-1].strip()
			active['Land Value'] = data[10].text.split(':')[-1].strip()
			active['Yard Items Value'] = data[11].text.split(':')[-1].strip()
			active['Total Value'] = data[12].text.split(':')[-1].strip()

			active['Fiscal data']['2022']['Tax Rate Res.:'] = data[24].text.split(':')[-1].strip()
			active['Fiscal data']['2021']['Tax Rate Res.:'] = data[27].text.split(':')[-1].strip()
			active['Fiscal data']['2020']['Tax Rate Res.:'] = data[30].text.split(':')[-1].strip()
			active['Fiscal data']['2022']['Tax rate Com.:'] = data[32].text.split(':')[-1].strip()
			active['Fiscal data']['2021']['Tax rate Com.:'] = data[35].text.split(':')[-1].strip()
			active['Fiscal data']['2020']['Tax rate Com.:'] = data[38].text.split(':')[-1].strip()
			active['Fiscal data']['2022']['Property Code'] = data[40].text.split(':')[-1].strip()
			active['Fiscal data']['2021']['Property Code'] = data[43].text.split(':')[-1].strip()
			active['Fiscal data']['2020']['Property Code'] = data[46].text.split(':')[-1].strip()
			active['Fiscal data']['2022']['Total Bldg Value'] = data[48].text.split(':')[-1].strip()
			active['Fiscal data']['2021']['Total Bldg Value'] = data[51].text.split(':')[-1].strip()
			active['Fiscal data']['2020']['Total Bldg Value'] = data[54].text.split(':')[-1].strip()
			active['Fiscal data']['2022']['Total Yard Value'] = data[56].text.split(':')[-1].strip()
			active['Fiscal data']['2021']['Total Yard Value'] = data[59].text.split(':')[-1].strip()
			active['Fiscal data']['2020']['Total Yard Value'] = data[62].text.split(':')[-1].strip()
			active['Fiscal data']['2022']['Land Value'] = data[64].text.split(':')[-1].strip()
			active['Fiscal data']['2021']['Land Value'] = data[67].text.split(':')[-1].strip()
			active['Fiscal data']['2020']['Land Value'] = data[70].text.split(':')[-1].strip()
			active['Fiscal data']['2022']['Total Value'] = data[72].text.split(':')[-1].strip()
			active['Fiscal data']['2021']['Total Value'] = data[75].text.split(':')[-1].strip()
			active['Fiscal data']['2020']['Total Value'] = data[78].text.split(':')[-1].strip()
			active['Fiscal data']['2022']['Tax'] = data[80].text.split(':')[-1].strip()
			active['Fiscal data']['2021']['Tax'] = data[83].text.split(':')[-1].strip()
			active['Fiscal data']['2020']['Tax'] = data[86].text.split(':')[-1].strip()

			properties.append(flatten_dict(active))

		except Exception as e:
			print(filename)
			raise e

# write to csv
with open('properties.csv', 'w') as f:
	writer = csv.DictWriter(f, fieldnames=properties[0].keys(), quoting=csv.QUOTE_ALL)
	writer.writeheader()
	writer.writerows(properties)
