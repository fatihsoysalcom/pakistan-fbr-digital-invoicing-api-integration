import os
import json
import http.client # Standard library for HTTP requests
import ssl # For HTTPS

# --- Configuration ---
# FBR API Host. In a real scenario, this would be provided by FBR.
FBR_API_HOST = os.getenv("FBR_API_HOST", "sandbox.fbr.gov.pk")
# FBR API Path for submitting invoices. Adjust as per actual FBR documentation.
FBR_API_PATH = os.getenv("FBR_API_PATH", "/digital-invoicing/v1/invoices")
# API Key or Token for authentication. This should be kept secure, e.g., via environment variables.
FBR_API_KEY = os.getenv("FBR_API_KEY", "YOUR_FBR_API_KEY_HERE")

# --- Sample Invoice Data ---
# This dictionary represents a simplified invoice payload as expected by the FBR API.
# Real FBR API schema would be much more complex and detailed.
sample_invoice = {
    "invoiceNumber": "INV-2023-001",
    "invoiceDate": "2023-10-27T10:30:00Z",
    "sellerInfo": {
        "ntn": "1234567-8", # National Tax Number
        "businessName": "Example Business Inc.",
        "address": "123 Main Street, Islamabad"
    },
    "buyerInfo": {
        "ntn": "8765432-1",
        "businessName": "Customer Co. Ltd.",
        "address": "456 Market Road, Lahore"
    },
    "items": [
        {
            "description": "Product A",
            "quantity": 2,
            "unitPrice": 100.00,
            "totalAmount": 200.00,
            "taxRate": 0.17,
            "taxAmount": 34.00
        },
        {
            "description": "Service B",
            "quantity": 1,
            "unitPrice": 500.00,
            "totalAmount": 500.00,
            "taxRate": 0.17,
            "taxAmount": 85.00
        }
    ],
    "totalGrossAmount": 700.00,
    "totalTaxAmount": 119.00,
    "totalNetAmount": 819.00,
    "currency": "PKR"
}

def submit_invoice_to_fbr(invoice_data):
    """
    Submits an invoice to the hypothetical FBR Digital Invoicing API using http.client.
    """
    if not FBR_API_KEY or FBR_API_KEY == "YOUR_FBR_API_KEY_HERE":
        print("Error: FBR_API_KEY not set. Please set the environment variable or replace the placeholder.")
        return None

    # Prepare the JSON payload for the API request
    json_payload = json.dumps(invoice_data)
    payload_bytes = json_payload.encode('utf-8')

    # Set up HTTP headers, including content type and authorization
    headers = {
        "Content-Type": "application/json",
        "Content-Length": str(len(payload_bytes)),
        "Authorization": f"Bearer {FBR_API_KEY}" # FBR API typically requires a Bearer token
    }

    print(f"Attempting to send invoice to: https://{FBR_API_HOST}{FBR_API_PATH}")
    print(f"Invoice payload: {json.dumps(invoice_data, indent=2)}")

    conn = None
    try:
        # Create a secure SSL context for HTTPS connection
        context = ssl.create_default_context()
        # Establish a secure HTTPS connection to the FBR API host
        conn = http.client.HTTPSConnection(FBR_API_HOST, context=context, timeout=10)

        # Send the POST request with the invoice payload and headers
        conn.request("POST", FBR_API_PATH, body=payload_bytes, headers=headers)

        # Get the response from the FBR API
        response = conn.getresponse()

        print("\n--- API Response ---")
        print(f"Status Code: {response.status}")
        print(f"Reason: {response.reason}")

        response_body = response.read().decode('utf-8')
        try:
            # Attempt to parse response body as JSON (common for APIs)
            json_response = json.loads(response_body)
            print(f"Response Body: {json.dumps(json_response, indent=2)}")
            return json_response
        except json.JSONDecodeError:
            # If response is not JSON, print raw body
            print(f"Raw Response Body: {response_body}")
            return response_body

    except http.client.HTTPException as e:
        print(f"\nError: HTTP Exception occurred: {e}")
    except ConnectionRefusedError as e:
        print(f"\nError: Connection refused. Is the host '{FBR_API_HOST}' reachable? {e}")
    except ssl.SSLError as e:
        print(f"\nError: SSL/TLS error occurred: {e}")
    except TimeoutError as e:
        print(f"\nError: The request timed out: {e}")
    except Exception as e:
        print(f"\nError: An unexpected error occurred: {e}")
    finally:
        if conn:
            conn.close() # Ensure the connection is closed

    return None

if __name__ == "__main__":
    print("--- FBR Digital Invoicing API Integration Example ---")
    print("This script simulates sending an invoice to a hypothetical FBR API using Python's standard library.")
    print("Please set FBR_API_KEY, FBR_API_HOST, and FBR_API_PATH environment variables for a real test.")

    # Call the function to submit the sample invoice
    fbr_response = submit_invoice_to_fbr(sample_invoice)

    if fbr_response:
        print("\nInvoice submission process completed.")
    else:
        print("\nInvoice submission failed or encountered an error.")
