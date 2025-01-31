# Copyright 2025 Pextra Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import json, requests, os
from urllib.parse import urlparse

from typing import TypedDict

def open_file(file_path: str):
	directory = os.path.dirname(file_path)

	if not os.path.exists(directory):
		os.makedirs(directory)
	return open(file_path, 'w')

def read_sources():
	with open('sources/iso_list.json') as json_file:
		return json.load(json_file)

def get_final_url_and_content_length(url: str, depth=0):
	if depth > 5:
		raise requests.RequestException("Too many redirects")
	else:
		response = requests.head(url)
		if response.status_code == 302:
			next_url = response.headers['Location']
			if next_url.startswith('/'):
				# Handle relative redirects
				parsed_url = urlparse(url)
				next_url = f"{parsed_url.scheme}://{parsed_url.netloc}{next_url}"

			return get_final_url_and_content_length(next_url, depth + 1)
		elif response.status_code != 200:
			raise requests.RequestException(f"Unexpected status code {response.status_code}")

		print(f" {response.status_code} ({depth} redirects)")
		return url, response.headers.get('Content-Length')

class ProbeIsoImagePayload(TypedDict):
	version: str
	long_version: str # optional
	architecture: str
	url_format: str
class ProbedIsoImage(TypedDict):
	download_url: str
	content_length: str
def probe_image(iso: ProbeIsoImagePayload) -> ProbedIsoImage:
	# Default long_version to version if not present
	if "long_version" not in iso:
		iso["long_version"] = iso["version"]
	formatted_url = iso["url_format"].format(version=iso["version"], arch=iso["architecture"], long_version=iso["long_version"])

	# Follow redirects to get final URL
	final_url = formatted_url
	try:
		response = get_final_url_and_content_length(formatted_url)
		final_url = response[0]
		content_length = response[1]
	except requests.RequestException:
		raise Exception(f"Failed to probe {formatted_url}!")

	return {
		"download_url": final_url,
		"content_length": content_length
	}

class IsoImageRequirements(TypedDict):
	cpu: int
	memory: int
	disk: int

class IsoImage(TypedDict):
	name: str
	description: str
	image: str
	versions: list[str]
	long_versions: list[str] # optional
	architectures: list[str]
	url_format: str
	# url_format_{arch} can be used to override url_format for specific architectures
	requirements: IsoImageRequirements # optional

def download_image(iso: IsoImage):
	image_ext = os.path.splitext(iso["image"])[1]
	image_path = f"output/images/{iso['name'].replace(' ', '_')}{image_ext}"
	print(f"\tDownloading image to {image_path}...")

	with requests.get(iso["image"], stream=True) as r:
		r.raise_for_status()
		with open(image_path, 'wb') as f:
			for chunk in r.iter_content(chunk_size=8192):
				f.write(chunk)

class IsoList(TypedDict):
	iso_images: list[IsoImage]
def build_iso_list(iso_list: IsoList):
	iso_imgs = []
	for iso in iso_list:
		iso_name = iso["name"]

		print(f"\nBuilding list for {iso_name}...")
		iso_img = {
			"name": iso_name,
			"description": iso["description"],
			"image": iso["image"],
			"requirements": iso.get("requirements", {}),
			"downloads": {}
		}

		download_image(iso)
		for i, version in enumerate(iso["versions"]):
			long_version = iso["long_versions"][i] if "long_versions" in iso else version

			iso_img["downloads"][version] = {}
			for architecture in iso["architectures"]:
				print(f"\tProbing {version} ({architecture})...", end='')
				probe_payload: ProbeIsoImagePayload = {
					"version": version,
					"long_version": long_version,
					"architecture": architecture,
					"url_format": iso.get(f"url_format_{architecture}", iso["url_format"]) # try url_format_{arch}, fallback to url_format
				}

				probed_iso = probe_image(probe_payload)
				iso_img["downloads"][version][architecture] = probed_iso

		iso_imgs.append(iso_img)
	return {
		"iso_images": iso_imgs
	}

iso_list = read_sources()
result = build_iso_list(iso_list)

output_file = open_file('output/library.json')
output_file.write(json.dumps(result, indent=2))
output_file.close()

print("ISO images JSON structure created successfully.")
