[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=EL-BID_github-api-traffic&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=EL-BID_github-api-traffic)

# Repository Traffic Data

This repository contains traffic data for multiple repositories. The data is provided in JSON format, with each repository having its own section. Below is an explanation of each section within the JSON data:

## Repository Section

The repository section provides information about a specific repository.

### `repository`

- Description: The name of the repository.
- Type: String

### Traffic Section

The traffic section provides traffic-related information for the repository, including clone and view statistics.

#### Clones

The clones section provides clone statistics for the repository.

##### `consolidated`

- Description: Consolidated clone count and unique clone count for the repository.
- Properties:
  - `count`: Total number of clones.
  - `unique`: Number of unique clones.

##### `history`

- Description: Historical clone data for the repository.
- Properties:
  - `timestamp`: Timestamp of the clone data.
  - `count`: Number of clones at the given timestamp.
  - `unique`: Number of unique clones at the given timestamp.

#### Views

The views section provides view statistics for the repository.

##### `consolidated`

- Description: Consolidated view count and unique view count for the repository.
- Properties:
  - `count`: Total number of views.
  - `unique`: Number of unique views.

##### `history`

- Description: Historical view data for the repository.
- Properties:
  - `timestamp`: Timestamp of the view data.
  - `count`: Number of views at the given timestamp.
  - `unique`: Number of unique views at the given timestamp.

#### Referrers

The referrers section provides information about the sources that referred to the repository.

- Description: List of referrer sources.
- Properties:
  - `source`: Source that referred to the repository.
  - `count`: Number of referrals from the source.
  - `unique`: Number of unique referrals from the source.

#### Paths

The paths section provides information about the paths within the repository that were accessed.

- Description: List of paths within the repository.
- Properties:
  - `path`: Path within the repository.
  - `title`: Title or description of the path.
  - `count`: Number of times the path was accessed.
  - `unique`: Number of unique accesses to the path.

#### Forks

The forks section provides information about the forks of the repository.

- Description: List of forks of the repository.
- Properties:
  - `url`: URL of the forked repository.

##### `forks_count`

- Description: Total count of forks for the repository.

