import asyncio
import logging
from datetime import datetime

try:
    import websockets
except ModuleNotFoundError:
    print("This example relies on the 'websockets' package.")
    print("Please install it by running: ")
    print()
    print(" $ pip install websockets")
    import sys
    sys.exit(1)

from ocpp.v16 import ChargePoint as cp
from ocpp.v16 import call
from ocpp.v16.enums import RegistrationStatus

logging.basicConfig(level=logging.INFO)


class ChargePoint(cp):
    async def send_boot_notification(self):
        request = call.BootNotificationPayload(
            charge_point_model="Optimus", charge_point_vendor="The Mobility House"
        )
        response = await self.call(request)
        if response.status == RegistrationStatus.accepted:
            logging.info("Connected to central system.")
            status_notification = call.StatusNotificationPayload(
                connector_id=0,
                error_code="NoError",
                status="Available",
                timestamp=datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S") + "Z",
                vendor_id="The Mobility House",
                vendor_error_code=None,
            )
            await self.call(status_notification)

    async def on_get_configuration(self, configuration_key):
        response_key = [
            {"key": "AllowOfflineTxForUnknownId", "readonly": False, "value": "false"},
            {"key": "AuthorizationCacheEnabled", "readonly": False, "value": "true"},
            {"key": "AuthorizeRemoteTxRequests", "readonly": False, "value": "false"},
            {"key": "ClockAlignedDataInterval", "readonly": False, "value": "0"},
            {"key": "ConnectionTimeOut", "readonly": False, "value": "120"},
            {"key": "GetConfigurationMaxKeys", "readonly": True, "value": "10"},
            {"key": "HeartbeatInterval", "readonly": False, "value": "900"},
            {"key": "LocalAuthorizeOffline", "readonly": False, "value": "true"},
            {"key": "LocalPreAuthorize", "readonly": False, "value": "true"},
            {"key": "MeterValueSampleInterval", "readonly": False, "value": "60"},
            {"key": "MinimumStatusDuration", "readonly": False, "value": "1"},
            {"key": "NumberOfConnectors", "readonly": True, "value": "1"},
            {"key": "ResetRetries", "readonly": False, "value": "1"},
            {"key": "StopTransactionOnEVSideDisconnect", "readonly": False, "value": "true"},
            {"key": "StopTransactionOnInvalidId", "readonly": False, "value": "true"},
            {"key": "TransactionMessageAttempts", "readonly": False, "value": "3"},
            {"key": "TransactionMessageRetryInterval", "readonly": False, "value": "5"},
            {"key": "UnlockConnectorOnEVSideDisconnect", "readonly": False, "value": "false"},
            {"key": "WebSocketPingInterval", "readonly": False, "value": "40"},
            {"key": "LocalAuthListEnabled", "readonly": False, "value": "true"},
            {"key": "LocalAuthListMaxLength", "readonly": True, "value": "200"},
            {"key": "SendLocalListMaxLength", "readonly": True, "value": "10"},
            {"key": "ReserveConnectorZeroSupported", "readonly": True, "value": "true"},
            {"key": "ChargeProfileMaxStackLevel", "readonly": True, "value": "10"},
            {"key": "ChargingScheduleAllowedChargingRateUnit", "readonly": True, "value": "Current,Power"},
            {"key": "ChargingScheduleMaxPeriods", "readonly": True, "value": "10"},
            {"key": "ConnectorSwitch3to1PhaseSupported", "readonly": True, "value": "false"},
            {"key": "MaxChargingProfilesInstalled", "readonly": True, "value": "20"}
        ]
        return call.GetConfigurationPayload(configuration_key=response_key)






async def main():
    async with websockets.connect(
        "ws://dev.wevolt-ev.com/cpms/websockets/e1x9QXk4", subprotocols=["ocpp1.6"]
    ) as ws:

        cp = ChargePoint("e1x9QXk4", ws)
        cp.on_get_configuration = ChargePoint.on_get_configuration
        await asyncio.gather(cp.start(), cp.send_boot_notification())



if __name__ == "__main__":
    # asyncio.run() is used when running this example with Python >= 3.7v
    asyncio.run(main())
