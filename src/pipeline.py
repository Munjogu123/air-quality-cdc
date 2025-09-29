import os

import requests
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import CollectionInvalid

load_dotenv()

URI = os.getenv("DB_URI")


def main():
    coords = {"nairobi": (-1.286389, 36.817223), "mombasa": (-4.043477, 39.668206)}

    db = create_db_collection("trial", coords)
    for city, coords in coords.items():
        try:
            data = extract(city, coords)
            load_data(db, city, data)
        except Exception as e:
            print(e)
            continue


def create_db_collection(db_name: str, coords: dict):
    client = MongoClient(URI)
    db = client[db_name]

    for town in coords:
        try:
            db.create_collection(town)
        except CollectionInvalid:
            print(f"Collection {town} already exists")

    return db


def extract(city: str, coords: tuple) -> list:
    lat = coords[0]
    lon = coords[1]
    base_url = f"https://air-quality-api.open-meteo.com/v1/air-quality?latitude={lat}&longitude={lon}&hourly=pm2_5,pm10,ozone,carbon_monoxide,nitrogen_dioxide,sulphur_dioxide,uv_index"
    response = requests.get(base_url)

    if response.status_code == 200:
        town_data = {}
        data = response.json()
        hourly_data = data["hourly"]
        town_data["time"] = hourly_data["time"]
        town_data["pm2_5"] = hourly_data["pm2_5"]
        town_data["pm10"] = hourly_data["pm10"]
        town_data["ozone"] = hourly_data["ozone"]
        town_data["carbon_monoxide"] = hourly_data["carbon_monoxide"]
        town_data["nitrogen_dioxide"] = hourly_data["nitrogen_dioxide"]
        town_data["sulphur_dioxide"] = hourly_data["sulphur_dioxide"]
        town_data["uv_index"] = hourly_data["uv_index"]

        mongo_data = []
        for index, time in enumerate(town_data["time"]):
            mongo_data.append(
                {
                    "city": city,
                    "time": time,
                    "pm2_5": town_data["pm2_5"][index],
                    "pm10": town_data["pm10"][index],
                    "ozone": town_data["ozone"][index],
                    "carbon_monoxide": town_data["carbon_monoxide"][index],
                    "nitrogen_dioxide": town_data["nitrogen_dioxide"][index],
                    "sulphur_dioxide": town_data["sulphur_dioxide"][index],
                    "uv_index": town_data["uv_index"][index],
                }
            )

        return mongo_data


def load_data(db, city: str, data: list) -> None:
    collection = db[str(city)]
    collection.insert_many(data)


if __name__ == "__main__":
    main()
