# Project Status

## Overview
The project provides a Flask-based HTTP API that exposes two GET endpoints for geospatial lookups:

- `/get_nearest_city`: returns the closest city and its distance from a provided latitude/longitude pair.
- `/get_country`: returns the country containing the coordinate, or a fallback derived from a global reverse-geocoder index.

The service relies on static datasets distributed in the repository (`data/world_cities_RG.csv` and `data/ec_pe_co.shp`) and uses the `reverse_geocoder`, `geopy`, and `pyshp` libraries for lookup logic.

## Application Structure
- **Application factory (`nearest_city_distance/__init__.py`)** – Implements `create_app`, which loads a configuration profile and registers the `main` blueprint containing all HTTP routes.
- **Configuration (`config.py`)** – Provides development and production configuration classes, including defaults for the access token and dataset paths. The factory always instantiates them from the module-level `config` mapping.
- **Blueprint (`nearest_city_distance/main/__init__.py`)** – Declares the `main` blueprint used by the application factory.
- **Views (`nearest_city_distance/main/views.py`)** – Defines the `/get_nearest_city` and `/get_country` endpoints. Both handlers validate an access token, parse query parameters, and call into helper modules.
- **Domain helpers (`nearest_city_distance/main/get_distance.py`, `nearest_city_distance/main/get_country.py`)** – Contain the geospatial lookup logic. Each helper loads its respective dataset and performs the necessary calculations every time it is invoked.
- **Legacy runner (`nearest_city_distance/app_get_distance.py`)** – A standalone Flask application that exposes only `/get_nearest_city` and duplicates authentication logic outside the package namespace.
- **Command entry point (`manage.py`)** – Creates the Flask application using the `FLASK_CONFIG` environment variable (defaulting to `default`) and runs the development server.
- **Tests (`test/test_get_distance.py`)** – Include two unit tests that exercise the helper functions directly, verifying the results for a known coordinate in Quito, Ecuador.

## Datasets & Assets
- `data/world_cities_RG.csv` – Reverse geocoder index used to find the nearest city and as a fallback when the shapefile does not contain a coordinate.
- `data/ec_pe_co.shp` and related shapefile assets – Polygon data for Ecuador, Colombia, and Peru used for point-in-polygon country detection.

## Security & Configuration
- Access control uses a single shared token stored in configuration and hashed per request inside each view.
- Configuration defaults embed the token and dataset paths; there is no environment-specific override for the dataset locations in the current helpers.

## Known Limitations & Bugs
- **Token failures raise server errors:** Both view functions return a response only when the token is valid. Invalid or missing tokens lead to Flask raising a “view function did not return a valid response” error (HTTP 500).
- **Duplicate nearest-city lookup:** `/get_nearest_city` calls `get_distance.get_nearest_city` twice per request, causing redundant file I/O and computation.
- **Fallback country name mismatch:** `get_nearest_country` returns the `admin2` attribute (a second-level administrative area) instead of the true country name when the shapefile lacks coverage.
- **Global configuration usage:** Helper modules import `config['default']` at import time, preventing alternative configurations from being injected and forcing dataset reloads per invocation.
- **High per-request overhead:** `reverse_geocoder.RGeocoder` and shapefile readers are instantiated inside each request handler, so no caching occurs across calls.

## Testing Status
- Automated coverage is limited to the two helper tests; there are no HTTP-level tests, no negative scenarios, and no coverage for authentication, fallback paths, or error handling.
- No continuous integration configuration is present in the repository to enforce linting or testing automatically.

## Documentation & Tooling
- The README documents basic setup with Conda and the manual `/get_nearest_city` request example.
- A Sphinx documentation scaffold exists under `docs/`, but its content is not evaluated as part of this summary.
