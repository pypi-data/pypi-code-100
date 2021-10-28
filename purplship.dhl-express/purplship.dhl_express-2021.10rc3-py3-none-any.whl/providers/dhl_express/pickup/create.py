from typing import Tuple, List
from dhl_express_lib.book_pickup_global_req_3_0 import BookPURequest, MetaData
from dhl_express_lib.book_pickup_global_res_3_0 import BookPUResponse
from dhl_express_lib.pickupdatatypes_global_3_0 import (
    Requestor,
    Place,
    Pickup,
    WeightSeg,
    RequestorContact,
)
from purplship.core.utils import (
    Serializable,
    Element,
    DF,
    NF,
    XP,
)
from purplship.core.models import (
    PickupRequest,
    Message,
    PickupDetails,
    ChargeDetails,
)
from purplship.core.units import WeightUnit, Weight, Packages
from purplship.providers.dhl_express.units import (
    CountryRegion,
    WeightUnit as DHLWeightUnit,
)
from purplship.providers.dhl_express.utils import Settings, reformat_time
from purplship.providers.dhl_express.error import parse_error_response


def parse_pickup_response(
    response, settings: Settings
) -> Tuple[PickupDetails, List[Message]]:
    successful = (
        len(response.xpath(".//*[local-name() = $name]", name="ConfirmationNumber")) > 0
    )
    pickup = _extract_pickup(response, settings) if successful else None
    return pickup, parse_error_response(response, settings)


def _extract_pickup(response: Element, settings: Settings) -> PickupDetails:
    pickup = BookPUResponse()
    pickup.build(response)
    pickup_charge = (
        ChargeDetails(
            name="Pickup Charge",
            amount=NF.decimal(pickup.PickupCharge),
            currency=pickup.CurrencyCode,
        )
        if pickup.PickupCharge is not None
        else None
    )
    return PickupDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        confirmation_number=str(pickup.ConfirmationNumber[0]),
        pickup_date=DF.fdate(pickup.NextPickupDate),
        pickup_charge=pickup_charge,
        ready_time=DF.ftime(pickup.ReadyByTime),
        closing_time=DF.ftime(pickup.CallInTime),
    )


def pickup_request(
    payload: PickupRequest, settings: Settings
) -> Serializable[BookPURequest]:
    packages = Packages(payload.parcels)

    request = BookPURequest(
        Request=settings.Request(
            MetaData=MetaData(SoftwareName="XMLPI", SoftwareVersion=3.0)
        ),
        schemaVersion=3.0,
        RegionCode=CountryRegion[payload.address.country_code].value
        if payload.address.country_code
        else "AM",
        Requestor=Requestor(
            AccountNumber=settings.account_number,
            AccountType="D",
            RequestorContact=RequestorContact(
                PersonName=payload.address.person_name,
                Phone=payload.address.phone_number,
                PhoneExtension=None,
            ),
            CompanyName=payload.address.company_name,
        ),
        Place=Place(
            City=payload.address.city,
            StateCode=payload.address.state_code,
            PostalCode=payload.address.postal_code,
            CompanyName=payload.address.company_name,
            CountryCode=payload.address.country_code,
            PackageLocation=payload.package_location,
            LocationType="R" if payload.address.residential else "B",
            Address1=payload.address.address_line1,
            Address2=payload.address.address_line2,
        ),
        PickupContact=RequestorContact(
            PersonName=payload.address.person_name, Phone=payload.address.phone_number
        ),
        Pickup=Pickup(
            Pieces=len(payload.parcels),
            PickupDate=payload.pickup_date,
            ReadyByTime=f"{payload.ready_time}:00",
            CloseTime=f"{payload.closing_time}:00",
            SpecialInstructions=[payload.instruction],
            RemotePickupFlag="Y",
            weight=WeightSeg(
                Weight=packages.weight.value,
                WeightUnit=DHLWeightUnit[packages.weight.unit].value
            ),
        ),
        ShipmentDetails=None,
        ConsigneeDetails=None,
    )
    return Serializable(request, _request_serializer)


def _request_serializer(request: BookPURequest) -> str:
    xml_str = XP.export(
        request,
        name_="req:BookPURequest",
        namespacedef_='xmlns:req="http://www.dhl.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.dhl.com book-pickup-global-req_EA.xsd"',
    ).replace("dhlPickup:", "").replace('schemaVersion="3"', 'schemaVersion="3.0"')

    xml_str = reformat_time("CloseTime", reformat_time("ReadyByTime", xml_str))
    return xml_str
