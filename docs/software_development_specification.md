# Software Development Specification (SDS)

## 1. Introduction
This Software Development Specification defines the functional and non-functional expectations for the Nearest City Distance service. The project delivers HTTP APIs that map geographic coordinates to nearby cities and enclosing countries. The SDS documents the current behavior, operational assumptions, technology stack, and quality requirements so the team can maintain, extend, and validate the system consistently.

## 2. Scope
The specification covers the Flask-based web service contained in this repository, including:

- Application factory and configuration objects under `nearest_city_distance/`.
- HTTP endpoints exposed by the `main` blueprint.
- Geospatial helper modules (`get_distance` and `get_country`) and their datasets.
- Shared security mechanism (token-based access control).
- Build, deployment, and testing practices codified in the repository.

Out-of-scope items include downstream consumers of the API, infrastructure outside the repository (e.g., hosting, load balancers), and any future interfaces that are not yet implemented (CLI, gRPC, etc.).

## 3. System Overview

### 3.1 High-Level Architecture
- **Presentation/API Layer**: Flask blueprint `nearest_city_distance.main` defines `/get_nearest_city` and `/get_country` routes.
- **Domain Layer**: `get_distance` computes nearest city and distance; `get_country` performs shapefile lookups and reverse geocoding fallbacks.
- **Infrastructure Layer**: Static datasets `data/world_cities_RG.csv` and `data/ec_pe_co.shp` provide geospatial data. Third-party libraries include `reverse_geocoder`, `geopy`, `pyshp`, and `flask`.
- **Configuration**: `config.py` supplies environment-specific settings, including dataset paths and a shared access token. `manage.py` bootstraps the app by invoking `create_app`.

### 3.2 Runtime Flow
1. Client issues a GET request with latitude, longitude, and access token.
2. Flask view validates the token against the configured hash.
3. Request parameters are parsed as floats; errors return HTTP 400.
4. The appropriate helper module loads geospatial data, runs the lookup, and returns results.
5. View serializes the response as JSON.

## 4. Functional Requirements

### 4.1 `/get_nearest_city`
- **Method**: GET
- **Parameters**:
  - `lat` (required, float)
  - `lng` (required, float)
  - `token` (required, string)
- **Behavior**:
  1. Validate the access token.
  2. Compute the nearest city using `world_cities_RG.csv` via `reverse_geocoder`.
  3. Compute geodesic distance to the provided coordinates using `geopy.distance.geodesic`.
  4. Return JSON containing the distance (kilometers), city name, and province/state.
- **Errors**:
  - Missing or invalid token → HTTP 401 with an error message.
  - Invalid coordinates → HTTP 400.
  - Internal errors → HTTP 500.

### 4.2 `/get_country`
- **Method**: GET
- **Parameters**: `lat`, `lng`, and `token` as above.
- **Behavior**:
  1. Validate the access token.
  2. Determine whether the coordinate lies within the Ecuador–Colombia–Peru shapefile. If so, return the associated country attribute.
  3. If the point is outside the shapefile, perform a reverse-geocoder lookup to obtain the ISO country code and map it to a full country name.
- **Errors**: Same as `/get_nearest_city`.

### 4.3 Authentication
- Access is protected by a shared secret token defined in configuration (`ACCESS_TOKEN`).
- Views hash the configured token with `werkzeug.security.generate_password_hash` and compare it with the client-provided token using `check_password_hash`.

### 4.4 Configuration
- Supported profiles: `development`, `testing`, and `production` (derived from `Config` subclasses).
- Datasets paths default to files in the `data/` directory but can be overridden via environment variables when instantiating the app factory.

## 5. Non-Functional Requirements

### 5.1 Performance
- Initial implementation reloads datasets per request. Future optimization goal: instantiate reverse geocoder and shapefile reader once per process (target response time < 200 ms for cached lookups).
- API should handle concurrent requests proportional to typical Flask deployments with Gunicorn/WSGI.

### 5.2 Reliability & Availability
- Service should return deterministic results for identical coordinates while datasets remain unchanged.
- Error handling must avoid leaking stack traces; return structured JSON with error codes/messages.

### 5.3 Security
- Enforce HTTPS termination at deployment level.
- Protect the shared token via environment variables or secrets management.
- Rate limiting is recommended for production usage (not currently implemented).

### 5.4 Maintainability
- Code should follow Python 3.10+ conventions, use dependency injection via `create_app`, and keep business logic separate from Flask views.
- Documentation (README and docs/) must reflect configuration and dataset requirements.

### 5.5 Observability
- Logging should capture request metadata, lookup results, and errors. Currently limited to default Flask logging; enhancements should define structured logging and metrics if needed.

## 6. Data Management
- **City Index**: `world_cities_RG.csv` must remain synchronized with the reverse-geocoder expectations (columns: latitude, longitude, city, admin area, country code).
- **Shapefile Assets**: `ec_pe_co.shp` plus companion files (.shx, .dbf, etc.) must be co-located. Coordinate reference system must align with input coordinates (WGS84).
- Data updates require regression testing to confirm lookup accuracy.

## 7. External Dependencies
- Python packages: `Flask`, `geopy`, `reverse_geocoder`, `pyshp`, `Werkzeug`, plus testing tools (`pytest`).
- Optional documentation dependencies defined in `docs/` Sphinx configuration.

## 8. Deployment & Environment
- Service is started via `manage.py` or by importing `create_app` into a WSGI runner (e.g., Gunicorn).
- Environment variables:
  - `FLASK_CONFIG`: selects configuration profile.
  - `ACCESS_TOKEN`: overrides default token.
  - `WORLD_CITIES_CSV`, `SHAPEFILE_PATH`: override dataset locations if needed.
- Containerization support provided via `Dockerfile` (ensure dependencies are installed via `requirements.txt`).

## 9. Testing & Quality Assurance
- Current automated tests: `test/test_get_distance.py` verifies helper functions for a Quito coordinate.
- Planned coverage improvements:
  - HTTP endpoint tests (success, authentication failure, invalid inputs).
  - Integration tests verifying fallback behavior outside shapefile coverage.
  - Performance smoke tests for dataset loading and caching.
- CI pipeline should run linting (`flake8`/`black`), static typing (`mypy`/`pyright`), and pytest suite.

## 10. Documentation & Training
- README provides setup instructions; keep it aligned with configuration changes.
- `docs/project_status.md` summarizes current architecture; `docs/suggested_modifications.md` tracks recommended refactors.
- Developers should update this SDS when introducing new endpoints, datasets, or architectural components.

## 11. Future Enhancements
- Introduce service layer classes (`CityLocator`, `CountryLocator`) to cache geospatial resources.
- Modularize the API layer to separate request parsing, authentication, and serialization.
- Expand authentication to support per-client tokens or OAuth if required.
- Add monitoring dashboards for request latency and dataset freshness.

## 12. Acceptance Criteria
- All implemented endpoints meet the functional requirements above.
- All dependencies are documented and pinned in `requirements.txt`.
- Automated test suite passes and covers critical paths (lookup success and error conditions).
- Deployment artifacts (Dockerfile, manage.py) can start the service with configured datasets.

## 13. Glossary
- **SDS**: Software Development Specification.
- **Geodesic Distance**: The shortest distance between two points on the Earth’s surface, accounting for its curvature.
- **Reverse Geocoding**: Converting latitude/longitude into human-readable location attributes.
- **Shapefile**: A geospatial vector data format containing geometries and attributes.

## 14. Revision History
- **v1.0 (2024-XX-XX)**: Initial SDS extracted from repository state and architecture review findings.
