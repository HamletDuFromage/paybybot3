# PayByPhone GraphQL API Documentation

This document provides a reference for the GraphQL endpoints used by PayByPhone as of July 2026.

## Base Endpoint

`POST https://consumer.paybyphoneapis.com/uapi/graphql`

Headers required:
- `x-pbp-version: 2`
- `x-api-key`: Found in the main.js chunk
- `Authorization`: `Bearer <token>`

## Parking Workflow

To initiate a parking session, the app executes the following GraphQL mutations/queries in order:

1. **GetLocationsV1**: Retrieve location details (including `legacyVendorId`).
2. **CreateQuotesV1**: Request a quote for a parking session to get a `quoteId`.
3. **StartParkingSessionV1**: Confirm the quote to get a `parkingSessionId` and `expireTime`.
4. **CreateJobV1**: Finalize the parking job.

## GraphQL Operations

### GetUserAccountV1

```graphql
query GetUserAccountV1 {
  getUserAccountV1 {
    memberId
    type
    status
    phone {
      number
      status
      isUsername
      country
      countryCode
      nationalNumber
      operator
      __typename
    }
    email {
      address
      status
      __typename
    }
    country
    language
    address {
      street
      city
      provinceState
      postalCode
      country
      __typename
    }
    name {
      firstName
      lastName
      __typename
    }
    __typename
  }
  __typename
}
```

### CreateMemberConsentsV1

```graphql
mutation CreateMemberConsentsV1($request: CreateMemberConsentTransactionInput!) {
  createMemberConsentsV1(input: {request: $request}) {
    generalResponse {
      success
      message
      __typename
    }
    __typename
  }
  __typename
}
```

### GetMemberConsentsV1

```graphql
query GetMemberConsentsV1 {
  getMemberConsentsV1 {
    purposeName
    purposeVersion
    purposeLanguage
    consentType
    consentData {
      contactMethods
      __typename
    }
    __typename
  }
  __typename
}
```

### GetMemberConsentsPromptsV1

```graphql
query GetMemberConsentsPromptsV1($country: String, $language: String) {
  getMemberConsentsPromptsV1(input: {country: $country, language: $language}) {
    promptConsents
    layout {
      newUpdatesAndSpecialOffersContents {
        items {
          title
          body
          __typename
        }
        consentPurposes {
          ...ConsentPurposeFields
          __typename
        }
        __typename
      }
      infoAndCustomizeContents {
        sections {
          header
          consentPurposes {
            ...ConsentPurposeFields
            __typename
          }
          __typename
        }
        __typename
      }
      __typename
    }
    __typename
  }
  __typename
}

fragment ConsentPurposeFields on ConsentPurpose {
  purposeName
  purposeVersion
  purposeLanguage
  displayName
  displayDescription
  defaultContactMethods
  contactMethodsAvailable {
    label
    contactMethods
    __typename
  }
  learnMore {
    type
    linkUrl
    __typename
  }
  __typename
}
```

### GetParkerCorporateProfilesV1

```graphql
query GetParkerCorporateProfilesV1 {
  getParkerCorporateProfilesV1 {
    corporateClientId
    name
    shortName
    icon
    isSmsReminderEnabled
    isSmsConfirmationEnabled
    vehicleIds
    status
    vehicles {
      id
      licensePlate
      countryCode
      jurisdiction
      corporateClientId
      vehicleId
      name
      __typename
    }
    contact {
      firstName
      lastName
      mobilePhoneNumber
      email
      __typename
    }
    __typename
  }
  __typename
}
```

### GetMemberEmailV1

```graphql
query GetMemberEmailV1 {
  getUserAccountV1 {
    email {
      address
      status
      __typename
    }
    __typename
  }
  __typename
}
```

### GetMemberSegmentsV1

```graphql
query GetMemberSegmentsV1 {
  getMemberSegmentsV1 {
    memberId
    segments {
      segmentName
      __typename
    }
    __typename
  }
  __typename
}
```

### GetOpenSessionsV1

```graphql
query GetOpenSessionsV1($input: GetOpenSessionsInput!) {
  getOpenSessionsV1(input: $input) {
    sessionId
    providerSessionRef
    subscriptionId
    plate
    memberId
    vendorId
    extSiteCode
    startTime
    quoteTime
    sessionStatus
    siteCode
    vendorLotId
    endTime
    rate
    txFee
    totalPrice
    receipt
    poeQuoteId
    __typename
  }
  __typename
}
```

### GetParkingSessionsV1

