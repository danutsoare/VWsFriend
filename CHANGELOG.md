# Changelog
All notable changes to this project will be documented in this file.

## [Unreleased] (Available through Edge Tag)
### Changed
- Updated API to 0.28.0

## [0.12.0] - 2021-12-15
### Added
- Recording of trips for ID vehicles

### Changed
- Interval can be decresed to 180 seconds
- Technical fields are now hidden in the tables
- Removed interpolation from charging graph

## [0.11.0] - 2021-12-11
### Added
- Added cartype gasoline
- Added UnlockPlugState permanent

### Changed
- Updated API to 0.27.0
- Updated Grafana to 8.3.1


## [0.10.1] - 2021-12-03
### Fixed
- Adding missing Enum types to database

## [0.10.0] - 2021-12-01
### Added
- ABRP now receives the new est_battery_range parameter
- Enabled grafana livenow mode
- New attributes in status page

### Fixed
- Ordering of refueling sessions
- Also use parking position from the past 15 mins when refueling
- Grouping by operator if there are several entries for a operator
- Deal with missing vehicle images

### Changed
- Updated Grafana to 8.2.5
- Updated requirements for forms
- Updated API to 0.25.1
- Changed all graphs from old version to the new time-series variant

## [0.9.6] - 2021-11-01
### Fixed
- Fixed an error occuring when the server unexpectedly closes the connection

### Changed
- Updated API to 0.22.1

## [0.9.5] - 2021-11-01
### Fixed
- Changed Ubuntu Image from 21.04 to 21.10 for better Raspberry Pi support

### Changed
- Updated API to 0.22.0

## [0.9.4] - 2021-10-27
### Added
- Possibility to configure database host, port and databasename

### Fixed
- Ghost trips when Server reports error

## [0.9.3] - 2021-10-22
### Fixed
- Create provisioning folder if not existing

## [0.9.2] - 2021-10-22
### Fixed
- Corrected filename when restoring

## [0.9.1] - 2021-10-21
### Fixed
- Correct postgres version to 13 in dockerfile

### Changed
- Updated API to 0.21.5

## [0.9.0] - 2021-10-20
### Added
- Possibility to backup and restore the database

## [0.8.2] - 2021-10-19
### Fixed
- Refueling seperated in two parts is now joined into one session

## [0.8.1] - 2021-10-16
### Fixed
- installation of panomap plugin

## [0.8.0] - 2021-10-14
### Added
- Charging map in charging statistics

### Fixed
- Caching of pictures improved
- Bug in Homekit Dummy device when no name was configured

### Changed
- More slim grafana configuration, don't distracting with unused features
- Updated API to 0.21.3

## [0.7.0] - 2021-10-12
### Fixed
- Interval is executed more precisely
- Will deal with corrupted cache file by deleting cache
- Various improvements in dashboards (e.g. optimized queries)
- Corrupted graphs for consumption, range and efficiency
- Unwanted refuel session entries when the car suddenly finds one or two percent of fuel

### Added
- New dashboard for journeys added
- It is now possible to add real amount and cost for refueling of gasoline cars and hybrids
- Statistics for the responsetime are collected

### Changed
- Updated API to 0.21.1
- Getting mileage from new odometerMeasurement instead of maintenanceStatus field
- Updated requirements for alembic to 1.7.4 and hyp-python to 4.3.0

## [0.6.0] - 2021-10-06
### Fixed
- Fixed recording of trips
- Fixed lost room assignment in HomeKit setup
- Problems with HomeKit setting climatization correctly
- Small improvements on Grafana Dashboards
- Fixed 32Bit ARM docker image building

### Changed
- Updated API to 0.21.0

### Added
- collecting errors in database for future visualization
- Possibility to correct recorded data and add missing information
- Status page car images now displays badges indicating lock/charging/etc
- Possiblity to configure logging output format
- Added time in logging

## [0.5.4] - 2021-09-23
### Fixed
- Fix due to changes in the API

### Changed
- Updated API to 0.20.12

## [0.5.3] - 2021-09-16
### Fixed
- Typo in default value in Dockerfile

## [0.5.2] - 2021-09-16
### Added
- Use retry mechanism for all http requests

### Changed
- Various improvements in the Dashboards. Better compatibility with legacy cars

