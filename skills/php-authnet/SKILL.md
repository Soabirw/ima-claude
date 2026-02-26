---
name: "php-authnet"
description: "Authorize.Net PHP SDK patterns for payment processing, CIM profiles, ARB subscriptions, Accept.js integration, and webhooks. Use when working with authorizenet/authorizenet Composer package, building payment forms, processing transactions, managing customer profiles, recurring billing, refunds, voids, or webhook handlers in PHP. Complements php-fp and php-fp-wordpress skills."
---

# Authorize.Net PHP SDK

Patterns and reference for the `authorizenet/authorizenet` PHP SDK (^2.0). PHP-only — no JavaScript, Python, Ruby, or Node patterns.

**Companion skills**: `php-fp` (core FP patterns), `php-fp-wordpress` (WordPress integration)

## Architecture: Three-Layer FP Pattern

Authorize.Net integration follows a strict three-layer separation:

```
[Pure Builders]  →  [SDK Adapter (Impure)]  →  [Pure Parsers]
   plain arrays         SDK objects + I/O          result arrays
```

### Layer 1: Pure Request Builders

Normalize input into plain arrays. No SDK imports, no `date()`, no side effects.

```php
<?php declare(strict_types=1);

function build_charge_request(array $payment_data): array {
    return [
        'amount'        => $payment_data['amount'],
        'payment_token' => $payment_data['payment_token'],
        'billing'       => !empty($payment_data['billing']) ? $payment_data['billing'] : null,
        'description'   => $payment_data['description'] ?? null,
    ];
}
```

### Layer 2: SDK Adapter (Impure)

All `use net\authorize\api\...` imports confined here. Builds SDK objects, executes requests, normalizes responses to plain arrays. Never throws — catches exceptions and returns error arrays.

```php
<?php declare(strict_types=1);

use net\authorize\api\contract\v1 as AnetAPI;
use net\authorize\api\controller as AnetController;

function sdk_charge_customer(array $payment_data, array $credentials): array {
    $null_response = [
        'result_code' => null, 'transaction_id' => null,
        'error_text' => null, 'error_code' => null,
        'has_transaction_messages' => false,
    ];

    try {
        $merchant_auth = new AnetAPI\MerchantAuthenticationType();
        $merchant_auth->setName($credentials['api_login_id']);
        $merchant_auth->setTransactionKey($credentials['transaction_key']);

        // ... build SDK objects from plain array ...

        $controller = new AnetController\CreateTransactionController($request);
        $response = $controller->executeWithApiResponse($credentials['api_url']);

        if ($response === null) return $null_response;

        return [
            'result_code'    => $response->getMessages()->getResultCode(),
            'transaction_id' => $response->getTransactionResponse()?->getTransId(),
            // ... normalize all fields to plain values ...
        ];
    } catch (\Exception $e) {
        return array_merge($null_response, [
            'result_code' => 'Error',
            'error_text'  => sprintf('%s: %s', get_class($e), $e->getMessage()),
        ]);
    }
}
```

### Layer 3: Pure Response Parsers

Interpret normalized arrays into standard `['success' => bool, ...]` results. No SDK dependencies.

```php
<?php declare(strict_types=1);

function parse_charge_response(array $response): array {
    if ($response['result_code'] === 'Ok' && $response['has_transaction_messages']) {
        return ['success' => true, 'transaction_id' => $response['transaction_id']];
    }
    if ($response['result_code'] === null) {
        return ['success' => false, 'error' => 'No response from payment gateway'];
    }
    return ['success' => false, 'error' => $response['error_text'] ?? 'Unknown error'];
}
```

### SDK Orchestrator Pattern

Thin glue connecting adapter to parser — no business logic:

```php
function charge_customer_via_sdk(array $payment_data, array $credentials): array {
    $normalized = sdk_charge_customer($payment_data, $credentials);
    return parse_charge_response($normalized);
}
```

## SDK Namespace Reference

```php
use net\authorize\api\contract\v1 as AnetAPI;    // Data types (request/response objects)
use net\authorize\api\controller as AnetController; // Controllers (execute requests)
use net\authorize\api\constants\ANetEnvironment;   // SANDBOX / PRODUCTION URLs
```

## Authentication

```php
$merchant_auth = new AnetAPI\MerchantAuthenticationType();
$merchant_auth->setName($credentials['api_login_id']);
$merchant_auth->setTransactionKey($credentials['transaction_key']);
```

**Credential storage**: Use `wp-config.php` constants first, options table as fallback.

```php
// Constants-first pattern
$api_login = defined('IMA_PAYMENTS_API_LOGIN_ID')
    ? IMA_PAYMENTS_API_LOGIN_ID
    : get_option('ima_payments_api_login_id', '');
```

**Environment switching**:

```php
// Sandbox
$controller->executeWithApiResponse(ANetEnvironment::SANDBOX);
// Production
$controller->executeWithApiResponse(ANetEnvironment::PRODUCTION);
```

## Transaction Types

| Type | `transactionType` value | Use case |
|------|------------------------|----------|
| Auth & Capture | `authCaptureTransaction` | One-step charge (most common) |
| Auth Only | `authOnlyTransaction` | Reserve funds, capture later |
| Capture Prior Auth | `priorAuthCaptureTransaction` | Capture a prior auth |
| Refund | `refundTransaction` | Refund settled transaction |
| Void | `voidTransaction` | Cancel unsettled transaction |

## Accept.js Integration (PCI Compliance)

Accept.js tokenizes card data client-side. The server never sees raw card numbers — only opaque payment nonces (valid 15 minutes).

**Server-side token consumption**:

```php
$opaque_data = new AnetAPI\OpaqueDataType();
$opaque_data->setDataDescriptor('COMMON.ACCEPT.INAPP.PAYMENT');
$opaque_data->setDataValue($payment_nonce);

$payment_type = new AnetAPI\PaymentType();
$payment_type->setOpaqueData($opaque_data);
```

**Data descriptor** is always `'COMMON.ACCEPT.INAPP.PAYMENT'` for Accept.js tokens.

## Quick Reference: Common Operations

### Charge with Accept.js Token

```php
$transaction_request = new AnetAPI\TransactionRequestType();
$transaction_request->setTransactionType('authCaptureTransaction');
$transaction_request->setAmount($amount);
$transaction_request->setPayment($payment_type); // from Accept.js opaque data
```

### Charge Stored CIM Profile

```php
$profile_to_charge = new AnetAPI\CustomerProfilePaymentType();
$profile_to_charge->setCustomerProfileId($customer_profile_id);

$pp = new AnetAPI\PaymentProfileType();
$pp->setPaymentProfileId($payment_profile_id);
$profile_to_charge->setPaymentProfile($pp);

$transaction_request = new AnetAPI\TransactionRequestType();
$transaction_request->setTransactionType('authCaptureTransaction');
$transaction_request->setAmount($amount);
$transaction_request->setProfile($profile_to_charge);
```

### Refund a Settled Transaction

```php
$credit_card = new AnetAPI\CreditCardType();
$credit_card->setCardNumber('XXXX1234'); // last 4 digits
$credit_card->setExpirationDate('XXXX');  // literal 'XXXX'

$payment = new AnetAPI\PaymentType();
$payment->setCreditCard($credit_card);

$tx = new AnetAPI\TransactionRequestType();
$tx->setTransactionType('refundTransaction');
$tx->setAmount($refund_amount);
$tx->setRefTransId($original_transaction_id);
$tx->setPayment($payment);
```

### Void an Unsettled Transaction

```php
$tx = new AnetAPI\TransactionRequestType();
$tx->setTransactionType('voidTransaction');
$tx->setRefTransId($transaction_id);
```

## Error Handling

### Response Structure

AuthNet responses have two levels of messages:

1. **Top-level**: `$response->getMessages()` — API-level success/failure
2. **Transaction-level**: `$tresponse->getErrors()` / `$tresponse->getMessages()` — transaction result

Always check both. A transaction can fail (`tresponse->getErrors()`) even when the API call succeeds (`result_code === 'Ok'`).

### Common Error Codes

| Code | Meaning | Action |
|------|---------|--------|
| `E00039` | Duplicate record (CIM profile exists) | Extract existing profile ID from error text |
| `E00040` | Record not found | Profile was deleted or never existed |
| `E00027` | Transaction declined | Show user-friendly decline message |
| `E00003` | Invalid login/transaction key | Check credentials configuration |
| `E00007` | Permission denied | Check account settings |
| `E00012` | Duplicate subscription (ARB) | Check for existing subscription |

### E00039 Duplicate Profile Recovery

AuthNet includes the existing profile ID in the error text:

```php
function extract_profile_id_from_error(string $error_text): string|false {
    return preg_match('/ID\s+(\d+)/', $error_text, $m) ? $m[1] : false;
}
```

## When to Load Reference Files

### Full API Reference
**File**: `references/api-reference.md`
**Load when**:
- Need complete SDK class/method listings
- Working with CIM customer profiles (create, update, delete, payment profiles)
- Working with ARB recurring billing (subscriptions, schedules, trials)
- Need webhook event types and HMAC-SHA512 signature validation
- Working with transaction reporting API
- Need response code tables or field constraints
- Implementing refunds, voids, or auth-only flows

### Sandbox & Testing Guide
**File**: `references/sandbox-testing.md`
**Load when**:
- Setting up sandbox environment or test credentials
- Need test card numbers and expected responses
- Debugging sandbox-specific issues (CIM→ARB propagation delay)
- Writing PHPUnit tests for payment functions
- Need sandbox vs production behavioral differences