```graphql
query GetParkingSessionsV1($input: GetParkingSessionsInput!) {
  getParkingSessionsV1(input: $input) {
    parkingSessionId
    status
    statusDetail
    type
    locationId
    startTime
    stall
    expireTime
    stopTime
    isStoppable
    fpsApplies
    isExtendable
    isRenewable
    renewableAfter
    maxStayState
    vehicle {
      id
      legacyVehicleId
      licensePlate
      countryCode
      type
      jurisdiction
      __typename
    }
    ratePolicy {
      ratePolicyId
      type
      __typename
    }
    totalCost {
      amount
      currency
      __typename
    }
    segments {
      parkingSegmentId
      parkingStart
      parkingEnd
      cost
      fees
      chargeableTimeUnitsParked
      chargeableTimeUnitType
      freeTimeUnitsApplied
      freeTimeUnitType
      isFreedayExtension
      isCredit
      status
      statusDetail
      failureReason
      parkingReferenceId
      jobLineItemId
      feesApplied {
        fees {
          name
          cost {
            amount
            currency
            __typename
          }
          __typename
        }
        total {
          amount
          currency
          __typename
        }
        __typename
      }
      __typename
    }
    feesApplied {
      fees {
        name
        cost {
          amount
          currency
          __typename
        }
        __typename
      }
      total {
        amount
        currency
        __typename
      }
      __typename
    }
    couponApplied {
      couponId
      appliedDate
      maxRedemptionValue {
        amount
        currency
        __typename
      }
      redeemedAmount {
        amount
        currency
        __typename
      }
      oldTotalSessionCost {
        amount
        currency
        __typename
      }
      newTotalSessionCost {
        amount
        currency
        __typename
      }
      __typename
    }
    jobId
    productType
    location {
      isStallBased
      advertisedLocationId
      name
      isReverseLookup
      __typename
    }
    __typename
  }
  __typename
}
```

### GetPaymentAccountsV1

```graphql
query GetPaymentAccountsV1($input: GetPaymentAccountsInput!) {
  getPaymentAccountsV1(input: $input) {
    paymentCards {
      cardType
      maskedCardNumber
      accountType
      paymentAccountId
      paymentScope
      corporateClientId
      expiryMonth
      expiryYear
      __typename
    }
    mno {
      status
      operator
      phoneNumber
      paymentAccountId
      paymentScope
      corporateClientId
      expiryMonth
      expiryYear
      __typename
    }
    twintAccounts {
      accountType
      paymentAccountId
      paymentScope
      mandates {
        id
        status
        __typename
      }
      __typename
    }
    paypalAccounts {
      accountType
      paymentAccountId
      paymentScope
      mandates {
        id
        status
        __typename
      }
      __typename
    }
    __typename
  }
  __typename
}
```

### GetOperatorsV1

```graphql
query GetOperatorsV1($input: GetOperatorsInput!) {
  getOperatorsV1(input: $input) {
    operatorId
    operatorName
    vendorId
    countries
    paymentTypes
    currencyCode
    languageCode
    needsEmblemPosition
    operatorState
    aggregatorId
    usesMandateGroups
    mandateGroups {
      mandateGroupId
      paymentTypes
      gateway
      primary
      __typename
    }
    jms
    aggregator
    __typename
  }
  __typename
}
```

### GetVehiclesV3

```graphql
query GetVehiclesV3($input: GetVehiclesInput!) {
  getVehiclesV3(input: $input) {
    vehicleId
    legacyVehicleId
    licensePlate
    country
    jurisdiction
    type
    attributes
    archived
    profile {
      photo
      description
      __typename
    }
    __typename
  }
  __typename
}
```

### GetLocationsV1

```graphql
query GetLocationsV1($input: GetLocationInput!) {
  getLocationsV1(input: $input) {
    locationId
    name
    vendorName
    vendorDisplayName
    status
    allowExtend
    allowStop
    isStallBased
    isPlateBased
    currency
    countryCode
    promptForCvv
    stall
    isReverseLookup
    acceptedPaymentTypes
    allowVisitors
    isPremierBays
    legacyVendorId
    parkingWorkflowType
    isAutoPay
    couponsEnabled
    requiresTicketScan
    lotMessages {
      key
      value
      __typename
    }
    distance {
      quantity
      unit
      __typename
    }
    locationAttributes {
      name
      value
      __typename
    }
    fps {
      applies
      amountApplicable {
        currency
        amount
        __typename
      }
      __typename
    }
    paymentProviderConfigurations {
      gateway
      supportedPaymentMethods
      configuration
      __typename
    }
    __typename
  }
  __typename
}
```

### GetRateOptionsV1

