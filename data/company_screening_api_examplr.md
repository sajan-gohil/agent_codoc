## Overview of API

Head to [Crustdata Discovery And Enrichment API](https://www.notion.so/Crustdata-Discovery-And-Enrichment-API-c66d5236e8ea40df8af114f6d447ab48?pvs=21) 

## Examples

### 1. Companies with given list of Crustdata company_id

Crustdata’s company_id is the unique identifier of a company in our database. It is unique and it never changes. It is numeric.

Use this request to get information for all companies with  `company_id` equal to any one of [680992, 673947, 631280, 636304, 631811] . The fields/columns in the response are depending on `metric_name` you provide (👇[see below](https://www.notion.so/Crustdata-Company-Screening-API-Detailed-Examples-375908d855464d87a01efd2c7a369750?pvs=21))

- **Curl**
    
    ```bash
    curl 'https://api.crustdata.com/screener/screen/' \
      -H 'Accept: application/json, text/plain, */*' \
      -H 'Accept-Language: en-US,en;q=0.9' \
      -H 'Authorization: Token $auth_token' \
      -H 'Cache-Control: no-cache' \
      -H 'Connection: keep-alive' \
      -H 'Content-Type: application/json' \
      -H 'Origin: https://crustdata.com' \
      --data-raw '{
        "metrics": [{"metric_name": "linkedin_headcount_and_glassdoor_ceo_approval_and_g2"}],
        "filters": {
            "op": "or",
            "conditions": [
                    {"column": "company_id", "type": "=", "value": 680992, "allow_null": false},
                    {"column": "company_id", "type": "=", "value": 673947, "allow_null": false},
                    {"column": "company_id", "type": "=", "value": 631280, "allow_null": false},
                    {"column": "company_id", "type": "=", "value": 636304, "allow_null": false},
                    {"column": "company_id", "type": "=", "value": 631811, "allow_null": false}
                ]
        },
        "hidden_columns": ["company_id", "total_rows"],
        "offset": 0,
        "count": 100,
        "sorts": []
    }' \
      --compressed
    ```
    
- **Python**
    
    ```python
    import requests
    
    # Endpoint and headers
    url = 'https://api.crustdata.com/screener/screen/'
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Authorization': 'Token $auth_token',  **# Replace with your actual token**
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'Origin': 'https://crustdata.com',
    }
    
    # Data payload
    data = {
        "metrics": [{
            "metric_name": $metric_name  # Replace with desired metric name
        }],
        "filters": {
            "op": "or",
            "conditions": [
    								{"column": "company_id", "type": "=", "value": 680992, "allow_null": False},
                    {"column": "company_id", "type": "=", "value": 673947, "allow_null": False},
                    {"column": "company_id", "type": "=", "value": 631280, "allow_null": False},
                    {"column": "company_id", "type": "=", "value": 636304, "allow_null": False},
                    {"column": "company_id", "type": "=", "value": 631811, "allow_null": False}            
    	        ]
        },
        "hidden_columns": [],
        "offset": 0,
        "count": 100,
        "sorts": []
    }
    
    # Send the request
    response = requests.post(url, headers=headers, json=data)
    
    # Parse the response
    json_response = response.json()
    
    # Print or use the response as needed
    print(json_response)
    ```
    
- **Response**
    
    [JSON Hero](https://jsonhero.io/j/ntHvSKVeZJIc)
    

**Note**:

1. You need to provide the following
    1. `$auth_token` : Your Crustdata API Key/Auth Token. Reach out to abhilash@crustdata.com through your company email if not available
    2. `$metric_name` : could be any of the following
        1. *linkedin_headcount_and_glassdoor_ceo_approval_and_g2*
2. To retrieve all the companies matching the filters, keep iterating over `offset` field in the payload. 
3. **Do not** increase `count` beyond 100 as the result will be truncated to 100 rows without any ordering.

### 2.Companies with given website domains (exact match)

Use this request to get metrics (depending in `metric_name` you provide 👇[see below](https://www.notion.so/Crustdata-Company-Screening-API-Detailed-Examples-375908d855464d87a01efd2c7a369750?pvs=21)) for all companies with their  `company_website_domain` exactly match any of [”kets-quantum.com”, “kasada.io”, “nisos.com”, “onamesecurity.com”, “medigate.io”]

- **cURL**
    
    ```python
    curl 'https://api.crustdata.com/screener/screen/' \
      -H 'Accept: application/json, text/plain, */*' \
      -H 'Accept-Language: en-US,en;q=0.9' \
      -H 'Authorization: Token $auth_token' \
      -H 'Cache-Control: no-cache' \
      -H 'Connection: keep-alive' \
      -H 'Content-Type: application/json' \
      -H 'Origin: https://crustdata.com' \
      --data-raw '{
        "metrics": [{"metric_name": $metric_name}],
        "filters": {
            "op": "or",
            "conditions": [
                    {"column": "company_website_domain", "type": "=", "value": "kets-quantum.com", "allow_null": false},
                    {"column": "company_website_domain", "type": "=", "value": "kasada.io", "allow_null": false},
                    {"column": "company_website_domain", "type": "=", "value": "nisos.com", "allow_null": false},
                    {"column": "company_website_domain", "type": "=", "value": "nonamesecurity.com", "allow_null": false},
                    {"column": "company_website_domain", "type": "=", "value": "medigate.io", "allow_null": false}
                ]
        },
        "hidden_columns": [],
        "offset": 0,
        "count": 100,
        "sorts": []
    }' \
      --compressed
    ```
    

- **Python**
    
    ```python
    import requests
    
    # Endpoint and headers
    url = 'https://api.crustdata.com/screener/screen/'
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Authorization': 'Token {}'.format(auth_token),  # <- Replace auth_token with your token
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'Origin': 'https://crustdata.com'
    }
    
    # Data payload
    data = {
        "metrics": [{"metric_name": metric_name}],  # <- Replace metric_name with your metric
        "filters": {
            "op": "or",
            "conditions": [
                    {"column": "company_website_domain", "type": "=", "value": "kets-quantum.com", "allow_null": False},
                    {"column": "company_website_domain", "type": "=", "value": "kasada.io", "allow_null": False},
                    {"column": "company_website_domain", "type": "=", "value": "nisos.com", "allow_null": False},
                    {"column": "company_website_domain", "type": "=", "value": "nonamesecurity.com", "allow_null": False},
                    {"column": "company_website_domain", "type": "=", "value": "medigate.io", "allow_null": False}
                ]
        },
        "hidden_columns": [],
        "offset": 0,
        "count": 100,
        "sorts": []
    }
    
    # TODO: Replace the following two lines with your actual values
    auth_token = "YOUR_AUTH_TOKEN"
    metric_name = "YOUR_METRIC_NAME"
    
    # Send the request
    response = requests.post(url, headers=headers, json=data)
    
    # Get and print the response
    json_response = response.json()
    print(json_response)
    ```
    

- **Response**
    
    [JSON Hero](https://jsonhero.io/j/nYBSy5Xm7ERA/editor)
    

### 3. Companies that Crustdata started tracking after a certain date

Add a filter on `created_at` column with specific date in `YYYY-MM-DD` format. 

For example if you wanted to get all the companies which Crustdata started tracking after 1st May, 2023, you would do:

- **cURL**
    
    ```jsx
    curl 'https://api.crustdata.com/screener/screen/' \
      -H 'Accept: application/json, text/plain, */*' \
      -H 'Accept-Language: en-US,en;q=0.9' \
      -H 'Authorization: Token $auth_token' \
      -H 'Cache-Control: no-cache' \
      -H 'Connection: keep-alive' \
      -H 'Content-Type: application/json' \
      -H 'Origin: https://crustdata.com' \
      --data-raw '{
        "metrics": [
          {
            "metric_name": "linkedin_headcount_and_glassdoor_ceo_approval_and_g2"
          }
        ],
        "filters": {
          "op": "and",
          "conditions": [
            {
              "column": "created_at",
              "type": ">",
              "value": "2023-05-01",
              "allow_null": false
            }
          ]
        },
        "hidden_columns": [],
        "offset": 0,
        "count": 100,
        "sorts": [],
      }' \
      --compressed
    ```
    
- **Python**
    
    ```jsx
    import requests
    
    # Endpoint and headers
    url = 'https://api.crustdata.com/screener/screen/'
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Authorization': 'Token {}'.format(auth_token),  # <- Replace auth_token with your token
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'Origin': 'https://crustdata.com'
    }
    
    # Data payload
    data = {
        "metrics": [{"metric_name": metric_name}],  # <- Replace metric_name with your metric
        "filters": {
            "op": "and",
            "conditions": [
    							{ "column": "created_at", "type": ">", "value": "2023-05-01", "allow_null": false }
             ]
        },
        "hidden_columns": [],
        "offset": 0,
        "count": 100,
        "sorts": []
    }
    
    # TODO: Replace the following two lines with your actual values
    auth_token = "YOUR_AUTH_TOKEN"
    metric_name = "YOUR_METRIC_NAME"
    
    # Send the request
    response = requests.post(url, headers=headers, json=data)
    
    # Get and print the response
    json_response = response.json()
    print(json_response
    ```
    

### 4. Companies with given website domains (case in-sensitive contains match)

Use this request to get metrics for all companies whose  `company_website_domain`  contains string “kasada.io”   

- **cURL**
    
    ```bash
    curl 'https://api.crustdata.com/screener/screen/' \
      -H 'Accept: application/json, text/plain, */*' \
      -H 'Accept-Language: en-US,en;q=0.9' \
      -H 'Authorization: Token $auth_token' \
      -H 'Cache-Control: no-cache' \
      -H 'Connection: keep-alive' \
      -H 'Content-Type: application/json' \
      -H 'Origin: https://crustdata.com' \
      --data-raw '{
        "metrics": [{"metric_name": $metric_name}],
        "filters": {
            "op": "and",
            "conditions": [
                    {"column": "company_website_domain", "type": "(.)", "value": "kasada.io", "allow_null": false}
             ]
        },
        "hidden_columns": [],
        "offset": 0,
        "count": 100,
        "sorts": []
    }' \
      --compressed
    ```
    
- **Python**
    
    ```python
    import requests
    
    # Endpoint and headers
    url = 'https://api.crustdata.com/screener/screen/'
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Authorization': 'Token {}'.format(auth_token),  # <- Replace auth_token with your token
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'Origin': 'https://crustdata.com'
    }
    
    # Data payload
    data = {
        "metrics": [{"metric_name": metric_name}],  # <- Replace metric_name with your metric
        "filters": {
            "op": "and",
            "conditions": [
                    {"column": "company_website_domain", "type": "(.)", "value": "kasada.io", "allow_null": False},
             ]
        },
        "hidden_columns": [],
        "offset": 0,
        "count": 100,
        "sorts": []
    }
    
    # TODO: Replace the following two lines with your actual values
    auth_token = "YOUR_AUTH_TOKEN"
    metric_name = "YOUR_METRIC_NAME"
    
    # Send the request
    response = requests.post(url, headers=headers, json=data)
    
    # Get and print the response
    json_response = response.json()
    print(json_response)
    ```
    

### 5. Companies with 31 to 50% of their employees skilled in “quality assurance”

- **cURL**
    
    ```bash
    curl 'https://api.crustdata.com/screener/screen/' \
      -H 'Accept: */*' \
      -H 'Content-Type: application/json' \
      -H 'Accept-Language: en-US,en;q=0.9' \
      -H 'Authorization: Token $token' \
      --data-raw '{"metrics":[{"metric_name":"linkedin_headcount_and_glassdoor_ceo_approval_and_g2"}],"filters":{"op":"and","conditions":[{"column":"linkedin_employee_skills_31_to_50_pct","type":"(.)","value":"quality assurance","allow_null":false}]},"offset":0,"count":150}' \
      --compressed
    ```
    
- **Python**
    
    ```python
    import requests
    
    # The API endpoint URL
    url = 'https://api.crustdata.com/screener/screen/'
    
    # Headers for the API request
    headers = {
        'Accept': '*/*',
        'Content-Type': 'application/json',
        'Accept-Language': 'en-US,en;q=0.9',
        
        # Replace '$token' with your actual authorization token
        'Authorization': 'Token YOUR_ACTUAL_TOKEN_HERE',
    }
    
    # Data payload for the API request
    data = {
        "metrics": [
            {"metric_name": "linkedin_headcount_and_glassdoor_ceo_approval_and_g2"}
        ],
        "filters": {
            "op": "and",
            "conditions": [
                {
                    "column": "linkedin_employee_skills_31_to_50_pct",
                    
                    # Ensure the 'type' and 'value' fields match your specific filtering needs
                    "type": "(.)",
                    "value": "quality assurance",
                    "allow_null": False
                }
            ]
        },
        
        # Adjust 'offset' and 'count' based on your pagination requirements
        "offset": 0,
        "count": 150
    }
    
    # Sending the POST request
    response = requests.post(url, headers=headers, json=data)
    
    # Output the response in JSON format
    print(response.json())
    
    ```
    

### 6. Companies that meet a specific criteria

- Example criteria #1
    
    Companies with:
    
    - with majority of the headcount in US AND
    - total headcount > 50 AND
    - total funds raised > $5M AND
    - **cURL**
        
        ```bash
        curl 'https://api.crustdata.com/screener/screen/' \
        -H 'Accept: application/json, text/plain, /' \
        -H 'Authorization: Token $auth_token' \
        -H 'Content-Type: application/json' \
        --data-raw '{
            "metrics": [
              {
                "metric_name": "linkedin_headcount_and_glassdoor_ceo_approval_and_g2"
              }
            ],
            "filters": {
              "op": "and",
              "conditions": [
                        {
                          "column": "crunchbase_total_investment_usd",
                          "type": "=>",
                          "value": "5000000"
                        },
                        {
                          "column": "linkedin_headcount",
                          "type": "=>",
                          "value": "50"
                        },
                        {
                          "column": "largest_headcount_country",
                          "type": "(.)",
                          "value": "USA",
                          "allow_null": false
                        }
              ]
            },
            "hidden_columns": [],
            "offset": 0,
            "count": 100,
            "sorts": []
          }' \
        
        ```
        
    - **Python**
        
        ```python
        import requests
        import os
        
        # Set up the endpoint and headers
        url = 'https://api.crustdata.com/screener/screen/'
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Authorization': 'Token {}'.format(auth_token),  # <- Replace auth_token with your token
            'Content-Type': 'application/json'
        }
        
        # Define the payload
        payload = {
            "metrics": [
                {
                    "metric_name": "linkedin_headcount_and_glassdoor_ceo_approval_and_g2"
                }
            ],
            "filters": {
                "op": "and",
                "conditions": [
                    {
                        "column": "crunchbase_total_investment_usd",
                        "type": "=>",
                        "value": "5000000",
                        "allow_null": False
                    },
                    {
                        "column": "linkedin_headcount",
                        "type": "=>",
                        "value": "50",
                        "allow_null": False
                    },
                    {
                        "column": "largest_headcount_country",
                        "type": "(.)",
                        "value": "USA",
                        "allow_null": False
                    }
                ]
            },
            "hidden_columns": [],
            "offset": 0,
            "count": 100,
            "sorts": []
        }
        
        # Make the request
        response = requests.post(url, headers=headers, json=payload)
        
        # Check the response
        if response.status_code == 200:
            data = response.json()
            print(data)
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
        
        ```
        
- Example criteria #2
    
    Companies with:
    
    - with “Crunchbase categories” as “Artificial Intelligence” or “Machine Learning” AND
    - with “Linkedin industries” as “Software Development” or “Research Services
    
    - **cURL**
        
        ```bash
        curl 'https://api.crustdata.com/screener/screen/' \
        -H 'Accept: application/json, text/plain, /' \
        -H 'Authorization: Token $auth_token' \
        -H 'Content-Type: application/json' \
        --data-raw '{
            "metrics": [
              {
                "metric_name": "linkedin_headcount_and_glassdoor_ceo_approval_and_g2"
              }
            ],
            "filters": {
              "op": "and",
              "conditions": [
                        {
                          "column": "linkedin_industries",
                          "type": "in",
                          "value": ["Software development", "Research services"]
                        },
                        {
                          "column": "crunchbase_categories",
                          "type": "in",
                          "value": ["Artificial Intelligence", "Machine Learning"]
                        }
              ]
            },
            "hidden_columns": [],
            "offset": 0,
            "count": 100,
            "sorts": []
          }' \
        
        ```
        
    - **Python**
        
        ```python
        import requests
        import os
        
        # Set up the endpoint and headers
        url = 'https://api.crustdata.com/screener/screen/'
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Authorization': 'Token {}'.format(auth_token),  # <- Replace auth_token with your token
            'Content-Type': 'application/json'
        }
        
        # Define the payload
        payload = {
            "metrics": [
                {
                    "metric_name": "linkedin_headcount_and_glassdoor_ceo_approval_and_g2"
                }
            ],
            "filters": {
                "op": "and",
                "conditions": [
                        {
                          "column": "linkedin_industries",
                          "type": "in",
                          "value": ["software development", "research services"]
                        },
                        {
                          "column": "crunchbase_categories",
                          "type": "in",
                          "value": ["artificial intelligence", "machine learning"]
                        }
                ]
            },
            "hidden_columns": [],
            "offset": 0,
            "count": 100,
            "sorts": []
        }
        
        # Make the request
        response = requests.post(url, headers=headers, json=payload)
        
        # Check the response
        if response.status_code == 200:
            data = response.json()
            print(data)
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
        
        ```
        
- Example criteria #3
    
    Companies with:
    
    - Total funding raised > $1,000,000
    - Last funding round type is “SEED”
    - Raised in last 90 days
    - with Linkedin Industries as “Software Development” or “Internet” or “Technology” OR Crunchbase Categories as “SaaS”
    
    - **cURL**
        
        ```bash
        curl --location 'https://api.crustdata.com/screener/screen/' \
        --header 'Authorization: Token $token' \
        --header 'Content-Type: application/json' \
        --data '{
            "metrics": [
                {
                    "metric_name": "linkedin_headcount_and_glassdoor_ceo_approval_and_g2"
                }
            ],
            "filters": {
                "op": "and",
                "conditions": [
                    {
                        "op": "or",
                        "conditions": [
                            {"column": "linkedin_industries", "type": "(.)", "value": "software"},
                            {"column": "linkedin_industries", "type": "(.)", "value": "internet"},
                            {"column": "linkedin_industries", "type": "(.)", "value": "technology"},
                            {"column": "crunchbase_categories", "type": "(.)", "value": "saas"}
                        ]
                    },
                    {"column": "crunchbase_total_investment_usd", "type": "=>", "value": 1000000},
                    {"column": "last_funding_round_type", "type": "(.)", "value": "seed"},
                    {"column": "days_since_last_fundraise", "type": "<", "value": "90"}
                ]
            },
            "offset": 0,
            "count": 100,
            "sorts": []
        }'
        
        ```
        
    - **Python**
        
        ```python
        import requests
        
        url = "https://api.crustdata.com/screener/screen/"
        headers = {
            "Authorization": "Token $token",
            "Content-Type": "application/json"
        }
        payload = {
            "metrics": [
                {"metric_name": "linkedin_headcount_and_glassdoor_ceo_approval_and_g2"}
            ],
            "filters": {
                "op": "and",
                "conditions": [
                    {
                        "op": "or",
                        "conditions": [
                            {"column": "linkedin_industries", "type": "(.)", "value": "software"},
                            {"column": "linkedin_industries", "type": "(.)", "value": "internet"},
                            {"column": "linkedin_industries", "type": "(.)", "value": "technology"},
                            {"column": "crunchbase_categories", "type": "(.)", "value": "saas"}
                        ]
                    },
                    {"column": "crunchbase_total_investment_usd", "type": "=>", "value": 1000000},
                    {"column": "last_funding_round_type", "type": "(.)", "value": "seed"},
                    {"column": "days_since_last_fundraise", "type": "<", "value": "90"}
                ]
            },
            "offset": 0,
            "count": 100,
            "sorts": []
        }
        
        response = requests.post(url, headers=headers, json=payload)
        
        print(response.status_code)
        print(response.json())
        
        ```
        

You can build a custom criteria using 

- Column names listed here [Crustdata Data Dictionary](https://www.notion.so/Crustdata-Data-Dictionary-c265aa415fda41cb871090cbf7275922?pvs=21)
- `filters` schema laid out here [**Request Body Overview** ](https://www.notion.so/Request-Body-Overview-042a89be6e0941e2b9e33cc22c1c2ecc?pvs=21)

### 7. Companies with a given list of `linkedin_id`

`linkedin_id` is the unique identifier of a company on LinkedIn. It is a numeric string.

Use this request to get information for all companies with  `linkedin_id` equal to any one of `["6452409","7597308","3991822","76987811"]`  **(NOTE: remember to have quotes on the values)**

- **Curl**
    
    ```bash
    curl 'https://api.crustdata.com/screener/screen/' \
      -H 'Authorization: Token $auth_token' \
      -H 'Content-Type: application/json' \
      --data-raw '{
        "metrics": [
          {
            "metric_name": "linkedin_headcount_and_glassdoor_ceo_approval_and_g2"
          }
        ],
        "filters": {
          "op": "or",
          "conditions": [
            {
              "column": "linkedin_id",
              "type": "in",
              "value": ["6452409", "7597308", "3991822", "76987811"],
              "allow_null": false
            }
          ]
        },
        "hidden_columns": ["company_id", "total_rows"],
        "offset": 0,
        "count": 100,
        "sorts": []
      }' \
      --compressed
    ```
    
- **Python**
    
    ```python
    import requests
    
    # Endpoint and headers
    url = 'https://api.crustdata.com/screener/screen/'
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Authorization': 'Token $auth_token',  **# Replace with your actual token**
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'Origin': 'https://crustdata.com',
    }
    
    # Data payload
    data = {
        "metrics": [{
            "metric_name": "lidin_headcount_and_glassdoor_ceo_approval_and_g2*"*
        }],
        "filters": {
            "op": "or",
            "conditions": [
    								{"column": "linkedin_id", "type": "in", "value": ["6452409","7597308","3991822","76987811"], "allow_null": False},
    	        ]
        },
        "hidden_columns": [],
        "offset": 0,
        "count": 100,
        "sorts": []
    }
    
    # Send the request
    response = requests.post(url, headers=headers, json=data)
    
    # Parse the response
    json_response = response.json()
    
    # Print or use the response as needed
    print(json_response)
    ```
    
- **Response**
    
    https://jsonhero.io/j/QEloNkNC4zhI
    

**Note**:

1. You need to provide the following
    1. `$auth_token` : Your Crustdata API Key/Auth Token. Reach out to abhilash@crustdata.com through your company email if not available
2. To retrieve all the companies matching the filters, keep iterating over `offset` field in the payload. 
3. **Do not** increase `count` beyond 100 as the result will be truncated to 100 rows without any ordering.

### Appendix

List of all possible values of various fields

- Crunchbase Categories
    
    ```bash
    ["E-Commerce Platforms", "Food Delivery", "Food Processing", "Internet", "Restaurants", "Snack Food", "Information Services", "Reservations", "Search Engine", "Delivery", "Delivery Service", "E-Commerce", "Grocery", "Retail", "Shopping", "E-Learning", "EdTech", "Education", "Higher Education", "Mobile", "Mobile Apps", "Secondary Education", "Software", "Tutoring", "Enterprise Software", "Logistics", "SaaS", "Supply Chain Management", "Transportation", "Banking", "Financial Services", "FinTech", "Insurance", "Apps", "Fitness", "Health Care", "Wellness", "Finance", "Marketplace", "Food and Beverage", "Training", "Public Transportation", "Ride Sharing", "Artificial Intelligence", "Customer Service", "Messaging", "Mobile Payments", "Cloud Data Services", "Consulting", "Information Technology", "Outsourcing", "Digital Media", "Video", "Video Streaming", "News", "Public Relations", "Publishing", "Consumer Goods", "Venture Capital", "Wealth Management", "Automotive", "Manufacturing", "Same Day Delivery", "Consumer Lending", "Lending", "Payments", "Hospitality", "Hotel", "Leisure", "Travel", "Health Diagnostics", "Medical", "Pharmaceutical", "QR Codes", "Beauty", "Fashion", "Lifestyle", "Online Portals", "Analytics", "Commercial Real Estate", "Property Management", "Real Estate", "Small and Medium Businesses", "Business Intelligence", "Telecommunications", "Social Network", "Auto Insurance", "Commercial Insurance", "Health Insurance", "Life Insurance", "Consumer", "Furniture", "Home Decor", "Home Improvement", "Rental", "Home Services", "Fantasy Sports", "Sports", "Developer APIs", "Cloud Security", "Cyber Security", "Accounting", "PaaS", "Advertising", "Advertising Platforms", "Marketing", "AgTech", "B2B", "Sales", "Agriculture", "Content Creators", "Digital Marketing", "Farming", "Hospital", "Therapeutics", "Interior Design", "Digital Entertainment", "Event Management", "Events", "Media and Entertainment", "Online Auctions", "Social Media", "Rental Property", "Emerging Markets", "Hedge Funds", "Sharing Economy", "InsurTech", "Music", "Music Streaming", "Gaming", "Biotechnology", "Genetics", "Big Data", "Brand Marketing", "Hardware", "Social Media Marketing", "Car Sharing", "Collaborative Consumption", "Communities", "Home Health Care", "CRM", "Computer", "Blockchain", "Cryptocurrency", "Trading Platform", "Classifieds", "Image Recognition", "STEM Education", "Private Social Networking", "Credit", "Credit Bureau", "Data Integration", "Cloud Computing", "Business Development", "Machine Learning", "Real Time", "Crowdfunding", "Knowledge Management", "Business Information Systems", "Crowdsourcing", "Market Research", "Service Industry", "Financial Exchanges", "Personal Finance", "Consumer Electronics", "Industrial Engineering", "Product Research", "Robotics", "Collaboration", "Developer Platform", "Productivity Tools", "Video Chat", "Angel Investment", "Social Shopping", "CleanTech", "Electric Vehicle", "Electronics", "Renewable Energy", "Biometrics", "Video Games", "Peer to Peer", "Sales Automation", "Point of Sale", "Coupons", "Enterprise", "Transaction Processing", "Android", "Natural Language Processing", "Industrial Automation", "Internet of Things", "Baby", "Travel Accommodations", "Corporate Training", "Employee Benefits", "Gift", "Human Resources", "Cloud Infrastructure", "Developer Tools", "Location Based Services", "Procurement", "Loyalty Programs", "Marketing Automation", "TV", "Eyewear", "Medical Device", "mHealth", "Mobile Advertising", "Forestry", "Information and Communications Technology (ICT)", "Predictive Analytics", "Satellite Communication", "Broadcasting", "Journalism", "Quality Assurance", "Virtualization", "Taxi Service", "Call Center", "Speech Recognition", "Virtual Assistant", "Management Information Systems", "Brewing", "Craft Beer", "Wine And Spirits", "Employment", "Recruiting", "EBooks", "Staffing Agency", "Infrastructure", "Impact Investing", "Virtual Reality", "Career Planning", "Wholesale", "Database", "Product Design", "Ad Exchange", "Solar", "Computer Vision", "Retail Technology", "Business Travel", "Intellectual Property", "Cosmetics", "Enterprise Applications", "Software Engineering", "Web Development", "Adventure Travel", "Enterprise Resource Planning (ERP)", "Project Management", "Operating Systems", "Social News", "Mobile Devices", "Wireless", "Electrical Distribution", "Billing", "Compliance", "Application Performance Management", "Jewelry", "Personalization", "Tourism", "Men\'s", "Autonomous Vehicles", "Communications Infrastructure", "Smart Cities", "Clean Energy", "Energy", "Wind Energy", "Professional Services", "Sustainability", "Lingerie", "Architecture", "Environmental Consulting", "Home Renovation", "Smart Home", "iOS", "Identity Management", "Network Security", "Security", "Auctions", "Tea", "Dietary Supplements", "Network Hardware", "Shoes", "Organic Food", "Property Development", "Alternative Medicine", "GPU", "Risk Management", "Parking", "Semiconductor", "Cycling", "Last Mile Transportation", "Emergency Medicine", "Non Profit", "Nanotechnology", "Universities", "Freelance", "Professional Networking", "Funding Platform", "App Marketing", "Wearables", "Content", "eSports", "Cloud Storage", "Industrial", "ISP", "Optical Communication", "Coffee", "Leasing", "Task Management", "Asset Management", "Fast-Moving Consumer Goods", "Nutrition", "Local Business", "Reading Apps", "Recreational Vehicles", "Legal", "Legal Tech", "SEO", "Web Hosting", "Green Consumer Goods", "B2C", "Micro Lending", "Women\'s", "Handmade", "Open Source", "Child Care", "Contact Management", "Document Management", "Air Transportation", "SNS", "Freight Service", "Marine Transportation", "Affiliate Marketing", "Video on Demand", "Commercial", "Energy Management", "Railroad", "Local Shopping", "Social Entrepreneurship", "Data Mining", "Intelligent Systems", "Bitcoin", "Association", "Email Marketing", "Personal Health", "Property Insurance", "Ticketing", "Toys", "Courier Service", "IT Infrastructure", "Photography", "Cloud Management", "Construction", "Waste Management", "IT Management", "Life Science", "Text Analytics", "Film", "Local", "Art", "Ediscovery", "Recycling", "Organic", "Coworking", "Horticulture", "Video Advertising", "Gift Card", "Ad Targeting", "Public Safety", "DSP", "Fleet Management", "Credit Cards", "Geospatial", "Mapping Services", "Blogging Platforms", "Content Delivery Network", "Augmented Reality", "Language Learning", "Unified Communications", "Debit Cards", "Price Comparison", "Test and Measurement", "Web Apps", "Building Material", "Online Games", "Social", "Travel Agency", "Drones", "Laundry and Dry-cleaning", "Product Search", "Residential", "3D Technology", "Field-Programmable Gate Array (FPGA)", "Wedding", "Content Discovery", "Energy Storage", "Management Consulting", "Aerospace", "Skill Assessment", "Elder Care", "Children", "Fruit", "Semantic Search", "Outdoor Advertising", "Shopping Mall", "IaaS", "GreenTech", "Debt Collections", "Stock Exchanges", "Windows Phone", "Retirement", "Parenting", "Data Visualization", "Personal Development", "Sensor", "Consumer Applications", "Primary Education", "Ad Network", "Social Bookmarking", "Bakery", "Energy Efficiency", "Oil and Gas", "Power Grid", "Water", "Water Purification", "Packaging Services", "Web Design", "Family", "Fuel", "Dating", "Mineral", "Mining", "Mining Technology", "Data Center Automation", "Bioinformatics", "VoIP", "UX Design", "Social CRM", "Environmental Engineering", "Clinical Trials", "Event Promotion", "Dental", "Celebrity", "Assistive Technology", "Cosmetic Surgery", "Data Center", "Browser Extensions", "Office Administration", "Battery", "Plastics and Rubber Manufacturing", "Comics", "Translation Service", "Textiles", "Animal Feed", "Incubators", "Mechanical Design", "Audio", "Warehousing", "Resorts", "Graphic Design", "Concerts", "Nightlife", "Veterinary", "Edutainment", "Government", "GovTech", "Chemical", "Online Forums", "Fertility", "Fraud Detection", "Charity", "Shipping", "Content Marketing", "Guides", "File Sharing", "Industrial Manufacturing", "Machinery Manufacturing", "Quantum Computing", "Civil Engineering", "Vacation Rental", "Innovation Management", "Biopharma", "Wired Telecommunications", "CMS", "Content Syndication", "Cooking", "Social Impact", "GPS", "Biomass Energy", "Catering", "Privacy", "Email", "Assisted Living", "Space Travel", "Social Media Management", "SMS", "Photo Sharing", "Electronic Design Automation (EDA)", "Biofuel", "Data Storage", "Flash Storage", "Farmers Market", "3D Printing", "Navigation", "Virtual World", "Nutraceutical", "PC Games", "Animation", "Physical Security", "College Recruiting", "Facilities Support Services", "Facility Management", "Presentations", "Livestock", "Printing", "Group Buying", "Outdoors", "Social Recruiting", "Internet Radio", "Electronic Health Record (EHR)", "Advice", "Housekeeping Service", "Real Estate Investment", "Performing Arts", "Google Glass", "Continuing Education", "Vocational Education", "RFID", "Religion", "Pet", "National Security", "Neuroscience", "Meeting Software", "Subscription Service", "Audiobooks", "Podcast", "Self-Storage", "Web Browsers", "Embedded Systems", "Freemium", "Diabetes", "Sporting Goods", "Consumer Reviews", "Advanced Materials", "Casual Games", "Vertical Search", "Paper Manufacturing", "Cannabis", "Law Enforcement", "Humanitarian", "Product Management", "Music Education", "Creative Agency", "Casino", "Gambling", "Gamification", "Homeland Security", "Lighting", "Digital Signage", "Natural Resources", "Video Conferencing", "Precious Metals", "Film Production", "A/B Testing", "Mechanical Engineering", "Consumer Software", "Nightclubs", "In-Flight Entertainment", "Local Advertising", "Marine Technology", "DIY", "TV Production", "Seafood", "Building Maintenance", "Recipes", "Politics", "Photo Editing", "Lead Management", "Virtual Currency", "Social Media Advertising", "Human Computer Interaction", "Outpatient Care", "Motion Capture", "Textbook", "MMO Games", "Simulation", "Recreation", "Reputation", "SEM", "Young Adults", "Technical Support", "Private Cloud", "Commercial Lending", "Tour Operator", "Psychology", "Racing", "Food Trucks", "Ad Retargeting", "Basketball", "Cricket", "Golf", "Hockey", "Swimming", "Table Tennis", "Volley Ball", "Direct Sales", "Film Distribution", "Wood Processing", "Franchise", "Scheduling", "Lead Generation", "Serious Games", "Virtual Workforce", "Video Editing", "Flowers", "NFC", "Visual Search", "CAD", "Corrections Facilities", "Console Games", "Semantic Web", "Embedded Software", "Landscaping", "Gift Exchange", "DRM", "Aquaculture", "Facial Recognition", "macOS", "Windows", "Alumni", "Ad Server", "Independent Music", "Sponsorship", "Personal Branding", "Music Label", "Consumer Research", "Ethereum", "Q&A", "App Discovery", "Hydroponics", "Archiving Service", "Social Assistance", "Direct Marketing", "Penetration Testing", "Usability Testing", "Diving", "Google", "Theatre", "Desktop Apps", "Facebook", "Millennials", "Pollution Control", "Spam Filtering", "Laser", "Indoor Positioning", "Domain Registrar", "Tobacco", "Field Support", "Document Preparation", "Soccer", "Smart Building", "Drone Management", "Water Transportation", "Confectionery", "Multi-level Marketing", "Charter Schools", "Industrial Design", "Home and Garden", "Military", "Presentation Software", "Playstation", "Virtual Desktop", "Fossil Fuels", "Intrusion Detection", "Nursing and Residential Care", "Amusement Park and Arcade", "Parks", "First Aid", "Virtual Goods", "Tennis", "Musical Instruments", "Elderly", "CivicTech", "Trade Shows", "Linux", "Green Building", "Music Venues", "Communication Hardware", "Adult", "Shipping Broker", "Prediction Markets", "Rehabilitation", "Ports and Harbors", "Twitter", "Gift Registry", "E-Signature", "Made to Order", "Foundries", "Cause Marketing", "Teenagers", "Janitorial Service", "Chemical Engineering", "Nuclear", "Sex Tech", "MOOC", "Distillery", "Collectibles", "Winery", "Collection Agency", "Skiing", "Contests", "Application Specific Integrated Circuit (ASIC)", "LGBT", "Homeless Shelter", "Vending and Concessions", "Boating", "Sailing", "Underserved Children", "Timeshare", "Museums and Historical Sites", "Timber", "Fuel Cell", "Quantified Self", "Sex Industry", "Funerals", "American Football", "Hunting", "Extermination Service", "Baseball", "Generation Z", "Darknet", "Xbox", "Equestrian", "Limousine Service", "WebOS", "Surfing", "Rugby", "Flash Sale", "RISC", "Generation Y", "Nintendo", "Roku", "Data Governance", "Data Management", "Artificial Intelligence (AI)", "Chatbot", "Generative AI", "Metaverse", "Web3", "Mental Health", "Oncology", "Carbon Capture", "DevOps", "PropTech", "Alternative Protein", "Smart Contracts", "Data Collection and Labeling", "Telehealth", "Books", "Charging Infrastructure", "Audio Recording and Production", "Geothermal Energy", "Foreign Exchange Trading", "Mortgage", "Sales Enablement", "Heating, Ventilation, and Air Conditioning (HVAC)", "Native Advertising", "Addiction Treatment", "Apparel", "Primary and Urgent Care", "Decentralized Finance (DeFi)", "Non-Fungible Token (NFT)", "Secondhand Goods", "Home Appliances", "Precision Medicine", "Robotic Process Automation (RPA)", "Warehouse Automation", "Motorsports", "Remote Sensing", "Prepaid Cards", "Hydroelectric", "Audio/Visual Equipment", "Bookkeeping and Payroll", "Cleaning Products", "Personal Care and Hygiene", "Meat and Poultry", "Tax Consulting", "Business Process Automation (BPA)", "Copywriting", "Plant-Based Foods", "Office Supplies", "Real Estate Brokerage", "Dairy", "Sports Leagues and Teams", "Wildlife Conservation", "Special Education", "Herbs and Spices", "Advocacy", "Tax Preparation", "Card and Board Games", "Ferry Service", "Ultimate Frisbee"]
    ```
    
    Or here is a more readable list
    
    ### E-Commerce and Retail
    
    - E-Commerce Platforms
    - E-Commerce
    - Online Portals
    - Shopping
    - Retail
    - Grocery
    - Retail Technology
    - Shopping Mall
    - Local Shopping
    - Local Business
    
    ### Food and Beverage
    
    - Food Delivery
    - Food Processing
    - Snack Food
    - Grocery
    - Restaurants
    - Food and Beverage
    - Same Day Delivery
    - Food Trucks
    - Dietary Supplements
    - Tea
    - Coffee
    - Organic Food
    - Brewery
    - Craft Beer
    - Wine And Spirits
    - Confectionery
    - Catering
    - Farmers Market
    - Meat and Poultry
    
    ### Education
    
    - E-Learning
    - EdTech
    - Education
    - Higher Education
    - Secondary Education
    - Tutoring
    - STEM Education
    - Online Courses
    - Continuing Education
    - Vocational Education
    - Special Education
    
    ### Technology and Software
    
    - Information Services
    - Software
    - Enterprise Software
    - SaaS
    - Artificial Intelligence
    - Blockchain
    - Cryptocurrency
    - Machine Learning
    - Big Data
    - Cloud Data Services
    - Cloud Computing
    - Cloud Infrastructure
    - Cloud Security
    - Cyber Security
    - Cloud Management
    - Data Storage
    - Data Integration
    - Data Center Automation
    - Cloud Management
    - IT Infrastructure
    - IT Management
    - IT Services
    - IaaS
    - PaaS
    - Developer APIs
    - Developer Tools
    - DevOps
    - CRM
    - ERP
    - Network Security
    - Network Hardware
    - Embedded Systems
    - Computer
    - Computer Vision
    - Data Center
    - Data Governance
    - Data Management
    - Data Mining
    - Data Visualization
    - AI
    - NLP
    - Predictive Analytics
    - Virtualization
    - Web Development
    - Software Engineering
    - Enterprise Applications
    - Web Hosting
    - Web Design
    - Web Browsers
    - CMS
    - App Development
    - App Marketing
    - Mobile Apps
    - Mobile Payments
    - Mobile Advertising
    - Mobile Devices
    - Android
    - iOS
    - Windows
    - macOS
    - Linux
    - UX Design
    - Embedded Software
    
    ### Finance and Insurance
    
    - Banking
    - Financial Services
    - FinTech
    - Insurance
    - Auto Insurance
    - Commercial Insurance
    - Health Insurance
    - Life Insurance
    - Consumer Lending
    - Lending
    - Payments
    - Wealth Management
    - Venture Capital
    - Micro Lending
    - Consumer Finance
    - Personal Finance
    - Tax Consulting
    - Accounting
    - Impact Investing
    - Investment Management
    - Hedge Funds
    - Crowdfunding
    - Debt Collections
    - Mortgage
    - Credit Bureau
    - Financial Exchanges
    - Financial Technology
    
    ### Health and Wellness
    
    - Health Care
    - Wellness
    - Health Diagnostics
    - Medical
    - Pharmaceutical
    - mHealth
    - Medical Device
    - Health Insurance
    - Assisted Living
    - Elder Care
    - Fitness
    - Sports
    - Health Tech
    - Therapeutics
    - Hospital
    - Nutrition
    - Mental Health
    - Oncology
    - Addiction Treatment
    - Precision Medicine
    
    ### Media and Entertainment
    
    - Digital Media
    - Video
    - Video Streaming
    - News
    - Public Relations
    - Publishing
    - Content Creators
    - Digital Entertainment
    - Event Management
    - Events
    - Media and Entertainment
    - Social Media
    - Music
    - Music Streaming
    - Gaming
    - Video Games
    - eSports
    - Animation
    - Film
    - Film Production
    - TV Production
    - In-Flight Entertainment
    - Video Advertising
    - Video Conferencing
    - Video Chat
    - Video on Demand
    - Content Marketing
    - Content Delivery Network
    - Content Syndication
    - Content Discovery
    - Digital Marketing
    
    ### Transportation and Logistics
    
    - Transportation
    - Logistics
    - Supply Chain Management
    - Delivery
    - Delivery Service
    - Ride Sharing
    - Public Transportation
    - Automotive
    - Fleet Management
    - Shipping
    - Freight Service
    - Marine Transportation
    - Air Transportation
    - Railroad
    - Last Mile Transportation
    - Car Sharing
    - Parking
    
    ### Real Estate and Construction
    
    - Real Estate
    - Commercial Real Estate
    - Property Management
    - Property Development
    - Real Estate Brokerage
    - Residential
    - Building Maintenance
    - Construction
    - Home Improvement
    - Home Renovation
    
    ### Energy and Environment
    
    - Clean Energy
    - Renewable Energy
    - Wind Energy
    - Solar
    - Biomass Energy
    - Energy Efficiency
    - Energy Management
    - Geothermal Energy
    - Hydroelectric
    - Power Grid
    - Water
    - Water Purification
    - Waste Management
    - Environmental Consulting
    - GreenTech
    - Sustainability
    
    ### Consumer Goods and Services
    
    - Consumer Goods
    - Consumer Electronics
    - Consumer Applications
    - Consumer Reviews
    - Consumer Research
    - Consumer Finance
    - Fast-Moving Consumer Goods
    - Home Appliances
    - Cleaning Products
    - Personal Care and Hygiene
    - Baby
    - Beauty
    - Fashion
    - Apparel
    - Cosmetics
    - Jewelry
    - Eyewear
    - Furniture
    - Home Decor
    - Lifestyle
    - Lingerie
    - Men's
    - Women's
    - Pet
    - Toys
    
    ### Professional Services and Consulting
    
    - Consulting
    - Professional Services
    - Management Consulting
    - Business Development
    - Business Process Automation
    - IT Consulting
    - Environmental Consulting
    - Public Relations
    - Recruiting
    - Staffing Agency
    - Accounting
    - Tax Consulting
    - Legal
    - Legal Tech
    - Real Estate Investment
    - Financial Technology
    - Market Research
    - Product Research
    - Design
    - Graphic Design
    - Interior Design
    
    ### Manufacturing and Industry
    
    - Manufacturing
    - Industrial Manufacturing
    - Industrial Engineering
    - Industrial Design
    - Machinery Manufacturing
    - Mechanical Design
    - Plastics and Rubber Manufacturing
    - Textiles
    - Construction
    - Building Material
    - Energy Storage
    
    ### Communications and Social Media
    
    - Telecommunications
    - Unified Communications
    - Messaging
    - Social Network
    - Social Media
    - Social Media Marketing
    - Social Media Management
    - Social Bookmarking
    - Private Social Networking
    - Social Shopping
    - Social Entrepreneurship
    - Social Recruiting
    - Social CRM
    
    ### Travel and Hospitality
    
    - Travel
    - Travel Accommodations
    - Business Travel
    - Leisure
    - Hospitality
    - Hotel
    - Adventure Travel
    - Travel Agency
    - Tourism
    - Vacation Rental
    
    ### Security and Safety
    
    - Security
    - Cyber Security
    - Network Security
    - Physical Security
    - Intrusion Detection
    - Public Safety
    - Fraud Detection
    - Risk Management
    
    ### Agriculture and Food Production
    
    - Agriculture
    - AgTech
    - Farming
    - Horticulture
    - Dairy
    - Meat and Poultry
    - Food Processing
    - Aquaculture
    - Animal Feed
    
    ### Science and Technology
    
    - Biotechnology
    - Genetics
    - Genomics
    - Bioinformatics
    - Biopharma
    - Nanotechnology
    - Quantum Computing
    - Robotics
    - Artificial Intelligence
    - Machine Learning
    - Big Data
    - Data Science
    
    ### Miscellaneous
    
    - Augmented Reality
    - Virtual Reality
    - Blockchain
    - Cryptocurrency
    - NFTs
    - Decentralized Finance
    - IoT
    - Smart Home
    - Smart Cities
    - Wearables
    - Telehealth
    - Remote Sensing
    - Drones
    - 3D Printing
    - Autonomous Vehicles
    - PropTech
    - Metaverse
    - Digital Twins
    - Generative AI
- LinkedIn Industries
    
    ```bash
    ["Marketing & Advertising", "Information Technology & Services", "Staffing & Recruiting", "Medical Device", "Computer Software", "Oil & Energy", "Financial Services", "Logistics & Supply Chain", "Venture Capital & Private Equity", "Leisure, Travel & Tourism", "Hospital & Health Care", "Mechanical Or Industrial Engineering", "Electrical & Electronic Manufacturing", "Outsourcing/Offshoring", "Mining & Metals", "Real Estate", "Internet", "Consumer Services", "Utilities", "Food Production", "Research", "Arts & Crafts", "Apparel & Fashion", "Newspapers", "Medical Practice", "Renewables & Environment", "Civic & Social Organization", "E-learning", "Broadcast Media", "Banking", "Machinery", "Facilities Services", "Textiles", "Photography", "Consumer Goods", "Construction", "Consumer Electronics", "Online Media", "Hospitality", "Cosmetics", "Market Research", "Writing & Editing", "Plastics", "Education Management", "Transportation/Trucking/Railroad", "Industrial Automation", "Telecommunications", "Packaging & Containers", "Legal Services", "Food & Beverages", "Executive Office", "Management Consulting", "Retail", "Business Supplies & Equipment", "Investment Management", "Design", "Computer Games", "Computer & Network Security", "Accounting", "Insurance", "Automotive", "Pharmaceuticals", "Chemicals", "Import & Export", "Information Services", "Translation & Localization", "Motion Pictures & Film", "Human Resources", "Environmental Services", "Non-profit Organization Management", "Building Materials", "Biotechnology", "Publishing", "Security & Investigations", "Architecture & Planning", "Farming", "Capital Markets", "Furniture", "Entertainment", "Veterinary", "Primary/Secondary Education", "Media Production", "Health, Wellness & Fitness", "Computer Hardware", "Civil Engineering", "Restaurants", "Fundraising", "Performing Arts", "Events Services", "Gambling & Casinos", "Airlines/Aviation", "Nanotechnology", "Wholesale", "Luxury Goods & Jewelry", "Professional Training & Coaching", "Semiconductors", "Computer Networking", "Warehousing", "Music", "Printing", "Graphic Design", "Sports", "Public Safety", "Libraries", "Animation", "Judiciary", "Wireless", "Individual & Family Services", "Think Tanks", "Higher Education", "Philanthropy", "Government Administration", "Glass, Ceramics & Concrete", "Sporting Goods", "Public Relations & Communications", "Wine & Spirits", "Fine Art", "Investment Banking", "Program Development", "Aviation & Aerospace", "Defense & Space", "Railroad Manufacture", "Paper & Forest Products", "Maritime", "Recreational Facilities & Services", "Alternative Medicine", "Law Practice", "Package/Freight Delivery", "Supermarkets", "Commercial Real Estate", "International Trade & Development", "Government Relations", "Fishery", "Military", "International Affairs", "Dairy", "Mental Health Care", "Shipbuilding", "Political Organization", "Alternative Dispute Resolution", "Law Enforcement", "Public Policy", "Religious Institutions", "Museums & Institutions", "Tobacco", "Mobile Games", "Ranching", "Legislative Office", "Software Development", "IT Services and IT Consulting", "Aviation and Aerospace Component Manufacturing", "Technology, Information and Internet", "Biotechnology Research", "Computer and Network Security", "Defense and Space Manufacturing", "Manufacturing", "Design Services", "Wellness and Fitness Services", "Spectator Sports", "Primary and Secondary Education", "Transportation, Logistics, Supply Chain and Storage", "Food and Beverage Services", "Hospitals and Health Care", "E-Learning Providers", "Computers and Electronics Manufacturing", "Medical Equipment Manufacturing", "Research Services", "Chemical Manufacturing", "Advertising Services", "Oil and Gas", "Individual and Family Services", "Business Consulting and Services", "Staffing and Recruiting", "Truck Transportation", "Non-profit Organizations", "Motor Vehicle Manufacturing", "Entertainment Providers", "Education Administration Programs", "Food and Beverage Manufacturing", "Retail Office Equipment", "Retail Apparel and Fashion", "Semiconductor Manufacturing", "Public Relations and Communications Services", "Medical Practices", "Human Resources Services", "Machinery Manufacturing", "Venture Capital and Private Equity Principals", "Airlines and Aviation", "Computer Networking Products", "Packaging and Containers Manufacturing", "Automation Machinery Manufacturing", "Musicians", "Architecture and Planning", "Mining", "Renewable Energy Semiconductor Manufacturing", "Book and Periodical Publishing", "Professional Training and Coaching", "Industrial Machinery Manufacturing", "Wholesale Import and Export", "Appliances, Electrical, and Electronics Manufacturing", "Broadcast Media Production and Distribution", "Pharmaceutical Manufacturing", "Translation and Localization", "Freight and Package Transportation", "Civic and Social Organizations", "Furniture and Home Furnishings Manufacturing", "Gambling Facilities and Casinos", "Online Audio and Video Media", "Personal Care Product Manufacturing", "Wholesale Building Materials", "Retail Luxury Goods and Jewelry", "Travel Arrangements", "International Trade and Development", "Plastics Manufacturing", "Outsourcing and Offshoring Consulting", "Nanotechnology Research", "Newspaper Publishing", "Artists and Writers", "Security and Investigations", "Paper and Forest Product Manufacturing", "Computer Hardware Manufacturing", "Beverage Manufacturing", "Animation and Post-production", "Leasing Non-residential Real Estate", "Textile Manufacturing", "Movies, Videos, and Sound", "Veterinary Services", "Wireless Services", "Dairy Product Manufacturing", "Executive Offices", "Retail Art Supplies", "Armed Forces", "Sporting Goods Manufacturing", "Printing Services", "Philanthropic Fundraising Services", "Strategic Management Services", "Recreational Facilities", "Writing and Editing", "Government Relations Services", "Mobile Gaming Apps", "Tobacco Manufacturing", "Railroad Equipment Manufacturing", "Glass, Ceramics and Concrete Manufacturing", "Retail Groceries", "Political Organizations", "Warehousing and Storage", "Museums, Historical Sites, and Zoos", "Maritime Transportation", "Public Policy Offices", "Fisheries", "Administration of Justice", "Legislative Offices"]
    ```
    
    Or here is a more readable list
    
    ### Technology
    
    - Information Technology & Services
    - Computer Software
    - Computer Games
    - Computer & Network Security
    - Computer Hardware
    - Computer Networking
    - Computers and Electronics Manufacturing
    - Computer Networking Products
    - Computer Hardware Manufacturing
    - Software Development
    - IT Services and IT Consulting
    - Technology, Information and Internet
    - Animation
    - Mobile Games
    - Mobile Gaming Apps
    - Wireless
    - Wireless Services
    - Internet
    - Online Media
    - Information Services
    - Broadcasting
    - Broadcast Media Production and Distribution
    - Digital Media
    - Online Audio and Video Media
    - Broadcast Media
    - Motion Pictures & Film
    - Animation and Post-production
    
    ### Health and Medical
    
    - Medical Device
    - Hospital & Health Care
    - Health, Wellness & Fitness
    - Pharmaceuticals
    - Medical Practice
    - Medical Equipment Manufacturing
    - Mental Health Care
    - Alternative Medicine
    - Health Tech
    - Biotechnology
    - Biotechnology Research
    - Health and Wellness Services
    - Medical Practices
    
    ### Finance and Investment
    
    - Financial Services
    - Banking
    - Venture Capital & Private Equity
    - Venture Capital and Private Equity Principals
    - Investment Management
    - Investment Banking
    - Capital Markets
    
    ### Marketing and Advertising
    
    - Marketing & Advertising
    - Advertising Services
    - Public Relations & Communications
    - Public Relations and Communications Services
    
    ### Logistics and Transportation
    
    - Logistics & Supply Chain
    - Transportation/Trucking/Railroad
    - Truck Transportation
    - Freight and Package Transportation
    - Airlines/Aviation
    - Airlines and Aviation
    - Package/Freight Delivery
    - Maritime
    - Warehousing
    - Warehousing and Storage
    - Shipping and Logistics
    
    ### Real Estate
    
    - Real Estate
    - Commercial Real Estate
    - Real Estate Investment
    - Leasing Non-residential Real Estate
    - Real Estate Brokerage
    
    ### Manufacturing and Engineering
    
    - Mechanical or Industrial Engineering
    - Electrical & Electronic Manufacturing
    - Industrial Automation
    - Industrial Machinery Manufacturing
    - Machinery
    - Machinery Manufacturing
    - Manufacturing
    - Defense and Space Manufacturing
    - Semiconductor Manufacturing
    - Chemical Manufacturing
    - Appliances, Electrical, and Electronics Manufacturing
    - Plastics Manufacturing
    - Textiles
    - Textile Manufacturing
    - Paper & Forest Products
    - Paper and Forest Product Manufacturing
    - Chemicals
    - Automotive
    - Motor Vehicle Manufacturing
    - Machinery
    - Machinery Manufacturing
    - Industrial Machinery Manufacturing
    - Mining & Metals
    - Mining
    - Mining and Metals
    - Nanotechnology
    - Nanotechnology Research
    - Biotechnology
    - Pharmaceuticals
    - Semiconductor Manufacturing
    - Renewable Energy Semiconductor Manufacturing
    
    ### Consumer Goods and Services
    
    - Consumer Services
    - Consumer Goods
    - Consumer Electronics
    - Consumer Electronics Manufacturing
    - Consumer Applications
    - Apparel & Fashion
    - Retail Apparel and Fashion
    - Food Production
    - Food & Beverages
    - Food and Beverage Manufacturing
    - Food Production and Manufacturing
    - Cosmetics
    - Personal Care Product Manufacturing
    - Luxury Goods & Jewelry
    - Retail Luxury Goods and Jewelry
    - Jewelry
    - Furniture
    - Furniture and Home Furnishings Manufacturing
    - Retail Groceries
    - Supermarkets
    
    ### Professional Services
    
    - Staffing & Recruiting
    - Staffing and Recruiting
    - Legal Services
    - Legal Services and Consulting
    - Management Consulting
    - Business Consulting and Services
    - Professional Training & Coaching
    - Professional Training and Coaching
    - Executive Office
    - Executive Offices
    - Accounting
    - Tax Consulting
    - Market Research
    - Research Services
    - Translation & Localization
    - Translation and Localization Services
    - Outsourcing/Offshoring
    - Outsourcing and Offshoring Consulting
    - Legal Practice
    - Law Practice
    
    ### Education
    
    - E-learning
    - E-Learning Providers
    - Education Management
    - Higher Education
    - Primary/Secondary Education
    - Primary and Secondary Education
    - Education Administration Programs
    
    ### Energy and Environment
    
    - Oil & Energy
    - Oil and Gas
    - Renewables & Environment
    - Renewable Energy Semiconductor Manufacturing
    - Environmental Services
    
    ### Arts and Entertainment
    
    - Arts & Crafts
    - Fine Art
    - Performing Arts
    - Entertainment
    - Music
    - Musicians
    - Gambling & Casinos
    - Gambling Facilities and Casinos
    - Publishing
    - Book and Periodical Publishing
    - Newspapers
    - Newspaper Publishing
    - Writing & Editing
    - Artists and Writers
    
    ### Government and Non-Profit
    
    - Civic & Social Organization
    - Non-profit Organization Management
    - Non-profit Organizations
    - Government Administration
    - Government Relations
    - Government Relations Services
    - Political Organization
    - Political Organizations
    - Public Policy
    - Public Policy Offices
    - Administration of Justice
    - Armed Forces
    - Military
    - Legislative Office
    - Legislative Offices
    
    ### Miscellaneous
    
    - Research
    - Research Services
    - Utilities
    - Facilities Services
    - Photography
    - Graphic Design
    - Printing
    - Printing Services
    - Security & Investigations
    - Security and Investigations
    - Public Safety
    - Individual & Family Services
    - Individual and Family Services
    - Social Services
    - Fishery
    - Fisheries
    - Fundraising
    - Philanthropy
    - Philanthropic Fundraising Services
    - Veterinary
    - Veterinary Services
    - Libraries
    - Museums & Institutions
    - Museums, Historical Sites, and Zoos
    - International Trade & Development
    - International Trade and Development
    - Leisure, Travel & Tourism
    - Travel Arrangements
    - Travel and Tourism
    - Glass, Ceramics & Concrete
    - Glass, Ceramics and Concrete Manufacturing
    - Building Materials
    - Wholesale Building Materials
    - Architectural Services
    - Architecture and Planning
    - Think Tanks
    - Civic and Social Organizations
    - Defense & Space
    - Space and Defense Services
    - Aviation & Aerospace
    - Aviation and Aerospace Component Manufacturing
    - Fundraising Services
    - Strategic Management Services
    - Recreation
    - Recreational Facilities & Services
    - Recreational Facilities
    - Sporting Goods
    - Sporting Goods Manufacturing
    - Spectator Sports
    - Restaurants
    - Food and Beverage Services
    - Hospitality
    - Hotels and Hospitality
    - Event Services
    - Events Services
    - Writing and Editing
    - Journalism
    - Judiciary
    - Legal Services and Consulting
    - Human Resources
    - Human Resources Services
    - Management and Consulting Services
    - Insurance
    - Mental Health Care Services
    - Civic and Social Organizations
    - Charity Organizations
    - Performing Arts