import logging
import re

import pandas as pd
from django.contrib.gis.geos import Polygon, Point
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from pyoscar import OSCARClient

from .constants import DATA_PARAMETERS_DICT

logger = logging.getLogger(__name__)


def get_data_parameters_as_choices():
    return [(key, value["name"]) for key, value in DATA_PARAMETERS_DICT.items()]


def create_default_data_parameters():
    from .models import DataParameter

    logger.info("Creating default data parameters")

    for key, value in DATA_PARAMETERS_DICT.items():
        data = {
            "name": value.get("name"),
            "parameter": key,
            "unit": value.get("unit"),
            "description": value.get("description"),
        }

        if DataParameter.objects.filter(parameter=key).exists():
            logger.info(f"Data parameter with parameter {key} already exists")
            continue

        logger.info(f"Creating data parameter with parameter {key} ...")
        DataParameter.objects.create(**data)

    logger.info("Default data parameters created successfully")


def is_valid_wigos_id(wigos_id):
    """
    Validates if the given string is a valid WMO WIGOS ID.

    Args:
    wigos_id (str): The WIGOS ID to validate.

    Returns:
    bool: True if the WIGOS ID is valid, False otherwise.
    """
    # Define the regular expression pattern for a valid WIGOS ID
    pattern = r"^\d+-\d+-\d+-\w+$"

    # Use the re.match function to check if the input string matches the pattern
    if re.match(pattern, wigos_id):
        return True
    else:
        return False


def get_wigos_id_parts(wigos_id):
    parts = wigos_id.split("-")

    wsi_series = parts[0]
    wsi_issuer = parts[1]
    wsi_issue_number = parts[2]
    wsi_local = parts[3]

    return {
        "wsi_series": wsi_series,
        "wsi_issuer": wsi_issuer,
        "wsi_issue_number": wsi_issue_number,
        "wsi_local": wsi_local,
    }


def get_stations_for_country_live(country, as_dict=False):
    client = OSCARClient()
    iso = country.alpha3

    stations = client.get_stations(country=iso)
    results = stations.get("stationSearchResults")

    stations = []

    bounds = country.geo_extent
    bounds_polygon = Polygon.from_bbox(bounds)

    for station in results:
        wigos_id = station.get("wigosId")
        longitude = station.get("longitude")
        latitude = station.get("latitude")

        wigos_station_identifiers = station.get("wigosStationIdentifiers")

        if not wigos_id and wigos_station_identifiers:
            wigos_id = wigos_station_identifiers[0].get("wigosStationIdentifier")

        if not wigos_id and not longitude and latitude:
            continue

        station_data = {
            "wigos_id": wigos_id,
            "name": station.get("name"),
            "elevation": station.get("elevation"),
            "longitude": station.get("longitude"),
            "latitude": station.get("latitude"),
        }

        point = Point(x=longitude, y=latitude)
        if not bounds_polygon.contains(point):
            station_data["out_of_bounds"] = True

        stations.append(station_data)

    if as_dict:
        stations = {station["wigos_id"]: station for station in stations}

    return stations


def get_stations_for_country_local(as_dict=False):
    from .models import OscarSurfaceStationLocal

    stations = OscarSurfaceStationLocal.objects.all().values()

    if as_dict:
        stations = {station.get("wigos_id"): station for station in stations}

    return stations


def get_object_or_none(model_class, **kwargs):
    try:
        return model_class.objects.get(**kwargs)
    except model_class.DoesNotExist:
        return None


def get_station_directory_path(ingestion_record, filename):
    wigos_id = ingestion_record.station.wigos_id
    date = ingestion_record.utc_time.strftime("%Y/%m/%d")

    return f"station_data/{wigos_id}/{date}/{filename}"


def extract_digits(s):
    # Regular expression to match the first continuous digits
    match = re.match(r"(\d+)", s)
    if match:
        return match.group(0)
    return None


def validate_as_integer(value):
    try:
        int(value)
    except ValueError:
        raise ValidationError("The value must be an integer")


def create_ingestion_file_with_hourly_time(ingestion_record):
    df = pd.read_csv(ingestion_record.file.path)

    new_time = ingestion_record.next_top_of_hour

    # Update the observation year, month, day, hour, and minute
    df["year"] = new_time.year
    df["month"] = new_time.month
    df["day"] = new_time.day
    df["hour"] = new_time.hour
    df["minute"] = new_time.minute

    csv_content = df.to_csv(index=False)
    file = ContentFile(csv_content, ingestion_record.filename)

    return file