## [0.5.1] - 2021-09-13
### Fixed
- Fixed vehicle image loading in Grafana car overview dashboard (thanks to [cmantsch](https://github.com/cmantsch))
- Database migration process
- VWsFriend is now waiting for the database to be available

## [0.5.0] - 2021-09-10
### Added
- New statistics dashboard for daily, weekly, monthly, yearly overview
- New statistics dashboard for mileage (including projection)

### Fixed
- Problem with recording fueling on hybird and fossil cars 

## [0.4.3] - 2021-09-09
### Fixed
- Crash when experiencing connection problems, e.g. due to internet outage
- Version footer
- Catching up a running charging session after restart

## [0.4.2] - 2021-09-08
### Fixed
- Some problems in grafana dashboards
- Problems with commiting changes to the database
- Several fixes in Grafana

### Added
- Possibility to make changes to trips
- Possibility to see version information in UI

## [0.4.1] - 2021-09-07
Happy Birthday Pia!

### Fixed
- Problem on database commit

### Changed
- Updated API to 0.20.6

## [0.4.0] - 2021-08-25
### Added
- New Homekit Accessories (Plug and Lock) added
- Homekit can now control charging and climatization (temperature and on/off state)
- Homekit configuration through UI

### Fixed
- Trips work again after changes to WeConnect Service

## [0.3.0] - 2021-08-24
This is a complete rewrite of VWsFriend using a self developed API. It drops ioBroker

### Added
- Several new dashboards for refueling (hybrid and gasoline only), charging sessions, trips (only when parking position is provided), ...
- Added support to forward telemetry to ABPR (A better route planner)
- Web Userinterface to see status and configure settings
- a lot more...

### Changed
- Now uses PostgreSQL instead of Influx

### Removed
- ioBroker is not shipped anymore with VWsFriend. If you still want to use ioBroker, you can use ioBroker with [WeConnect-mqt](https://github.com/tillsteinbach/WeConnect-mqtt).

## [0.2.0] - 2021-04-25
### Added
- Now understanding climate state 'ventilation' in grafana and homekit
- carCapturedTimestampLatest in userdata area

### Changed
- Updating Grafana from 7.5.3 to 7.5.4
- More accurate Grafana Annotations by using timestamp from server
- Last connection information on dashboard now based on latest timestamp from API
- All states written by VWsFriend to iobroker are now set with ack: true

### Fixed
- Text is now consistently in english

## [0.1.0] - 2021-04-22
Initial release to enable "latest" tag on dockerhub

[unreleased]: https://github.com/tillsteinbach/VWsFriend/compare/v0.12.0...HEAD
[0.12.0]: https://github.com/tillsteinbach/VWsFriend/releases/tag/v0.12.0
[0.11.0]: https://github.com/tillsteinbach/VWsFriend/releases/tag/v0.11.0
[0.10.1]: https://github.com/tillsteinbach/VWsFriend/releases/tag/v0.10.1
[0.10.0]: https://github.com/tillsteinbach/VWsFriend/releases/tag/v0.10.0
[0.9.6]: https://github.com/tillsteinbach/VWsFriend/releases/tag/v0.9.6
[0.9.5]: https://github.com/tillsteinbach/VWsFriend/releases/tag/v0.9.5
[0.9.4]: https://github.com/tillsteinbach/VWsFriend/releases/tag/v0.9.4
[0.9.3]: https://github.com/tillsteinbach/VWsFriend/releases/tag/v0.9.3
[0.9.2]: https://github.com/tillsteinbach/VWsFriend/releases/tag/v0.9.2
[0.9.1]: https://github.com/tillsteinbach/VWsFriend/releases/tag/v0.9.1
[0.9.0]: https://github.com/tillsteinbach/VWsFriend/releases/tag/v0.9.0
[0.8.2]: https://github.com/tillsteinbach/VWsFriend/releases/tag/v0.8.2
[0.8.1]: https://github.com/tillsteinbach/VWsFriend/releases/tag/v0.8.1
[0.8.0]: https://github.com/tillsteinbach/VWsFriend/releases/tag/v0.8.0
[0.7.1]: https://github.com/tillsteinbach/VWsFriend/releases/tag/v0.7.1
[0.7.0]: https://github.com/tillsteinbach/VWsFriend/releases/tag/v0.7.0
[0.6.0]: https://github.com/tillsteinbach/VWsFriend/releases/tag/v0.6.0
[0.5.4]: https://github.com/tillsteinbach/VWsFriend/releases/tag/v0.5.4
[0.5.3]: https://github.com/tillsteinbach/VWsFriend/releases/tag/v0.5.3
[0.5.2]: https://github.com/tillsteinbach/VWsFriend/releases/tag/v0.5.2
[0.5.1]: https://github.com/tillsteinbach/VWsFriend/releases/tag/v0.5.1
[0.5.0]: https://github.com/tillsteinbach/VWsFriend/releases/tag/v0.5.0
[0.4.3]: https://github.com/tillsteinbach/VWsFriend/releases/tag/v0.4.3
[0.4.2]: https://github.com/tillsteinbach/VWsFriend/releases/tag/v0.4.2
[0.4.1]: https://github.com/tillsteinbach/VWsFriend/releases/tag/v0.4.1
[0.4.0]: https://github.com/tillsteinbach/VWsFriend/releases/tag/v0.4.0
[0.3.0]: https://github.com/tillsteinbach/VWsFriend/releases/tag/v0.3.0
[0.2.0]: https://github.com/tillsteinbach/VWsFriend/releases/tag/v0.2.0
[0.1.0]: https://github.com/tillsteinbach/VWsFriend/releases/tag/v0.1.0
