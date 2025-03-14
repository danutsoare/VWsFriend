from datetime import datetime, timedelta, timezone
import logging
from sqlalchemy.exc import IntegrityError

from vwsfriend.model.refuel_session import RefuelSession
from vwsfriend.util.location_util import locationFromLatLon

from weconnect.addressable import AddressableLeaf, AddressableAttribute
from weconnect.elements.range_status import RangeStatus

LOG = logging.getLogger("VWsFriend")


class RefuelAgent():
    def __init__(self, session, vehicle):
        self.session = session
        self.vehicle = vehicle
        self.primary_currentSOC_pct = None
        self.previousRefuelSession = None
        self.lastPosition = None

        # register for updates:
        if self.vehicle.weConnectVehicle is not None:
            if 'rangeStatus' in self.vehicle.weConnectVehicle.statuses and self.vehicle.weConnectVehicle.statuses['rangeStatus'].enabled:
                self.vehicle.weConnectVehicle.statuses['rangeStatus'].carCapturedTimestamp.addObserver(self.__onCarCapturedTimestampChange,
                                                                                                       AddressableLeaf.ObserverEvent.VALUE_CHANGED,
                                                                                                       onUpdateComplete=True)
                self.__onCarCapturedTimestampChange(None, None)
            if 'parkingPosition' in self.vehicle.weConnectVehicle.statuses and self.vehicle.weConnectVehicle.statuses['parkingPosition'].enabled:
                self.vehicle.weConnectVehicle.statuses['parkingPosition'].carCapturedTimestamp.addObserver(self.__onParkingPositionCarCapturedTimestampChanged,
                                                                                                           AddressableLeaf.ObserverEvent.VALUE_CHANGED,
                                                                                                           onUpdateComplete=True)
                self.__onParkingPositionCarCapturedTimestampChanged(self.vehicle.weConnectVehicle.statuses['parkingPosition'].carCapturedTimestamp, None)
            else:
                self.vehicle.weConnectVehicle.statuses.addObserver(self.__onStatusesChange,
                                                                   AddressableLeaf.ObserverEvent.ENABLED,
                                                                   onUpdateComplete=True)

    def __onStatusesChange(self, element, flags):
        if isinstance(element, AddressableAttribute) and element.getGlobalAddress().endswith('parkingPosition/carCapturedTimestamp'):
            # only add if not in list of observers
            if self.__onParkingPositionCarCapturedTimestampChanged not in element.getObservers(flags=AddressableLeaf.ObserverEvent.VALUE_CHANGED,
                                                                                               onUpdateComplete=True):
                element.addObserver(self.__onParkingPositionCarCapturedTimestampChanged,
                                    AddressableLeaf.ObserverEvent.VALUE_CHANGED,
                                    onUpdateComplete=True)
                self.vehicle.weConnectVehicle.statuses.removeObserver(self.__onStatusesChange)
                self.__onParkingPositionCarCapturedTimestampChanged(element, flags)

    def __onCarCapturedTimestampChange(self, element, flags):  # noqa: C901
        rangeStatus = self.vehicle.weConnectVehicle.statuses['rangeStatus']
        if self.vehicle.carType in [RangeStatus.CarType.HYBRID] and rangeStatus.primaryEngine.currentSOC_pct.enabled \
                and element is not None and element.value > (datetime.utcnow().replace(tzinfo=timezone.utc) - timedelta(days=1)):
            current_primary_currentSOC_pct = rangeStatus.primaryEngine.currentSOC_pct.value

            mileage_km = None
            if 'odometerMeasurement' in self.vehicle.weConnectVehicle.statuses:
                odometerMeasurement = self.vehicle.weConnectVehicle.statuses['odometerMeasurement']
                if odometerMeasurement.odometer.enabled:
                    mileage_km = odometerMeasurement.odometer.value

            position_latitude = None
            position_longitude = None
            location = None
            if 'parkingPosition' in self.vehicle.weConnectVehicle.statuses:
                parkingPosition = self.vehicle.weConnectVehicle.statuses['parkingPosition']
                if parkingPosition.latitude.enabled and parkingPosition.latitude.value is not None \
                        and parkingPosition.longitude.enabled and parkingPosition.longitude.value is not None:
                    position_latitude = parkingPosition.latitude.value
                    position_longitude = parkingPosition.longitude.value
                    location = locationFromLatLon(self.session, parkingPosition.latitude.value, parkingPosition.longitude.value)
            if position_latitude is None and self.lastPosition is not None and (self.lastPosition[0] > (element.value - timedelta(minutes=15))):
                _, position_latitude, position_longitude = self.lastPosition
                location = locationFromLatLon(self.session, position_latitude, position_longitude)

            # Refuel event took place (as the car somethimes finds one or two percent of fuel somewhere lets give a 5 percent margin)
            if self.primary_currentSOC_pct is not None and ((current_primary_currentSOC_pct - 5) > self.primary_currentSOC_pct):
                if self.previousRefuelSession is None or (self.previousRefuelSession.date < (element.value - timedelta(minutes=30))):
                    LOG.info('Vehicle %s refueled from %d percent to %d percent', self.vehicle.vin, self.primary_currentSOC_pct, current_primary_currentSOC_pct)
                    refuelSession = RefuelSession(self.vehicle, element.value, self.primary_currentSOC_pct, current_primary_currentSOC_pct, mileage_km,
                                                  position_latitude, position_longitude, location)
                    try:
                        with self.session.begin_nested():
                            self.session.add(refuelSession)
                            self.previousRefuelSession = refuelSession
                        self.session.commit()
                    except IntegrityError:
                        LOG.warning('Could not add range entry to the database, this is usually due to an error in the WeConnect API')
                else:
                    LOG.info('Vehicle %s refueled from %d percent to %d percent. It looks like this session is continueing the previous refuel session',
                             self.vehicle.vin, self.primary_currentSOC_pct, current_primary_currentSOC_pct)
                    self.previousRefuelSession.endSOC_pct = current_primary_currentSOC_pct
                    if self.previousRefuelSession.mileage_km is None:
                        self.previousRefuelSession.mileage_km = mileage_km
                    if self.previousRefuelSession.position_latitude is None or self.previousRefuelSession.position_longitude is None:
                        self.previousRefuelSession.position_latitude = position_latitude
                        self.previousRefuelSession.position_longitude = position_longitude
                        self.previousRefuelSession.location = location
                    self.session.commit()
                self.primary_currentSOC_pct = current_primary_currentSOC_pct
            # SoC decreased, normal usage
            elif self.primary_currentSOC_pct is None or current_primary_currentSOC_pct < self.primary_currentSOC_pct:
                self.primary_currentSOC_pct = current_primary_currentSOC_pct

    def __onParkingPositionCarCapturedTimestampChanged(self, element, flags):
        if 'parkingPosition' in self.vehicle.weConnectVehicle.statuses:
            parkingPosition = self.vehicle.weConnectVehicle.statuses['parkingPosition']
            if parkingPosition.carCapturedTimestamp.enabled and parkingPosition.carCapturedTimestamp.value is not None \
                    and parkingPosition.latitude.enabled and parkingPosition.latitude.value is not None \
                    and parkingPosition.longitude.enabled and parkingPosition.longitude.value is not None:
                position_timestamp = parkingPosition.carCapturedTimestamp.value
                position_latitude = parkingPosition.latitude.value
                position_longitude = parkingPosition.longitude.value
                self.lastPosition = (position_timestamp, position_latitude, position_longitude)
                return
        self.lastPosition = None

    def commit(self):
        pass
