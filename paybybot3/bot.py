import uuid
import json
from datetime import datetime
import re
import requests

class Bot:
    base_headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://m2.paybyphone.fr/",
        "Origin": "https://m2.paybyphone.fr",
        "DNT": "1",
        "Connection": "keep-alive",
    }

    def __init__(self, username, password):
        url = "https://m2.paybyphone.fr/static/js/main.0aec44c0.chunk.js"
        try:
            resp = requests.get(url)
            resp.raise_for_status()
            pattern = r'paymentService:{[^}]*apiKey:\"(.*?)\"'
            result = re.search(pattern, resp.text, flags=re.MULTILINE)
            self.apiKey = result.group(1) if result else None
        except (requests.exceptions.HTTPError, KeyError):
            self.apiKey = None

        r = requests.post(
            "https://auth.paybyphoneapis.com/token",
            headers={
                **self.base_headers,
                "Accept": "application/json, text/plain, */*",
                "X-Pbp-ClientType": "WebApp",
            },
            data={
                "grant_type": "password",
                "username": username,
                "password": password,
                "client_id": "paybyphone_webapp",
            },
        )
        j = r.json()
        self.authorization = j["token_type"] + " " + j["access_token"]
        
    def _graphql(self, query, variables):
        return requests.post(
            "https://consumer.paybyphoneapis.com/uapi/graphql",
            headers={
                **self.base_headers,
                "Accept": "application/json, text/plain, */*",
                "x-pbp-version": "2",
                "x-api-key": self.apiKey,
                "Authorization": self.authorization,
            },
            json={
                "operationName": None,
                "variables": variables,
                "query": query
            }
        ).json()

    def _get_parking_sessions(self):
        query = """query GetParkingSessionsV1($input: GetParkingSessionsInput!) {
          getParkingSessionsV1(input: $input) {
            parkingSessionId
            locationId
            startTime
            expireTime
            vehicle {
              licensePlate
            }
          }
        }"""
        variables = {"input": {"periodType": "CURRENT", "offset": 0, "limit": 10}}
        ans = self._graphql(query, variables).get("data", {}).get("getParkingSessionsV1", [])
        for s in ans:
            try:
                s["startTime"] = datetime.strptime(s["startTime"][:19], "%Y-%m-%dT%H:%M:%S")
                s["expireTime"] = datetime.strptime(s["expireTime"][:19], "%Y-%m-%dT%H:%M:%S")
            except Exception:
                pass
            if "vehicle" in s and s["vehicle"]:
                s["vehicle"]["licensePlate"] = s["vehicle"].get("licensePlate")
        return ans

    def get_parking_sessions(self, licensePlate=None, locationId=None):
        def pred(p):
            if licensePlate is not None:
                if p.get("vehicle", {}).get("licensePlate") != licensePlate:
                    return False
            if locationId is not None:
                if p.get("locationId") != locationId:
                    return False
            return True

        return list(filter(pred, self._get_parking_sessions()))

    def last_expiry(self, licensePlate, locationId):
        return max(
            (
                session["expireTime"]
                for session in self.get_parking_sessions(licensePlate, locationId)
            ),
            default=None,
        )

    def get_payment_accounts(self):
        query = """query GetPaymentAccountsV1($input: GetPaymentAccountsInput!) {
          getPaymentAccountsV1(input: $input) {
            paymentCards { cardType maskedCardNumber accountType paymentAccountId paymentScope corporateClientId expiryMonth expiryYear }
            mno { status operator phoneNumber paymentAccountId paymentScope corporateClientId expiryMonth expiryYear }
            twintAccounts { accountType paymentAccountId paymentScope mandates { id status } }
            paypalAccounts { accountType paymentAccountId paymentScope mandates { id status } }
          }
        }"""
        return self._graphql(query, {"input": {"mandateCountryCode": "FR"}}).get("data", {}).get("getPaymentAccountsV1", {})

    def _get_rate_options(self, location, licensePlate):
        pass

    def _get_rate_options_renew(self, location, parkingSessionId):
        pass

    def _get_quote(
        self, durationQuantity, durationTimeUnit, licensePlate, locationId, rateOptionId
    ):
        pass

    def _get_renew_quote(self, durationQuantity, durationTimeUnit, parkingSessionId):
        pass

    def _post_quote(
        self,
        quoteId,
        paymentAccountId,
        licensePlate,
        rateOptionId,
        locationId,
        durationQuantity,
        durationTimeUnit,
        startTime,
    ):
        pass

    def _put_renew_quote(
        self,
        parkingSessionId,
        quoteId,
        paymentAccountId,
        durationQuantity,
        durationTimeUnit,
    ):
        pass

    def _get_workflow(self, quoteId):
        pass

    def get_vehicles(self):
        query = """query GetVehiclesV3($input: GetVehiclesInput!) {
          getVehiclesV3(input: $input) {
            licensePlate
          }
        }"""
        return self._graphql(query, {"input": {"profileName": "PayByPhone"}}).get("data", {}).get("getVehiclesV3", [])

    def pay(
        self,
        durationQuantity,
        durationTimeUnit,
        licensePlate,
        locationId,
        rateOptionId,
        paymentAccountId,
    ):
        loc_query = """query GetLocationsV1($input: GetLocationInput!) {
          getLocationsV1(input: $input) { legacyVendorId }
        }"""
        loc_resp = self._graphql(loc_query, {"input": {"locationId": locationId}})
        vendor_id = loc_resp.get("data", {}).get("getLocationsV1", {}).get("legacyVendorId", "6201")

        query_quote = """mutation CreateQuotesV1($requests: [QuoteRequestInput!]!) {
          createQuotesV1(input: {requests: $requests}) {
            createQuotesResponse {
              quotes { quoteId }
            }
          }
        }"""
        quote_req = {
            "quoteRequestId": str(uuid.uuid4()),
            "product": "PARKING",
            "details": {
                "locationId": str(locationId),
                "advertisedLocationId": str(locationId),
                "ratePolicyId": str(rateOptionId),
                "parkingQuoteOperation": "Start",
                "durationTimeUnit": durationTimeUnit,
                "durationQuantity": str(durationQuantity),
                "licensePlate": licensePlate,
                "stall": "",
                "parkingSessionId": "",
                "paymentAccountId": str(paymentAccountId) if paymentAccountId else "",
                "paymentCardType": "",
                "paymentScope": ""
            }
        }
        quote_resp = self._graphql(query_quote, {"requests": [quote_req]})
        try:
            quote_id = quote_resp["data"]["createQuotesV1"]["createQuotesResponse"]["quotes"][0]["quoteId"]
        except Exception:
            return "Failed to get quote: " + str(quote_resp)

        query_start = """mutation StartParkingSessionV1($input: StartParkingSessionV1Input!) {
          startParkingSessionV1(input: $input) {
            parkingSessionResponse {
              parkingSessionId
              expireTime
              isEarlyCapture
              metadata
            }
          }
        }"""
        start_resp = self._graphql(query_start, {"input": {"request": {"quoteId": quote_id}}})
        try:
            session = start_resp["data"]["startParkingSessionV1"]["parkingSessionResponse"]
            parkingSessionId = session["parkingSessionId"]
            expireTime = session["expireTime"]
            isEarlyCapture = session["isEarlyCapture"]
            metadata = session.get("metadata", {})
        except Exception:
            return "Failed to start parking session: " + str(start_resp)
            
        if isinstance(metadata, dict):
            metadata = json.dumps(metadata)

        query_job = """mutation CreateJobV1($input: CreateJobV1Input!) {
          createJobV1(input: $input) {
            createJobResponse { jobId }
          }
        }"""
        job_req = {
            "input": {
                "request": {
                    "lineItems": [
                        {
                            "productType": "parking",
                            "productReferenceId": parkingSessionId,
                            "vendorId": vendor_id,
                            "endingTime": expireTime,
                            "isEarlyCapture": isEarlyCapture,
                            "required": True,
                            "metadata": metadata
                        }
                    ]
                }
            }
        }
        job_resp = self._graphql(query_job, job_req)
        return json.dumps(job_resp)
