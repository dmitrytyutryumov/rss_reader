# RSS reader

## Description
The project collects RSS feeds and show collected.

## How to run the project
### Local run

Prepare env
1. install [pyenv](https://github.com/pyenv/pyenv#installation)
2. Install [poetry](https://python-poetry.org/docs/#installation)
3. Install python 3.9 `pyenv install 3.9.4`
4. Set 3.9 version local for project `pyenv local 3.9.4`
5. Install dependencies `poetry install`

Run services

api_server and stock_server have `.env-base` file.
Please, verify settings before running.

1. Run api service `make ap i-server`
2. Run stock service `make stock-server`
3. Apply migration `make api-server-migrate`
4. Create superuser `make api-server-createsuperuser`

### Docker run
1. Install docker and docker-compose https://docs.docker.com/engine/install/
2. Start project `make docker-up`
3. Run migration `make docker-migrate`
4. Create superuser `make docker-create-createsuperuser`
5. Stop the project `make docker-down`

## Development
1. Install [pre-commit](https://pre-commit.com/#install)
2. Add pre-commit hook `pre-commit install`
3. Install hooks `pre-commit run`

Run code formatting `make fmt`

Run code linters `make lint`




Database

user
id | username |
_______________
1  | me       |

==================================================================================================

rss
id | title     | description | link                                        | ttl |
__________________________________________________________________________________
1  | cnn       |             | http://rss.cnn.com/rss/edition.rss          | 10  |
2  | nu        |             | http://www.nu.nl/rss/Algemeen               | 60  |
3  | tweakers  |             | https://feeds.feedburner.com/tweakers/mixed | 60  |

==================================================================================================

rss_item
id | title         | link                 | published_date      | last_updated        | rss__id |
________________________________________________________________________________________________
1  | smth happened | http://sxample.com/1 | 2022-02-02 12:23:32 | 2022-02-02 12:23:32 | 1       |
1  | smth happened | http://sxample.com/1 | 2022-02-02 12:23:32 | 2022-02-02 12:23:32 | 2       |
1  | smth happened | http://sxample.com/1 | 2022-02-02 12:23:32 | 2022-02-02 12:23:32 | 3       |

==================================================================================================

user_rss
id | user__id | rss__id      |
________________________________
1  | 1        | 1            |
1  | 1        | 2            |
1  | 1        | 3            |

==================================================================================================

user_rss_item
id | user__id | rss_item__id | is_read  |
_________________________________________
1  | 1        | 1            | true     |
1  | 1        | 2            | false    |
1  | 1        | 3            | false    |
1  | 1        | 4            | true     |
1  | 1        | 5            | false    |
1  | 1        | 6            | true     |

=================================================================================================