```graphql
query GetRateOptionsV1($input: GetRateOptionsInput!) {
  getRateOptionsV1(input: $input) {
    name
    type
    ratePolicyId
    maxStayStatus
    maxStayEndTime
    effectiveMaxStayDuration {
      quantity
      timeUnit
      __typename
    }
    acceptedTimeUnits
    areas
    eligibilityEndDate
    parkingNotAllowedReason
    restrictionPeriods {
      startTime
      endTime
      maxStay {
        quantity
        timeUnit
        __typename
      }
      __typename
    }
    renewalParking {
      isAllowed
      window {
        unit
        quantity
        __typename
      }
      __typename
    }
    fps {
      id
      active
      validityTime
      __typename
    }
    profile {
      profileName
      icon {
        iconId
        iconImage
        iconMimeType
        __typename
      }
      userMessages {
        locale
        message
        __typename
      }
      __typename
    }
    availablePromotions {
      id
      cost {
        amount
        currency
        __typename
      }
      duration
      configuredDuration
      usage
      displayName
      __typename
    }
    timeSteps {
      quantity
      timeUnit
      __typename
    }
    vehicleRegistrationFound
    isVehicleRegistrationMissing
    __typename
  }
  __typename
}
```

### CreateQuotesV1

```graphql
mutation CreateQuotesV1($requests: [QuoteRequestInput!]!) {
  createQuotesV1(input: {requests: $requests}) {
    createQuotesResponse {
      totalCost {
        amount
        currency
        __typename
      }
      quotes {
        quoteId
        quoteRequestId
        cost {
          amount
          currency
          __typename
        }
        details {
          quoteId
          locationId
          stall
          quoteDate
          parkingStartTime
          parkingExpiryTime
          parkingDurationAdjustment
          licensePlate
          corporateAccountSmsOverride
          corporateAccountSmsConfirmationOverride
          corporateAccountSmsReminderOverride
          promotionApplied {
            id
            cost {
              amount
              currency
              __typename
            }
            duration {
              quantity
              timeUnit
              __typename
            }
            displayName
            usage
            isSelectedByUser
            isTimeSplit
            isExternal
            configuredDuration {
              quantity
              timeUnit
              __typename
            }
            minimumIncrement {
              quantity
              timeUnit
              __typename
            }
            __typename
          }
          totalCost {
            amount
            currency
            __typename
          }
          quoteItems {
            quoteItemType
            name
            costAmount {
              amount
              currency
              __typename
            }
            subQuoteItems {
              quoteItemType
              name
              costAmount {
                amount
                currency
                __typename
              }
              __typename
            }
            __typename
          }
          __typename
        }
        product
        __typename
      }
      quoteErrors {
        quoteRequestId
        product
        status
        reason
        __typename
      }
      __typename
    }
    __typename
  }
  __typename
}
```

### StartParkingSessionV1

```graphql
mutation StartParkingSessionV1($input: StartParkingSessionV1Input!) {
  startParkingSessionV1(input: $input) {
    parkingSessionResponse {
      parkingSessionId
      expireTime
      isEarlyCapture
      segmentTotalCost {
        amount
        currency
        __typename
      }
      metadata
      __typename
    }
    __typename
  }
  __typename
}
```

### CreateJobV1

```graphql
mutation CreateJobV1($input: CreateJobV1Input!) {
  createJobV1(input: $input) {
    createJobResponse {
      jobId
      __typename
    }
    __typename
  }
  __typename
}
```

### GetJobV1

```graphql
query GetJobV1($jobId: UUID!) {
  getJobV1(jobId: $jobId) {
    jobId
    status
    captureGroups {
      captureGroupId
      stage
      status
      closedAt
      authentication {
        hiddenIframe
        challengeHtml
        token
        __typename
      }
      lineItems {
        itemId
        productReferenceId
        status
        metadata
        amount {
          value
          isoCurrencyCode
          __typename
        }
        executionDetails {
          isFailure
          code
          message
          metadata
          __typename
        }
        __typename
      }
      couponAmount {
        value
        isoCurrencyCode
        __typename
      }
      couponDetails {
        status {
          code
          status
          message
          __typename
        }
        couponId
        redeemedAt
        requestedAt
        totalAmountRedeemed {
          value
          isoCurrencyCode
          __typename
        }
        __typename
      }
      executionDetails {
        isFailure
        code
        message
        metadata
        captureGroupStage
        __typename
      }
      __typename
    }
    executionDetails {
      isFailure
      code
      message
      metadata
      __typename
    }
    __typename
  }
  __typename
}
```

