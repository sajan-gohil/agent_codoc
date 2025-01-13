Head to [**Company Dataset API**](https://www.notion.so/Company-Dataset-API-a6c3072d9dd2423bb5dda4a37e2666a6?pvs=21) 

## Dataset API Endpoints

### 1. Job Listings

Crustdata’s company_id is the unique identifier of a company in our database. It is unique and it never changes. It is numeric.

Use this request to get job listings that were last updated by the company on 1st Feb, 2024 for all companies with  `company_id` equal to any one of [680992, 673947, 631280, 636304, 631811]

**Note**:

1. To retrieve all the jobs listings, keep iterating over `offset` field in the payload. 
2. **Do not** increase `limit` beyond 100 as the result will be truncated without any ordering.
3. Real-time Fetch (`sync_from_source`): 
    1. Allows fetching up to 100 jobs in real-time (*use `background_task` if all the jobs needs to be fetched)* 
    2. Works for **1 company** per request
4. Background Task (`background_task`):
    1. Updates job listings for up to **10 companies** at a time in the background
    2. Returns a task ID in the response. Use this task ID to check the status or results via the endpoint `task/result/<task_id>`
5. You need to provide `$auth_token` : Your Crustdata API Key/Auth Token. Reach out to support@crustdata.com through your company email if not available
- **Request Body Overview**
    
    The request body is a JSON object that contains the following parameters:
    
    ### Parameters:
    
    | **Parameter** | **Required** | **Description** |
    | --- | --- | --- |
    | filters | Yes | An object containing the filter conditions. |
    | offset | Yes | The starting point of the result set. Default value is 0. |
    | limit | Yes | The number of results to return in a single request. 
    Maximum value is `100`. 
    Default value is `100`. |
    | sorts | No | An array of sorting criteria. |
    | aggregations | No | [Optional] List of column objects you want to aggregate on with aggregate type |
    | functions | No | [Optional] List of functions you want to apply |
    | groups | No | [Optional] List of group by you want to apply |
    | background_task | No | [Optional] A boolean flag. If `true`, triggers a background task to update jobs for up to 10 companies at a time. Returns a task ID that can be used to fetch results later. |
    | sync_from_source | No  | [Optional] A boolean flag. If `true`, fetches up to 100 jobs in real-time. Requires a filter on `company_id` and only allows one `company_id` in the filter. |
    - **`filters`**
        
        Example: 
        
        ```json
        {
            "op": "and",
            "conditions": [
        		    {
        				    "op": "or",
        				    "conditions": [
        							   {"largest_headcount_country", "type": "(.)", "value": "USA"},
        							   {"largest_headcount_country", "type": "(.)", "value": "IND"}
        						],
        				}
                {"column": "title", "type": "in", "value": [ "Sales Development Representative", "SDR", "Business Development Representative", "BDR", "Business Development Manager", "Account Development Representative", "ADR", "Account Development Manager", "Outbound Sales Representative", "Lead Generation Specialist", "Market Development Representative", "MDR", "Inside Sales Representative", "ISR", "Territory Development Representative", "Pipeline Development Representative", "New Business Development Representative", "Customer Acquisition Specialist" ]},
                {"column": "description", "type": "(.)", "value": "Sales Development Representative"}
            ]
        }
        ```
        
        The filters object contains the following parameters:
        
        | **Parameter** | **Description** | **Required** |
        | --- | --- | --- |
        | op | The operator to apply on the conditions. The value can be `"and"` or `"or"`. | Yes |
        | conditions | An array of complex filter objects or basic filter objects (see below) | Yes |
    - **`conditions` parameter**
        
        This has two possible types of values
        
        1. **Basic Filter Object**
            
            Example: `{"column": "crunchbase_total_investment_usd", "type": "=>", "value": "50" }` 
            
            The object contains the following parameters:
            
            | **Parameter** | **Description** | **Required** |
            | --- | --- | --- |
            | column | The name of the column to filter. | Yes |
            | type | The filter type. The value can be "=>", "=<", "=", "!=", “in”, “(.)”, “[.]” | Yes |
            | value | The filter value. | Yes |
            | allow_null | Whether to allow null values. The value can be "true" or "false". Default value is "false". | No |
            - List of all `column` values
                - linkedin_id
                - company_website
                - fiscal_year_end
                - company_name
                - markets
                - company_website_domain
                - largest_headcount_country
                - crunchbase_total_investment_usd
                - acquisition_status
                - crunchbase_valuation_usd
                - crunchbase_valuation_lower_bound_usd
                - crunchbase_valuation_date
                - crunchbase_profile_url
                - title
                - category
                - url
                - domain
                - number_of_openings
                - description
                - date_added
                - date_updated
                - city
                - location_text
                - workplace_type
                - reposted_job
                - dataset_row_id
                - pin_area_name
                - pincode
                - district
                - district_geocode
                - wikidata_id
                - state
                - state_geocode
                - country
                - country_code
                - company_id
            - List of all `type` values
                
                
                | condition type | condition description | applicable column types | example |
                | --- | --- | --- | --- |
                | "=>" | Greater than or equal | number | { "column": "crunchbase_total_investment_usd", "type": "=>", "value": "500000"} |
                | "=<" | Lesser than or equal | number | { "column": "crunchbase_total_investment_usd", "type": "=<", "value": "50"} |
                | "=", | Equal | number | { "column": "crunchbase_total_investment_usd", "type": "=", "value": "50"} |
                | “<” | Lesser than | number | { "column": "crunchbase_total_investment_usd", "type": "<", "value": "50"} |
                | “>” | Greater than | number | { "column": "crunchbase_total_investment_usd", "type": ">", "value": "50"} |
                | “(.)” | Contains, case insensitive | string | { "column": "title", "type": "(.)", "value": "artificial intelligence"} |
                | “[.]” | Contains, case sensitive | string | { "column": "title", "type": "[.]", "value": "Artificial Intelligence"} |
                | "!=" | Not equals | number |  |
                | “in” | Exactly matches atleast one of the elements of list | string, number | { "column": "company_id", "type": "in", "value": [123, 346. 564]} |
        2. **Complex Filter Object**
            
            Example: 
            
            ```json
            {
            	 "op": "or",
            	 "conditions": [
            			 {"largest_headcount_country", "type": "(.)", "value": "USA"},
            			 {"largest_headcount_country", "type": "(.)", "value": "IND"}
            	 ]
            }
            ```
            
            Same schema as the parent [**`filters`**](https://www.notion.so/filters-8a72acfe02a5455e895ea9a9dede08c4?pvs=21) parameter 
            
- **Curl**
    
    ```bash
    curl --request POST \
      --url https://api.crustdata.com/data_lab/job_listings/Table/ \
      --header 'Accept: application/json, text/plain, */*' \
      --header 'Accept-Language: en-US,en;q=0.9' \
      --header 'Authorization: Token $token' \
      --header 'Content-Type: application/json' \
      --header 'Origin: https://crustdata.com' \
      --header 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36' \
      --data '{
        "tickers": [],
        "dataset": {
          "name": "job_listings",
          "id": "joblisting"
        },
        "filters": {
          "op": "and",
          "conditions": [
            {"column": "company_id", "type": "in", "value": [7576, 680992, 673947, 631280, 636304, 631811]},
            {"column": "date_updated", "type": ">", "value": "2024-02-01"}
          ]
        },
        "groups": [],
        "aggregations": [],
        "functions": [],
        "offset": 0,
        "limit": 100,
        "sorts": []
      }'
    ```
    
- **Python**
    
    ```python
    import requests
    import json
    
    url = "https://api.crustdata.com/data_lab/job_listings/Table/"
    
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.9",
        "Authorization": "Token $token",
        "Content-Type": "application/json",
        "Origin": "https://crustdata.com",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
    }
    
    data = {
        "tickers": [],
        "dataset": {
            "name": "job_listings",
            "id": "joblisting"
        },
        "filters": {
            "op": "and",
            "conditions": [
                        {"column": "company_id", "type": "in", "value": [7576, 680992, 673947, 631280, 636304, 631811]},
    				            {"column": "date_updated", "type": ">", "value": "2024-02-01"}
            ]
        },
        "groups": [],
        "aggregations": [],
        "functions": [],
        "offset": 0,
        "limit": 100,
        "sorts": []
    }
    
    response = requests.post(url, headers=headers, data=json.dumps(data))
    
    print(response.json())
    ```
    
- **Example requests**
    1. Get all job listings that 
        - from a list of company domains AND
        - posted after a specific data AND
        - have specific keywords in title
    
    ```bash
    curl --location 'https://api.crustdata.com/data_lab/job_listings/Table/' \
    --header 'Accept: application/json, text/plain, */*' \
    --header 'Authorization: Token $token' \
    --header 'Content-Type: application/json' \
    --data '{
        "tickers": [],
        "dataset": {
          "name": "job_listings",
          "id": "joblisting"
        },
        "filters": {
          "op": "and",
          "conditions": [
            {"column": "company_website_domain", "type": "(.)", "value": "ziphq.com"},
            {"column": "date_updated", "type": ">", "value": "2024-08-01"},
    		    {
    				    "op": "or",
    				    "conditions": [
    							   {"column": "title", "type": "(.)", "value": "Sales Development Representative"},
    							   {"column": "title", "type": "(.)", "value": "SDR"},
    							   {"column": "title", "type": "(.)", "value": "Business Development Representative"}
    						],
    				}       
          ]
        },
        "offset": 0,
        "limit": 100,
        "sorts": [],
      }'
    ```
    
    1. Get real time job listings from the source for company Rippling
        
        ```bash
        curl --location 'https://api.crustdata.com/data_lab/job_listings/Table/' \
        --header 'Accept: application/json, text/plain, */*' \
        --header 'Authorization: Token $token' \
        --header 'Content-Type: application/json' \
        --data '{
            "tickers": [],
            "dataset": {
              "name": "job_listings",
              "id": "joblisting"
            },
            "filters": {
              "op": "and",
              "conditions": [
        	        {"column": "company_id", "type": "in", "value": [634043]},      ]
            },
            "offset": 0,
            "limit": 100,
            "sorts": [],
            "sync_from_source": true
          }'
        ```
        
    2. Fetch job listings for list of company ids from the source in the background
        
          **Request:**
        
        ```bash
        curl --location 'https://api.crustdata.com/data_lab/job_listings/Table/' \
        --header 'Accept: application/json, text/plain, */*' \
        --header 'Authorization: Token $token' \
        --header 'Content-Type: application/json' \
        --data '{
            "tickers": [],
            "dataset": {
              "name": "job_listings",
              "id": "joblisting"
            },
            "filters": {
              "op": "and",
              "conditions": [
        	        {"column": "company_id", "type": "in", "value": [631394, 7576, 680992, 673947, 631280, 636304, 631811]},
              ]
            },
            "offset": 0,
            "limit": 10000,
            "sorts": [],
            "backgrond_task": true
          }'
        ```
        
        - Response would be
            
            ```bash
            {
                "task_id": "3d729bd0-a113-4b31-b09f-65eff79f06fe",
                "task_type": "job_listings",
                "status": "not_started",
                "completed_task_result_endpoint": "/task/result/3d729bd0-a113-4b31-b09f-65eff79f06fe/",
                "created_at": "2024-12-25T02:32:42.811843Z",
                "started_at": null
            }
            ```
            
    3. Get all job listings that are
        - from a list of Crustdata company_ids AND
        - posted after a specific data AND
        - exactly has one of the given titles
    
    ```bash
    curl --location 'https://api.crustdata.com/data_lab/job_listings/Table/' \
    --header 'Accept: application/json, text/plain, */*' \
    --header 'Authorization: Token $token' \
    --header 'Content-Type: application/json' \
    --data '{
        "tickers": [],
        "dataset": {
          "name": "job_listings",
          "id": "joblisting"
        },
        "filters": {
          "op": "and",
          "conditions": [
    	        {"column": "company_id", "type": "in", "value": [631394, 7576, 680992, 673947, 631280, 636304, 631811]},
            {"column": "date_updated", "type": ">", "value": "2024-08-01"},
            {
            "column": "title",
            "type": "in",
            "value": [
              "Sales Development Representative",
              "SDR",
              "Business Development Representative",
              "BDR",
              "Business Development Manager",
              "Account Development Representative",
              "ADR",
              "Account Development Manager",
              "Outbound Sales Representative",
              "Lead Generation Specialist",
              "Market Development Representative",
              "MDR",
              "Inside Sales Representative",
              "ISR",
              "Territory Development Representative",
              "Pipeline Development Representative",
              "New Business Development Representative",
              "Customer Acquisition Specialist"
            ]
          }
          ]
        },
        "offset": 0,
        "count": 100,
        "sorts": []
      }'
    ```
    
    1. **Get count of job listing meeting a criteria**
        
        You can set `"count": 1` . The last value of the first (and the only) row would be the total count of jobs meeting the criteria
        
        ```bash
        curl --location 'https://api.crustdata.com/data_lab/job_listings/Table/' \
        --header 'Accept: application/json, text/plain, */*' \
        --header 'Accept-Language: en-US,en;q=0.9' \
        --header 'Authorization: Token $token' \
        --header 'Content-Type: application/json' \
        --header 'Origin: https://crustdata.com' \
        --data '{
            "tickers": [],
            "dataset": {
              "name": "job_listings",
              "id": "joblisting"
            },
            "filters": {
              "op": "and",
              "conditions": [
                {"column": "company_id", "type": "in", "value": [631394]},
                {
                    "column": "title",
                    "type": "in",
                    "value": [
                    "Sales Development Representative",
                    "SDR",
                    "Business Development Representative",
                    "BDR",
                    "Business Development Manager",
                    "Account Development Representative",
                    "ADR",
                    "Account Development Manager",
                    "Outbound Sales Representative",
                    "Lead Generation Specialist",
                    "Market Development Representative",
                    "MDR",
                    "Inside Sales Representative",
                    "ISR",
                    "Territory Development Representative",
                    "Pipeline Development Representative",
                    "New Business Development Representative",
                    "Customer Acquisition Specialist"
                    ]
                }
              ]
            },
            "offset": 0,
            "count": 1,
            "sorts": []
          }'
        ```
        
        - Response would be
            
            ```bash
            {
                "fields": [
                    {
                        "type": "string",
                        "api_name": "linkedin_id",
                        "hidden": true,
                        "options": [],
                        "summary": "",
                        "local_metric": false,
                        "display_name": "",
                        "company_profile_name": "",
                        "preview_description": "",
                        "geocode": false
                    },
                    {
                        "type": "string",
                        "api_name": "company_website",
                        "hidden": false,
                        "options": [],
                        "summary": "",
                        "local_metric": false,
                        "display_name": "",
                        "company_profile_name": "",
                        "preview_description": "",
                        "geocode": false
                    },
            				...
                    {
                        "type": "number",
                        "api_name": "total_rows",
                        "hidden": true,
                        "options": [],
                        "summary": "",
                        "local_metric": false,
                        "display_name": "",
                        "company_profile_name": "",
                        "preview_description": "",
                        "geocode": false
                    }
                ],
                "rows": [
                    [
                        "2135371",
                        "https://stripe.com",
                        null,
                        "Stripe",
                        "stripe",
                        "PRIVATE",
                        "stripe.com",
                        "USA",
                        9440247725,
                        null,
                        50000000000,
                        10000000000,
                        "2023-03-15",
                        "https://crunchbase.com/organization/stripe",
                        "Sales Development Representative",
                        "Sales",
                        "https://www.linkedin.com/jobs/view/3877324263",
                        "www.linkedin.com",
                        1,
                        "Who we are\n\nAbout Stripe\n\nStripe is a financial infrastructure platform for businesses. Millions of companies—from the world’s largest enterprises to the most ambitious startups—use Stripe to accept payments, grow their revenue, and accelerate new business opportunities. Our mission is to increase the GDP of the internet, and we have a staggering amount of work ahead. That means you have an unprecedented opportunity to put the global economy within everyone’s reach while doing the most important work of your career.\n\nAbout The Team\n\nAs a Sales Development Representative (SDR) at Stripe, you will drive Stripe’s future growth engine by working with Demand Gen and the Account Executive team to qualify leads and collaboratively build Stripe’s sales pipeline. You get excited about engaging with prospects to better qualify needs. You are adept at identifying high value opportunities and capable of managing early sales funnel activities.You are used to delivering value in complex situations and are energized by learning about new and existing products. Finally, you enjoy building – you like to actively participate in the development of the demand generation and sales process, the articulation of Stripe’s value proposition, and the creation of key tools and assets. If you’re hungry, smart, persistent, and a great teammate, we want to hear from you!\n\nFor the first months, you’ll be part of the SD Associate program which is designed to accelerate your onboarding and ramp to full productivity as an SDR. This intensive program is built to help you quickly build and develop skills required to be successful in this role. Upon completion, you’ll continue learning and growing in your career as part of Stripe’s Sales Development Academy. These programs are endorsed and supported by sales leaders as an important part of investing in our people.\n\nWe take a data driven, analytical approach to sales development, and are looking for someone who is confident in both prospecting to customers and in helping design our strategy. If you’re hungry, smart, persistent, and a great teammate, we want to hear from you!\n\nWhat you’ll do\n\nResponsibilities\n\nResearch and create outreach materials for high value prospects, in partnership with SDRs and AEsFollow up with Marketing generated leads to qualify as sales opportunities. Move solid leads through the funnel connecting them to a salesperson, and arranging meetingsExecute outbound sales plays created by marketingInitiate contact with potential customers through cold-calling or responding to inquiries generated from MarketingDevelop relationships with prospects to uncover needs through effective questioning to qualify interest and viability to prepare hand-off to salesFollow-up with potential customers who expressed interest but did not initially result in a sales opportunityEffectively work through lead list meeting/exceeding SLAs, consistently update activity and contact information within the CRM system and support weekly reporting effortsCollaborate and provide feedback and insights to Marketing to help improve targeting and messaging\n\n\nWho you are\n\nWe’re looking for someone who meets the minimum requirements to be considered for the role. If you meet these requirements, you are encouraged to apply.\n\nMinimum Requirements\n\nA track record of top performance or prior successSuperior verbal and written communication skillsSelf starter who is able to operate in a hyper growth environmentThis role requires in-office participation three (3) days per week in our Chicago office \n\n\nPreferred Qualifications\n\nProfessional experience\n\n\nHybrid work at Stripe\n\nOffice-assigned Stripes spend at least 50% of the time in a given month in their local office or with users. This hits a balance between bringing people together for in-person collaboration and learning from each other, while supporting flexibility about how to do this in a way that makes sense for individuals and their teams.\n\nPay and benefits\n\nThe annual US base salary range for this role is $65,600 - $98,300. For sales roles, the range provided is the role’s On Target Earnings (\"OTE\") range, meaning that the range includes both the sales commissions/sales bonuses target and annual base salary for the role. This salary range may be inclusive of several career levels at Stripe and will be narrowed during the interview process based on a number of factors, including the candidate’s experience, qualifications, and location. Applicants interested in this role and who are not located in the US may request the annual salary range for their location during the interview process.\n\nAdditional benefits for this role may include: equity, company bonus or sales commissions/bonuses; 401(k) plan; medical, dental, and vision benefits; and wellness stipends.",
                        "2024-03-29T22:35:22Z",
                        "2024-12-05T00:00:00Z",
                        "chicago",
                        "Chicago, Illinois, United States",
                        "On-site",
                        "True",
                        13385453,
                        null,
                        null,
                        null,
                        null,
                        null,
                        null,
                        null,
                        "United States of America (the)",
                        "USA",
                        "840",
                        631394,
                        3
                    ]
                ]
            }
            ```
            
        
        And total count of results matching the search query would be:  `response[rows][0][-1]`  (`-1` refers to last item of the row), which would be 3 in the case above
        
- **Response**
    
    https://jsonhero.io/j/3ZQ16TON5oUV
    
    [JSON Hero](https://jsonhero.io/j/gTebm3gqR4em/tree)
    
    **Parsing the response**
    
    The response format is same as that of Company Discovery: Screening API.
    
    You refer here on how to parse the response [**Parsing the response**](https://www.notion.so/Parsing-the-response-28de6e16940c4615b5872020a345766a?pvs=21) 
    

### 2. Funding Milestones

Use this request to get a time-series of funding milestones with  `company_id` equal to any one of [637158, 674265, 674657]

- **Curl**
    
    ```bash
    curl --request POST \
      --url https://api.crustdata.com/data_lab/funding_milestone_timeseries/ \
      --header 'Accept: application/json, text/plain, */*' \
      --header 'Accept-Language: en-US,en;q=0.9' \
      --header 'Authorization: Token $auth_token' \
      --header 'Content-Type: application/json' \
      --header 'Origin: https://crustdata.com' \
      --header 'Referer: https://crustdata.com/' \
      --data '{"filters":{"op": "or", "conditions": [{"column": "company_id", "type": "in", "value": [637158,674265,674657]}]},"offset":0,"count":1000,"sorts":[]}'
    ```
    
- **Python**
    
    ```python
    import requests
    import json
    
    url = "https://api.crustdata.com/data_lab/funding_milestone_timeseries/"
    
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Authorization': f'Token {auth_token}',  # Ensure the auth_token variable is defined
        'Content-Type': 'application/json',
        'Origin': 'https://crustdata.com',
        'Referer': 'https://crustdata.com/',
    }
    
    data = {
        "filters": {
            "op": "or",
            "conditions": [
                {
                    "column": "company_id",
                    "type": "in",
                    "value": [637158, 674265, 674657]
                }
            ]
        },
        "offset": 0,
        "count": 1000,
        "sorts": []
    }
    
    response = requests.post(url, headers=headers, data=json.dumps(data))
    
    # Print the response content
    print(response.text)
    ```
    
- **Response**
    
    https://jsonhero.io/j/XDfprlYDbOvf 
    

### 3. Decision Makers/People Info

- All decision makers: for a given `company_id=632328`
    
    Decision makers include the people with following titles
    
    - Included decision maker titles
        
        ### Founders
        
        - CEO
        - Founder
        - Co-founder
        - Co founder
        - Cofounder
        - Co-fondateur
        - Fondateur
        - Cofondateur
        - Cofondatrice
        - Co-fondatrice
        - Fondatrice
        
        ### Executive Officers
        
        - Chief Executive Officer
        - Chief Technical Officer
        - Chief Technology Officer
        - Chief Financial Officer
        - Chief Marketing Officer
        - Chief Sales Officer
        - Chief Marketing and Digital Officer
        - Chief Market Officer
        
        ### Technical Leadership
        
        - CTO
        - VP Engineering
        - VP of Engineering
        - Vice President Engineering
        - Vice President of Engineering
        - Head Engineering
        - Head of Engineering
        
        ### Marketing Leadership
        
        - CMO
        - Chief Marketing Officer
        - Chief Marketing and Digital Officer
        - Chief Market Officer
        - VP Marketing
        - VP of Marketing
        - Vice President Marketing
        - Vice President of Marketing
        
        ### Sales Leadership
        
        - Chief Sales Officer
        - VP Sales
        - VP of Sales
        - Vice President Sales
        - Vice President of Sales
        - Vice President (Sales & Pre-Sales)
        - Head Sales
        - Head of Sales
        
        ### Product Leadership
        
        - VP Product
        - VP of Product
        - Vice President Product
        - Vice President of Product
        - Head of Product
        - Head Product
        
        ### Software Leadership
        
        - VP Software
        - VP of Software
        - Vice President Software
        - Vice President of Software
        
        ### Financial Leadership
        
        - CFO
        - Chief Financial Officer
    - **Curl**
        
        ```bash
        curl --request POST \
              --url https://api.crustdata.com/data_lab/decision_makers/ \
              --header 'Accept: application/json, text/plain, */*' \
              --header 'Accept-Language: en-US,en;q=0.9' \
              --header 'Authorization: Token $auth_token' \
              --header 'Content-Type: application/json' \
              --header 'Origin: http://localhost:3000' \
              --header 'Referer: http://localhost:3000/' \
              --data '{"filters":{"op": "and", "conditions": [{"column": "company_id", "type": "in", "value": [632328]}] },"offset":0,"count":100,"sorts":[]}'
        ```
        
    - **Python**
        
        ```python
        import requests
        import json
        
        url = "https://api.crustdata.com/data_lab/decision_makers/"
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Authorization': 'Token $auth_token',  # Replace with your actual token
            'Content-Type': 'application/json',
            'Origin': 'http://localhost:3000',
            'Referer': 'http://localhost:3000/'
        }
        
        data = {
            "filters": {
                "op": "or",
                "conditions": [
                    {"column": "company_id", "type": "in", "value": [632328]}
                ]
            },
            "offset": 0,
            "count": 100,
            "sorts": []
        }
        
        response = requests.post(url, headers=headers, data=json.dumps(data))
        print(response.text)
        ```
        
- Decision makers with specific titles: for a given `company_id=632328`
    
    For example, get all decision makers “vice president” and “chief” in their title
    
    - **Curl**
        
        ```bash
        curl --request POST \
          --url https://api.crustdata.com/data_lab/decision_makers/ \
          --header 'Accept: application/json, text/plain, */*' \
          --header 'Accept-Language: en-US,en;q=0.9' \
          --header 'Authorization: Token $auth_token' \
          --data '{
            "filters": {
              "op": "or",
              "conditions": [
                {
                  "column": "company_id",
                  "type": "in",
                  "value": [632328]
                },
                {
                  "column": "title",
                  "type": "in",
                  "value": ["vice president", "chief"]
                }
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
        
        url = "https://api.crustdata.com/data_lab/decision_makers/"
        
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.9",
            "Authorization": "Token YOUR_AUTH_TOKEN"
        }
        
        payload = {
            "filters": {
                "op": "or",
                "conditions": [
                    {
                        "column": "company_id",
                        "type": "in",
                        "value": [632328]
                    },
                    {
                        "column": "title",
                        "type": "in",
                        "value": ["vice president", "chief"]
                    }
                ]
            },
            "offset": 0,
            "count": 100,
            "sorts": []
        }
        
        response = requests.post(url, headers=headers, json=payload)
        
        # Print the response status and data
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        ```
        
- People profiles by their LinkedIn’s “flagship_url”
    
    For example, decision makers with LinkedIn profile url as "https://www.linkedin.com/in/alikashani"
    
    - **Curl**
        
        ```bash
        curl --request POST \
              --url https://api.crustdata.com/data_lab/decision_makers/ \
              --header 'Accept: application/json, text/plain, */*' \
              --header 'Accept-Language: en-US,en;q=0.9' \
              --header 'Authorization: Token $auth_token' \
              --header 'Content-Type: application/json' \
              --data '{"filters":{"op": "and", "conditions": [{"column": "linkedin_flagship_profile_url", "type": "in", "value": ["https://www.linkedin.com/in/alikashani"]}] },"offset":0,"count":100,"sorts":[]}'
        ```
        
    - **Python**
        
        ```python
        import requests
        import json
        
        url = "https://api.crustdata.com/data_lab/decision_makers/"
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Authorization': 'Token $auth_token',  # Replace with your actual token
            'Content-Type': 'application/json',
            'Origin': 'http://localhost:3000',
            'Referer': 'http://localhost:3000/'
        }
        
        data = {
            "filters": {
                "op": "or",
                "conditions": [
                    {"column": "linkedin_flagship_profile_url", "type": "in", "value": ["https://www.linkedin.com/in/alikashani"]}
                ]
            },
            "offset": 0,
            "count": 100,
            "sorts": []
        }
        
        response = requests.post(url, headers=headers, data=json.dumps(data))
        print(response.text)
        ```
        
- People profiles by their “linkedin_urn”
    
    For example, decision makers with `linkedin_urn` as "ACwAAAVhcDEBbTdJtuc-KHsdYfPU1JAdBmHkh8I" . `linkedin_urn` is a 30-40 character alphanumeric sequence that includes both uppercase letters and numbers
    
    - **Curl**
        
        ```bash
        curl --request POST \
              --url https://api.crustdata.com/data_lab/decision_makers/ \
              --header 'Accept: application/json, text/plain, */*' \
              --header 'Accept-Language: en-US,en;q=0.9' \
              --header 'Authorization: Token $auth_token' \
              --header 'Content-Type: application/json' \
              --header 'Origin: http://localhost:3000' \
              --header 'Referer: http://localhost:3000/' \
              --data '{"filters":{"op": "or", "conditions": [{"column": "linkedin_profile_urn", "type": "in", "value": ["ACwAAAVhcDEBbTdJtuc-KHsdYfPU1JAdBmHkh8I"]}] },"offset":0,"count":100,"sorts":[]}'
        ```
        
    - **Python**
        
        ```python
        import requests
        import json
        
        url = "https://api.crustdata.com/data_lab/decision_makers/"
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Authorization': 'Token $auth_token',  # Replace with your actual token
            'Content-Type': 'application/json',
            'Origin': 'http://localhost:3000',
            'Referer': 'http://localhost:3000/'
        }
        
        data = {
            "filters": {
                "op": "or",
                "conditions": [
                    {"column": "linkedin_profile_urn", "type": "in", "value": ["ACwAAAVhcDEBbTdJtuc-KHsdYfPU1JAdBmHkh8I"]}
                ]
            },
            "offset": 0,
            "count": 100,
            "sorts": []
        }
        
        response = requests.post(url, headers=headers, data=json.dumps(data))
        print(response.text)
        ```
        

- **Response**
    
    https://jsonhero.io/j/QSAlhbuflhie
    

### 4. LinkedIn Employee Headcount and LinkedIn Follower Count

Use this request to get weekly and monthly timeseries of employee headcount as a JSON blob.

You either provide with list a list of Crustdata `company_id`  or `linkedin_id` or `company_website_domain`

In the following example, we request the employee headcount timeseries of companies with  `company_id` equal to any one of [680992, 673947, 631280, 636304, 631811]

- **CUrl**
    
    ```bash
    curl 'https://api.crustdata.com/data_lab/headcount_timeseries/' \
      -H 'Accept: application/json, text/plain, */*' \
      -H 'Accept-Language: en-US,en;q=0.9' \
      -H 'Authorization: Token $auth_token' \
      -H 'Content-Type: application/json' \
      -H 'Origin: https://crustdata.com' \
      -H 'Referer: https://crustdata.com' \
      --data-raw '{
        "filters": {
            "op": "or",
            "conditions": [
                        {
                            "column": "company_id",
                            "type": "=",
                            "value": 634995
                        },
                        {
                            "column": "company_id",
                            "type": "=",
                            "value": 680992
                        },
                        {
                            "column": "company_id",
                            "type": "=",
                            "value": 673947
                        },
                        {
                            "column": "company_id",
                            "type": "=",
                            "value": 631811
                        }
            ]
        },
        "offset": 0,
        "count": 100,
        "sorts": []
    }' \
      --compressed
    ```
    
- **Python**
    
    ```python
    import requests
    
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Authorization': 'Token $auth_token',
        'Content-Type': 'application/json',
        'Origin': 'https://crustdata.com',
        'Referer': 'https://crustdata.com',
    }
    
    json_data = {
        'filters': {
            'op': 'and',
            'conditions': [
                {
                    'op': 'or',
                    'conditions': [
                        {
                            'column': 'company_id',
                            'type': '=',
                            'value': 634995,
                        },
                        {
                            'column': 'company_id',
                            'type': '=',
                            'value': 680992,
                        },
                        {
                            'column': 'company_id',
                            'type': '=',
                            'value': 673947,
                        },
                        {
                            'column': 'company_id',
                            'type': '=',
                            'value': 631811,
                        },
                    ],
                },
            ],
        },
        'offset': 0,
        'count': 100,
        'sorts': [],
    }
    
    response = requests.post('https://api.crustdata.com/data_lab/headcount_timeseries/', headers=headers, json=json_data)
    ```
    
- **Response**
    
    [JSON Hero](https://jsonhero.io/j/bd2OKMSu8ZQ0/editor)
    
    ```json
    {
      "fields": [
        {
          "type": "foreign_key",
          "api_name": "company_id",
          "hidden": false,
          "options": [],
          "summary": "",
          "local_metric": false,
          "display_name": "",
          "company_profile_name": "",
          "geocode": false
        },
        {
          "type": "string",
          "api_name": "company_website",
          "hidden": false,
          "options": [],
          "summary": "",
          "local_metric": false,
          "display_name": "",
          "company_profile_name": "",
          "geocode": false
        },
        {
          "type": "string",
          "api_name": "linkedin_id",
          "hidden": false,
          "options": [],
          "summary": "",
          "local_metric": false,
          "display_name": "",
          "company_profile_name": "",
          "geocode": false
        },
        {
          "type": "string",
          "api_name": "company_website_domain",
          "hidden": false,
          "options": [],
          "summary": "",
          "local_metric": false,
          "display_name": "",
          "company_profile_name": "",
          "geocode": false
        },
        {
          "type": "array",
          "api_name": "headcount_timeseries",
          "hidden": false,
          "options": [],
          "summary": "",
          "local_metric": false,
          "display_name": "",
          "company_profile_name": "",
          "geocode": false
        },
        {
          "type": "number",
          "api_name": "total_rows",
          "hidden": true,
          "options": [],
          "summary": "",
          "local_metric": false,
          "display_name": "",
          "company_profile_name": "",
          "geocode": false
        }
      ],
      "rows": [
        [
          631280,
          "https://www.lacework.com",
          "17932068",
          "lacework.com",
          [
            {
              "date": "2021-08-01T00:00:00+00:00",
              "employee_count": 643,
              "follower_count": null
            },
            {
              "date": "2021-08-02T00:00:00+00:00",
              "employee_count": 643,
              "follower_count": null
            },
            {
              "date": "2021-08-09T00:00:00+00:00",
              "employee_count": 643,
              "follower_count": null
            },
            {
              "date": "2021-08-16T00:00:00+00:00",
              "employee_count": 643,
              "follower_count": null
            },
            {
              "date": "2021-08-23T00:00:00+00:00",
              "employee_count": 643,
              "follower_count": null
            },
            {
              "date": "2021-08-30T00:00:00+00:00",
              "employee_count": 643,
              "follower_count": null
            },
            {
              "date": "2021-09-01T00:00:00+00:00",
              "employee_count": 687,
              "follower_count": null
            },
            {
              "date": "2021-09-06T00:00:00+00:00",
              "employee_count": 687,
              "follower_count": null
            },
            {
              "date": "2021-09-13T00:00:00+00:00",
              "employee_count": 687,
              "follower_count": null
            },
            {
              "date": "2021-09-20T00:00:00+00:00",
              "employee_count": 687,
              "follower_count": null
            },
            {
              "date": "2021-09-27T00:00:00+00:00",
              "employee_count": 687,
              "follower_count": null
            },
            {
              "date": "2021-10-01T00:00:00+00:00",
              "employee_count": 737,
              "follower_count": null
            },
            {
              "date": "2021-10-04T00:00:00+00:00",
              "employee_count": 737,
              "follower_count": null
            },
            {
              "date": "2021-10-11T00:00:00+00:00",
              "employee_count": 737,
              "follower_count": null
            },
            {
              "date": "2021-10-18T00:00:00+00:00",
              "employee_count": 737,
              "follower_count": null
            },
            {
              "date": "2021-10-25T00:00:00+00:00",
              "employee_count": 737,
              "follower_count": null
            },
            {
              "date": "2021-11-01T00:00:00+00:00",
              "employee_count": 805,
              "follower_count": null
            },
            {
              "date": "2021-11-08T00:00:00+00:00",
              "employee_count": 805,
              "follower_count": null
            },
            {
              "date": "2021-11-15T00:00:00+00:00",
              "employee_count": 805,
              "follower_count": null
            },
            {
              "date": "2021-11-22T00:00:00+00:00",
              "employee_count": 805,
              "follower_count": null
            },
            {
              "date": "2021-11-29T00:00:00+00:00",
              "employee_count": 805,
              "follower_count": null
            },
            {
              "date": "2021-12-01T00:00:00+00:00",
              "employee_count": 853,
              "follower_count": null
            },
            {
              "date": "2021-12-06T00:00:00+00:00",
              "employee_count": 853,
              "follower_count": null
            },
            {
              "date": "2021-12-13T00:00:00+00:00",
              "employee_count": 853,
              "follower_count": null
            },
            {
              "date": "2021-12-20T00:00:00+00:00",
              "employee_count": 853,
              "follower_count": null
            },
            {
              "date": "2021-12-27T00:00:00+00:00",
              "employee_count": 853,
              "follower_count": null
            },
            {
              "date": "2022-01-01T00:00:00+00:00",
              "employee_count": 919,
              "follower_count": null
            },
            {
              "date": "2022-01-03T00:00:00+00:00",
              "employee_count": 919,
              "follower_count": null
            },
            {
              "date": "2022-01-10T00:00:00+00:00",
              "employee_count": 919,
              "follower_count": null
            },
            {
              "date": "2022-01-17T00:00:00+00:00",
              "employee_count": 919,
              "follower_count": null
            },
            {
              "date": "2022-01-24T00:00:00+00:00",
              "employee_count": 919,
              "follower_count": null
            },
            {
              "date": "2022-01-31T00:00:00+00:00",
              "employee_count": 919,
              "follower_count": null
            },
            {
              "date": "2022-02-01T00:00:00+00:00",
              "employee_count": 996,
              "follower_count": null
            },
            {
              "date": "2022-02-07T00:00:00+00:00",
              "employee_count": 996,
              "follower_count": null
            },
            {
              "date": "2022-02-14T00:00:00+00:00",
              "employee_count": 996,
              "follower_count": null
            },
            {
              "date": "2022-02-21T00:00:00+00:00",
              "employee_count": 996,
              "follower_count": null
            },
            {
              "date": "2022-02-28T00:00:00+00:00",
              "employee_count": 996,
              "follower_count": null
            },
            {
              "date": "2022-03-01T00:00:00+00:00",
              "employee_count": 1069,
              "follower_count": null
            },
            {
              "date": "2022-03-07T00:00:00+00:00",
              "employee_count": 1069,
              "follower_count": null
            },
            {
              "date": "2022-03-14T00:00:00+00:00",
              "employee_count": 1069,
              "follower_count": null
            },
            {
              "date": "2022-03-21T00:00:00+00:00",
              "employee_count": 1069,
              "follower_count": null
            },
            {
              "date": "2022-03-28T00:00:00+00:00",
              "employee_count": 1069,
              "follower_count": null
            },
            {
              "date": "2022-04-01T00:00:00+00:00",
              "employee_count": 1121,
              "follower_count": null
            },
            {
              "date": "2022-04-04T00:00:00+00:00",
              "employee_count": 1121,
              "follower_count": null
            },
            {
              "date": "2022-04-11T00:00:00+00:00",
              "employee_count": 1121,
              "follower_count": null
            },
            {
              "date": "2022-04-18T00:00:00+00:00",
              "employee_count": 1121,
              "follower_count": null
            },
            {
              "date": "2022-04-25T00:00:00+00:00",
              "employee_count": 1121,
              "follower_count": null
            },
            {
              "date": "2022-05-01T00:00:00+00:00",
              "employee_count": 1160,
              "follower_count": null
            },
            {
              "date": "2022-05-02T00:00:00+00:00",
              "employee_count": 1160,
              "follower_count": null
            },
            {
              "date": "2022-05-09T00:00:00+00:00",
              "employee_count": 1160,
              "follower_count": null
            },
            {
              "date": "2022-05-16T00:00:00+00:00",
              "employee_count": 1160,
              "follower_count": null
            },
            {
              "date": "2022-05-23T00:00:00+00:00",
              "employee_count": 1160,
              "follower_count": null
            },
            {
              "date": "2022-05-30T00:00:00+00:00",
              "employee_count": 1160,
              "follower_count": null
            },
            {
              "date": "2022-06-01T00:00:00+00:00",
              "employee_count": 1085,
              "follower_count": null
            },
            {
              "date": "2022-06-06T00:00:00+00:00",
              "employee_count": 1085,
              "follower_count": null
            },
            {
              "date": "2022-06-13T00:00:00+00:00",
              "employee_count": 1085,
              "follower_count": null
            },
            {
              "date": "2022-06-20T00:00:00+00:00",
              "employee_count": 1085,
              "follower_count": null
            },
            {
              "date": "2022-06-27T00:00:00+00:00",
              "employee_count": 1085,
              "follower_count": null
            },
            {
              "date": "2022-07-01T00:00:00+00:00",
              "employee_count": 1053,
              "follower_count": null
            },
            {
              "date": "2022-07-04T00:00:00+00:00",
              "employee_count": 1053,
              "follower_count": null
            },
            {
              "date": "2022-07-11T00:00:00+00:00",
              "employee_count": 1053,
              "follower_count": null
            },
            {
              "date": "2022-07-18T00:00:00+00:00",
              "employee_count": 1053,
              "follower_count": null
            },
            {
              "date": "2022-07-25T00:00:00+00:00",
              "employee_count": 1053,
              "follower_count": null
            },
            {
              "date": "2022-08-01T00:00:00+00:00",
              "employee_count": 1008,
              "follower_count": null
            },
            {
              "date": "2022-08-08T00:00:00+00:00",
              "employee_count": 1008,
              "follower_count": null
            },
            {
              "date": "2022-08-15T00:00:00+00:00",
              "employee_count": 1008,
              "follower_count": null
            },
            {
              "date": "2022-08-22T00:00:00+00:00",
              "employee_count": 1008,
              "follower_count": null
            },
            {
              "date": "2022-08-29T00:00:00+00:00",
              "employee_count": 1008,
              "follower_count": null
            },
            {
              "date": "2022-09-01T00:00:00+00:00",
              "employee_count": 994,
              "follower_count": null
            },
            {
              "date": "2022-09-05T00:00:00+00:00",
              "employee_count": 994,
              "follower_count": null
            },
            {
              "date": "2022-09-12T00:00:00+00:00",
              "employee_count": 994,
              "follower_count": null
            },
            {
              "date": "2022-09-19T00:00:00+00:00",
              "employee_count": 994,
              "follower_count": null
            },
            {
              "date": "2022-09-26T00:00:00+00:00",
              "employee_count": 994,
              "follower_count": null
            },
            {
              "date": "2022-10-01T00:00:00+00:00",
              "employee_count": 993,
              "follower_count": null
            },
            {
              "date": "2022-10-03T00:00:00+00:00",
              "employee_count": 993,
              "follower_count": null
            },
            {
              "date": "2022-10-10T00:00:00+00:00",
              "employee_count": 993,
              "follower_count": null
            },
            {
              "date": "2022-10-17T00:00:00+00:00",
              "employee_count": 993,
              "follower_count": null
            },
            {
              "date": "2022-10-24T00:00:00+00:00",
              "employee_count": 993,
              "follower_count": null
            },
            {
              "date": "2022-10-31T00:00:00+00:00",
              "employee_count": 993,
              "follower_count": null
            },
            {
              "date": "2022-11-01T00:00:00+00:00",
              "employee_count": 977,
              "follower_count": null
            },
            {
              "date": "2022-11-07T00:00:00+00:00",
              "employee_count": 977,
              "follower_count": null
            },
            {
              "date": "2022-11-14T00:00:00+00:00",
              "employee_count": 977,
              "follower_count": null
            },
            {
              "date": "2022-11-21T00:00:00+00:00",
              "employee_count": 977,
              "follower_count": null
            },
            {
              "date": "2022-11-28T00:00:00+00:00",
              "employee_count": 977,
              "follower_count": null
            },
            {
              "date": "2022-12-01T00:00:00+00:00",
              "employee_count": 968,
              "follower_count": null
            },
            {
              "date": "2022-12-05T00:00:00+00:00",
              "employee_count": 968,
              "follower_count": null
            },
            {
              "date": "2022-12-12T00:00:00+00:00",
              "employee_count": 968,
              "follower_count": null
            },
            {
              "date": "2022-12-19T00:00:00+00:00",
              "employee_count": 968,
              "follower_count": null
            },
            {
              "date": "2022-12-26T00:00:00+00:00",
              "employee_count": 968,
              "follower_count": null
            },
            {
              "date": "2023-01-01T00:00:00+00:00",
              "employee_count": 975,
              "follower_count": null
            },
            {
              "date": "2023-01-02T00:00:00+00:00",
              "employee_count": 975,
              "follower_count": null
            },
            {
              "date": "2023-01-09T00:00:00+00:00",
              "employee_count": 975,
              "follower_count": null
            },
            {
              "date": "2023-01-16T00:00:00+00:00",
              "employee_count": 975,
              "follower_count": null
            },
            {
              "date": "2023-01-23T00:00:00+00:00",
              "employee_count": 975,
              "follower_count": null
            },
            {
              "date": "2023-01-30T00:00:00+00:00",
              "employee_count": 975,
              "follower_count": null
            },
            {
              "date": "2023-02-01T00:00:00+00:00",
              "employee_count": 979,
              "follower_count": null
            },
            {
              "date": "2023-02-06T00:00:00+00:00",
              "employee_count": 979,
              "follower_count": null
            },
            {
              "date": "2023-02-13T00:00:00+00:00",
              "employee_count": 979,
              "follower_count": null
            },
            {
              "date": "2023-02-20T00:00:00+00:00",
              "employee_count": 979,
              "follower_count": null
            },
            {
              "date": "2023-02-27T00:00:00+00:00",
              "employee_count": 979,
              "follower_count": null
            },
            {
              "date": "2023-03-01T00:00:00+00:00",
              "employee_count": 987,
              "follower_count": null
            },
            {
              "date": "2023-03-06T00:00:00+00:00",
              "employee_count": 987,
              "follower_count": null
            },
            {
              "date": "2023-03-13T00:00:00+00:00",
              "employee_count": 987,
              "follower_count": null
            },
            {
              "date": "2023-03-20T00:00:00+00:00",
              "employee_count": 987,
              "follower_count": null
            },
            {
              "date": "2023-03-27T00:00:00+00:00",
              "employee_count": 987,
              "follower_count": null
            },
            {
              "date": "2023-04-01T00:00:00+00:00",
              "employee_count": 988,
              "follower_count": null
            },
            {
              "date": "2023-04-03T00:00:00+00:00",
              "employee_count": 988,
              "follower_count": null
            },
            {
              "date": "2023-04-10T00:00:00+00:00",
              "employee_count": 988,
              "follower_count": null
            },
            {
              "date": "2023-04-17T00:00:00+00:00",
              "employee_count": 988,
              "follower_count": null
            },
            {
              "date": "2023-04-24T00:00:00+00:00",
              "employee_count": 988,
              "follower_count": null
            },
            {
              "date": "2023-05-01T00:00:00+00:00",
              "employee_count": 1027,
              "follower_count": null
            },
            {
              "date": "2023-05-08T00:00:00+00:00",
              "employee_count": 1027,
              "follower_count": null
            },
            {
              "date": "2023-05-15T00:00:00+00:00",
              "employee_count": 1027,
              "follower_count": null
            },
            {
              "date": "2023-05-22T00:00:00+00:00",
              "employee_count": 1027,
              "follower_count": null
            },
            {
              "date": "2023-05-29T00:00:00+00:00",
              "employee_count": 1027,
              "follower_count": null
            },
            {
              "date": "2023-06-01T00:00:00+00:00",
              "employee_count": 1009,
              "follower_count": null
            },
            {
              "date": "2023-06-05T00:00:00+00:00",
              "employee_count": 1009,
              "follower_count": null
            },
            {
              "date": "2023-06-12T00:00:00+00:00",
              "employee_count": 1009,
              "follower_count": null
            },
            {
              "date": "2023-06-19T00:00:00+00:00",
              "employee_count": 1009,
              "follower_count": null
            },
            {
              "date": "2023-06-26T00:00:00+00:00",
              "employee_count": 1009,
              "follower_count": null
            },
            {
              "date": "2023-07-01T00:00:00+00:00",
              "employee_count": 989,
              "follower_count": null
            },
            {
              "date": "2023-07-03T00:00:00+00:00",
              "employee_count": 989,
              "follower_count": null
            },
            {
              "date": "2023-07-10T00:00:00+00:00",
              "employee_count": 1009,
              "follower_count": 37367
            },
            {
              "date": "2023-07-17T00:00:00+00:00",
              "employee_count": 1005,
              "follower_count": null
            },
            {
              "date": "2023-07-24T00:00:00+00:00",
              "employee_count": 1005,
              "follower_count": 37680
            },
            {
              "date": "2023-07-31T00:00:00+00:00",
              "employee_count": 1005,
              "follower_count": 37680
            },
            {
              "date": "2023-08-01T00:00:00+00:00",
              "employee_count": 994,
              "follower_count": 38148
            },
            {
              "date": "2023-08-07T00:00:00+00:00",
              "employee_count": 983,
              "follower_count": 38303
            },
            {
              "date": "2023-08-14T00:00:00+00:00",
              "employee_count": 973,
              "follower_count": 38583
            },
            {
              "date": "2023-08-21T00:00:00+00:00",
              "employee_count": 966,
              "follower_count": 38780
            },
            {
              "date": "2023-08-28T00:00:00+00:00",
              "employee_count": 956,
              "follower_count": 39043
            },
            {
              "date": "2023-09-01T00:00:00+00:00",
              "employee_count": 955,
              "follower_count": 39072
            },
            {
              "date": "2023-09-04T00:00:00+00:00",
              "employee_count": 955,
              "follower_count": 39072
            },
            {
              "date": "2023-09-11T00:00:00+00:00",
              "employee_count": 946,
              "follower_count": 39307
            },
            {
              "date": "2023-09-18T00:00:00+00:00",
              "employee_count": 939,
              "follower_count": 39543
            },
            {
              "date": "2023-09-25T00:00:00+00:00",
              "employee_count": 939,
              "follower_count": 39543
            },
            {
              "date": "2023-10-01T00:00:00+00:00",
              "employee_count": 905,
              "follower_count": 40190
            },
            {
              "date": "2023-10-02T00:00:00+00:00",
              "employee_count": 905,
              "follower_count": 40190
            },
            {
              "date": "2023-10-09T00:00:00+00:00",
              "employee_count": 905,
              "follower_count": 40385
            },
            {
              "date": "2023-10-16T00:00:00+00:00",
              "employee_count": 894,
              "follower_count": 40732
            },
            {
              "date": "2023-10-23T00:00:00+00:00",
              "employee_count": 878,
              "follower_count": 41285
            },
            {
              "date": "2023-10-30T00:00:00+00:00",
              "employee_count": 878,
              "follower_count": 41507
            },
            {
              "date": "2023-11-01T00:00:00+00:00",
              "employee_count": 878,
              "follower_count": 41616
            },
            {
              "date": "2023-11-06T00:00:00+00:00",
              "employee_count": 863,
              "follower_count": 41025
            },
            {
              "date": "2023-11-13T00:00:00+00:00",
              "employee_count": 854,
              "follower_count": 41048
            },
            {
              "date": "2023-11-20T00:00:00+00:00",
              "employee_count": 845,
              "follower_count": 41259
            },
            {
              "date": "2023-11-27T00:00:00+00:00",
              "employee_count": 843,
              "follower_count": 43498
            },
            {
              "date": "2023-12-01T00:00:00+00:00",
              "employee_count": 843,
              "follower_count": 43498
            },
            {
              "date": "2023-12-04T00:00:00+00:00",
              "employee_count": 832,
              "follower_count": 43685
            },
            {
              "date": "2023-12-11T00:00:00+00:00",
              "employee_count": 829,
              "follower_count": 43805
            },
            {
              "date": "2023-12-18T00:00:00+00:00",
              "employee_count": 826,
              "follower_count": 44118
            },
            {
              "date": "2023-12-25T00:00:00+00:00",
              "employee_count": 826,
              "follower_count": 46066
            },
            {
              "date": "2024-01-01T00:00:00+00:00",
              "employee_count": 823,
              "follower_count": 47044
            },
            {
              "date": "2024-01-08T00:00:00+00:00",
              "employee_count": 818,
              "follower_count": 47582
            },
            {
              "date": "2024-01-15T00:00:00+00:00",
              "employee_count": 811,
              "follower_count": 47646
            },
            {
              "date": "2024-01-22T00:00:00+00:00",
              "employee_count": 808,
              "follower_count": 47917
            },
            {
              "date": "2024-01-29T00:00:00+00:00",
              "employee_count": 804,
              "follower_count": 48116
            },
            {
              "date": "2024-02-01T00:00:00+00:00",
              "employee_count": 799,
              "follower_count": 49145
            },
            {
              "date": "2024-02-05T00:00:00+00:00",
              "employee_count": 799,
              "follower_count": 49145
            },
            {
              "date": "2024-02-12T00:00:00+00:00",
              "employee_count": 791,
              "follower_count": 50425
            },
            {
              "date": "2024-02-19T00:00:00+00:00",
              "employee_count": 778,
              "follower_count": 50568
            },
            {
              "date": "2024-02-26T00:00:00+00:00",
              "employee_count": 770,
              "follower_count": 50849
            },
            {
              "date": "2024-03-01T00:00:00+00:00",
              "employee_count": 769,
              "follower_count": 50972
            }
          ],
          5
        ],
        [
          631811,
          "http://jumpcloud.com",
          "3033823",
          "jumpcloud.com",
          [
            {
              "date": "2021-08-01T00:00:00+00:00",
              "employee_count": 390,
              "follower_count": null
            },
            {
              "date": "2021-08-02T00:00:00+00:00",
              "employee_count": 390,
              "follower_count": null
            },
            {
              "date": "2021-08-09T00:00:00+00:00",
              "employee_count": 390,
              "follower_count": null
            },
            {
              "date": "2021-08-16T00:00:00+00:00",
              "employee_count": 390,
              "follower_count": null
            },
            {
              "date": "2021-08-23T00:00:00+00:00",
              "employee_count": 390,
              "follower_count": null
            },
            {
              "date": "2021-08-30T00:00:00+00:00",
              "employee_count": 390,
              "follower_count": null
            },
            {
              "date": "2021-09-01T00:00:00+00:00",
              "employee_count": 409,
              "follower_count": null
            },
            {
              "date": "2021-09-06T00:00:00+00:00",
              "employee_count": 409,
              "follower_count": null
            },
            {
              "date": "2021-09-13T00:00:00+00:00",
              "employee_count": 409,
              "follower_count": null
            },
            {
              "date": "2021-09-20T00:00:00+00:00",
              "employee_count": 409,
              "follower_count": null
            },
            {
              "date": "2021-09-27T00:00:00+00:00",
              "employee_count": 409,
              "follower_count": null
            },
            {
              "date": "2021-10-01T00:00:00+00:00",
              "employee_count": 420,
              "follower_count": null
            },
            {
              "date": "2021-10-04T00:00:00+00:00",
              "employee_count": 420,
              "follower_count": null
            },
            {
              "date": "2021-10-11T00:00:00+00:00",
              "employee_count": 420,
              "follower_count": null
            },
            {
              "date": "2021-10-18T00:00:00+00:00",
              "employee_count": 420,
              "follower_count": null
            },
            {
              "date": "2021-10-25T00:00:00+00:00",
              "employee_count": 420,
              "follower_count": null
            },
            {
              "date": "2021-11-01T00:00:00+00:00",
              "employee_count": 477,
              "follower_count": null
            },
            {
              "date": "2021-11-08T00:00:00+00:00",
              "employee_count": 477,
              "follower_count": null
            },
            {
              "date": "2021-11-15T00:00:00+00:00",
              "employee_count": 477,
              "follower_count": null
            },
            {
              "date": "2021-11-22T00:00:00+00:00",
              "employee_count": 477,
              "follower_count": null
            },
            {
              "date": "2021-11-29T00:00:00+00:00",
              "employee_count": 477,
              "follower_count": null
            },
            {
              "date": "2021-12-01T00:00:00+00:00",
              "employee_count": 487,
              "follower_count": null
            },
            {
              "date": "2021-12-06T00:00:00+00:00",
              "employee_count": 487,
              "follower_count": null
            },
            {
              "date": "2021-12-13T00:00:00+00:00",
              "employee_count": 487,
              "follower_count": null
            },
            {
              "date": "2021-12-20T00:00:00+00:00",
              "employee_count": 487,
              "follower_count": null
            },
            {
              "date": "2021-12-27T00:00:00+00:00",
              "employee_count": 487,
              "follower_count": null
            },
            {
              "date": "2022-01-01T00:00:00+00:00",
              "employee_count": 538,
              "follower_count": null
            },
            {
              "date": "2022-01-03T00:00:00+00:00",
              "employee_count": 538,
              "follower_count": null
            },
            {
              "date": "2022-01-10T00:00:00+00:00",
              "employee_count": 538,
              "follower_count": null
            },
            {
              "date": "2022-01-17T00:00:00+00:00",
              "employee_count": 538,
              "follower_count": null
            },
            {
              "date": "2022-01-24T00:00:00+00:00",
              "employee_count": 538,
              "follower_count": null
            },
            {
              "date": "2022-01-31T00:00:00+00:00",
              "employee_count": 538,
              "follower_count": null
            },
            {
              "date": "2022-02-01T00:00:00+00:00",
              "employee_count": 569,
              "follower_count": null
            },
            {
              "date": "2022-02-07T00:00:00+00:00",
              "employee_count": 569,
              "follower_count": null
            },
            {
              "date": "2022-02-14T00:00:00+00:00",
              "employee_count": 569,
              "follower_count": null
            },
            {
              "date": "2022-02-21T00:00:00+00:00",
              "employee_count": 569,
              "follower_count": null
            },
            {
              "date": "2022-02-28T00:00:00+00:00",
              "employee_count": 569,
              "follower_count": null
            },
            {
              "date": "2022-03-01T00:00:00+00:00",
              "employee_count": 600,
              "follower_count": null
            },
            {
              "date": "2022-03-07T00:00:00+00:00",
              "employee_count": 600,
              "follower_count": null
            },
            {
              "date": "2022-03-14T00:00:00+00:00",
              "employee_count": 600,
              "follower_count": null
            },
            {
              "date": "2022-03-21T00:00:00+00:00",
              "employee_count": 600,
              "follower_count": null
            },
            {
              "date": "2022-03-28T00:00:00+00:00",
              "employee_count": 600,
              "follower_count": null
            },
            {
              "date": "2022-04-01T00:00:00+00:00",
              "employee_count": 614,
              "follower_count": null
            },
            {
              "date": "2022-04-04T00:00:00+00:00",
              "employee_count": 614,
              "follower_count": null
            },
            {
              "date": "2022-04-11T00:00:00+00:00",
              "employee_count": 614,
              "follower_count": null
            },
            {
              "date": "2022-04-18T00:00:00+00:00",
              "employee_count": 614,
              "follower_count": null
            },
            {
              "date": "2022-04-25T00:00:00+00:00",
              "employee_count": 614,
              "follower_count": null
            },
            {
              "date": "2022-05-01T00:00:00+00:00",
              "employee_count": 631,
              "follower_count": null
            },
            {
              "date": "2022-05-02T00:00:00+00:00",
              "employee_count": 631,
              "follower_count": null
            },
            {
              "date": "2022-05-09T00:00:00+00:00",
              "employee_count": 631,
              "follower_count": null
            },
            {
              "date": "2022-05-16T00:00:00+00:00",
              "employee_count": 631,
              "follower_count": null
            },
            {
              "date": "2022-05-23T00:00:00+00:00",
              "employee_count": 631,
              "follower_count": null
            },
            {
              "date": "2022-05-30T00:00:00+00:00",
              "employee_count": 631,
              "follower_count": null
            },
            {
              "date": "2022-06-01T00:00:00+00:00",
              "employee_count": 641,
              "follower_count": null
            },
            {
              "date": "2022-06-06T00:00:00+00:00",
              "employee_count": 641,
              "follower_count": null
            },
            {
              "date": "2022-06-13T00:00:00+00:00",
              "employee_count": 641,
              "follower_count": null
            },
            {
              "date": "2022-06-20T00:00:00+00:00",
              "employee_count": 641,
              "follower_count": null
            },
            {
              "date": "2022-06-27T00:00:00+00:00",
              "employee_count": 641,
              "follower_count": null
            },
            {
              "date": "2022-07-01T00:00:00+00:00",
              "employee_count": 659,
              "follower_count": null
            },
            {
              "date": "2022-07-04T00:00:00+00:00",
              "employee_count": 659,
              "follower_count": null
            },
            {
              "date": "2022-07-11T00:00:00+00:00",
              "employee_count": 659,
              "follower_count": null
            },
            {
              "date": "2022-07-18T00:00:00+00:00",
              "employee_count": 659,
              "follower_count": null
            },
            {
              "date": "2022-07-25T00:00:00+00:00",
              "employee_count": 659,
              "follower_count": null
            },
            {
              "date": "2022-08-01T00:00:00+00:00",
              "employee_count": 656,
              "follower_count": null
            },
            {
              "date": "2022-08-08T00:00:00+00:00",
              "employee_count": 656,
              "follower_count": null
            },
            {
              "date": "2022-08-15T00:00:00+00:00",
              "employee_count": 656,
              "follower_count": null
            },
            {
              "date": "2022-08-22T00:00:00+00:00",
              "employee_count": 656,
              "follower_count": null
            },
            {
              "date": "2022-08-29T00:00:00+00:00",
              "employee_count": 656,
              "follower_count": null
            },
            {
              "date": "2022-09-01T00:00:00+00:00",
              "employee_count": 654,
              "follower_count": null
            },
            {
              "date": "2022-09-05T00:00:00+00:00",
              "employee_count": 654,
              "follower_count": null
            },
            {
              "date": "2022-09-12T00:00:00+00:00",
              "employee_count": 654,
              "follower_count": null
            },
            {
              "date": "2022-09-19T00:00:00+00:00",
              "employee_count": 654,
              "follower_count": null
            },
            {
              "date": "2022-09-26T00:00:00+00:00",
              "employee_count": 654,
              "follower_count": null
            },
            {
              "date": "2022-10-01T00:00:00+00:00",
              "employee_count": 657,
              "follower_count": null
            },
            {
              "date": "2022-10-03T00:00:00+00:00",
              "employee_count": 657,
              "follower_count": null
            },
            {
              "date": "2022-10-10T00:00:00+00:00",
              "employee_count": 657,
              "follower_count": null
            },
            {
              "date": "2022-10-17T00:00:00+00:00",
              "employee_count": 657,
              "follower_count": null
            },
            {
              "date": "2022-10-24T00:00:00+00:00",
              "employee_count": 657,
              "follower_count": null
            },
            {
              "date": "2022-10-31T00:00:00+00:00",
              "employee_count": 657,
              "follower_count": null
            },
            {
              "date": "2022-11-01T00:00:00+00:00",
              "employee_count": 669,
              "follower_count": null
            },
            {
              "date": "2022-11-07T00:00:00+00:00",
              "employee_count": 669,
              "follower_count": null
            },
            {
              "date": "2022-11-14T00:00:00+00:00",
              "employee_count": 669,
              "follower_count": null
            },
            {
              "date": "2022-11-21T00:00:00+00:00",
              "employee_count": 669,
              "follower_count": null
            },
            {
              "date": "2022-11-28T00:00:00+00:00",
              "employee_count": 669,
              "follower_count": null
            },
            {
              "date": "2022-12-01T00:00:00+00:00",
              "employee_count": 672,
              "follower_count": null
            },
            {
              "date": "2022-12-05T00:00:00+00:00",
              "employee_count": 672,
              "follower_count": null
            },
            {
              "date": "2022-12-12T00:00:00+00:00",
              "employee_count": 672,
              "follower_count": null
            },
            {
              "date": "2022-12-19T00:00:00+00:00",
              "employee_count": 672,
              "follower_count": null
            },
            {
              "date": "2022-12-26T00:00:00+00:00",
              "employee_count": 672,
              "follower_count": null
            },
            {
              "date": "2023-01-01T00:00:00+00:00",
              "employee_count": 620,
              "follower_count": null
            },
            {
              "date": "2023-01-02T00:00:00+00:00",
              "employee_count": 620,
              "follower_count": null
            },
            {
              "date": "2023-01-09T00:00:00+00:00",
              "employee_count": 620,
              "follower_count": null
            },
            {
              "date": "2023-01-16T00:00:00+00:00",
              "employee_count": 620,
              "follower_count": null
            },
            {
              "date": "2023-01-23T00:00:00+00:00",
              "employee_count": 620,
              "follower_count": null
            },
            {
              "date": "2023-01-30T00:00:00+00:00",
              "employee_count": 620,
              "follower_count": null
            },
            {
              "date": "2023-02-01T00:00:00+00:00",
              "employee_count": 626,
              "follower_count": null
            },
            {
              "date": "2023-02-06T00:00:00+00:00",
              "employee_count": 626,
              "follower_count": null
            },
            {
              "date": "2023-02-13T00:00:00+00:00",
              "employee_count": 626,
              "follower_count": null
            },
            {
              "date": "2023-02-20T00:00:00+00:00",
              "employee_count": 626,
              "follower_count": null
            },
            {
              "date": "2023-02-27T00:00:00+00:00",
              "employee_count": 626,
              "follower_count": null
            },
            {
              "date": "2023-03-01T00:00:00+00:00",
              "employee_count": 638,
              "follower_count": null
            },
            {
              "date": "2023-03-06T00:00:00+00:00",
              "employee_count": 638,
              "follower_count": null
            },
            {
              "date": "2023-03-13T00:00:00+00:00",
              "employee_count": 638,
              "follower_count": null
            },
            {
              "date": "2023-03-20T00:00:00+00:00",
              "employee_count": 638,
              "follower_count": null
            },
            {
              "date": "2023-03-27T00:00:00+00:00",
              "employee_count": 638,
              "follower_count": null
            },
            {
              "date": "2023-04-01T00:00:00+00:00",
              "employee_count": 648,
              "follower_count": null
            },
            {
              "date": "2023-04-03T00:00:00+00:00",
              "employee_count": 648,
              "follower_count": null
            },
            {
              "date": "2023-04-10T00:00:00+00:00",
              "employee_count": 648,
              "follower_count": null
            },
            {
              "date": "2023-04-17T00:00:00+00:00",
              "employee_count": 648,
              "follower_count": null
            },
            {
              "date": "2023-04-24T00:00:00+00:00",
              "employee_count": 648,
              "follower_count": null
            },
            {
              "date": "2023-05-01T00:00:00+00:00",
              "employee_count": 656,
              "follower_count": null
            },
            {
              "date": "2023-05-08T00:00:00+00:00",
              "employee_count": 656,
              "follower_count": null
            },
            {
              "date": "2023-05-15T00:00:00+00:00",
              "employee_count": 656,
              "follower_count": null
            },
            {
              "date": "2023-05-22T00:00:00+00:00",
              "employee_count": 656,
              "follower_count": null
            },
            {
              "date": "2023-05-29T00:00:00+00:00",
              "employee_count": 656,
              "follower_count": null
            },
            {
              "date": "2023-06-01T00:00:00+00:00",
              "employee_count": 663,
              "follower_count": null
            },
            {
              "date": "2023-06-05T00:00:00+00:00",
              "employee_count": 663,
              "follower_count": null
            },
            {
              "date": "2023-06-12T00:00:00+00:00",
              "employee_count": 663,
              "follower_count": null
            },
            {
              "date": "2023-06-19T00:00:00+00:00",
              "employee_count": 663,
              "follower_count": null
            },
            {
              "date": "2023-06-26T00:00:00+00:00",
              "employee_count": 663,
              "follower_count": null
            },
            {
              "date": "2023-07-01T00:00:00+00:00",
              "employee_count": 672,
              "follower_count": null
            },
            {
              "date": "2023-07-03T00:00:00+00:00",
              "employee_count": 672,
              "follower_count": null
            },
            {
              "date": "2023-07-10T00:00:00+00:00",
              "employee_count": 665,
              "follower_count": 23350
            },
            {
              "date": "2023-07-17T00:00:00+00:00",
              "employee_count": 665,
              "follower_count": 23457
            },
            {
              "date": "2023-07-24T00:00:00+00:00",
              "employee_count": 666,
              "follower_count": 23543
            },
            {
              "date": "2023-07-31T00:00:00+00:00",
              "employee_count": 666,
              "follower_count": 23543
            },
            {
              "date": "2023-08-01T00:00:00+00:00",
              "employee_count": 670,
              "follower_count": 24043
            },
            {
              "date": "2023-08-07T00:00:00+00:00",
              "employee_count": 671,
              "follower_count": 24424
            },
            {
              "date": "2023-08-14T00:00:00+00:00",
              "employee_count": 672,
              "follower_count": 24717
            },
            {
              "date": "2023-08-21T00:00:00+00:00",
              "employee_count": 669,
              "follower_count": 24888
            },
            {
              "date": "2023-08-28T00:00:00+00:00",
              "employee_count": 671,
              "follower_count": 25203
            },
            {
              "date": "2023-09-01T00:00:00+00:00",
              "employee_count": 671,
              "follower_count": 25276
            },
            {
              "date": "2023-09-04T00:00:00+00:00",
              "employee_count": 671,
              "follower_count": 25276
            },
            {
              "date": "2023-09-11T00:00:00+00:00",
              "employee_count": 673,
              "follower_count": 25428
            },
            {
              "date": "2023-09-18T00:00:00+00:00",
              "employee_count": 676,
              "follower_count": 25563
            },
            {
              "date": "2023-09-25T00:00:00+00:00",
              "employee_count": 676,
              "follower_count": 25563
            },
            {
              "date": "2023-10-01T00:00:00+00:00",
              "employee_count": 684,
              "follower_count": 25827
            },
            {
              "date": "2023-10-02T00:00:00+00:00",
              "employee_count": 684,
              "follower_count": 25827
            },
            {
              "date": "2023-10-09T00:00:00+00:00",
              "employee_count": 684,
              "follower_count": 25957
            },
            {
              "date": "2023-10-16T00:00:00+00:00",
              "employee_count": 687,
              "follower_count": 26155
            },
            {
              "date": "2023-10-23T00:00:00+00:00",
              "employee_count": 690,
              "follower_count": 26264
            },
            {
              "date": "2023-10-30T00:00:00+00:00",
              "employee_count": 690,
              "follower_count": 26378
            },
            {
              "date": "2023-11-01T00:00:00+00:00",
              "employee_count": 690,
              "follower_count": 26495
            },
            {
              "date": "2023-11-06T00:00:00+00:00",
              "employee_count": 700,
              "follower_count": 26509
            },
            {
              "date": "2023-11-13T00:00:00+00:00",
              "employee_count": 700,
              "follower_count": 26616
            },
            {
              "date": "2023-11-20T00:00:00+00:00",
              "employee_count": 700,
              "follower_count": 26690
            },
            {
              "date": "2023-11-27T00:00:00+00:00",
              "employee_count": 696,
              "follower_count": 26769
            },
            {
              "date": "2023-12-01T00:00:00+00:00",
              "employee_count": 697,
              "follower_count": 26420
            },
            {
              "date": "2023-12-04T00:00:00+00:00",
              "employee_count": 697,
              "follower_count": 26469
            },
            {
              "date": "2023-12-11T00:00:00+00:00",
              "employee_count": 701,
              "follower_count": 26584
            },
            {
              "date": "2023-12-18T00:00:00+00:00",
              "employee_count": 700,
              "follower_count": 28131
            },
            {
              "date": "2023-12-25T00:00:00+00:00",
              "employee_count": 699,
              "follower_count": 28430
            },
            {
              "date": "2024-01-01T00:00:00+00:00",
              "employee_count": 697,
              "follower_count": 28743
            },
            {
              "date": "2024-01-08T00:00:00+00:00",
              "employee_count": 699,
              "follower_count": 29264
            },
            {
              "date": "2024-01-15T00:00:00+00:00",
              "employee_count": 693,
              "follower_count": 29661
            },
            {
              "date": "2024-01-22T00:00:00+00:00",
              "employee_count": 695,
              "follower_count": 29836
            },
            {
              "date": "2024-01-29T00:00:00+00:00",
              "employee_count": 697,
              "follower_count": 29966
            },
            {
              "date": "2024-02-01T00:00:00+00:00",
              "employee_count": 697,
              "follower_count": 30080
            },
            {
              "date": "2024-02-05T00:00:00+00:00",
              "employee_count": 697,
              "follower_count": 30080
            },
            {
              "date": "2024-02-12T00:00:00+00:00",
              "employee_count": 700,
              "follower_count": 30409
            },
            {
              "date": "2024-02-19T00:00:00+00:00",
              "employee_count": 703,
              "follower_count": 30516
            },
            {
              "date": "2024-02-26T00:00:00+00:00",
              "employee_count": 701,
              "follower_count": 30763
            }
          ],
          5
        ],
        [
          636304,
          "http://www.nowsecure.com",
          "336243",
          "nowsecure.com",
          [
            {
              "date": "2021-10-01T00:00:00+00:00",
              "employee_count": 124,
              "follower_count": null
            },
            {
              "date": "2021-10-04T00:00:00+00:00",
              "employee_count": 124,
              "follower_count": null
            },
            {
              "date": "2021-10-11T00:00:00+00:00",
              "employee_count": 124,
              "follower_count": null
            },
            {
              "date": "2021-10-18T00:00:00+00:00",
              "employee_count": 124,
              "follower_count": null
            },
            {
              "date": "2021-10-25T00:00:00+00:00",
              "employee_count": 124,
              "follower_count": null
            },
            {
              "date": "2021-11-01T00:00:00+00:00",
              "employee_count": 134,
              "follower_count": null
            },
            {
              "date": "2021-11-08T00:00:00+00:00",
              "employee_count": 134,
              "follower_count": null
            },
            {
              "date": "2021-11-15T00:00:00+00:00",
              "employee_count": 134,
              "follower_count": null
            },
            {
              "date": "2021-11-22T00:00:00+00:00",
              "employee_count": 134,
              "follower_count": null
            },
            {
              "date": "2021-11-29T00:00:00+00:00",
              "employee_count": 134,
              "follower_count": null
            },
            {
              "date": "2021-12-01T00:00:00+00:00",
              "employee_count": 141,
              "follower_count": null
            },
            {
              "date": "2021-12-06T00:00:00+00:00",
              "employee_count": 141,
              "follower_count": null
            },
            {
              "date": "2021-12-13T00:00:00+00:00",
              "employee_count": 141,
              "follower_count": null
            },
            {
              "date": "2021-12-20T00:00:00+00:00",
              "employee_count": 141,
              "follower_count": null
            },
            {
              "date": "2021-12-27T00:00:00+00:00",
              "employee_count": 141,
              "follower_count": null
            },
            {
              "date": "2022-01-01T00:00:00+00:00",
              "employee_count": 144,
              "follower_count": null
            },
            {
              "date": "2022-01-03T00:00:00+00:00",
              "employee_count": 144,
              "follower_count": null
            },
            {
              "date": "2022-01-10T00:00:00+00:00",
              "employee_count": 144,
              "follower_count": null
            },
            {
              "date": "2022-01-17T00:00:00+00:00",
              "employee_count": 144,
              "follower_count": null
            },
            {
              "date": "2022-01-24T00:00:00+00:00",
              "employee_count": 144,
              "follower_count": null
            },
            {
              "date": "2022-01-31T00:00:00+00:00",
              "employee_count": 144,
              "follower_count": null
            },
            {
              "date": "2022-02-01T00:00:00+00:00",
              "employee_count": 143,
              "follower_count": null
            },
            {
              "date": "2022-02-07T00:00:00+00:00",
              "employee_count": 143,
              "follower_count": null
            },
            {
              "date": "2022-02-14T00:00:00+00:00",
              "employee_count": 143,
              "follower_count": null
            },
            {
              "date": "2022-02-21T00:00:00+00:00",
              "employee_count": 143,
              "follower_count": null
            },
            {
              "date": "2022-02-28T00:00:00+00:00",
              "employee_count": 143,
              "follower_count": null
            },
            {
              "date": "2022-03-01T00:00:00+00:00",
              "employee_count": 147,
              "follower_count": null
            },
            {
              "date": "2022-03-07T00:00:00+00:00",
              "employee_count": 147,
              "follower_count": null
            },
            {
              "date": "2022-03-14T00:00:00+00:00",
              "employee_count": 147,
              "follower_count": null
            },
            {
              "date": "2022-03-21T00:00:00+00:00",
              "employee_count": 147,
              "follower_count": null
            },
            {
              "date": "2022-03-28T00:00:00+00:00",
              "employee_count": 147,
              "follower_count": null
            },
            {
              "date": "2022-04-01T00:00:00+00:00",
              "employee_count": 147,
              "follower_count": null
            },
            {
              "date": "2022-04-04T00:00:00+00:00",
              "employee_count": 147,
              "follower_count": null
            },
            {
              "date": "2022-04-11T00:00:00+00:00",
              "employee_count": 147,
              "follower_count": null
            },
            {
              "date": "2022-04-18T00:00:00+00:00",
              "employee_count": 147,
              "follower_count": null
            },
            {
              "date": "2022-04-25T00:00:00+00:00",
              "employee_count": 147,
              "follower_count": null
            },
            {
              "date": "2022-05-01T00:00:00+00:00",
              "employee_count": 152,
              "follower_count": null
            },
            {
              "date": "2022-05-02T00:00:00+00:00",
              "employee_count": 152,
              "follower_count": null
            },
            {
              "date": "2022-05-09T00:00:00+00:00",
              "employee_count": 152,
              "follower_count": null
            },
            {
              "date": "2022-05-16T00:00:00+00:00",
              "employee_count": 152,
              "follower_count": null
            },
            {
              "date": "2022-05-23T00:00:00+00:00",
              "employee_count": 152,
              "follower_count": null
            },
            {
              "date": "2022-05-30T00:00:00+00:00",
              "employee_count": 152,
              "follower_count": null
            },
            {
              "date": "2022-06-01T00:00:00+00:00",
              "employee_count": 159,
              "follower_count": null
            },
            {
              "date": "2022-06-06T00:00:00+00:00",
              "employee_count": 159,
              "follower_count": null
            },
            {
              "date": "2022-06-13T00:00:00+00:00",
              "employee_count": 159,
              "follower_count": null
            },
            {
              "date": "2022-06-20T00:00:00+00:00",
              "employee_count": 159,
              "follower_count": null
            },
            {
              "date": "2022-06-27T00:00:00+00:00",
              "employee_count": 159,
              "follower_count": null
            },
            {
              "date": "2022-07-01T00:00:00+00:00",
              "employee_count": 163,
              "follower_count": null
            },
            {
              "date": "2022-07-04T00:00:00+00:00",
              "employee_count": 163,
              "follower_count": null
            },
            {
              "date": "2022-07-11T00:00:00+00:00",
              "employee_count": 163,
              "follower_count": null
            },
            {
              "date": "2022-07-18T00:00:00+00:00",
              "employee_count": 163,
              "follower_count": null
            },
            {
              "date": "2022-07-25T00:00:00+00:00",
              "employee_count": 163,
              "follower_count": null
            },
            {
              "date": "2022-08-01T00:00:00+00:00",
              "employee_count": 163,
              "follower_count": null
            },
            {
              "date": "2022-08-08T00:00:00+00:00",
              "employee_count": 163,
              "follower_count": null
            },
            {
              "date": "2022-08-15T00:00:00+00:00",
              "employee_count": 163,
              "follower_count": null
            },
            {
              "date": "2022-08-22T00:00:00+00:00",
              "employee_count": 163,
              "follower_count": null
            },
            {
              "date": "2022-08-29T00:00:00+00:00",
              "employee_count": 163,
              "follower_count": null
            },
            {
              "date": "2022-09-01T00:00:00+00:00",
              "employee_count": 165,
              "follower_count": null
            },
            {
              "date": "2022-09-05T00:00:00+00:00",
              "employee_count": 165,
              "follower_count": null
            },
            {
              "date": "2022-09-12T00:00:00+00:00",
              "employee_count": 165,
              "follower_count": null
            },
            {
              "date": "2022-09-19T00:00:00+00:00",
              "employee_count": 165,
              "follower_count": null
            },
            {
              "date": "2022-09-26T00:00:00+00:00",
              "employee_count": 165,
              "follower_count": null
            },
            {
              "date": "2022-10-01T00:00:00+00:00",
              "employee_count": 164,
              "follower_count": null
            },
            {
              "date": "2022-10-03T00:00:00+00:00",
              "employee_count": 164,
              "follower_count": null
            },
            {
              "date": "2022-10-10T00:00:00+00:00",
              "employee_count": 164,
              "follower_count": null
            },
            {
              "date": "2022-10-17T00:00:00+00:00",
              "employee_count": 164,
              "follower_count": null
            },
            {
              "date": "2022-10-24T00:00:00+00:00",
              "employee_count": 164,
              "follower_count": null
            },
            {
              "date": "2022-10-31T00:00:00+00:00",
              "employee_count": 164,
              "follower_count": null
            },
            {
              "date": "2022-11-01T00:00:00+00:00",
              "employee_count": 166,
              "follower_count": null
            },
            {
              "date": "2022-11-07T00:00:00+00:00",
              "employee_count": 166,
              "follower_count": null
            },
            {
              "date": "2022-11-14T00:00:00+00:00",
              "employee_count": 166,
              "follower_count": null
            },
            {
              "date": "2022-11-21T00:00:00+00:00",
              "employee_count": 166,
              "follower_count": null
            },
            {
              "date": "2022-11-28T00:00:00+00:00",
              "employee_count": 166,
              "follower_count": null
            },
            {
              "date": "2022-12-01T00:00:00+00:00",
              "employee_count": 161,
              "follower_count": null
            },
            {
              "date": "2022-12-05T00:00:00+00:00",
              "employee_count": 161,
              "follower_count": null
            },
            {
              "date": "2022-12-12T00:00:00+00:00",
              "employee_count": 161,
              "follower_count": null
            },
            {
              "date": "2022-12-19T00:00:00+00:00",
              "employee_count": 161,
              "follower_count": null
            },
            {
              "date": "2022-12-26T00:00:00+00:00",
              "employee_count": 161,
              "follower_count": null
            },
            {
              "date": "2023-01-01T00:00:00+00:00",
              "employee_count": 163,
              "follower_count": null
            },
            {
              "date": "2023-01-02T00:00:00+00:00",
              "employee_count": 163,
              "follower_count": null
            },
            {
              "date": "2023-01-09T00:00:00+00:00",
              "employee_count": 163,
              "follower_count": null
            },
            {
              "date": "2023-01-16T00:00:00+00:00",
              "employee_count": 163,
              "follower_count": null
            },
            {
              "date": "2023-01-23T00:00:00+00:00",
              "employee_count": 163,
              "follower_count": null
            },
            {
              "date": "2023-01-30T00:00:00+00:00",
              "employee_count": 163,
              "follower_count": null
            },
            {
              "date": "2023-02-01T00:00:00+00:00",
              "employee_count": 164,
              "follower_count": null
            },
            {
              "date": "2023-02-06T00:00:00+00:00",
              "employee_count": 164,
              "follower_count": null
            },
            {
              "date": "2023-02-13T00:00:00+00:00",
              "employee_count": 164,
              "follower_count": null
            },
            {
              "date": "2023-02-20T00:00:00+00:00",
              "employee_count": 164,
              "follower_count": null
            },
            {
              "date": "2023-02-27T00:00:00+00:00",
              "employee_count": 164,
              "follower_count": null
            },
            {
              "date": "2023-03-01T00:00:00+00:00",
              "employee_count": 164,
              "follower_count": null
            },
            {
              "date": "2023-03-06T00:00:00+00:00",
              "employee_count": 164,
              "follower_count": null
            },
            {
              "date": "2023-03-13T00:00:00+00:00",
              "employee_count": 164,
              "follower_count": null
            },
            {
              "date": "2023-03-20T00:00:00+00:00",
              "employee_count": 164,
              "follower_count": null
            },
            {
              "date": "2023-03-27T00:00:00+00:00",
              "employee_count": 164,
              "follower_count": null
            },
            {
              "date": "2023-04-01T00:00:00+00:00",
              "employee_count": 159,
              "follower_count": null
            },
            {
              "date": "2023-04-03T00:00:00+00:00",
              "employee_count": 159,
              "follower_count": null
            },
            {
              "date": "2023-04-10T00:00:00+00:00",
              "employee_count": 159,
              "follower_count": null
            },
            {
              "date": "2023-04-17T00:00:00+00:00",
              "employee_count": 159,
              "follower_count": null
            },
            {
              "date": "2023-04-24T00:00:00+00:00",
              "employee_count": 159,
              "follower_count": null
            },
            {
              "date": "2023-05-01T00:00:00+00:00",
              "employee_count": 152,
              "follower_count": null
            },
            {
              "date": "2023-05-08T00:00:00+00:00",
              "employee_count": 152,
              "follower_count": null
            },
            {
              "date": "2023-05-15T00:00:00+00:00",
              "employee_count": 152,
              "follower_count": null
            },
            {
              "date": "2023-05-22T00:00:00+00:00",
              "employee_count": 152,
              "follower_count": null
            },
            {
              "date": "2023-05-29T00:00:00+00:00",
              "employee_count": 152,
              "follower_count": null
            },
            {
              "date": "2023-06-01T00:00:00+00:00",
              "employee_count": 147,
              "follower_count": null
            },
            {
              "date": "2023-06-05T00:00:00+00:00",
              "employee_count": 147,
              "follower_count": null
            },
            {
              "date": "2023-06-12T00:00:00+00:00",
              "employee_count": 147,
              "follower_count": null
            },
            {
              "date": "2023-06-19T00:00:00+00:00",
              "employee_count": 147,
              "follower_count": null
            },
            {
              "date": "2023-06-26T00:00:00+00:00",
              "employee_count": 147,
              "follower_count": null
            },
            {
              "date": "2023-07-01T00:00:00+00:00",
              "employee_count": 145,
              "follower_count": null
            },
            {
              "date": "2023-07-03T00:00:00+00:00",
              "employee_count": 145,
              "follower_count": null
            },
            {
              "date": "2023-07-10T00:00:00+00:00",
              "employee_count": 149,
              "follower_count": 15659
            },
            {
              "date": "2023-07-17T00:00:00+00:00",
              "employee_count": 146,
              "follower_count": 15809
            },
            {
              "date": "2023-07-24T00:00:00+00:00",
              "employee_count": 146,
              "follower_count": 15837
            },
            {
              "date": "2023-07-31T00:00:00+00:00",
              "employee_count": 146,
              "follower_count": 15837
            },
            {
              "date": "2023-08-01T00:00:00+00:00",
              "employee_count": 145,
              "follower_count": 15883
            },
            {
              "date": "2023-08-07T00:00:00+00:00",
              "employee_count": 145,
              "follower_count": 15892
            },
            {
              "date": "2023-08-14T00:00:00+00:00",
              "employee_count": 143,
              "follower_count": 15921
            },
            {
              "date": "2023-08-21T00:00:00+00:00",
              "employee_count": 144,
              "follower_count": 15936
            },
            {
              "date": "2023-08-28T00:00:00+00:00",
              "employee_count": 144,
              "follower_count": 15936
            },
            {
              "date": "2023-09-01T00:00:00+00:00",
              "employee_count": 143,
              "follower_count": 15963
            },
            {
              "date": "2023-09-04T00:00:00+00:00",
              "employee_count": 143,
              "follower_count": 15963
            },
            {
              "date": "2023-09-11T00:00:00+00:00",
              "employee_count": 140,
              "follower_count": 16098
            },
            {
              "date": "2023-09-18T00:00:00+00:00",
              "employee_count": 140,
              "follower_count": 16129
            },
            {
              "date": "2023-09-25T00:00:00+00:00",
              "employee_count": 140,
              "follower_count": 16129
            },
            {
              "date": "2023-10-01T00:00:00+00:00",
              "employee_count": 140,
              "follower_count": 16290
            },
            {
              "date": "2023-10-02T00:00:00+00:00",
              "employee_count": 140,
              "follower_count": 16290
            },
            {
              "date": "2023-10-09T00:00:00+00:00",
              "employee_count": 140,
              "follower_count": 16381
            },
            {
              "date": "2023-10-16T00:00:00+00:00",
              "employee_count": 140,
              "follower_count": 16466
            },
            {
              "date": "2023-10-23T00:00:00+00:00",
              "employee_count": 139,
              "follower_count": null
            },
            {
              "date": "2023-10-30T00:00:00+00:00",
              "employee_count": 139,
              "follower_count": 16525
            },
            {
              "date": "2023-11-01T00:00:00+00:00",
              "employee_count": 139,
              "follower_count": 16584
            },
            {
              "date": "2023-11-06T00:00:00+00:00",
              "employee_count": 139,
              "follower_count": 16133
            },
            {
              "date": "2023-11-13T00:00:00+00:00",
              "employee_count": 139,
              "follower_count": 16165
            },
            {
              "date": "2023-11-20T00:00:00+00:00",
              "employee_count": 139,
              "follower_count": 16173
            },
            {
              "date": "2023-11-27T00:00:00+00:00",
              "employee_count": 139,
              "follower_count": 16179
            },
            {
              "date": "2023-12-01T00:00:00+00:00",
              "employee_count": 139,
              "follower_count": 16179
            },
            {
              "date": "2023-12-04T00:00:00+00:00",
              "employee_count": 139,
              "follower_count": 16191
            },
            {
              "date": "2023-12-11T00:00:00+00:00",
              "employee_count": 138,
              "follower_count": 16202
            },
            {
              "date": "2023-12-18T00:00:00+00:00",
              "employee_count": 137,
              "follower_count": 16224
            },
            {
              "date": "2023-12-25T00:00:00+00:00",
              "employee_count": 137,
              "follower_count": 16223
            },
            {
              "date": "2024-01-01T00:00:00+00:00",
              "employee_count": 137,
              "follower_count": 16229
            },
            {
              "date": "2024-01-08T00:00:00+00:00",
              "employee_count": 134,
              "follower_count": 16231
            },
            {
              "date": "2024-01-15T00:00:00+00:00",
              "employee_count": 133,
              "follower_count": 16238
            },
            {
              "date": "2024-01-22T00:00:00+00:00",
              "employee_count": 134,
              "follower_count": 16241
            },
            {
              "date": "2024-01-29T00:00:00+00:00",
              "employee_count": 133,
              "follower_count": 16265
            },
            {
              "date": "2024-02-01T00:00:00+00:00",
              "employee_count": 133,
              "follower_count": 16265
            },
            {
              "date": "2024-02-05T00:00:00+00:00",
              "employee_count": 132,
              "follower_count": 16273
            },
            {
              "date": "2024-02-12T00:00:00+00:00",
              "employee_count": 132,
              "follower_count": 16276
            },
            {
              "date": "2024-02-19T00:00:00+00:00",
              "employee_count": 130,
              "follower_count": 16276
            },
            {
              "date": "2024-02-26T00:00:00+00:00",
              "employee_count": 130,
              "follower_count": 16279
            }
          ],
          5
        ],
        [
          673947,
          "https://www.sketch.com/",
          "35625249",
          "sketch.com",
          [
            {
              "date": "2021-10-01T00:00:00+00:00",
              "employee_count": 243,
              "follower_count": null
            },
            {
              "date": "2021-10-04T00:00:00+00:00",
              "employee_count": 243,
              "follower_count": null
            },
            {
              "date": "2021-10-11T00:00:00+00:00",
              "employee_count": 243,
              "follower_count": null
            },
            {
              "date": "2021-10-18T00:00:00+00:00",
              "employee_count": 243,
              "follower_count": null
            },
            {
              "date": "2021-10-25T00:00:00+00:00",
              "employee_count": 243,
              "follower_count": null
            },
            {
              "date": "2021-11-01T00:00:00+00:00",
              "employee_count": 257,
              "follower_count": null
            },
            {
              "date": "2021-11-08T00:00:00+00:00",
              "employee_count": 257,
              "follower_count": null
            },
            {
              "date": "2021-11-15T00:00:00+00:00",
              "employee_count": 257,
              "follower_count": null
            },
            {
              "date": "2021-11-22T00:00:00+00:00",
              "employee_count": 257,
              "follower_count": null
            },
            {
              "date": "2021-11-29T00:00:00+00:00",
              "employee_count": 257,
              "follower_count": null
            },
            {
              "date": "2021-12-01T00:00:00+00:00",
              "employee_count": 258,
              "follower_count": null
            },
            {
              "date": "2021-12-06T00:00:00+00:00",
              "employee_count": 258,
              "follower_count": null
            },
            {
              "date": "2021-12-13T00:00:00+00:00",
              "employee_count": 258,
              "follower_count": null
            },
            {
              "date": "2021-12-20T00:00:00+00:00",
              "employee_count": 258,
              "follower_count": null
            },
            {
              "date": "2021-12-27T00:00:00+00:00",
              "employee_count": 258,
              "follower_count": null
            },
            {
              "date": "2022-01-01T00:00:00+00:00",
              "employee_count": 268,
              "follower_count": null
            },
            {
              "date": "2022-01-03T00:00:00+00:00",
              "employee_count": 268,
              "follower_count": null
            },
            {
              "date": "2022-01-10T00:00:00+00:00",
              "employee_count": 268,
              "follower_count": null
            },
            {
              "date": "2022-01-17T00:00:00+00:00",
              "employee_count": 268,
              "follower_count": null
            },
            {
              "date": "2022-01-24T00:00:00+00:00",
              "employee_count": 268,
              "follower_count": null
            },
            {
              "date": "2022-01-31T00:00:00+00:00",
              "employee_count": 268,
              "follower_count": null
            },
            {
              "date": "2022-02-01T00:00:00+00:00",
              "employee_count": 277,
              "follower_count": null
            },
            {
              "date": "2022-02-07T00:00:00+00:00",
              "employee_count": 277,
              "follower_count": null
            },
            {
              "date": "2022-02-14T00:00:00+00:00",
              "employee_count": 277,
              "follower_count": null
            },
            {
              "date": "2022-02-21T00:00:00+00:00",
              "employee_count": 277,
              "follower_count": null
            },
            {
              "date": "2022-02-28T00:00:00+00:00",
              "employee_count": 277,
              "follower_count": null
            },
            {
              "date": "2022-03-01T00:00:00+00:00",
              "employee_count": 283,
              "follower_count": null
            },
            {
              "date": "2022-03-07T00:00:00+00:00",
              "employee_count": 283,
              "follower_count": null
            },
            {
              "date": "2022-03-14T00:00:00+00:00",
              "employee_count": 283,
              "follower_count": null
            },
            {
              "date": "2022-03-21T00:00:00+00:00",
              "employee_count": 283,
              "follower_count": null
            },
            {
              "date": "2022-03-28T00:00:00+00:00",
              "employee_count": 283,
              "follower_count": null
            },
            {
              "date": "2022-04-01T00:00:00+00:00",
              "employee_count": 294,
              "follower_count": null
            },
            {
              "date": "2022-04-04T00:00:00+00:00",
              "employee_count": 294,
              "follower_count": null
            },
            {
              "date": "2022-04-11T00:00:00+00:00",
              "employee_count": 294,
              "follower_count": null
            },
            {
              "date": "2022-04-18T00:00:00+00:00",
              "employee_count": 294,
              "follower_count": null
            },
            {
              "date": "2022-04-25T00:00:00+00:00",
              "employee_count": 294,
              "follower_count": null
            },
            {
              "date": "2022-05-01T00:00:00+00:00",
              "employee_count": 298,
              "follower_count": null
            },
            {
              "date": "2022-05-02T00:00:00+00:00",
              "employee_count": 298,
              "follower_count": null
            },
            {
              "date": "2022-05-09T00:00:00+00:00",
              "employee_count": 298,
              "follower_count": null
            },
            {
              "date": "2022-05-16T00:00:00+00:00",
              "employee_count": 298,
              "follower_count": null
            },
            {
              "date": "2022-05-23T00:00:00+00:00",
              "employee_count": 298,
              "follower_count": null
            },
            {
              "date": "2022-05-30T00:00:00+00:00",
              "employee_count": 298,
              "follower_count": null
            },
            {
              "date": "2022-06-01T00:00:00+00:00",
              "employee_count": 303,
              "follower_count": null
            },
            {
              "date": "2022-06-06T00:00:00+00:00",
              "employee_count": 303,
              "follower_count": null
            },
            {
              "date": "2022-06-13T00:00:00+00:00",
              "employee_count": 303,
              "follower_count": null
            },
            {
              "date": "2022-06-20T00:00:00+00:00",
              "employee_count": 303,
              "follower_count": null
            },
            {
              "date": "2022-06-27T00:00:00+00:00",
              "employee_count": 303,
              "follower_count": null
            },
            {
              "date": "2022-07-01T00:00:00+00:00",
              "employee_count": 314,
              "follower_count": null
            },
            {
              "date": "2022-07-04T00:00:00+00:00",
              "employee_count": 314,
              "follower_count": null
            },
            {
              "date": "2022-07-11T00:00:00+00:00",
              "employee_count": 314,
              "follower_count": null
            },
            {
              "date": "2022-07-18T00:00:00+00:00",
              "employee_count": 314,
              "follower_count": null
            },
            {
              "date": "2022-07-25T00:00:00+00:00",
              "employee_count": 314,
              "follower_count": null
            },
            {
              "date": "2022-08-01T00:00:00+00:00",
              "employee_count": 312,
              "follower_count": null
            },
            {
              "date": "2022-08-08T00:00:00+00:00",
              "employee_count": 312,
              "follower_count": null
            },
            {
              "date": "2022-08-15T00:00:00+00:00",
              "employee_count": 312,
              "follower_count": null
            },
            {
              "date": "2022-08-22T00:00:00+00:00",
              "employee_count": 312,
              "follower_count": null
            },
            {
              "date": "2022-08-29T00:00:00+00:00",
              "employee_count": 312,
              "follower_count": null
            },
            {
              "date": "2022-09-01T00:00:00+00:00",
              "employee_count": 316,
              "follower_count": null
            },
            {
              "date": "2022-09-05T00:00:00+00:00",
              "employee_count": 316,
              "follower_count": null
            },
            {
              "date": "2022-09-12T00:00:00+00:00",
              "employee_count": 316,
              "follower_count": null
            },
            {
              "date": "2022-09-19T00:00:00+00:00",
              "employee_count": 316,
              "follower_count": null
            },
            {
              "date": "2022-09-26T00:00:00+00:00",
              "employee_count": 316,
              "follower_count": null
            },
            {
              "date": "2022-10-01T00:00:00+00:00",
              "employee_count": 267,
              "follower_count": null
            },
            {
              "date": "2022-10-03T00:00:00+00:00",
              "employee_count": 267,
              "follower_count": null
            },
            {
              "date": "2022-10-10T00:00:00+00:00",
              "employee_count": 267,
              "follower_count": null
            },
            {
              "date": "2022-10-17T00:00:00+00:00",
              "employee_count": 267,
              "follower_count": null
            },
            {
              "date": "2022-10-24T00:00:00+00:00",
              "employee_count": 267,
              "follower_count": null
            },
            {
              "date": "2022-10-31T00:00:00+00:00",
              "employee_count": 267,
              "follower_count": null
            },
            {
              "date": "2022-11-01T00:00:00+00:00",
              "employee_count": 252,
              "follower_count": null
            },
            {
              "date": "2022-11-07T00:00:00+00:00",
              "employee_count": 252,
              "follower_count": null
            },
            {
              "date": "2022-11-14T00:00:00+00:00",
              "employee_count": 252,
              "follower_count": null
            },
            {
              "date": "2022-11-21T00:00:00+00:00",
              "employee_count": 252,
              "follower_count": null
            },
            {
              "date": "2022-11-28T00:00:00+00:00",
              "employee_count": 252,
              "follower_count": null
            },
            {
              "date": "2022-12-01T00:00:00+00:00",
              "employee_count": 242,
              "follower_count": null
            },
            {
              "date": "2022-12-05T00:00:00+00:00",
              "employee_count": 242,
              "follower_count": null
            },
            {
              "date": "2022-12-12T00:00:00+00:00",
              "employee_count": 242,
              "follower_count": null
            },
            {
              "date": "2022-12-19T00:00:00+00:00",
              "employee_count": 242,
              "follower_count": null
            },
            {
              "date": "2022-12-26T00:00:00+00:00",
              "employee_count": 242,
              "follower_count": null
            },
            {
              "date": "2023-01-01T00:00:00+00:00",
              "employee_count": 240,
              "follower_count": null
            },
            {
              "date": "2023-01-02T00:00:00+00:00",
              "employee_count": 240,
              "follower_count": null
            },
            {
              "date": "2023-01-09T00:00:00+00:00",
              "employee_count": 240,
              "follower_count": null
            },
            {
              "date": "2023-01-16T00:00:00+00:00",
              "employee_count": 240,
              "follower_count": null
            },
            {
              "date": "2023-01-23T00:00:00+00:00",
              "employee_count": 240,
              "follower_count": null
            },
            {
              "date": "2023-01-30T00:00:00+00:00",
              "employee_count": 240,
              "follower_count": null
            },
            {
              "date": "2023-02-01T00:00:00+00:00",
              "employee_count": 241,
              "follower_count": null
            },
            {
              "date": "2023-02-06T00:00:00+00:00",
              "employee_count": 241,
              "follower_count": null
            },
            {
              "date": "2023-02-13T00:00:00+00:00",
              "employee_count": 241,
              "follower_count": null
            },
            {
              "date": "2023-02-20T00:00:00+00:00",
              "employee_count": 241,
              "follower_count": null
            },
            {
              "date": "2023-02-27T00:00:00+00:00",
              "employee_count": 241,
              "follower_count": null
            },
            {
              "date": "2023-03-01T00:00:00+00:00",
              "employee_count": 242,
              "follower_count": null
            },
            {
              "date": "2023-03-06T00:00:00+00:00",
              "employee_count": 242,
              "follower_count": null
            },
            {
              "date": "2023-03-13T00:00:00+00:00",
              "employee_count": 242,
              "follower_count": null
            },
            {
              "date": "2023-03-20T00:00:00+00:00",
              "employee_count": 242,
              "follower_count": null
            },
            {
              "date": "2023-03-27T00:00:00+00:00",
              "employee_count": 242,
              "follower_count": null
            },
            {
              "date": "2023-04-01T00:00:00+00:00",
              "employee_count": 238,
              "follower_count": null
            },
            {
              "date": "2023-04-03T00:00:00+00:00",
              "employee_count": 238,
              "follower_count": null
            },
            {
              "date": "2023-04-10T00:00:00+00:00",
              "employee_count": 238,
              "follower_count": null
            },
            {
              "date": "2023-04-17T00:00:00+00:00",
              "employee_count": 238,
              "follower_count": null
            },
            {
              "date": "2023-04-24T00:00:00+00:00",
              "employee_count": 238,
              "follower_count": null
            },
            {
              "date": "2023-05-01T00:00:00+00:00",
              "employee_count": 238,
              "follower_count": null
            },
            {
              "date": "2023-05-08T00:00:00+00:00",
              "employee_count": 238,
              "follower_count": null
            },
            {
              "date": "2023-05-15T00:00:00+00:00",
              "employee_count": 238,
              "follower_count": null
            },
            {
              "date": "2023-05-22T00:00:00+00:00",
              "employee_count": 238,
              "follower_count": null
            },
            {
              "date": "2023-05-29T00:00:00+00:00",
              "employee_count": 238,
              "follower_count": null
            },
            {
              "date": "2023-06-01T00:00:00+00:00",
              "employee_count": 240,
              "follower_count": null
            },
            {
              "date": "2023-06-05T00:00:00+00:00",
              "employee_count": 240,
              "follower_count": null
            },
            {
              "date": "2023-06-12T00:00:00+00:00",
              "employee_count": 240,
              "follower_count": null
            },
            {
              "date": "2023-06-19T00:00:00+00:00",
              "employee_count": 240,
              "follower_count": null
            },
            {
              "date": "2023-06-26T00:00:00+00:00",
              "employee_count": 240,
              "follower_count": null
            },
            {
              "date": "2023-07-01T00:00:00+00:00",
              "employee_count": 240,
              "follower_count": null
            },
            {
              "date": "2023-07-03T00:00:00+00:00",
              "employee_count": 240,
              "follower_count": null
            },
            {
              "date": "2023-07-10T00:00:00+00:00",
              "employee_count": 292,
              "follower_count": 71247
            },
            {
              "date": "2023-07-17T00:00:00+00:00",
              "employee_count": 291,
              "follower_count": 71299
            },
            {
              "date": "2023-07-24T00:00:00+00:00",
              "employee_count": 290,
              "follower_count": 71338
            },
            {
              "date": "2023-07-31T00:00:00+00:00",
              "employee_count": 290,
              "follower_count": 71338
            },
            {
              "date": "2023-08-01T00:00:00+00:00",
              "employee_count": 276,
              "follower_count": 71429
            },
            {
              "date": "2023-08-07T00:00:00+00:00",
              "employee_count": 258,
              "follower_count": 71453
            },
            {
              "date": "2023-08-14T00:00:00+00:00",
              "employee_count": 258,
              "follower_count": 71453
            },
            {
              "date": "2023-08-21T00:00:00+00:00",
              "employee_count": 258,
              "follower_count": 71453
            },
            {
              "date": "2023-08-28T00:00:00+00:00",
              "employee_count": 253,
              "follower_count": 71577
            },
            {
              "date": "2023-09-01T00:00:00+00:00",
              "employee_count": 254,
              "follower_count": 71580
            },
            {
              "date": "2023-09-04T00:00:00+00:00",
              "employee_count": 254,
              "follower_count": 71580
            },
            {
              "date": "2023-09-11T00:00:00+00:00",
              "employee_count": 254,
              "follower_count": 71612
            },
            {
              "date": "2023-09-18T00:00:00+00:00",
              "employee_count": 240,
              "follower_count": 71677
            },
            {
              "date": "2023-09-25T00:00:00+00:00",
              "employee_count": 240,
              "follower_count": 71677
            },
            {
              "date": "2023-10-01T00:00:00+00:00",
              "employee_count": 234,
              "follower_count": 71733
            },
            {
              "date": "2023-10-02T00:00:00+00:00",
              "employee_count": 234,
              "follower_count": 71733
            },
            {
              "date": "2023-10-09T00:00:00+00:00",
              "employee_count": 233,
              "follower_count": 71753
            },
            {
              "date": "2023-10-16T00:00:00+00:00",
              "employee_count": 232,
              "follower_count": 71775
            },
            {
              "date": "2023-10-23T00:00:00+00:00",
              "employee_count": 235,
              "follower_count": 71806
            },
            {
              "date": "2023-10-30T00:00:00+00:00",
              "employee_count": 235,
              "follower_count": null
            },
            {
              "date": "2023-11-01T00:00:00+00:00",
              "employee_count": 235,
              "follower_count": 70563
            },
            {
              "date": "2023-11-06T00:00:00+00:00",
              "employee_count": 234,
              "follower_count": 70266
            },
            {
              "date": "2023-11-13T00:00:00+00:00",
              "employee_count": 235,
              "follower_count": 70280
            },
            {
              "date": "2023-11-20T00:00:00+00:00",
              "employee_count": 236,
              "follower_count": 70298
            },
            {
              "date": "2023-11-27T00:00:00+00:00",
              "employee_count": 234,
              "follower_count": 70295
            },
            {
              "date": "2023-12-01T00:00:00+00:00",
              "employee_count": 234,
              "follower_count": 70305
            },
            {
              "date": "2023-12-04T00:00:00+00:00",
              "employee_count": 235,
              "follower_count": 70327
            },
            {
              "date": "2023-12-11T00:00:00+00:00",
              "employee_count": 234,
              "follower_count": 70350
            },
            {
              "date": "2023-12-18T00:00:00+00:00",
              "employee_count": 236,
              "follower_count": 70370
            },
            {
              "date": "2023-12-25T00:00:00+00:00",
              "employee_count": 235,
              "follower_count": 70385
            },
            {
              "date": "2024-01-01T00:00:00+00:00",
              "employee_count": 235,
              "follower_count": 70407
            },
            {
              "date": "2024-01-08T00:00:00+00:00",
              "employee_count": 234,
              "follower_count": 70456
            },
            {
              "date": "2024-01-15T00:00:00+00:00",
              "employee_count": 234,
              "follower_count": 70494
            },
            {
              "date": "2024-01-22T00:00:00+00:00",
              "employee_count": 230,
              "follower_count": 70574
            },
            {
              "date": "2024-01-29T00:00:00+00:00",
              "employee_count": 230,
              "follower_count": 70616
            },
            {
              "date": "2024-02-01T00:00:00+00:00",
              "employee_count": 228,
              "follower_count": 70636
            },
            {
              "date": "2024-02-05T00:00:00+00:00",
              "employee_count": 228,
              "follower_count": 70636
            },
            {
              "date": "2024-02-12T00:00:00+00:00",
              "employee_count": 223,
              "follower_count": 70626
            },
            {
              "date": "2024-02-19T00:00:00+00:00",
              "employee_count": 224,
              "follower_count": 70643
            },
            {
              "date": "2024-02-26T00:00:00+00:00",
              "employee_count": 223,
              "follower_count": 70643
            }
          ],
          5
        ],
        [
          680992,
          "http://www.microstrategy.com",
          "3643",
          "microstrategy.com",
          [
            {
              "date": "2021-08-01T00:00:00+00:00",
              "employee_count": 3266,
              "follower_count": null
            },
            {
              "date": "2021-08-02T00:00:00+00:00",
              "employee_count": 3266,
              "follower_count": null
            },
            {
              "date": "2021-08-09T00:00:00+00:00",
              "employee_count": 3266,
              "follower_count": null
            },
            {
              "date": "2021-08-16T00:00:00+00:00",
              "employee_count": 3266,
              "follower_count": null
            },
            {
              "date": "2021-08-23T00:00:00+00:00",
              "employee_count": 3266,
              "follower_count": null
            },
            {
              "date": "2021-08-30T00:00:00+00:00",
              "employee_count": 3266,
              "follower_count": null
            },
            {
              "date": "2021-09-01T00:00:00+00:00",
              "employee_count": 3278,
              "follower_count": null
            },
            {
              "date": "2021-09-06T00:00:00+00:00",
              "employee_count": 3278,
              "follower_count": null
            },
            {
              "date": "2021-09-13T00:00:00+00:00",
              "employee_count": 3278,
              "follower_count": null
            },
            {
              "date": "2021-09-20T00:00:00+00:00",
              "employee_count": 3278,
              "follower_count": null
            },
            {
              "date": "2021-09-27T00:00:00+00:00",
              "employee_count": 3278,
              "follower_count": null
            },
            {
              "date": "2021-10-01T00:00:00+00:00",
              "employee_count": 3305,
              "follower_count": null
            },
            {
              "date": "2021-10-04T00:00:00+00:00",
              "employee_count": 3305,
              "follower_count": null
            },
            {
              "date": "2021-10-11T00:00:00+00:00",
              "employee_count": 3305,
              "follower_count": null
            },
            {
              "date": "2021-10-18T00:00:00+00:00",
              "employee_count": 3305,
              "follower_count": null
            },
            {
              "date": "2021-10-25T00:00:00+00:00",
              "employee_count": 3305,
              "follower_count": null
            },
            {
              "date": "2021-11-01T00:00:00+00:00",
              "employee_count": 3327,
              "follower_count": null
            },
            {
              "date": "2021-11-08T00:00:00+00:00",
              "employee_count": 3327,
              "follower_count": null
            },
            {
              "date": "2021-11-15T00:00:00+00:00",
              "employee_count": 3327,
              "follower_count": null
            },
            {
              "date": "2021-11-22T00:00:00+00:00",
              "employee_count": 3327,
              "follower_count": null
            },
            {
              "date": "2021-11-29T00:00:00+00:00",
              "employee_count": 3327,
              "follower_count": null
            },
            {
              "date": "2021-12-01T00:00:00+00:00",
              "employee_count": 3331,
              "follower_count": null
            },
            {
              "date": "2021-12-06T00:00:00+00:00",
              "employee_count": 3331,
              "follower_count": null
            },
            {
              "date": "2021-12-13T00:00:00+00:00",
              "employee_count": 3331,
              "follower_count": null
            },
            {
              "date": "2021-12-20T00:00:00+00:00",
              "employee_count": 3331,
              "follower_count": null
            },
            {
              "date": "2021-12-27T00:00:00+00:00",
              "employee_count": 3331,
              "follower_count": null
            },
            {
              "date": "2022-01-01T00:00:00+00:00",
              "employee_count": 3359,
              "follower_count": null
            },
            {
              "date": "2022-01-03T00:00:00+00:00",
              "employee_count": 3359,
              "follower_count": null
            },
            {
              "date": "2022-01-10T00:00:00+00:00",
              "employee_count": 3359,
              "follower_count": null
            },
            {
              "date": "2022-01-17T00:00:00+00:00",
              "employee_count": 3359,
              "follower_count": null
            },
            {
              "date": "2022-01-24T00:00:00+00:00",
              "employee_count": 3359,
              "follower_count": null
            },
            {
              "date": "2022-01-31T00:00:00+00:00",
              "employee_count": 3359,
              "follower_count": null
            },
            {
              "date": "2022-02-01T00:00:00+00:00",
              "employee_count": 3366,
              "follower_count": null
            },
            {
              "date": "2022-02-07T00:00:00+00:00",
              "employee_count": 3366,
              "follower_count": null
            },
            {
              "date": "2022-02-14T00:00:00+00:00",
              "employee_count": 3366,
              "follower_count": null
            },
            {
              "date": "2022-02-21T00:00:00+00:00",
              "employee_count": 3366,
              "follower_count": null
            },
            {
              "date": "2022-02-28T00:00:00+00:00",
              "employee_count": 3366,
              "follower_count": null
            },
            {
              "date": "2022-03-01T00:00:00+00:00",
              "employee_count": 3388,
              "follower_count": null
            },
            {
              "date": "2022-03-07T00:00:00+00:00",
              "employee_count": 3388,
              "follower_count": null
            },
            {
              "date": "2022-03-14T00:00:00+00:00",
              "employee_count": 3388,
              "follower_count": null
            },
            {
              "date": "2022-03-21T00:00:00+00:00",
              "employee_count": 3388,
              "follower_count": null
            },
            {
              "date": "2022-03-28T00:00:00+00:00",
              "employee_count": 3388,
              "follower_count": null
            },
            {
              "date": "2022-04-01T00:00:00+00:00",
              "employee_count": 3391,
              "follower_count": null
            },
            {
              "date": "2022-04-04T00:00:00+00:00",
              "employee_count": 3391,
              "follower_count": null
            },
            {
              "date": "2022-04-11T00:00:00+00:00",
              "employee_count": 3391,
              "follower_count": null
            },
            {
              "date": "2022-04-18T00:00:00+00:00",
              "employee_count": 3391,
              "follower_count": null
            },
            {
              "date": "2022-04-25T00:00:00+00:00",
              "employee_count": 3391,
              "follower_count": null
            },
            {
              "date": "2022-05-01T00:00:00+00:00",
              "employee_count": 3409,
              "follower_count": null
            },
            {
              "date": "2022-05-02T00:00:00+00:00",
              "employee_count": 3409,
              "follower_count": null
            },
            {
              "date": "2022-05-09T00:00:00+00:00",
              "employee_count": 3409,
              "follower_count": null
            },
            {
              "date": "2022-05-16T00:00:00+00:00",
              "employee_count": 3409,
              "follower_count": null
            },
            {
              "date": "2022-05-23T00:00:00+00:00",
              "employee_count": 3409,
              "follower_count": null
            },
            {
              "date": "2022-05-30T00:00:00+00:00",
              "employee_count": 3409,
              "follower_count": null
            },
            {
              "date": "2022-06-01T00:00:00+00:00",
              "employee_count": 3414,
              "follower_count": null
            },
            {
              "date": "2022-06-06T00:00:00+00:00",
              "employee_count": 3414,
              "follower_count": null
            },
            {
              "date": "2022-06-13T00:00:00+00:00",
              "employee_count": 3414,
              "follower_count": null
            },
            {
              "date": "2022-06-20T00:00:00+00:00",
              "employee_count": 3414,
              "follower_count": null
            },
            {
              "date": "2022-06-27T00:00:00+00:00",
              "employee_count": 3414,
              "follower_count": null
            },
            {
              "date": "2022-07-01T00:00:00+00:00",
              "employee_count": 3428,
              "follower_count": null
            },
            {
              "date": "2022-07-04T00:00:00+00:00",
              "employee_count": 3428,
              "follower_count": null
            },
            {
              "date": "2022-07-11T00:00:00+00:00",
              "employee_count": 3428,
              "follower_count": null
            },
            {
              "date": "2022-07-18T00:00:00+00:00",
              "employee_count": 3428,
              "follower_count": null
            },
            {
              "date": "2022-07-25T00:00:00+00:00",
              "employee_count": 3428,
              "follower_count": null
            },
            {
              "date": "2022-08-01T00:00:00+00:00",
              "employee_count": 3429,
              "follower_count": null
            },
            {
              "date": "2022-08-08T00:00:00+00:00",
              "employee_count": 3429,
              "follower_count": null
            },
            {
              "date": "2022-08-15T00:00:00+00:00",
              "employee_count": 3429,
              "follower_count": null
            },
            {
              "date": "2022-08-22T00:00:00+00:00",
              "employee_count": 3429,
              "follower_count": null
            },
            {
              "date": "2022-08-29T00:00:00+00:00",
              "employee_count": 3429,
              "follower_count": null
            },
            {
              "date": "2022-09-01T00:00:00+00:00",
              "employee_count": 3442,
              "follower_count": null
            },
            {
              "date": "2022-09-05T00:00:00+00:00",
              "employee_count": 3442,
              "follower_count": null
            },
            {
              "date": "2022-09-12T00:00:00+00:00",
              "employee_count": 3442,
              "follower_count": null
            },
            {
              "date": "2022-09-19T00:00:00+00:00",
              "employee_count": 3442,
              "follower_count": null
            },
            {
              "date": "2022-09-26T00:00:00+00:00",
              "employee_count": 3442,
              "follower_count": null
            },
            {
              "date": "2022-10-01T00:00:00+00:00",
              "employee_count": 3446,
              "follower_count": null
            },
            {
              "date": "2022-10-03T00:00:00+00:00",
              "employee_count": 3446,
              "follower_count": null
            },
            {
              "date": "2022-10-10T00:00:00+00:00",
              "employee_count": 3446,
              "follower_count": null
            },
            {
              "date": "2022-10-17T00:00:00+00:00",
              "employee_count": 3446,
              "follower_count": null
            },
            {
              "date": "2022-10-24T00:00:00+00:00",
              "employee_count": 3446,
              "follower_count": null
            },
            {
              "date": "2022-10-31T00:00:00+00:00",
              "employee_count": 3446,
              "follower_count": null
            },
            {
              "date": "2022-11-01T00:00:00+00:00",
              "employee_count": 3471,
              "follower_count": null
            },
            {
              "date": "2022-11-07T00:00:00+00:00",
              "employee_count": 3471,
              "follower_count": null
            },
            {
              "date": "2022-11-14T00:00:00+00:00",
              "employee_count": 3471,
              "follower_count": null
            },
            {
              "date": "2022-11-21T00:00:00+00:00",
              "employee_count": 3471,
              "follower_count": null
            },
            {
              "date": "2022-11-28T00:00:00+00:00",
              "employee_count": 3471,
              "follower_count": null
            },
            {
              "date": "2022-12-01T00:00:00+00:00",
              "employee_count": 3448,
              "follower_count": null
            },
            {
              "date": "2022-12-05T00:00:00+00:00",
              "employee_count": 3448,
              "follower_count": null
            },
            {
              "date": "2022-12-12T00:00:00+00:00",
              "employee_count": 3448,
              "follower_count": null
            },
            {
              "date": "2022-12-19T00:00:00+00:00",
              "employee_count": 3448,
              "follower_count": null
            },
            {
              "date": "2022-12-26T00:00:00+00:00",
              "employee_count": 3448,
              "follower_count": null
            },
            {
              "date": "2023-01-01T00:00:00+00:00",
              "employee_count": 3463,
              "follower_count": null
            },
            {
              "date": "2023-01-02T00:00:00+00:00",
              "employee_count": 3463,
              "follower_count": null
            },
            {
              "date": "2023-01-09T00:00:00+00:00",
              "employee_count": 3463,
              "follower_count": null
            },
            {
              "date": "2023-01-16T00:00:00+00:00",
              "employee_count": 3463,
              "follower_count": null
            },
            {
              "date": "2023-01-23T00:00:00+00:00",
              "employee_count": 3463,
              "follower_count": null
            },
            {
              "date": "2023-01-30T00:00:00+00:00",
              "employee_count": 3463,
              "follower_count": null
            },
            {
              "date": "2023-02-01T00:00:00+00:00",
              "employee_count": 3470,
              "follower_count": null
            },
            {
              "date": "2023-02-06T00:00:00+00:00",
              "employee_count": 3470,
              "follower_count": null
            },
            {
              "date": "2023-02-13T00:00:00+00:00",
              "employee_count": 3470,
              "follower_count": null
            },
            {
              "date": "2023-02-20T00:00:00+00:00",
              "employee_count": 3470,
              "follower_count": null
            },
            {
              "date": "2023-02-27T00:00:00+00:00",
              "employee_count": 3470,
              "follower_count": null
            },
            {
              "date": "2023-03-01T00:00:00+00:00",
              "employee_count": 3467,
              "follower_count": null
            },
            {
              "date": "2023-03-06T00:00:00+00:00",
              "employee_count": 3467,
              "follower_count": null
            },
            {
              "date": "2023-03-13T00:00:00+00:00",
              "employee_count": 3467,
              "follower_count": null
            },
            {
              "date": "2023-03-20T00:00:00+00:00",
              "employee_count": 3467,
              "follower_count": null
            },
            {
              "date": "2023-03-27T00:00:00+00:00",
              "employee_count": 3467,
              "follower_count": null
            },
            {
              "date": "2023-04-01T00:00:00+00:00",
              "employee_count": 3470,
              "follower_count": null
            },
            {
              "date": "2023-04-03T00:00:00+00:00",
              "employee_count": 3470,
              "follower_count": null
            },
            {
              "date": "2023-04-10T00:00:00+00:00",
              "employee_count": 3470,
              "follower_count": null
            },
            {
              "date": "2023-04-17T00:00:00+00:00",
              "employee_count": 3470,
              "follower_count": null
            },
            {
              "date": "2023-04-24T00:00:00+00:00",
              "employee_count": 3470,
              "follower_count": null
            },
            {
              "date": "2023-05-01T00:00:00+00:00",
              "employee_count": 3479,
              "follower_count": null
            },
            {
              "date": "2023-05-08T00:00:00+00:00",
              "employee_count": 3479,
              "follower_count": null
            },
            {
              "date": "2023-05-15T00:00:00+00:00",
              "employee_count": 3479,
              "follower_count": null
            },
            {
              "date": "2023-05-22T00:00:00+00:00",
              "employee_count": 3479,
              "follower_count": null
            },
            {
              "date": "2023-05-29T00:00:00+00:00",
              "employee_count": 3479,
              "follower_count": null
            },
            {
              "date": "2023-06-01T00:00:00+00:00",
              "employee_count": 3484,
              "follower_count": null
            },
            {
              "date": "2023-06-05T00:00:00+00:00",
              "employee_count": 3484,
              "follower_count": null
            },
            {
              "date": "2023-06-12T00:00:00+00:00",
              "employee_count": 3484,
              "follower_count": null
            },
            {
              "date": "2023-06-19T00:00:00+00:00",
              "employee_count": 3484,
              "follower_count": null
            },
            {
              "date": "2023-06-26T00:00:00+00:00",
              "employee_count": 3484,
              "follower_count": null
            },
            {
              "date": "2023-07-01T00:00:00+00:00",
              "employee_count": 3482,
              "follower_count": null
            },
            {
              "date": "2023-07-03T00:00:00+00:00",
              "employee_count": 3482,
              "follower_count": null
            },
            {
              "date": "2023-07-10T00:00:00+00:00",
              "employee_count": 3472,
              "follower_count": 194951
            },
            {
              "date": "2023-07-17T00:00:00+00:00",
              "employee_count": 3463,
              "follower_count": null
            },
            {
              "date": "2023-07-24T00:00:00+00:00",
              "employee_count": 3466,
              "follower_count": 195483
            },
            {
              "date": "2023-07-31T00:00:00+00:00",
              "employee_count": 3466,
              "follower_count": 195483
            },
            {
              "date": "2023-08-01T00:00:00+00:00",
              "employee_count": 3463,
              "follower_count": 196567
            },
            {
              "date": "2023-08-07T00:00:00+00:00",
              "employee_count": 3469,
              "follower_count": 196846
            },
            {
              "date": "2023-08-14T00:00:00+00:00",
              "employee_count": 3473,
              "follower_count": 197196
            },
            {
              "date": "2023-08-21T00:00:00+00:00",
              "employee_count": 3457,
              "follower_count": 197391
            },
            {
              "date": "2023-08-28T00:00:00+00:00",
              "employee_count": 3443,
              "follower_count": 197800
            },
            {
              "date": "2023-09-01T00:00:00+00:00",
              "employee_count": 3443,
              "follower_count": 197842
            },
            {
              "date": "2023-09-04T00:00:00+00:00",
              "employee_count": 3443,
              "follower_count": 197842
            },
            {
              "date": "2023-09-11T00:00:00+00:00",
              "employee_count": 3440,
              "follower_count": 198532
            },
            {
              "date": "2023-09-18T00:00:00+00:00",
              "employee_count": 3431,
              "follower_count": 198877
            },
            {
              "date": "2023-09-25T00:00:00+00:00",
              "employee_count": 3431,
              "follower_count": 198877
            },
            {
              "date": "2023-10-01T00:00:00+00:00",
              "employee_count": 3408,
              "follower_count": 201809
            },
            {
              "date": "2023-10-02T00:00:00+00:00",
              "employee_count": 3408,
              "follower_count": 201809
            },
            {
              "date": "2023-10-09T00:00:00+00:00",
              "employee_count": 3402,
              "follower_count": 202936
            },
            {
              "date": "2023-10-16T00:00:00+00:00",
              "employee_count": 3405,
              "follower_count": 203790
            },
            {
              "date": "2023-10-23T00:00:00+00:00",
              "employee_count": 3397,
              "follower_count": 205640
            },
            {
              "date": "2023-10-30T00:00:00+00:00",
              "employee_count": 3397,
              "follower_count": 207228
            },
            {
              "date": "2023-11-01T00:00:00+00:00",
              "employee_count": 3397,
              "follower_count": 207977
            },
            {
              "date": "2023-11-06T00:00:00+00:00",
              "employee_count": 3399,
              "follower_count": 205522
            },
            {
              "date": "2023-11-13T00:00:00+00:00",
              "employee_count": 3397,
              "follower_count": 204410
            },
            {
              "date": "2023-11-20T00:00:00+00:00",
              "employee_count": 3395,
              "follower_count": 204500
            },
            {
              "date": "2023-11-27T00:00:00+00:00",
              "employee_count": 3399,
              "follower_count": 204605
            },
            {
              "date": "2023-12-01T00:00:00+00:00",
              "employee_count": 3396,
              "follower_count": 204673
            },
            {
              "date": "2023-12-04T00:00:00+00:00",
              "employee_count": 3396,
              "follower_count": 204749
            },
            {
              "date": "2023-12-11T00:00:00+00:00",
              "employee_count": 3394,
              "follower_count": 205277
            },
            {
              "date": "2023-12-18T00:00:00+00:00",
              "employee_count": 3409,
              "follower_count": 206548
            },
            {
              "date": "2023-12-25T00:00:00+00:00",
              "employee_count": 3397,
              "follower_count": 207119
            },
            {
              "date": "2024-01-01T00:00:00+00:00",
              "employee_count": 3405,
              "follower_count": 207810
            },
            {
              "date": "2024-01-08T00:00:00+00:00",
              "employee_count": 3402,
              "follower_count": 208576
            },
            {
              "date": "2024-01-15T00:00:00+00:00",
              "employee_count": 3426,
              "follower_count": 209746
            },
            {
              "date": "2024-01-22T00:00:00+00:00",
              "employee_count": 3415,
              "follower_count": 210596
            },
            {
              "date": "2024-01-29T00:00:00+00:00",
              "employee_count": 3406,
              "follower_count": 211112
            },
            {
              "date": "2024-02-01T00:00:00+00:00",
              "employee_count": 3406,
              "follower_count": 211112
            },
            {
              "date": "2024-02-05T00:00:00+00:00",
              "employee_count": 3398,
              "follower_count": 211743
            },
            {
              "date": "2024-02-12T00:00:00+00:00",
              "employee_count": 3385,
              "follower_count": 211974
            },
            {
              "date": "2024-02-19T00:00:00+00:00",
              "employee_count": 3387,
              "follower_count": 212161
            },
            {
              "date": "2024-02-26T00:00:00+00:00",
              "employee_count": 3391,
              "follower_count": 212385
            },
            {
              "date": "2024-03-01T00:00:00+00:00",
              "employee_count": 3384,
              "follower_count": 212564
            }
          ],
          5
        ]
      ],
      "is_trial_user": false
    }
    ```
    

### 5. Employee Headcount By Function

Use this request to get the headcount by function for the given company.

You either provide with a list of Crustdata’s `company_id`  or `company_website_domain` in the filters

- **CUrl**
    
    ```bash
    curl --request POST \
      --url https://api.crustdata.com/data_lab/linkedin_headcount_by_facet/Table/ \
      --header 'Accept: application/json, text/plain, */*' \
      --header 'Accept-Language: en-US,en;q=0.9' \
      --header 'Authorization: Token $token' \
      --header 'Content-Type: application/json' \
      --header 'Origin: https://crustdata.com' \
      --data '{
        "tickers": [],
        "dataset": {
          "name": "linkedin_headcount_by_facet",
          "id": "linkedinheadcountbyfacet"
        },
        "filters": {
          "op": "and",
          "conditions": [
                {"column": "company_id", "type": "in", "value": [680992, 673947, 631280], "allow_null": false}
          ]
        },
        "groups": [],
        "aggregations": [],
        "functions": [],
        "offset": 0,
        "count": 100,
        "sorts": []
      }'
    ```
    
- **Result**
    
    [JSON Hero](https://jsonhero.io/j/SC3GAjKPzkDw/editor)
    
    ```bash
    {
      "fields": [
        {
          "type": "string",
          "api_name": "linkedin_id",
          "hidden": true,
          "options": [],
          "summary": "",
          "local_metric": false,
          "display_name": "",
          "company_profile_name": "",
          "geocode": false
        },
        {
          "type": "string",
          "api_name": "company_website",
          "hidden": false,
          "options": [],
          "summary": "",
          "local_metric": false,
          "display_name": "",
          "company_profile_name": "",
          "geocode": false
        },
        {
          "type": "string",
          "api_name": "company_name",
          "hidden": false,
          "options": [],
          "summary": "",
          "local_metric": false,
          "display_name": "",
          "company_profile_name": "",
          "geocode": false
        },
        {
          "type": "string",
          "api_name": "company_website_domain",
          "hidden": false,
          "options": [],
          "summary": "",
          "local_metric": false,
          "display_name": "",
          "company_profile_name": "",
          "geocode": false
        },
        {
          "type": "number",
          "api_name": "facet_linkedin_employee_count",
          "hidden": false,
          "options": [],
          "summary": "",
          "local_metric": false,
          "display_name": "",
          "company_profile_name": "",
          "geocode": false
        },
        {
          "type": "date",
          "api_name": "as_of_date",
          "hidden": false,
          "options": [
            "-default_sort"
          ],
          "summary": "",
          "local_metric": false,
          "display_name": "",
          "company_profile_name": "",
          "geocode": false
        },
        {
          "type": "number",
          "api_name": "dataset_row_id",
          "hidden": true,
          "options": [],
          "summary": "",
          "local_metric": false,
          "display_name": null,
          "company_profile_name": null,
          "geocode": false
        },
        {
          "type": "string",
          "api_name": "linkedin_headcount_facet_type",
          "hidden": false,
          "options": [],
          "summary": "",
          "local_metric": false,
          "display_name": "",
          "company_profile_name": "",
          "geocode": false
        },
        {
          "type": "string",
          "api_name": "linkedin_headcount_facet_value",
          "hidden": false,
          "options": [],
          "summary": "",
          "local_metric": false,
          "display_name": "",
          "company_profile_name": "",
          "geocode": false
        },
        {
          "type": "string",
          "api_name": "linkedin_headcount_facet_name",
          "hidden": false,
          "options": [],
          "summary": "",
          "local_metric": false,
          "display_name": "",
          "company_profile_name": "",
          "geocode": false
        },
        {
          "type": "string",
          "api_name": "linkedin_profile_url",
          "hidden": false,
          "options": [],
          "summary": "",
          "local_metric": false,
          "display_name": "",
          "company_profile_name": "",
          "geocode": false
        },
        {
          "type": "string",
          "api_name": "company_website",
          "hidden": false,
          "options": [],
          "summary": "",
          "local_metric": false,
          "display_name": "",
          "company_profile_name": "",
          "geocode": false
        },
        {
          "type": "string",
          "api_name": "company_website_domain",
          "hidden": false,
          "options": [],
          "summary": "",
          "local_metric": false,
          "display_name": "",
          "company_profile_name": "",
          "geocode": false
        },
        {
          "type": "number",
          "api_name": "company_id",
          "hidden": true,
          "options": [],
          "summary": "",
          "local_metric": false,
          "display_name": null,
          "company_profile_name": null,
          "geocode": false
        },
        {
          "type": "number",
          "api_name": "total_rows",
          "hidden": true,
          "options": [],
          "summary": "",
          "local_metric": false,
          "display_name": "",
          "company_profile_name": "",
          "geocode": false
        }
      ],
      "rows": [
        [
          "35625249",
          "https://www.sketch.com/",
          "Sketch",
          "sketch.com",
          6,
          "2024-02-28T00:00:00Z",
          41260836,
          "CURRENT_FUNCTION",
          "5",
          "Community and Social Services",
          "https://www.linkedin.com/company/sketchbv",
          "https://sketch.com/",
          "sketch.com",
          673947,
          1411
        ],
        [
          "35625249",
          "https://www.sketch.com/",
          "Sketch",
          "sketch.com",
          13,
          "2024-02-28T00:00:00Z",
          41260818,
          "GEO_REGION",
          "106057199",
          "Brazil",
          "https://www.linkedin.com/company/sketchbv",
          "https://sketch.com/",
          "sketch.com",
          673947,
          1411
        ],
        [
          "35625249",
          "https://www.sketch.com/",
          "Sketch",
          "sketch.com",
          5,
          "2024-02-28T00:00:00Z",
          41260838,
          "CURRENT_FUNCTION",
          "15",
          "Marketing",
          "https://www.linkedin.com/company/sketchbv",
          "https://sketch.com/",
          "sketch.com",
          673947,
          1411
        ],
        [
          "35625249",
          "https://www.sketch.com/",
          "Sketch",
          "sketch.com",
          4,
          "2024-02-28T00:00:00Z",
          41260841,
          "CURRENT_FUNCTION",
          "14",
          "Legal",
          "https://www.linkedin.com/company/sketchbv",
          "https://sketch.com/",
          "sketch.com",
          673947,
          1411
        ],
        [
          "35625249",
          "https://www.sketch.com/",
          "Sketch",
          "sketch.com",
          10,
          "2024-02-28T00:00:00Z",
          41260824,
          "GEO_REGION",
          "90009790",
          "Greater Madrid Metropolitan Area",
          "https://www.linkedin.com/company/sketchbv",
          "https://sketch.com/",
          "sketch.com",
          673947,
          1411
        ],
        [
          "35625249",
          "https://www.sketch.com/",
          "Sketch",
          "sketch.com",
          8,
          "2024-02-28T00:00:00Z",
          41260826,
          "GEO_REGION",
          "105088894",
          "Barcelona",
          "https://www.linkedin.com/company/sketchbv",
          "https://sketch.com/",
          "sketch.com",
          673947,
          1411
        ],
        [
          "35625249",
          "https://www.sketch.com/",
          "Sketch",
          "sketch.com",
          24,
          "2024-02-28T00:00:00Z",
          41260829,
          "CURRENT_FUNCTION",
          "4",
          "Business Development",
          "https://www.linkedin.com/company/sketchbv",
          "https://sketch.com/",
          "sketch.com",
          673947,
          1411
        ],
        [
          "35625249",
          "https://www.sketch.com/",
          "Sketch",
          "sketch.com",
          14,
          "2024-02-28T00:00:00Z",
          41260832,
          "CURRENT_FUNCTION",
          "26",
          "Customer Success and Support",
          "https://www.linkedin.com/company/sketchbv",
          "https://sketch.com/",
          "sketch.com",
          673947,
          1411
        ],
        [
          "35625249",
          "https://www.sketch.com/",
          "Sketch",
          "sketch.com",
          7,
          "2024-02-28T00:00:00Z",
          41260835,
          "CURRENT_FUNCTION",
          "2",
          "Administrative",
          "https://www.linkedin.com/company/sketchbv",
          "https://sketch.com/",
          "sketch.com",
          673947,
          1411
        ],
        [
          "35625249",
          "https://www.sketch.com/",
          "Sketch",
          "sketch.com",
          4,
          "2024-02-28T00:00:00Z",
          41260840,
          "CURRENT_FUNCTION",
          "12",
          "Human Resources",
          "https://www.linkedin.com/company/sketchbv",
          "https://sketch.com/",
          "sketch.com",
          673947,
          1411
        ],
        [
          "35625249",
          "https://www.sketch.com/",
          "Sketch",
          "sketch.com",
          62,
          "2024-02-28T00:00:00Z",
          41260827,
          "CURRENT_FUNCTION",
          "3",
          "Arts and Design",
          "https://www.linkedin.com/company/sketchbv",
          "https://sketch.com/",
          "sketch.com",
          673947,
          1411
        ],
        [
          "35625249",
          "https://www.sketch.com/",
          "Sketch",
          "sketch.com",
          15,
          "2024-02-28T00:00:00Z",
          41260831,
          "CURRENT_FUNCTION",
          "13",
          "Information Technology",
          "https://www.linkedin.com/company/sketchbv",
          "https://sketch.com/",
          "sketch.com",
          673947,
          1411
        ],
        [
          "35625249",
          "https://www.sketch.com/",
          "Sketch",
          "sketch.com",
          10,
          "2024-02-28T00:00:00Z",
          41260822,
          "GEO_REGION",
          "100994331",
          "Madrid",
          "https://www.linkedin.com/company/sketchbv",
          "https://sketch.com/",
          "sketch.com",
          673947,
          1411
        ],
        [
          "35625249",
          "https://www.sketch.com/",
          "Sketch",
          "sketch.com",
          11,
          "2024-02-28T00:00:00Z",
          41260821,
          "GEO_REGION",
          "106155005",
          "Egypt",
          "https://www.linkedin.com/company/sketchbv",
          "https://sketch.com/",
          "sketch.com",
          673947,
          1411
        ],
        [
          "35625249",
          "https://www.sketch.com/",
          "Sketch",
          "sketch.com",
          9,
          "2024-02-28T00:00:00Z",
          41260825,
          "GEO_REGION",
          "90009706",
          "The Randstad, Netherlands",
          "https://www.linkedin.com/company/sketchbv",
          "https://sketch.com/",
          "sketch.com",
          673947,
          1411
        ],
        [
          "35625249",
          "https://www.sketch.com/",
          "Sketch",
          "sketch.com",
          60,
          "2024-02-28T00:00:00Z",
          41260828,
          "CURRENT_FUNCTION",
          "8",
          "Engineering",
          "https://www.linkedin.com/company/sketchbv",
          "https://sketch.com/",
          "sketch.com",
          673947,
          1411
        ],
        [
          "35625249",
          "https://www.sketch.com/",
          "Sketch",
          "sketch.com",
          13,
          "2024-02-28T00:00:00Z",
          41260817,
          "GEO_REGION",
          "102299470",
          "England, United Kingdom",
          "https://www.linkedin.com/company/sketchbv",
          "https://sketch.com/",
          "sketch.com",
          673947,
          1411
        ],
        [
          "35625249",
          "https://www.sketch.com/",
          "Sketch",
          "sketch.com",
          10,
          "2024-02-28T00:00:00Z",
          41260823,
          "GEO_REGION",
          "103335767",
          "Community of Madrid, Spain",
          "https://www.linkedin.com/company/sketchbv",
          "https://sketch.com/",
          "sketch.com",
          673947,
          1411
        ],
        [
          "35625249",
          "https://www.sketch.com/",
          "Sketch",
          "sketch.com",
          5,
          "2024-02-28T00:00:00Z",
          41260839,
          "CURRENT_FUNCTION",
          "7",
          "Education",
          "https://www.linkedin.com/company/sketchbv",
          "https://sketch.com/",
          "sketch.com",
          673947,
          1411
        ],
        [
          "35625249",
          "https://www.sketch.com/",
          "Sketch",
          "sketch.com",
          18,
          "2024-02-28T00:00:00Z",
          41260815,
          "GEO_REGION",
          "101165590",
          "United Kingdom",
          "https://www.linkedin.com/company/sketchbv",
          "https://sketch.com/",
          "sketch.com",
          673947,
          1411
        ],
        [
          "35625249",
          "https://www.sketch.com/",
          "Sketch",
          "sketch.com",
          26,
          "2024-02-28T00:00:00Z",
          41260812,
          "GEO_REGION",
          "102713980",
          "India",
          "https://www.linkedin.com/company/sketchbv",
          "https://sketch.com/",
          "sketch.com",
          673947,
          1411
        ],
        [
          "35625249",
          "https://www.sketch.com/",
          "Sketch",
          "sketch.com",
          11,
          "2024-02-28T00:00:00Z",
          41260819,
          "GEO_REGION",
          "100358611",
          "Minas Gerais, Brazil",
          "https://www.linkedin.com/company/sketchbv",
          "https://sketch.com/",
          "sketch.com",
          673947,
          1411
        ],
        [
          "35625249",
          "https://www.sketch.com/",
          "Sketch",
          "sketch.com",
          5,
          "2024-02-28T00:00:00Z",
          41260837,
          "CURRENT_FUNCTION",
          "1",
          "Accounting",
          "https://www.linkedin.com/company/sketchbv",
          "https://sketch.com/",
          "sketch.com",
          673947,
          1411
        ],
        [
          "35625249",
          "https://www.sketch.com/",
          "Sketch",
          "sketch.com",
          14,
          "2024-02-28T00:00:00Z",
          41260816,
          "GEO_REGION",
          "102890719",
          "Netherlands",
          "https://www.linkedin.com/company/sketchbv",
          "https://sketch.com/",
          "sketch.com",
          673947,
          1411
        ],
        [
          "35625249",
          "https://www.sketch.com/",
          "Sketch",
          "sketch.com",
          11,
          "2024-02-28T00:00:00Z",
          41260833,
          "CURRENT_FUNCTION",
          "25",
          "Sales",
          "https://www.linkedin.com/company/sketchbv",
          "https://sketch.com/",
          "sketch.com",
          673947,
          1411
        ],
        [
          "35625249",
          "https://www.sketch.com/",
          "Sketch",
          "sketch.com",
          16,
          "2024-02-28T00:00:00Z",
          41260830,
          "CURRENT_FUNCTION",
          "18",
          "Operations",
          "https://www.linkedin.com/company/sketchbv",
          "https://sketch.com/",
          "sketch.com",
          673947,
          1411
        ],
        [
          "35625249",
          "https://www.sketch.com/",
          "Sketch",
          "sketch.com",
          26,
          "2024-02-28T00:00:00Z",
          41260813,
          "GEO_REGION",
          "105646813",
          "Spain",
          "https://www.linkedin.com/company/sketchbv",
          "https://sketch.com/",
          "sketch.com",
          673947,
          1411
        ],
        [
          "35625249",
          "https://www.sketch.com/",
          "Sketch",
          "sketch.com",
          21,
          "2024-02-28T00:00:00Z",
          41260814,
          "GEO_REGION",
          "100364837",
          "Portugal",
          "https://www.linkedin.com/company/sketchbv",
          "https://sketch.com/",
          "sketch.com",
          673947,
          1411
        ],
        [
          "35625249",
          "https://www.sketch.com/",
          "Sketch",
          "sketch.com",
          9,
          "2024-02-28T00:00:00Z",
          41260834,
          "CURRENT_FUNCTION",
          "16",
          "Media and Communication",
          "https://www.linkedin.com/company/sketchbv",
          "https://sketch.com/",
          "sketch.com",
          673947,
          1411
        ],
        [
          "35625249",
          "https://www.sketch.com/",
          "Sketch",
          "sketch.com",
          11,
          "2024-02-28T00:00:00Z",
          41260820,
          "GEO_REGION",
          "103644278",
          "United States",
          "https://www.linkedin.com/company/sketchbv",
          "https://sketch.com/",
          "sketch.com",
          673947,
          1411
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          95,
          "2023-12-22T00:00:00Z",
          37687823,
          "CURRENT_FUNCTION",
          "19",
          "Product Management",
          "https://www.linkedin.com/company/microstrategy",
          "http://www.microstrategy.com",
          "microstrategy.com",
          680992,
          1411
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          876,
          "2023-12-22T00:00:00Z",
          37687802,
          "GEO_REGION",
          "102890883",
          "China",
          "https://www.linkedin.com/company/microstrategy",
          "http://www.microstrategy.com",
          "microstrategy.com",
          680992,
          1411
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          677,
          "2023-12-22T00:00:00Z",
          37687803,
          "GEO_REGION",
          "90000097",
          "Washington DC-Baltimore Area",
          "https://www.linkedin.com/company/microstrategy",
          "http://www.microstrategy.com",
          "microstrategy.com",
          680992,
          1411
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          1082,
          "2023-12-22T00:00:00Z",
          37687801,
          "GEO_REGION",
          "103644278",
          "United States",
          "https://www.linkedin.com/company/microstrategy",
          "http://www.microstrategy.com",
          "microstrategy.com",
          680992,
          1411
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          428,
          "2023-12-22T00:00:00Z",
          37687805,
          "GEO_REGION",
          "105072130",
          "Poland",
          "https://www.linkedin.com/company/microstrategy",
          "http://www.microstrategy.com",
          "microstrategy.com",
          680992,
          1411
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          95,
          "2023-12-22T00:00:00Z",
          37687824,
          "CURRENT_FUNCTION",
          "22",
          "Quality Assurance",
          "https://www.linkedin.com/company/microstrategy",
          "http://www.microstrategy.com",
          "microstrategy.com",
          680992,
          1411
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          80,
          "2023-12-22T00:00:00Z",
          37687829,
          "CURRENT_FUNCTION",
          "10",
          "Finance",
          "https://www.linkedin.com/company/microstrategy",
          "http://www.microstrategy.com",
          "microstrategy.com",
          680992,
          1411
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          119,
          "2023-12-22T00:00:00Z",
          37687822,
          "CURRENT_FUNCTION",
          "1",
          "Accounting",
          "https://www.linkedin.com/company/microstrategy",
          "http://www.microstrategy.com",
          "microstrategy.com",
          680992,
          1411
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          573,
          "2023-12-22T00:00:00Z",
          37687804,
          "GEO_REGION",
          "101630962",
          "Virginia, United States",
          "https://www.linkedin.com/company/microstrategy",
          "http://www.microstrategy.com",
          "microstrategy.com",
          680992,
          1411
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          335,
          "2023-12-22T00:00:00Z",
          37687810,
          "GEO_REGION",
          "90009563",
          "Hangzhou-Shaoxing Metropolitan Area",
          "https://www.linkedin.com/company/microstrategy",
          "http://www.microstrategy.com",
          "microstrategy.com",
          680992,
          1411
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          95,
          "2023-12-22T00:00:00Z",
          37687824,
          "CURRENT_FUNCTION",
          "22",
          "Quality Assurance",
          "https://www.linkedin.com/company/microstrategy",
          "http://www.microstrategy.com",
          "microstrategy.com",
          680992,
          1411
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          85,
          "2023-12-22T00:00:00Z",
          37687827,
          "CURRENT_FUNCTION",
          "12",
          "Human Resources",
          "https://www.linkedin.com/company/microstrategy",
          "http://www.microstrategy.com",
          "microstrategy.com",
          680992,
          1411
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          321,
          "2023-12-22T00:00:00Z",
          37687811,
          "GEO_REGION",
          "101821877",
          "Hangzhou",
          "https://www.linkedin.com/company/microstrategy",
          "http://www.microstrategy.com",
          "microstrategy.com",
          680992,
          1411
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          340,
          "2023-12-22T00:00:00Z",
          37687809,
          "GEO_REGION",
          "105076658",
          "Warsaw",
          "https://www.linkedin.com/company/microstrategy",
          "http://www.microstrategy.com",
          "microstrategy.com",
          680992,
          1411
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          94,
          "2023-12-22T00:00:00Z",
          37687825,
          "CURRENT_FUNCTION",
          "20",
          "Program and Project Management",
          "https://www.linkedin.com/company/microstrategy",
          "http://www.microstrategy.com",
          "microstrategy.com",
          680992,
          1411
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          91,
          "2023-12-22T00:00:00Z",
          37687826,
          "CURRENT_FUNCTION",
          "7",
          "Education",
          "https://www.linkedin.com/company/microstrategy",
          "http://www.microstrategy.com",
          "microstrategy.com",
          680992,
          1411
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          428,
          "2023-12-22T00:00:00Z",
          37687805,
          "GEO_REGION",
          "105072130",
          "Poland",
          "https://www.linkedin.com/company/microstrategy",
          "http://www.microstrategy.com",
          "microstrategy.com",
          680992,
          1411
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          573,
          "2023-12-22T00:00:00Z",
          37687804,
          "GEO_REGION",
          "101630962",
          "Virginia, United States",
          "https://www.linkedin.com/company/microstrategy",
          "http://www.microstrategy.com",
          "microstrategy.com",
          680992,
          1411
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          75,
          "2023-12-22T00:00:00Z",
          37687830,
          "CURRENT_FUNCTION",
          "2",
          "Administrative",
          "https://www.linkedin.com/company/microstrategy",
          "http://www.microstrategy.com",
          "microstrategy.com",
          680992,
          1411
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          368,
          "2023-12-22T00:00:00Z",
          37687806,
          "GEO_REGION",
          "102996679",
          "Mazowieckie, Poland",
          "https://www.linkedin.com/company/microstrategy",
          "http://www.microstrategy.com",
          "microstrategy.com",
          680992,
          1411
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          83,
          "2023-12-22T00:00:00Z",
          37687828,
          "CURRENT_FUNCTION",
          "3",
          "Arts and Design",
          "https://www.linkedin.com/company/microstrategy",
          "http://www.microstrategy.com",
          "microstrategy.com",
          680992,
          1411
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          94,
          "2023-12-22T00:00:00Z",
          37687825,
          "CURRENT_FUNCTION",
          "20",
          "Program and Project Management",
          "https://www.linkedin.com/company/microstrategy",
          "http://www.microstrategy.com",
          "microstrategy.com",
          680992,
          1411
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          91,
          "2023-12-22T00:00:00Z",
          37687826,
          "CURRENT_FUNCTION",
          "7",
          "Education",
          "https://www.linkedin.com/company/microstrategy",
          "http://www.microstrategy.com",
          "microstrategy.com",
          680992,
          1411
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          85,
          "2023-12-22T00:00:00Z",
          37687827,
          "CURRENT_FUNCTION",
          "12",
          "Human Resources",
          "https://www.linkedin.com/company/microstrategy",
          "http://www.microstrategy.com",
          "microstrategy.com",
          680992,
          1411
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          118,
          "2023-12-22T00:00:00Z",
          37687813,
          "GEO_REGION",
          "101627305",
          "Vienna, VA",
          "https://www.linkedin.com/company/microstrategy",
          "http://www.microstrategy.com",
          "microstrategy.com",
          680992,
          1411
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          876,
          "2023-12-22T00:00:00Z",
          37687802,
          "GEO_REGION",
          "102890883",
          "China",
          "https://www.linkedin.com/company/microstrategy",
          "http://www.microstrategy.com",
          "microstrategy.com",
          680992,
          1411
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          677,
          "2023-12-22T00:00:00Z",
          37687803,
          "GEO_REGION",
          "90000097",
          "Washington DC-Baltimore Area",
          "https://www.linkedin.com/company/microstrategy",
          "http://www.microstrategy.com",
          "microstrategy.com",
          680992,
          1411
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          112,
          "2023-12-22T00:00:00Z",
          37687814,
          "GEO_REGION",
          "103873152",
          "Beijing, China",
          "https://www.linkedin.com/company/microstrategy",
          "http://www.microstrategy.com",
          "microstrategy.com",
          680992,
          1411
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          142,
          "2023-12-22T00:00:00Z",
          37687812,
          "GEO_REGION",
          "102713980",
          "India",
          "https://www.linkedin.com/company/microstrategy",
          "http://www.microstrategy.com",
          "microstrategy.com",
          680992,
          1411
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          343,
          "2023-12-22T00:00:00Z",
          37687808,
          "GEO_REGION",
          "106834892",
          "Zhejiang, China",
          "https://www.linkedin.com/company/microstrategy",
          "http://www.microstrategy.com",
          "microstrategy.com",
          680992,
          1411
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          321,
          "2023-12-22T00:00:00Z",
          37687811,
          "GEO_REGION",
          "101821877",
          "Hangzhou",
          "https://www.linkedin.com/company/microstrategy",
          "http://www.microstrategy.com",
          "microstrategy.com",
          680992,
          1411
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          335,
          "2023-12-22T00:00:00Z",
          37687810,
          "GEO_REGION",
          "90009563",
          "Hangzhou-Shaoxing Metropolitan Area",
          "https://www.linkedin.com/company/microstrategy",
          "http://www.microstrategy.com",
          "microstrategy.com",
          680992,
          1411
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          647,
          "2023-12-22T00:00:00Z",
          37687817,
          "CURRENT_FUNCTION",
          "25",
          "Sales",
          "https://www.linkedin.com/company/microstrategy",
          "http://www.microstrategy.com",
          "microstrategy.com",
          680992,
          1411
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          340,
          "2023-12-22T00:00:00Z",
          37687809,
          "GEO_REGION",
          "105076658",
          "Warsaw",
          "https://www.linkedin.com/company/microstrategy",
          "http://www.microstrategy.com",
          "microstrategy.com",
          680992,
          1411
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          112,
          "2023-12-22T00:00:00Z",
          37687814,
          "GEO_REGION",
          "103873152",
          "Beijing, China",
          "https://www.linkedin.com/company/microstrategy",
          "http://www.microstrategy.com",
          "microstrategy.com",
          680992,
          1411
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          480,
          "2023-12-22T00:00:00Z",
          37687818,
          "CURRENT_FUNCTION",
          "13",
          "Information Technology",
          "https://www.linkedin.com/company/microstrategy",
          "http://www.microstrategy.com",
          "microstrategy.com",
          680992,
          1411
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          768,
          "2023-12-22T00:00:00Z",
          37687816,
          "CURRENT_FUNCTION",
          "8",
          "Engineering",
          "https://www.linkedin.com/company/microstrategy",
          "http://www.microstrategy.com",
          "microstrategy.com",
          680992,
          1411
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          198,
          "2023-12-22T00:00:00Z",
          37687820,
          "CURRENT_FUNCTION",
          "4",
          "Business Development",
          "https://www.linkedin.com/company/microstrategy",
          "http://www.microstrategy.com",
          "microstrategy.com",
          680992,
          1411
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          359,
          "2023-12-22T00:00:00Z",
          37687819,
          "CURRENT_FUNCTION",
          "6",
          "Consulting",
          "https://www.linkedin.com/company/microstrategy",
          "http://www.microstrategy.com",
          "microstrategy.com",
          680992,
          1411
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          134,
          "2023-12-22T00:00:00Z",
          37687821,
          "CURRENT_FUNCTION",
          "18",
          "Operations",
          "https://www.linkedin.com/company/microstrategy",
          "http://www.microstrategy.com",
          "microstrategy.com",
          680992,
          1411
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          134,
          "2023-12-22T00:00:00Z",
          37687821,
          "CURRENT_FUNCTION",
          "18",
          "Operations",
          "https://www.linkedin.com/company/microstrategy",
          "http://www.microstrategy.com",
          "microstrategy.com",
          680992,
          1411
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          480,
          "2023-12-22T00:00:00Z",
          37687818,
          "CURRENT_FUNCTION",
          "13",
          "Information Technology",
          "https://www.linkedin.com/company/microstrategy",
          "http://www.microstrategy.com",
          "microstrategy.com",
          680992,
          1411
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          104,
          "2023-12-22T00:00:00Z",
          37687815,
          "GEO_REGION",
          "100446943",
          "Argentina",
          "https://www.linkedin.com/company/microstrategy",
          "http://www.microstrategy.com",
          "microstrategy.com",
          680992,
          1411
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          768,
          "2023-12-22T00:00:00Z",
          37687816,
          "CURRENT_FUNCTION",
          "8",
          "Engineering",
          "https://www.linkedin.com/company/microstrategy",
          "http://www.microstrategy.com",
          "microstrategy.com",
          680992,
          1411
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          118,
          "2023-12-22T00:00:00Z",
          37687813,
          "GEO_REGION",
          "101627305",
          "Vienna, VA",
          "https://www.linkedin.com/company/microstrategy",
          "http://www.microstrategy.com",
          "microstrategy.com",
          680992,
          1411
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          198,
          "2023-12-22T00:00:00Z",
          37687820,
          "CURRENT_FUNCTION",
          "4",
          "Business Development",
          "https://www.linkedin.com/company/microstrategy",
          "http://www.microstrategy.com",
          "microstrategy.com",
          680992,
          1411
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          343,
          "2023-12-22T00:00:00Z",
          37687808,
          "GEO_REGION",
          "106834892",
          "Zhejiang, China",
          "https://www.linkedin.com/company/microstrategy",
          "http://www.microstrategy.com",
          "microstrategy.com",
          680992,
          1411
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          142,
          "2023-12-22T00:00:00Z",
          37687812,
          "GEO_REGION",
          "102713980",
          "India",
          "https://www.linkedin.com/company/microstrategy",
          "http://www.microstrategy.com",
          "microstrategy.com",
          680992,
          1411
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          119,
          "2023-12-22T00:00:00Z",
          37687822,
          "CURRENT_FUNCTION",
          "1",
          "Accounting",
          "https://www.linkedin.com/company/microstrategy",
          "http://www.microstrategy.com",
          "microstrategy.com",
          680992,
          1411
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          95,
          "2023-12-22T00:00:00Z",
          37687823,
          "CURRENT_FUNCTION",
          "19",
          "Product Management",
          "https://www.linkedin.com/company/microstrategy",
          "http://www.microstrategy.com",
          "microstrategy.com",
          680992,
          1411
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          75,
          "2023-12-22T00:00:00Z",
          37687830,
          "CURRENT_FUNCTION",
          "2",
          "Administrative",
          "https://www.linkedin.com/company/microstrategy",
          "http://www.microstrategy.com",
          "microstrategy.com",
          680992,
          1411
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          647,
          "2023-12-22T00:00:00Z",
          37687817,
          "CURRENT_FUNCTION",
          "25",
          "Sales",
          "https://www.linkedin.com/company/microstrategy",
          "http://www.microstrategy.com",
          "microstrategy.com",
          680992,
          1411
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          365,
          "2023-12-22T00:00:00Z",
          37687807,
          "GEO_REGION",
          "90009828",
          "Warsaw Metropolitan Area",
          "https://www.linkedin.com/company/microstrategy",
          "http://www.microstrategy.com",
          "microstrategy.com",
          680992,
          1411
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          1082,
          "2023-12-22T00:00:00Z",
          37687801,
          "GEO_REGION",
          "103644278",
          "United States",
          "https://www.linkedin.com/company/microstrategy",
          "http://www.microstrategy.com",
          "microstrategy.com",
          680992,
          1411
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          359,
          "2023-12-22T00:00:00Z",
          37687819,
          "CURRENT_FUNCTION",
          "6",
          "Consulting",
          "https://www.linkedin.com/company/microstrategy",
          "http://www.microstrategy.com",
          "microstrategy.com",
          680992,
          1411
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          368,
          "2023-12-22T00:00:00Z",
          37687806,
          "GEO_REGION",
          "102996679",
          "Mazowieckie, Poland",
          "https://www.linkedin.com/company/microstrategy",
          "http://www.microstrategy.com",
          "microstrategy.com",
          680992,
          1411
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          104,
          "2023-12-22T00:00:00Z",
          37687815,
          "GEO_REGION",
          "100446943",
          "Argentina",
          "https://www.linkedin.com/company/microstrategy",
          "http://www.microstrategy.com",
          "microstrategy.com",
          680992,
          1411
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          365,
          "2023-12-22T00:00:00Z",
          37687807,
          "GEO_REGION",
          "90009828",
          "Warsaw Metropolitan Area",
          "https://www.linkedin.com/company/microstrategy",
          "http://www.microstrategy.com",
          "microstrategy.com",
          680992,
          1411
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          83,
          "2023-12-22T00:00:00Z",
          37687828,
          "CURRENT_FUNCTION",
          "3",
          "Arts and Design",
          "https://www.linkedin.com/company/microstrategy",
          "http://www.microstrategy.com",
          "microstrategy.com",
          680992,
          1411
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          80,
          "2023-12-22T00:00:00Z",
          37687829,
          "CURRENT_FUNCTION",
          "10",
          "Finance",
          "https://www.linkedin.com/company/microstrategy",
          "http://www.microstrategy.com",
          "microstrategy.com",
          680992,
          1411
        ],
        [
          "17932068",
          "https://www.lacework.com",
          "Lacework",
          "lacework.com",
          274,
          "2023-12-12T00:00:00Z",
          37662401,
          "CURRENT_FUNCTION",
          "8",
          "Engineering",
          "https://www.linkedin.com/company/lacework",
          "https://www.lacework.com/",
          "lacework.com",
          631280,
          1411
        ],
        [
          "17932068",
          "https://www.lacework.com",
          "Lacework",
          "lacework.com",
          29,
          "2023-12-12T00:00:00Z",
          37662409,
          "CURRENT_FUNCTION",
          "3",
          "Arts and Design",
          "https://www.linkedin.com/company/lacework",
          "https://www.lacework.com/",
          "lacework.com",
          631280,
          1411
        ],
        [
          "17932068",
          "https://www.lacework.com",
          "Lacework",
          "lacework.com",
          636,
          "2023-12-12T00:00:00Z",
          37662386,
          "GEO_REGION",
          "103644278",
          "United States",
          "https://www.linkedin.com/company/lacework",
          "https://www.lacework.com/",
          "lacework.com",
          631280,
          1411
        ],
        [
          "17932068",
          "https://www.lacework.com",
          "Lacework",
          "lacework.com",
          322,
          "2023-12-12T00:00:00Z",
          37662387,
          "GEO_REGION",
          "102095887",
          "California, United States",
          "https://www.linkedin.com/company/lacework",
          "https://www.lacework.com/",
          "lacework.com",
          631280,
          1411
        ],
        [
          "17932068",
          "https://www.lacework.com",
          "Lacework",
          "lacework.com",
          201,
          "2023-12-12T00:00:00Z",
          37662402,
          "CURRENT_FUNCTION",
          "25",
          "Sales",
          "https://www.linkedin.com/company/lacework",
          "https://www.lacework.com/",
          "lacework.com",
          631280,
          1411
        ],
        [
          "17932068",
          "https://www.lacework.com",
          "Lacework",
          "lacework.com",
          285,
          "2023-12-12T00:00:00Z",
          37662388,
          "GEO_REGION",
          "90000084",
          "San Francisco Bay Area",
          "https://www.linkedin.com/company/lacework",
          "https://www.lacework.com/",
          "lacework.com",
          631280,
          1411
        ],
        [
          "17932068",
          "https://www.lacework.com",
          "Lacework",
          "lacework.com",
          17,
          "2023-12-12T00:00:00Z",
          37662413,
          "CURRENT_FUNCTION",
          "20",
          "Program and Project Management",
          "https://www.linkedin.com/company/lacework",
          "https://www.lacework.com/",
          "lacework.com",
          631280,
          1411
        ],
        [
          "17932068",
          "https://www.lacework.com",
          "Lacework",
          "lacework.com",
          75,
          "2023-12-12T00:00:00Z",
          37662389,
          "GEO_REGION",
          "101165590",
          "United Kingdom",
          "https://www.linkedin.com/company/lacework",
          "https://www.lacework.com/",
          "lacework.com",
          631280,
          1411
        ],
        [
          "17932068",
          "https://www.lacework.com",
          "Lacework",
          "lacework.com",
          97,
          "2023-12-12T00:00:00Z",
          37662403,
          "CURRENT_FUNCTION",
          "13",
          "Information Technology",
          "https://www.linkedin.com/company/lacework",
          "https://www.lacework.com/",
          "lacework.com",
          631280,
          1411
        ],
        [
          "17932068",
          "https://www.lacework.com",
          "Lacework",
          "lacework.com",
          61,
          "2023-12-12T00:00:00Z",
          37662390,
          "GEO_REGION",
          "102277331",
          "San Francisco, CA",
          "https://www.linkedin.com/company/lacework",
          "https://www.lacework.com/",
          "lacework.com",
          631280,
          1411
        ]
      ],
      "is_trial_user": false
    }
    ```
    

### 6. Glassdoor Profile Metrics

Use this request to get the rating of a company on Glassdoor, number of reviews, business outlook, CEO approval rating etc.  

You either provide with a list of Crustdata’s `company_id`  or `company_website_domain` in the filters

- **CUrl**
    
    ```bash
    curl --request POST \
      --url https://api.crustdata.com/data_lab/glassdoor_profile_metric/Table/ \
      --header 'Accept: application/json, text/plain, */*' \
      --header 'Accept-Language: en-US,en;q=0.9' \
      --header 'Authorization: Token $token' \
      --header 'Content-Type: application/json' \
      --header 'Origin: https://crustdata.com' \
      --data '{
        "tickers": [],
        "dataset": {
          "name": "glassdoor_profile_metric",
          "id": "glassdoorprofilemetric"
        },
        "filters": {
          "op": "and",
          "conditions": [
            {"column": "company_id", "type": "in", "value": [680992,673947,631280,636304,631811], "allow_null": false}
          ]
        },
        "groups": [],
        "aggregations": [],
        "functions": [],
        "offset": 0,
        "count": 100,
        "sorts": []
      }'
    ```
    
- **Result**
    
    [JSON Hero](https://jsonhero.io/j/SdGsOnEIJ33x/editor)
    
    ```bash
    {
      "fields": [
        {
          "type": "string",
          "api_name": "linkedin_id",
          "hidden": true,
          "options": [],
          "summary": "",
          "local_metric": false,
          "display_name": "",
          "company_profile_name": "",
          "geocode": false
        },
        {
          "type": "string",
          "api_name": "company_website",
          "hidden": false,
          "options": [],
          "summary": "",
          "local_metric": false,
          "display_name": "",
          "company_profile_name": "",
          "geocode": false
        },
        {
          "type": "string",
          "api_name": "company_name",
          "hidden": false,
          "options": [],
          "summary": "",
          "local_metric": false,
          "display_name": "",
          "company_profile_name": "",
          "geocode": false
        },
        {
          "type": "string",
          "api_name": "company_website_domain",
          "hidden": false,
          "options": [],
          "summary": "",
          "local_metric": false,
          "display_name": "",
          "company_profile_name": "",
          "geocode": false
        },
        {
          "type": "date",
          "api_name": "as_of_date",
          "hidden": false,
          "options": [
            "-default_sort"
          ],
          "summary": "",
          "local_metric": false,
          "display_name": "",
          "company_profile_name": "",
          "geocode": false
        },
        {
          "type": "number",
          "api_name": "overall_rating",
          "hidden": false,
          "options": [],
          "summary": "",
          "local_metric": false,
          "display_name": "",
          "company_profile_name": "",
          "geocode": false
        },
        {
          "type": "number",
          "api_name": "culture_rating",
          "hidden": false,
          "options": [],
          "summary": "",
          "local_metric": false,
          "display_name": "",
          "company_profile_name": "",
          "geocode": false
        },
        {
          "type": "number",
          "api_name": "diversity_rating",
          "hidden": false,
          "options": [],
          "summary": "",
          "local_metric": false,
          "display_name": "",
          "company_profile_name": "",
          "geocode": false
        },
        {
          "type": "number",
          "api_name": "work_life_balance_rating",
          "hidden": false,
          "options": [],
          "summary": "",
          "local_metric": false,
          "display_name": "",
          "company_profile_name": "",
          "geocode": false
        },
        {
          "type": "number",
          "api_name": "senior_management_rating",
          "hidden": false,
          "options": [],
          "summary": "",
          "local_metric": false,
          "display_name": "",
          "company_profile_name": "",
          "geocode": false
        },
        {
          "type": "number",
          "api_name": "compensation_rating",
          "hidden": false,
          "options": [],
          "summary": "",
          "local_metric": false,
          "display_name": "",
          "company_profile_name": "",
          "geocode": false
        },
        {
          "type": "number",
          "api_name": "career_opportunities_rating",
          "hidden": false,
          "options": [],
          "summary": "",
          "local_metric": false,
          "display_name": "",
          "company_profile_name": "",
          "geocode": false
        },
        {
          "type": "number",
          "api_name": "recommend_to_friend_pct",
          "hidden": false,
          "options": [],
          "summary": "",
          "local_metric": false,
          "display_name": "",
          "company_profile_name": "",
          "geocode": false
        },
        {
          "type": "number",
          "api_name": "ceo_approval_pct",
          "hidden": false,
          "options": [],
          "summary": "",
          "local_metric": false,
          "display_name": "",
          "company_profile_name": "",
          "geocode": false
        },
        {
          "type": "number",
          "api_name": "business_outlook_pct",
          "hidden": false,
          "options": [],
          "summary": "",
          "local_metric": false,
          "display_name": "",
          "company_profile_name": "",
          "geocode": false
        },
        {
          "type": "number",
          "api_name": "glassdoor_profile_review_count",
          "hidden": false,
          "options": [],
          "summary": "",
          "local_metric": false,
          "display_name": "",
          "company_profile_name": "",
          "geocode": false
        },
        {
          "type": "number",
          "api_name": "dataset_row_id",
          "hidden": true,
          "options": [],
          "summary": "",
          "local_metric": false,
          "display_name": null,
          "company_profile_name": null,
          "geocode": false
        },
        {
          "type": "string",
          "api_name": "glassdoor_profile_url",
          "hidden": false,
          "options": [],
          "summary": "",
          "local_metric": false,
          "display_name": "",
          "company_profile_name": "",
          "geocode": false
        },
        {
          "type": "number",
          "api_name": "company_id",
          "hidden": true,
          "options": [],
          "summary": "",
          "local_metric": false,
          "display_name": null,
          "company_profile_name": null,
          "geocode": false
        },
        {
          "type": "number",
          "api_name": "total_rows",
          "hidden": true,
          "options": [],
          "summary": "",
          "local_metric": false,
          "display_name": "",
          "company_profile_name": "",
          "geocode": false
        }
      ],
      "rows": [
        [
          "3033823",
          "http://jumpcloud.com",
          "JumpCloud",
          "jumpcloud.com",
          "2024-01-07T00:00:00Z",
          3.45124,
          3.38798,
          3.67852,
          3.84519,
          3.13893,
          3.42953,
          3.06081,
          53,
          82,
          48,
          null,
          10358925,
          "https://www.glassdoor.co.in/Overview/Working-at-jumpcloud-EI_IE1446075.htm",
          631811,
          2512
        ],
        [
          "17932068",
          "https://www.lacework.com",
          "Lacework",
          "lacework.com",
          "2024-01-07T00:00:00Z",
          3.67224,
          3.57151,
          3.70108,
          3.42699,
          3.41481,
          4.24173,
          3.66685,
          64,
          68,
          59,
          null,
          10358663,
          "https://www.glassdoor.co.in/Overview/Working-at-lacework-EI_IE1373969.htm",
          631280,
          2512
        ],
        [
          "35625249",
          "https://www.sketch.com/",
          "Sketch",
          "sketch.com",
          "2023-12-15T00:00:00Z",
          4.81397,
          4.82756,
          4.60647,
          5,
          4.58143,
          4.7735,
          4.24984,
          91,
          100,
          69,
          null,
          10351760,
          "https://www.glassdoor.com/Overview/Working-at-sketch-EI_IE3068411.htm",
          673947,
          2512
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          "2023-12-14T00:00:00Z",
          3.79139,
          3.78391,
          4.08457,
          3.98375,
          3.29903,
          3.68142,
          3.57313,
          72,
          44,
          52,
          null,
          10347613,
          "https://www.glassdoor.com/Overview/Working-at-microstrategy-EI_IE8018.htm",
          680992,
          2512
        ],
        [
          "336243",
          "http://www.nowsecure.com",
          "NowSecure",
          "nowsecure.com",
          "2023-12-14T00:00:00Z",
          3.35782,
          3.25678,
          3.43557,
          3.20794,
          3.0963,
          3.72396,
          2.7581,
          52,
          52,
          44,
          null,
          10340407,
          "https://www.glassdoor.co.in/Overview/Working-at-nowsecure-EI_IE753560.htm",
          636304,
          2512
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          "2023-12-14T00:00:00Z",
          3.79139,
          3.78391,
          4.08457,
          3.98375,
          3.29903,
          3.68142,
          3.57313,
          72,
          44,
          52,
          null,
          10347613,
          "https://www.glassdoor.com/Overview/Working-at-microstrategy-EI_IE8018.htm",
          680992,
          2512
        ],
        [
          "17932068",
          "https://www.lacework.com",
          "Lacework",
          "lacework.com",
          "2023-12-09T00:00:00Z",
          3.66592,
          3.55772,
          3.73303,
          3.48027,
          3.40452,
          4.24256,
          3.6359,
          64,
          69,
          59,
          null,
          10326729,
          "https://www.glassdoor.co.in/Overview/Working-at-lacework-EI_IE1373969.htm",
          631280,
          2512
        ],
        [
          "3033823",
          "http://jumpcloud.com",
          "JumpCloud",
          "jumpcloud.com",
          "2023-12-09T00:00:00Z",
          3.45719,
          3.39712,
          3.68392,
          3.85088,
          3.14617,
          3.43255,
          3.07375,
          53,
          82,
          49,
          null,
          10326947,
          "https://www.glassdoor.co.in/Overview/Working-at-jumpcloud-EI_IE1446075.htm",
          631811,
          2512
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          "2023-11-29T00:00:00Z",
          3.78005,
          3.77406,
          4.15817,
          3.95615,
          3.29744,
          3.71042,
          3.56022,
          72,
          49,
          54,
          null,
          10316287,
          "https://www.glassdoor.com/Overview/Working-at-microstrategy-EI_IE8018.htm",
          680992,
          2512
        ],
        [
          "17932068",
          "https://www.lacework.com",
          "Lacework",
          "lacework.com",
          "2023-11-29T00:00:00Z",
          3.75364,
          3.64831,
          3.79233,
          3.54338,
          3.47932,
          4.28775,
          3.70777,
          67,
          73,
          62,
          null,
          10303197,
          "https://www.glassdoor.co.in/Overview/Working-at-lacework-EI_IE1373969.htm",
          631280,
          2512
        ],
        [
          "3033823",
          "http://jumpcloud.com",
          "JumpCloud",
          "jumpcloud.com",
          "2023-11-29T00:00:00Z",
          3.46299,
          3.40603,
          3.68921,
          3.85645,
          3.15324,
          3.43549,
          3.0864,
          54,
          81,
          49,
          null,
          10303661,
          "https://www.glassdoor.co.in/Overview/Working-at-jumpcloud-EI_IE1446075.htm",
          631811,
          2512
        ],
        [
          "35625249",
          "https://www.sketch.com/",
          "Sketch",
          "sketch.com",
          "2023-11-29T00:00:00Z",
          4.81397,
          4.82756,
          4.60647,
          5,
          4.58143,
          4.7735,
          4.24984,
          91,
          100,
          69,
          null,
          10314166,
          "https://www.glassdoor.com/Overview/Working-at-sketch-EI_IE3068411.htm",
          673947,
          2512
        ],
        [
          "336243",
          "http://www.nowsecure.com",
          "NowSecure",
          "nowsecure.com",
          "2023-11-29T00:00:00Z",
          3.36071,
          3.25607,
          3.43968,
          3.20678,
          3.10027,
          3.72756,
          2.76508,
          52,
          53,
          45,
          null,
          10306852,
          "https://www.glassdoor.co.in/Overview/Working-at-nowsecure-EI_IE753560.htm",
          636304,
          2512
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          "2023-11-29T00:00:00Z",
          3.78005,
          3.77406,
          4.15817,
          3.95615,
          3.29744,
          3.71042,
          3.56022,
          72,
          49,
          54,
          null,
          10316287,
          "https://www.glassdoor.com/Overview/Working-at-microstrategy-EI_IE8018.htm",
          680992,
          2512
        ],
        [
          "17932068",
          "https://www.lacework.com",
          "Lacework",
          "lacework.com",
          "2023-11-28T00:00:00Z",
          3.75364,
          3.64831,
          3.79233,
          3.54338,
          3.47932,
          4.28775,
          3.70777,
          67,
          73,
          62,
          null,
          10271730,
          "https://www.glassdoor.co.in/Overview/Working-at-lacework-EI_IE1373969.htm",
          631280,
          2512
        ],
        [
          "336243",
          "http://www.nowsecure.com",
          "NowSecure",
          "nowsecure.com",
          "2023-11-28T00:00:00Z",
          3.36071,
          3.25607,
          3.43968,
          3.20678,
          3.10027,
          3.72756,
          2.76508,
          52,
          53,
          45,
          null,
          10275385,
          "https://www.glassdoor.co.in/Overview/Working-at-nowsecure-EI_IE753560.htm",
          636304,
          2512
        ],
        [
          "3033823",
          "http://jumpcloud.com",
          "JumpCloud",
          "jumpcloud.com",
          "2023-11-28T00:00:00Z",
          3.46299,
          3.40603,
          3.68921,
          3.85645,
          3.15324,
          3.43549,
          3.0864,
          54,
          81,
          49,
          null,
          10272194,
          "https://www.glassdoor.co.in/Overview/Working-at-jumpcloud-EI_IE1446075.htm",
          631811,
          2512
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          "2023-11-28T00:00:00Z",
          3.78005,
          3.77406,
          4.15817,
          3.95615,
          3.29744,
          3.71042,
          3.56022,
          72,
          49,
          54,
          null,
          10284819,
          "https://www.glassdoor.com/Overview/Working-at-microstrategy-EI_IE8018.htm",
          680992,
          2512
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          "2023-11-28T00:00:00Z",
          3.78005,
          3.77406,
          4.15817,
          3.95615,
          3.29744,
          3.71042,
          3.56022,
          72,
          49,
          54,
          null,
          10284819,
          "https://www.glassdoor.com/Overview/Working-at-microstrategy-EI_IE8018.htm",
          680992,
          2512
        ],
        [
          "35625249",
          "https://www.sketch.com/",
          "Sketch",
          "sketch.com",
          "2023-11-28T00:00:00Z",
          4.81397,
          4.82756,
          4.60647,
          5,
          4.58143,
          4.7735,
          4.24984,
          91,
          100,
          69,
          null,
          10282698,
          "https://www.glassdoor.com/Overview/Working-at-sketch-EI_IE3068411.htm",
          673947,
          2512
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          "2023-11-27T00:00:00Z",
          3.78005,
          3.77406,
          4.15817,
          3.95615,
          3.29744,
          3.71042,
          3.56022,
          72,
          49,
          54,
          null,
          10253095,
          "https://www.glassdoor.com/Overview/Working-at-microstrategy-EI_IE8018.htm",
          680992,
          2512
        ],
        [
          "35625249",
          "https://www.sketch.com/",
          "Sketch",
          "sketch.com",
          "2023-11-27T00:00:00Z",
          4.81397,
          4.82756,
          4.60647,
          5,
          4.58143,
          4.7735,
          4.24984,
          91,
          100,
          69,
          null,
          10250974,
          "https://www.glassdoor.com/Overview/Working-at-sketch-EI_IE3068411.htm",
          673947,
          2512
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          "2023-11-27T00:00:00Z",
          3.78005,
          3.77406,
          4.15817,
          3.95615,
          3.29744,
          3.71042,
          3.56022,
          72,
          49,
          54,
          null,
          10253095,
          "https://www.glassdoor.com/Overview/Working-at-microstrategy-EI_IE8018.htm",
          680992,
          2512
        ],
        [
          "17932068",
          "https://www.lacework.com",
          "Lacework",
          "lacework.com",
          "2023-11-27T00:00:00Z",
          3.75364,
          3.64831,
          3.79233,
          3.54338,
          3.47932,
          4.28775,
          3.70777,
          67,
          73,
          62,
          null,
          10240005,
          "https://www.glassdoor.co.in/Overview/Working-at-lacework-EI_IE1373969.htm",
          631280,
          2512
        ],
        [
          "3033823",
          "http://jumpcloud.com",
          "JumpCloud",
          "jumpcloud.com",
          "2023-11-27T00:00:00Z",
          3.46299,
          3.40603,
          3.68921,
          3.85645,
          3.15324,
          3.43549,
          3.0864,
          54,
          81,
          49,
          null,
          10240469,
          "https://www.glassdoor.co.in/Overview/Working-at-jumpcloud-EI_IE1446075.htm",
          631811,
          2512
        ],
        [
          "336243",
          "http://www.nowsecure.com",
          "NowSecure",
          "nowsecure.com",
          "2023-11-27T00:00:00Z",
          3.36071,
          3.25607,
          3.43968,
          3.20678,
          3.10027,
          3.72756,
          2.76508,
          52,
          53,
          45,
          null,
          10243660,
          "https://www.glassdoor.co.in/Overview/Working-at-nowsecure-EI_IE753560.htm",
          636304,
          2512
        ],
        [
          "35625249",
          "https://www.sketch.com/",
          "Sketch",
          "sketch.com",
          "2023-11-26T00:00:00Z",
          4.81397,
          4.82756,
          4.60647,
          5,
          4.58143,
          4.7735,
          4.24984,
          91,
          100,
          69,
          null,
          9422658,
          "https://www.glassdoor.com/Overview/Working-at-sketch-EI_IE3068411.htm",
          673947,
          2512
        ],
        [
          "17932068",
          "https://www.lacework.com",
          "Lacework",
          "lacework.com",
          "2023-11-26T00:00:00Z",
          3.75364,
          3.64831,
          3.79233,
          3.54338,
          3.47932,
          4.28775,
          3.70777,
          67,
          73,
          62,
          null,
          10222325,
          "https://www.glassdoor.co.in/Overview/Working-at-lacework-EI_IE1373969.htm",
          631280,
          2512
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          "2023-11-26T00:00:00Z",
          3.78005,
          3.77406,
          4.15817,
          3.95615,
          3.29744,
          3.71042,
          3.56022,
          72,
          49,
          54,
          null,
          10228802,
          "https://www.glassdoor.com/Overview/Working-at-microstrategy-EI_IE8018.htm",
          680992,
          2512
        ],
        [
          "3033823",
          "http://jumpcloud.com",
          "JumpCloud",
          "jumpcloud.com",
          "2023-11-26T00:00:00Z",
          3.46299,
          3.40603,
          3.68921,
          3.85645,
          3.15324,
          3.43549,
          3.0864,
          54,
          81,
          49,
          null,
          10222663,
          "https://www.glassdoor.co.in/Overview/Working-at-jumpcloud-EI_IE1446075.htm",
          631811,
          2512
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          "2023-11-26T00:00:00Z",
          3.78005,
          3.77406,
          4.15817,
          3.95615,
          3.29744,
          3.71042,
          3.56022,
          72,
          49,
          54,
          null,
          10228802,
          "https://www.glassdoor.com/Overview/Working-at-microstrategy-EI_IE8018.htm",
          680992,
          2512
        ],
        [
          "336243",
          "http://www.nowsecure.com",
          "NowSecure",
          "nowsecure.com",
          "2023-11-26T00:00:00Z",
          3.36071,
          3.25607,
          3.43968,
          3.20678,
          3.10027,
          3.72756,
          2.76508,
          52,
          53,
          45,
          null,
          10224517,
          "https://www.glassdoor.co.in/Overview/Working-at-nowsecure-EI_IE753560.htm",
          636304,
          2512
        ],
        [
          "3033823",
          "http://jumpcloud.com",
          "JumpCloud",
          "jumpcloud.com",
          "2023-11-25T00:00:00Z",
          3.46299,
          3.40603,
          3.68921,
          3.85645,
          3.15324,
          3.43549,
          3.0864,
          54,
          81,
          49,
          null,
          10192615,
          "https://www.glassdoor.co.in/Overview/Working-at-jumpcloud-EI_IE1446075.htm",
          631811,
          2512
        ],
        [
          "336243",
          "http://www.nowsecure.com",
          "NowSecure",
          "nowsecure.com",
          "2023-11-25T00:00:00Z",
          3.36071,
          3.25607,
          3.43968,
          3.20678,
          3.10027,
          3.72756,
          2.76508,
          52,
          53,
          45,
          null,
          10195806,
          "https://www.glassdoor.co.in/Overview/Working-at-nowsecure-EI_IE753560.htm",
          636304,
          2512
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          "2023-11-25T00:00:00Z",
          3.78005,
          3.77406,
          4.15817,
          3.95615,
          3.29744,
          3.71042,
          3.56022,
          72,
          49,
          54,
          null,
          10205241,
          "https://www.glassdoor.com/Overview/Working-at-microstrategy-EI_IE8018.htm",
          680992,
          2512
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          "2023-11-25T00:00:00Z",
          3.78005,
          3.77406,
          4.15817,
          3.95615,
          3.29744,
          3.71042,
          3.56022,
          72,
          49,
          54,
          null,
          10205241,
          "https://www.glassdoor.com/Overview/Working-at-microstrategy-EI_IE8018.htm",
          680992,
          2512
        ],
        [
          "35625249",
          "https://www.sketch.com/",
          "Sketch",
          "sketch.com",
          "2023-11-25T00:00:00Z",
          4.81397,
          4.82756,
          4.60647,
          5,
          4.58143,
          4.7735,
          4.24984,
          91,
          100,
          69,
          null,
          10203120,
          "https://www.glassdoor.com/Overview/Working-at-sketch-EI_IE3068411.htm",
          673947,
          2512
        ],
        [
          "17932068",
          "https://www.lacework.com",
          "Lacework",
          "lacework.com",
          "2023-11-25T00:00:00Z",
          3.75364,
          3.64831,
          3.79233,
          3.54338,
          3.47932,
          4.28775,
          3.70777,
          67,
          73,
          62,
          null,
          10192151,
          "https://www.glassdoor.co.in/Overview/Working-at-lacework-EI_IE1373969.htm",
          631280,
          2512
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          "2023-11-24T00:00:00Z",
          3.78005,
          3.77406,
          4.15817,
          3.95615,
          3.29744,
          3.71042,
          3.56022,
          72,
          49,
          54,
          null,
          10173515,
          "https://www.glassdoor.com/Overview/Working-at-microstrategy-EI_IE8018.htm",
          680992,
          2512
        ],
        [
          "3033823",
          "http://jumpcloud.com",
          "JumpCloud",
          "jumpcloud.com",
          "2023-11-24T00:00:00Z",
          3.46299,
          3.40603,
          3.68921,
          3.85645,
          3.15324,
          3.43549,
          3.0864,
          54,
          81,
          49,
          null,
          10160889,
          "https://www.glassdoor.co.in/Overview/Working-at-jumpcloud-EI_IE1446075.htm",
          631811,
          2512
        ],
        [
          "35625249",
          "https://www.sketch.com/",
          "Sketch",
          "sketch.com",
          "2023-11-24T00:00:00Z",
          4.81397,
          4.82756,
          4.60647,
          5,
          4.58143,
          4.7735,
          4.24984,
          91,
          100,
          69,
          null,
          10171394,
          "https://www.glassdoor.com/Overview/Working-at-sketch-EI_IE3068411.htm",
          673947,
          2512
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          "2023-11-24T00:00:00Z",
          3.78005,
          3.77406,
          4.15817,
          3.95615,
          3.29744,
          3.71042,
          3.56022,
          72,
          49,
          54,
          null,
          10173515,
          "https://www.glassdoor.com/Overview/Working-at-microstrategy-EI_IE8018.htm",
          680992,
          2512
        ],
        [
          "17932068",
          "https://www.lacework.com",
          "Lacework",
          "lacework.com",
          "2023-11-24T00:00:00Z",
          3.75364,
          3.64831,
          3.79233,
          3.54338,
          3.47932,
          4.28775,
          3.70777,
          67,
          73,
          62,
          null,
          10160425,
          "https://www.glassdoor.co.in/Overview/Working-at-lacework-EI_IE1373969.htm",
          631280,
          2512
        ],
        [
          "336243",
          "http://www.nowsecure.com",
          "NowSecure",
          "nowsecure.com",
          "2023-11-24T00:00:00Z",
          3.36071,
          3.25607,
          3.43968,
          3.20678,
          3.10027,
          3.72756,
          2.76508,
          52,
          53,
          45,
          null,
          10164080,
          "https://www.glassdoor.co.in/Overview/Working-at-nowsecure-EI_IE753560.htm",
          636304,
          2512
        ],
        [
          "3033823",
          "http://jumpcloud.com",
          "JumpCloud",
          "jumpcloud.com",
          "2023-11-23T00:00:00Z",
          3.46299,
          3.40603,
          3.68921,
          3.85645,
          3.15324,
          3.43549,
          3.0864,
          54,
          81,
          49,
          null,
          10129163,
          "https://www.glassdoor.co.in/Overview/Working-at-jumpcloud-EI_IE1446075.htm",
          631811,
          2512
        ],
        [
          "17932068",
          "https://www.lacework.com",
          "Lacework",
          "lacework.com",
          "2023-11-23T00:00:00Z",
          3.75364,
          3.64831,
          3.79233,
          3.54338,
          3.47932,
          4.28775,
          3.70777,
          67,
          73,
          62,
          null,
          10128699,
          "https://www.glassdoor.co.in/Overview/Working-at-lacework-EI_IE1373969.htm",
          631280,
          2512
        ],
        [
          "35625249",
          "https://www.sketch.com/",
          "Sketch",
          "sketch.com",
          "2023-11-23T00:00:00Z",
          4.81397,
          4.82756,
          4.60647,
          5,
          4.58143,
          4.7735,
          4.24984,
          91,
          100,
          69,
          null,
          10139668,
          "https://www.glassdoor.com/Overview/Working-at-sketch-EI_IE3068411.htm",
          673947,
          2512
        ],
        [
          "336243",
          "http://www.nowsecure.com",
          "NowSecure",
          "nowsecure.com",
          "2023-11-23T00:00:00Z",
          3.36071,
          3.25607,
          3.43968,
          3.20678,
          3.10027,
          3.72756,
          2.76508,
          52,
          53,
          45,
          null,
          10132354,
          "https://www.glassdoor.co.in/Overview/Working-at-nowsecure-EI_IE753560.htm",
          636304,
          2512
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          "2023-11-23T00:00:00Z",
          3.78005,
          3.77406,
          4.15817,
          3.95615,
          3.29744,
          3.71042,
          3.56022,
          72,
          49,
          54,
          null,
          10141789,
          "https://www.glassdoor.com/Overview/Working-at-microstrategy-EI_IE8018.htm",
          680992,
          2512
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          "2023-11-23T00:00:00Z",
          3.78005,
          3.77406,
          4.15817,
          3.95615,
          3.29744,
          3.71042,
          3.56022,
          72,
          49,
          54,
          null,
          10141789,
          "https://www.glassdoor.com/Overview/Working-at-microstrategy-EI_IE8018.htm",
          680992,
          2512
        ],
        [
          "35625249",
          "https://www.sketch.com/",
          "Sketch",
          "sketch.com",
          "2023-11-22T00:00:00Z",
          4.81397,
          4.82756,
          4.60647,
          5,
          4.58143,
          4.7735,
          4.24984,
          91,
          100,
          69,
          null,
          10107942,
          "https://www.glassdoor.com/Overview/Working-at-sketch-EI_IE3068411.htm",
          673947,
          2512
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          "2023-11-22T00:00:00Z",
          3.78005,
          3.77406,
          4.15817,
          3.95615,
          3.29744,
          3.71042,
          3.56022,
          72,
          49,
          54,
          null,
          10110063,
          "https://www.glassdoor.com/Overview/Working-at-microstrategy-EI_IE8018.htm",
          680992,
          2512
        ],
        [
          "3033823",
          "http://jumpcloud.com",
          "JumpCloud",
          "jumpcloud.com",
          "2023-11-22T00:00:00Z",
          3.46299,
          3.40603,
          3.68921,
          3.85645,
          3.15324,
          3.43549,
          3.0864,
          54,
          81,
          49,
          null,
          10097437,
          "https://www.glassdoor.co.in/Overview/Working-at-jumpcloud-EI_IE1446075.htm",
          631811,
          2512
        ],
        [
          "336243",
          "http://www.nowsecure.com",
          "NowSecure",
          "nowsecure.com",
          "2023-11-22T00:00:00Z",
          3.36071,
          3.25607,
          3.43968,
          3.20678,
          3.10027,
          3.72756,
          2.76508,
          52,
          53,
          45,
          null,
          10100628,
          "https://www.glassdoor.co.in/Overview/Working-at-nowsecure-EI_IE753560.htm",
          636304,
          2512
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          "2023-11-22T00:00:00Z",
          3.78005,
          3.77406,
          4.15817,
          3.95615,
          3.29744,
          3.71042,
          3.56022,
          72,
          49,
          54,
          null,
          10110063,
          "https://www.glassdoor.com/Overview/Working-at-microstrategy-EI_IE8018.htm",
          680992,
          2512
        ],
        [
          "17932068",
          "https://www.lacework.com",
          "Lacework",
          "lacework.com",
          "2023-11-22T00:00:00Z",
          3.75364,
          3.64831,
          3.79233,
          3.54338,
          3.47932,
          4.28775,
          3.70777,
          67,
          73,
          62,
          null,
          10096973,
          "https://www.glassdoor.co.in/Overview/Working-at-lacework-EI_IE1373969.htm",
          631280,
          2512
        ],
        [
          "35625249",
          "https://www.sketch.com/",
          "Sketch",
          "sketch.com",
          "2023-11-21T00:00:00Z",
          4.81397,
          4.82756,
          4.60647,
          5,
          4.58143,
          4.7735,
          4.24984,
          91,
          100,
          69,
          null,
          10076216,
          "https://www.glassdoor.com/Overview/Working-at-sketch-EI_IE3068411.htm",
          673947,
          2512
        ],
        [
          "3033823",
          "http://jumpcloud.com",
          "JumpCloud",
          "jumpcloud.com",
          "2023-11-21T00:00:00Z",
          3.46299,
          3.40603,
          3.68921,
          3.85645,
          3.15324,
          3.43549,
          3.0864,
          54,
          81,
          49,
          null,
          10065711,
          "https://www.glassdoor.co.in/Overview/Working-at-jumpcloud-EI_IE1446075.htm",
          631811,
          2512
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          "2023-11-21T00:00:00Z",
          3.78005,
          3.77406,
          4.15817,
          3.95615,
          3.29744,
          3.71042,
          3.56022,
          72,
          49,
          54,
          null,
          10078337,
          "https://www.glassdoor.com/Overview/Working-at-microstrategy-EI_IE8018.htm",
          680992,
          2512
        ],
        [
          "17932068",
          "https://www.lacework.com",
          "Lacework",
          "lacework.com",
          "2023-11-21T00:00:00Z",
          3.75364,
          3.64831,
          3.79233,
          3.54338,
          3.47932,
          4.28775,
          3.70777,
          67,
          73,
          62,
          null,
          10065247,
          "https://www.glassdoor.co.in/Overview/Working-at-lacework-EI_IE1373969.htm",
          631280,
          2512
        ],
        [
          "336243",
          "http://www.nowsecure.com",
          "NowSecure",
          "nowsecure.com",
          "2023-11-21T00:00:00Z",
          3.36071,
          3.25607,
          3.43968,
          3.20678,
          3.10027,
          3.72756,
          2.76508,
          52,
          53,
          45,
          null,
          10068902,
          "https://www.glassdoor.co.in/Overview/Working-at-nowsecure-EI_IE753560.htm",
          636304,
          2512
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          "2023-11-21T00:00:00Z",
          3.78005,
          3.77406,
          4.15817,
          3.95615,
          3.29744,
          3.71042,
          3.56022,
          72,
          49,
          54,
          null,
          10078337,
          "https://www.glassdoor.com/Overview/Working-at-microstrategy-EI_IE8018.htm",
          680992,
          2512
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          "2023-11-20T00:00:00Z",
          3.78005,
          3.77406,
          4.15817,
          3.95615,
          3.29744,
          3.71042,
          3.56022,
          72,
          49,
          54,
          null,
          10046611,
          "https://www.glassdoor.com/Overview/Working-at-microstrategy-EI_IE8018.htm",
          680992,
          2512
        ],
        [
          "336243",
          "http://www.nowsecure.com",
          "NowSecure",
          "nowsecure.com",
          "2023-11-20T00:00:00Z",
          3.36071,
          3.25607,
          3.43968,
          3.20678,
          3.10027,
          3.72756,
          2.76508,
          52,
          53,
          45,
          null,
          10037176,
          "https://www.glassdoor.co.in/Overview/Working-at-nowsecure-EI_IE753560.htm",
          636304,
          2512
        ],
        [
          "3033823",
          "http://jumpcloud.com",
          "JumpCloud",
          "jumpcloud.com",
          "2023-11-20T00:00:00Z",
          3.46299,
          3.40603,
          3.68921,
          3.85645,
          3.15324,
          3.43549,
          3.0864,
          54,
          81,
          49,
          null,
          10033985,
          "https://www.glassdoor.co.in/Overview/Working-at-jumpcloud-EI_IE1446075.htm",
          631811,
          2512
        ],
        [
          "35625249",
          "https://www.sketch.com/",
          "Sketch",
          "sketch.com",
          "2023-11-20T00:00:00Z",
          4.81397,
          4.82756,
          4.60647,
          5,
          4.58143,
          4.7735,
          4.24984,
          91,
          100,
          69,
          null,
          10044490,
          "https://www.glassdoor.com/Overview/Working-at-sketch-EI_IE3068411.htm",
          673947,
          2512
        ],
        [
          "17932068",
          "https://www.lacework.com",
          "Lacework",
          "lacework.com",
          "2023-11-20T00:00:00Z",
          3.75364,
          3.64831,
          3.79233,
          3.54338,
          3.47932,
          4.28775,
          3.70777,
          67,
          73,
          62,
          null,
          10033521,
          "https://www.glassdoor.co.in/Overview/Working-at-lacework-EI_IE1373969.htm",
          631280,
          2512
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          "2023-11-20T00:00:00Z",
          3.78005,
          3.77406,
          4.15817,
          3.95615,
          3.29744,
          3.71042,
          3.56022,
          72,
          49,
          54,
          null,
          10046611,
          "https://www.glassdoor.com/Overview/Working-at-microstrategy-EI_IE8018.htm",
          680992,
          2512
        ],
        [
          "336243",
          "http://www.nowsecure.com",
          "NowSecure",
          "nowsecure.com",
          "2023-11-19T00:00:00Z",
          3.36071,
          3.25607,
          3.43968,
          3.20678,
          3.10027,
          3.72756,
          2.76508,
          52,
          53,
          45,
          null,
          10005450,
          "https://www.glassdoor.co.in/Overview/Working-at-nowsecure-EI_IE753560.htm",
          636304,
          2512
        ],
        [
          "3033823",
          "http://jumpcloud.com",
          "JumpCloud",
          "jumpcloud.com",
          "2023-11-19T00:00:00Z",
          3.46299,
          3.40603,
          3.68921,
          3.85645,
          3.15324,
          3.43549,
          3.0864,
          54,
          81,
          49,
          null,
          10002259,
          "https://www.glassdoor.co.in/Overview/Working-at-jumpcloud-EI_IE1446075.htm",
          631811,
          2512
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          "2023-11-19T00:00:00Z",
          3.78005,
          3.77406,
          4.15817,
          3.95615,
          3.29744,
          3.71042,
          3.56022,
          72,
          49,
          54,
          null,
          10014885,
          "https://www.glassdoor.com/Overview/Working-at-microstrategy-EI_IE8018.htm",
          680992,
          2512
        ],
        [
          "17932068",
          "https://www.lacework.com",
          "Lacework",
          "lacework.com",
          "2023-11-19T00:00:00Z",
          3.75364,
          3.64831,
          3.79233,
          3.54338,
          3.47932,
          4.28775,
          3.70777,
          67,
          73,
          62,
          null,
          10001795,
          "https://www.glassdoor.co.in/Overview/Working-at-lacework-EI_IE1373969.htm",
          631280,
          2512
        ],
        [
          "35625249",
          "https://www.sketch.com/",
          "Sketch",
          "sketch.com",
          "2023-11-19T00:00:00Z",
          4.81397,
          4.82756,
          4.60647,
          5,
          4.58143,
          4.7735,
          4.24984,
          91,
          100,
          69,
          null,
          10012764,
          "https://www.glassdoor.com/Overview/Working-at-sketch-EI_IE3068411.htm",
          673947,
          2512
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          "2023-11-19T00:00:00Z",
          3.78005,
          3.77406,
          4.15817,
          3.95615,
          3.29744,
          3.71042,
          3.56022,
          72,
          49,
          54,
          null,
          10014885,
          "https://www.glassdoor.com/Overview/Working-at-microstrategy-EI_IE8018.htm",
          680992,
          2512
        ],
        [
          "35625249",
          "https://www.sketch.com/",
          "Sketch",
          "sketch.com",
          "2023-11-18T00:00:00Z",
          4.81397,
          4.82756,
          4.60647,
          5,
          4.58143,
          4.7735,
          4.24984,
          91,
          100,
          69,
          null,
          9981038,
          "https://www.glassdoor.com/Overview/Working-at-sketch-EI_IE3068411.htm",
          673947,
          2512
        ],
        [
          "336243",
          "http://www.nowsecure.com",
          "NowSecure",
          "nowsecure.com",
          "2023-11-18T00:00:00Z",
          3.36071,
          3.25607,
          3.43968,
          3.20678,
          3.10027,
          3.72756,
          2.76508,
          52,
          53,
          45,
          null,
          9973724,
          "https://www.glassdoor.co.in/Overview/Working-at-nowsecure-EI_IE753560.htm",
          636304,
          2512
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          "2023-11-18T00:00:00Z",
          3.78005,
          3.77406,
          4.15817,
          3.95615,
          3.29744,
          3.71042,
          3.56022,
          72,
          49,
          54,
          null,
          9983159,
          "https://www.glassdoor.com/Overview/Working-at-microstrategy-EI_IE8018.htm",
          680992,
          2512
        ],
        [
          "17932068",
          "https://www.lacework.com",
          "Lacework",
          "lacework.com",
          "2023-11-18T00:00:00Z",
          3.75364,
          3.64831,
          3.79233,
          3.54338,
          3.47932,
          4.28775,
          3.70777,
          67,
          73,
          62,
          null,
          9970069,
          "https://www.glassdoor.co.in/Overview/Working-at-lacework-EI_IE1373969.htm",
          631280,
          2512
        ],
        [
          "3033823",
          "http://jumpcloud.com",
          "JumpCloud",
          "jumpcloud.com",
          "2023-11-18T00:00:00Z",
          3.46299,
          3.40603,
          3.68921,
          3.85645,
          3.15324,
          3.43549,
          3.0864,
          54,
          81,
          49,
          null,
          9970533,
          "https://www.glassdoor.co.in/Overview/Working-at-jumpcloud-EI_IE1446075.htm",
          631811,
          2512
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          "2023-11-18T00:00:00Z",
          3.78005,
          3.77406,
          4.15817,
          3.95615,
          3.29744,
          3.71042,
          3.56022,
          72,
          49,
          54,
          null,
          9983159,
          "https://www.glassdoor.com/Overview/Working-at-microstrategy-EI_IE8018.htm",
          680992,
          2512
        ],
        [
          "336243",
          "http://www.nowsecure.com",
          "NowSecure",
          "nowsecure.com",
          "2023-11-17T00:00:00Z",
          3.36071,
          3.25607,
          3.43968,
          3.20678,
          3.10027,
          3.72756,
          2.76508,
          52,
          53,
          45,
          null,
          9941998,
          "https://www.glassdoor.co.in/Overview/Working-at-nowsecure-EI_IE753560.htm",
          636304,
          2512
        ],
        [
          "3033823",
          "http://jumpcloud.com",
          "JumpCloud",
          "jumpcloud.com",
          "2023-11-17T00:00:00Z",
          3.46299,
          3.40603,
          3.68921,
          3.85645,
          3.15324,
          3.43549,
          3.0864,
          54,
          81,
          49,
          null,
          9938807,
          "https://www.glassdoor.co.in/Overview/Working-at-jumpcloud-EI_IE1446075.htm",
          631811,
          2512
        ],
        [
          "35625249",
          "https://www.sketch.com/",
          "Sketch",
          "sketch.com",
          "2023-11-17T00:00:00Z",
          4.81397,
          4.82756,
          4.60647,
          5,
          4.58143,
          4.7735,
          4.24984,
          91,
          100,
          69,
          null,
          9949312,
          "https://www.glassdoor.com/Overview/Working-at-sketch-EI_IE3068411.htm",
          673947,
          2512
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          "2023-11-17T00:00:00Z",
          3.78005,
          3.77406,
          4.15817,
          3.95615,
          3.29744,
          3.71042,
          3.56022,
          72,
          49,
          54,
          null,
          9951433,
          "https://www.glassdoor.com/Overview/Working-at-microstrategy-EI_IE8018.htm",
          680992,
          2512
        ],
        [
          "17932068",
          "https://www.lacework.com",
          "Lacework",
          "lacework.com",
          "2023-11-17T00:00:00Z",
          3.75364,
          3.64831,
          3.79233,
          3.54338,
          3.47932,
          4.28775,
          3.70777,
          67,
          73,
          62,
          null,
          9938343,
          "https://www.glassdoor.co.in/Overview/Working-at-lacework-EI_IE1373969.htm",
          631280,
          2512
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          "2023-11-17T00:00:00Z",
          3.78005,
          3.77406,
          4.15817,
          3.95615,
          3.29744,
          3.71042,
          3.56022,
          72,
          49,
          54,
          null,
          9951433,
          "https://www.glassdoor.com/Overview/Working-at-microstrategy-EI_IE8018.htm",
          680992,
          2512
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          "2023-11-16T00:00:00Z",
          3.78005,
          3.77406,
          4.15817,
          3.95615,
          3.29744,
          3.71042,
          3.56022,
          72,
          49,
          54,
          null,
          9919707,
          "https://www.glassdoor.com/Overview/Working-at-microstrategy-EI_IE8018.htm",
          680992,
          2512
        ],
        [
          "3033823",
          "http://jumpcloud.com",
          "JumpCloud",
          "jumpcloud.com",
          "2023-11-16T00:00:00Z",
          3.46299,
          3.40603,
          3.68921,
          3.85645,
          3.15324,
          3.43549,
          3.0864,
          54,
          81,
          49,
          null,
          9907081,
          "https://www.glassdoor.co.in/Overview/Working-at-jumpcloud-EI_IE1446075.htm",
          631811,
          2512
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          "2023-11-16T00:00:00Z",
          3.78005,
          3.77406,
          4.15817,
          3.95615,
          3.29744,
          3.71042,
          3.56022,
          72,
          49,
          54,
          null,
          9919707,
          "https://www.glassdoor.com/Overview/Working-at-microstrategy-EI_IE8018.htm",
          680992,
          2512
        ],
        [
          "35625249",
          "https://www.sketch.com/",
          "Sketch",
          "sketch.com",
          "2023-11-16T00:00:00Z",
          4.81397,
          4.82756,
          4.60647,
          5,
          4.58143,
          4.7735,
          4.24984,
          91,
          100,
          69,
          null,
          9917586,
          "https://www.glassdoor.com/Overview/Working-at-sketch-EI_IE3068411.htm",
          673947,
          2512
        ],
        [
          "17932068",
          "https://www.lacework.com",
          "Lacework",
          "lacework.com",
          "2023-11-16T00:00:00Z",
          3.75364,
          3.64831,
          3.79233,
          3.54338,
          3.47932,
          4.28775,
          3.70777,
          67,
          73,
          62,
          null,
          9906617,
          "https://www.glassdoor.co.in/Overview/Working-at-lacework-EI_IE1373969.htm",
          631280,
          2512
        ],
        [
          "336243",
          "http://www.nowsecure.com",
          "NowSecure",
          "nowsecure.com",
          "2023-11-16T00:00:00Z",
          3.36071,
          3.25607,
          3.43968,
          3.20678,
          3.10027,
          3.72756,
          2.76508,
          52,
          53,
          45,
          null,
          9910272,
          "https://www.glassdoor.co.in/Overview/Working-at-nowsecure-EI_IE753560.htm",
          636304,
          2512
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          "2023-11-15T00:00:00Z",
          3.78005,
          3.77406,
          4.15817,
          3.95615,
          3.29744,
          3.71042,
          3.56022,
          72,
          49,
          54,
          null,
          9887981,
          "https://www.glassdoor.com/Overview/Working-at-microstrategy-EI_IE8018.htm",
          680992,
          2512
        ],
        [
          "3033823",
          "http://jumpcloud.com",
          "JumpCloud",
          "jumpcloud.com",
          "2023-11-15T00:00:00Z",
          3.46299,
          3.40603,
          3.68921,
          3.85645,
          3.15324,
          3.43549,
          3.0864,
          54,
          81,
          49,
          null,
          9875355,
          "https://www.glassdoor.co.in/Overview/Working-at-jumpcloud-EI_IE1446075.htm",
          631811,
          2512
        ],
        [
          "336243",
          "http://www.nowsecure.com",
          "NowSecure",
          "nowsecure.com",
          "2023-11-15T00:00:00Z",
          3.36071,
          3.25607,
          3.43968,
          3.20678,
          3.10027,
          3.72756,
          2.76508,
          52,
          53,
          45,
          null,
          9878546,
          "https://www.glassdoor.co.in/Overview/Working-at-nowsecure-EI_IE753560.htm",
          636304,
          2512
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          "2023-11-15T00:00:00Z",
          3.78005,
          3.77406,
          4.15817,
          3.95615,
          3.29744,
          3.71042,
          3.56022,
          72,
          49,
          54,
          null,
          9887981,
          "https://www.glassdoor.com/Overview/Working-at-microstrategy-EI_IE8018.htm",
          680992,
          2512
        ],
        [
          "35625249",
          "https://www.sketch.com/",
          "Sketch",
          "sketch.com",
          "2023-11-15T00:00:00Z",
          4.81397,
          4.82756,
          4.60647,
          5,
          4.58143,
          4.7735,
          4.24984,
          91,
          100,
          69,
          null,
          9885860,
          "https://www.glassdoor.com/Overview/Working-at-sketch-EI_IE3068411.htm",
          673947,
          2512
        ],
        [
          "17932068",
          "https://www.lacework.com",
          "Lacework",
          "lacework.com",
          "2023-11-15T00:00:00Z",
          3.75364,
          3.64831,
          3.79233,
          3.54338,
          3.47932,
          4.28775,
          3.70777,
          67,
          73,
          62,
          null,
          9874891,
          "https://www.glassdoor.co.in/Overview/Working-at-lacework-EI_IE1373969.htm",
          631280,
          2512
        ],
        [
          "35625249",
          "https://www.sketch.com/",
          "Sketch",
          "sketch.com",
          "2023-11-14T00:00:00Z",
          4.81397,
          4.82756,
          4.60647,
          5,
          4.58143,
          4.7735,
          4.24984,
          91,
          100,
          69,
          null,
          9854134,
          "https://www.glassdoor.com/Overview/Working-at-sketch-EI_IE3068411.htm",
          673947,
          2512
        ],
        [
          "17932068",
          "https://www.lacework.com",
          "Lacework",
          "lacework.com",
          "2023-11-14T00:00:00Z",
          3.75364,
          3.64831,
          3.79233,
          3.54338,
          3.47932,
          4.28775,
          3.70777,
          67,
          73,
          62,
          null,
          9843165,
          "https://www.glassdoor.co.in/Overview/Working-at-lacework-EI_IE1373969.htm",
          631280,
          2512
        ]
      ],
      "is_trial_user": false
    }
    ```
    

### 7. G2 Profile Metrics

Use this request to get the rating of a company’s product on G2 and number of reviews etc.  

- **CUrl**
    
    ```bash
    curl --request POST \
      --url http://api.crustdata.com/data_lab/g2_profile_metrics/Table/ \
      --header 'Accept: application/json, text/plain, */*' \
      --header 'Accept-Language: en-US,en;q=0.9' \
      --header 'Authorization: Token $token' \
      --header 'Content-Type: application/json' \
      --header 'Origin: https://crustdata.com' \
      --data '{
        "tickers": [],
        "dataset": {
          "name": "g2_profile_metrics",
          "id": "g2profilemetric"
        },
        "filters": {
          "op": "or",
          "conditions": [
            {"column": "company_website_domain", "type": "=", "value": "microstrategy.com", "allow_null": false},
    			  {"column": "company_website_domain", "type": "=", "value": "lacework.com", "allow_null": false},
    				{"column": "company_website_domain", "type": "=", "value": "jumpcloud.com", "allow_null": false}
          ]
        },
        "groups": [],
        "aggregations": [],
        "functions": [],
        "offset": 0,
        "count": 100,
        "sorts": []
      }'
    
    ```
    
- **Result**
    
    [JSON Hero](https://jsonhero.io/j/DUeuNGh42nyO/editor)
    
    ```bash
    {
      "fields": [
        {
          "type": "string",
          "api_name": "linkedin_id",
          "hidden": true,
          "options": [],
          "summary": "",
          "local_metric": false,
          "display_name": "",
          "company_profile_name": "",
          "geocode": false
        },
        {
          "type": "string",
          "api_name": "company_website",
          "hidden": false,
          "options": [],
          "summary": "",
          "local_metric": false,
          "display_name": "",
          "company_profile_name": "",
          "geocode": false
        },
        {
          "type": "string",
          "api_name": "company_name",
          "hidden": false,
          "options": [],
          "summary": "",
          "local_metric": false,
          "display_name": "",
          "company_profile_name": "",
          "geocode": false
        },
        {
          "type": "string",
          "api_name": "company_website_domain",
          "hidden": false,
          "options": [],
          "summary": "",
          "local_metric": false,
          "display_name": "",
          "company_profile_name": "",
          "geocode": false
        },
        {
          "type": "date",
          "api_name": "as_of_date",
          "hidden": false,
          "options": [
            "-default_sort"
          ],
          "summary": "",
          "local_metric": false,
          "display_name": "",
          "company_profile_name": "",
          "geocode": false
        },
        {
          "type": "number",
          "api_name": "review_count",
          "hidden": false,
          "options": [],
          "summary": "",
          "local_metric": false,
          "display_name": "",
          "company_profile_name": "",
          "geocode": false
        },
        {
          "type": "number",
          "api_name": "average_rating",
          "hidden": false,
          "options": [],
          "summary": "",
          "local_metric": false,
          "display_name": "",
          "company_profile_name": "",
          "geocode": false
        },
        {
          "type": "number",
          "api_name": "g2_rating",
          "hidden": false,
          "options": [],
          "summary": "",
          "local_metric": false,
          "display_name": "",
          "company_profile_name": "",
          "geocode": false
        },
        {
          "type": "number",
          "api_name": "dataset_row_id",
          "hidden": true,
          "options": [],
          "summary": "",
          "local_metric": false,
          "display_name": null,
          "company_profile_name": null,
          "geocode": false
        },
        {
          "type": "string",
          "api_name": "title",
          "hidden": false,
          "options": [],
          "summary": "",
          "local_metric": false,
          "display_name": "",
          "company_profile_name": "",
          "geocode": false
        },
        {
          "type": "string",
          "api_name": "slug",
          "hidden": false,
          "options": [],
          "summary": "",
          "local_metric": false,
          "display_name": "",
          "company_profile_name": "",
          "geocode": false
        },
        {
          "type": "string",
          "api_name": "profile_url",
          "hidden": false,
          "options": [
            "url"
          ],
          "summary": "",
          "local_metric": false,
          "display_name": "",
          "company_profile_name": "",
          "geocode": false
        },
        {
          "type": "string",
          "api_name": "vendor_name",
          "hidden": false,
          "options": [],
          "summary": "",
          "local_metric": false,
          "display_name": "",
          "company_profile_name": "",
          "geocode": false
        },
        {
          "type": "string",
          "api_name": "description",
          "hidden": false,
          "options": [],
          "summary": "",
          "local_metric": false,
          "display_name": "",
          "company_profile_name": "",
          "geocode": false
        },
        {
          "type": "string",
          "api_name": "type",
          "hidden": false,
          "options": [],
          "summary": "",
          "local_metric": false,
          "display_name": "",
          "company_profile_name": "",
          "geocode": false
        },
        {
          "type": "number",
          "api_name": "company_id",
          "hidden": true,
          "options": [],
          "summary": "",
          "local_metric": false,
          "display_name": null,
          "company_profile_name": null,
          "geocode": false
        },
        {
          "type": "number",
          "api_name": "total_rows",
          "hidden": true,
          "options": [],
          "summary": "",
          "local_metric": false,
          "display_name": "",
          "company_profile_name": "",
          "geocode": false
        }
      ],
      "rows": [
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          "2023-07-28T00:00:00Z",
          464,
          8.35345,
          8.4,
          1234738,
          "microstrategy",
          "microstrategy",
          "https://www.g2.com/products/microstrategy/reviews",
          "MicroStrategy",
          "MicroStrategy provides a high performance, scalable Business Intelligence platform delivering insight with interactive dashboards and superior analytics.",
          "Software",
          680992,
          1266
        ],
        [
          "17932068",
          "https://www.lacework.com",
          "Lacework",
          "lacework.com",
          "2023-07-28T00:00:00Z",
          269,
          8.82836,
          8.8,
          1231195,
          "lacework",
          "lacework",
          "https://www.g2.com/products/lacework/reviews",
          "Lacework",
          "Lacework automates security and compliance across AWS, Azure, GCP, and private clouds, providing a comprehensive view of risks across cloud workloads and containers. Lacework’s unified cloud security platform provides unmatched visibility, automates intrusion detection, delivers one-click investigation, and simplifies cloud compliance.",
          "Software",
          631280,
          1266
        ],
        [
          "3033823",
          "http://jumpcloud.com",
          "JumpCloud",
          "jumpcloud.com",
          "2023-07-28T00:00:00Z",
          1802,
          9.08657,
          9.1,
          1231396,
          "jumpcloud",
          "jumpcloud",
          "https://www.g2.com/products/jumpcloud/reviews",
          "JumpCloud Inc.",
          "The JumpCloud Directory Platform reimagines the directory as a complete platform for identity, access, and device management.",
          "Software",
          631811,
          1266
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          "2023-07-28T00:00:00Z",
          464,
          8.35345,
          8.4,
          1234738,
          "microstrategy",
          "microstrategy",
          "https://www.g2.com/products/microstrategy/reviews",
          "MicroStrategy",
          "MicroStrategy provides a high performance, scalable Business Intelligence platform delivering insight with interactive dashboards and superior analytics.",
          "Software",
          680992,
          1266
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          "2023-07-27T00:00:00Z",
          464,
          8.35345,
          8.4,
          743350,
          "microstrategy",
          "microstrategy",
          "https://www.g2.com/products/microstrategy/reviews",
          "MicroStrategy",
          "MicroStrategy provides a high performance, scalable Business Intelligence platform delivering insight with interactive dashboards and superior analytics.",
          "Software",
          680992,
          1266
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          "2023-07-27T00:00:00Z",
          464,
          8.35345,
          8.4,
          743350,
          "microstrategy",
          "microstrategy",
          "https://www.g2.com/products/microstrategy/reviews",
          "MicroStrategy",
          "MicroStrategy provides a high performance, scalable Business Intelligence platform delivering insight with interactive dashboards and superior analytics.",
          "Software",
          680992,
          1266
        ],
        [
          "17932068",
          "https://www.lacework.com",
          "Lacework",
          "lacework.com",
          "2023-07-27T00:00:00Z",
          269,
          8.82836,
          8.8,
          741662,
          "lacework",
          "lacework",
          "https://www.g2.com/products/lacework/reviews",
          "Lacework",
          "Lacework automates security and compliance across AWS, Azure, GCP, and private clouds, providing a comprehensive view of risks across cloud workloads and containers. Lacework’s unified cloud security platform provides unmatched visibility, automates intrusion detection, delivers one-click investigation, and simplifies cloud compliance.",
          "Software",
          631280,
          1266
        ],
        [
          "3033823",
          "http://jumpcloud.com",
          "JumpCloud",
          "jumpcloud.com",
          "2023-07-27T00:00:00Z",
          1802,
          9.08657,
          9.1,
          741746,
          "jumpcloud",
          "jumpcloud",
          "https://www.g2.com/products/jumpcloud/reviews",
          "JumpCloud Inc.",
          "The JumpCloud Directory Platform reimagines the directory as a complete platform for identity, access, and device management.",
          "Software",
          631811,
          1266
        ],
        [
          "17932068",
          "https://www.lacework.com",
          "Lacework",
          "lacework.com",
          "2023-07-26T00:00:00Z",
          219,
          8.78539,
          8.8,
          1227348,
          "lacework",
          "lacework",
          "https://www.g2.com/products/lacework/reviews",
          "Lacework",
          "Lacework automates security and compliance across AWS, Azure, GCP, and private clouds, providing a comprehensive view of risks across cloud workloads and containers. Lacework’s unified cloud security platform provides unmatched visibility, automates intrusion detection, delivers one-click investigation, and simplifies cloud compliance.",
          "Software",
          631280,
          1266
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          "2023-07-26T00:00:00Z",
          463,
          8.34989,
          8.3,
          1230891,
          "microstrategy",
          "microstrategy",
          "https://www.g2.com/products/microstrategy/reviews",
          "MicroStrategy",
          "MicroStrategy provides a high performance, scalable Business Intelligence platform delivering insight with interactive dashboards and superior analytics.",
          "Software",
          680992,
          1266
        ],
        [
          "3033823",
          "http://jumpcloud.com",
          "JumpCloud",
          "jumpcloud.com",
          "2023-07-26T00:00:00Z",
          1667,
          9.08578,
          9.1,
          1227549,
          "jumpcloud",
          "jumpcloud",
          "https://www.g2.com/products/jumpcloud/reviews",
          "JumpCloud Inc.",
          "The JumpCloud Directory Platform reimagines the directory as a complete platform for identity, access, and device management.",
          "Software",
          631811,
          1266
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          "2023-07-26T00:00:00Z",
          463,
          8.34989,
          8.3,
          1230891,
          "microstrategy",
          "microstrategy",
          "https://www.g2.com/products/microstrategy/reviews",
          "MicroStrategy",
          "MicroStrategy provides a high performance, scalable Business Intelligence platform delivering insight with interactive dashboards and superior analytics.",
          "Software",
          680992,
          1266
        ],
        [
          "17932068",
          "https://www.lacework.com",
          "Lacework",
          "lacework.com",
          "2023-07-25T00:00:00Z",
          219,
          8.78539,
          8.8,
          1223762,
          "lacework",
          "lacework",
          "https://www.g2.com/products/lacework/reviews",
          "Lacework",
          "Lacework automates security and compliance across AWS, Azure, GCP, and private clouds, providing a comprehensive view of risks across cloud workloads and containers. Lacework’s unified cloud security platform provides unmatched visibility, automates intrusion detection, delivers one-click investigation, and simplifies cloud compliance.",
          "Software",
          631280,
          1266
        ],
        [
          "3033823",
          "http://jumpcloud.com",
          "JumpCloud",
          "jumpcloud.com",
          "2023-07-25T00:00:00Z",
          1667,
          9.08578,
          9.1,
          1223963,
          "jumpcloud",
          "jumpcloud",
          "https://www.g2.com/products/jumpcloud/reviews",
          "JumpCloud Inc.",
          "The JumpCloud Directory Platform reimagines the directory as a complete platform for identity, access, and device management.",
          "Software",
          631811,
          1266
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          "2023-07-25T00:00:00Z",
          463,
          8.34989,
          8.3,
          1227305,
          "microstrategy",
          "microstrategy",
          "https://www.g2.com/products/microstrategy/reviews",
          "MicroStrategy",
          "MicroStrategy provides a high performance, scalable Business Intelligence platform delivering insight with interactive dashboards and superior analytics.",
          "Software",
          680992,
          1266
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          "2023-07-25T00:00:00Z",
          463,
          8.34989,
          8.3,
          1227305,
          "microstrategy",
          "microstrategy",
          "https://www.g2.com/products/microstrategy/reviews",
          "MicroStrategy",
          "MicroStrategy provides a high performance, scalable Business Intelligence platform delivering insight with interactive dashboards and superior analytics.",
          "Software",
          680992,
          1266
        ],
        [
          "17932068",
          "https://www.lacework.com",
          "Lacework",
          "lacework.com",
          "2023-07-24T00:00:00Z",
          219,
          8.78539,
          8.8,
          1220176,
          "lacework",
          "lacework",
          "https://www.g2.com/products/lacework/reviews",
          "Lacework",
          "Lacework automates security and compliance across AWS, Azure, GCP, and private clouds, providing a comprehensive view of risks across cloud workloads and containers. Lacework’s unified cloud security platform provides unmatched visibility, automates intrusion detection, delivers one-click investigation, and simplifies cloud compliance.",
          "Software",
          631280,
          1266
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          "2023-07-24T00:00:00Z",
          463,
          8.34989,
          8.3,
          1223719,
          "microstrategy",
          "microstrategy",
          "https://www.g2.com/products/microstrategy/reviews",
          "MicroStrategy",
          "MicroStrategy provides a high performance, scalable Business Intelligence platform delivering insight with interactive dashboards and superior analytics.",
          "Software",
          680992,
          1266
        ],
        [
          "3033823",
          "http://jumpcloud.com",
          "JumpCloud",
          "jumpcloud.com",
          "2023-07-24T00:00:00Z",
          1667,
          9.08578,
          9.1,
          1220377,
          "jumpcloud",
          "jumpcloud",
          "https://www.g2.com/products/jumpcloud/reviews",
          "JumpCloud Inc.",
          "The JumpCloud Directory Platform reimagines the directory as a complete platform for identity, access, and device management.",
          "Software",
          631811,
          1266
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          "2023-07-24T00:00:00Z",
          463,
          8.34989,
          8.3,
          1223719,
          "microstrategy",
          "microstrategy",
          "https://www.g2.com/products/microstrategy/reviews",
          "MicroStrategy",
          "MicroStrategy provides a high performance, scalable Business Intelligence platform delivering insight with interactive dashboards and superior analytics.",
          "Software",
          680992,
          1266
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          "2023-07-23T00:00:00Z",
          463,
          8.34989,
          8.3,
          1220133,
          "microstrategy",
          "microstrategy",
          "https://www.g2.com/products/microstrategy/reviews",
          "MicroStrategy",
          "MicroStrategy provides a high performance, scalable Business Intelligence platform delivering insight with interactive dashboards and superior analytics.",
          "Software",
          680992,
          1266
        ],
        [
          "17932068",
          "https://www.lacework.com",
          "Lacework",
          "lacework.com",
          "2023-07-23T00:00:00Z",
          219,
          8.78539,
          8.8,
          1216590,
          "lacework",
          "lacework",
          "https://www.g2.com/products/lacework/reviews",
          "Lacework",
          "Lacework automates security and compliance across AWS, Azure, GCP, and private clouds, providing a comprehensive view of risks across cloud workloads and containers. Lacework’s unified cloud security platform provides unmatched visibility, automates intrusion detection, delivers one-click investigation, and simplifies cloud compliance.",
          "Software",
          631280,
          1266
        ],
        [
          "3033823",
          "http://jumpcloud.com",
          "JumpCloud",
          "jumpcloud.com",
          "2023-07-23T00:00:00Z",
          1667,
          9.08578,
          9.1,
          1216791,
          "jumpcloud",
          "jumpcloud",
          "https://www.g2.com/products/jumpcloud/reviews",
          "JumpCloud Inc.",
          "The JumpCloud Directory Platform reimagines the directory as a complete platform for identity, access, and device management.",
          "Software",
          631811,
          1266
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          "2023-07-23T00:00:00Z",
          463,
          8.34989,
          8.3,
          1220133,
          "microstrategy",
          "microstrategy",
          "https://www.g2.com/products/microstrategy/reviews",
          "MicroStrategy",
          "MicroStrategy provides a high performance, scalable Business Intelligence platform delivering insight with interactive dashboards and superior analytics.",
          "Software",
          680992,
          1266
        ],
        [
          "17932068",
          "https://www.lacework.com",
          "Lacework",
          "lacework.com",
          "2023-07-22T00:00:00Z",
          219,
          8.78539,
          8.8,
          1213004,
          "lacework",
          "lacework",
          "https://www.g2.com/products/lacework/reviews",
          "Lacework",
          "Lacework automates security and compliance across AWS, Azure, GCP, and private clouds, providing a comprehensive view of risks across cloud workloads and containers. Lacework’s unified cloud security platform provides unmatched visibility, automates intrusion detection, delivers one-click investigation, and simplifies cloud compliance.",
          "Software",
          631280,
          1266
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          "2023-07-22T00:00:00Z",
          463,
          8.34989,
          8.3,
          1216547,
          "microstrategy",
          "microstrategy",
          "https://www.g2.com/products/microstrategy/reviews",
          "MicroStrategy",
          "MicroStrategy provides a high performance, scalable Business Intelligence platform delivering insight with interactive dashboards and superior analytics.",
          "Software",
          680992,
          1266
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          "2023-07-22T00:00:00Z",
          463,
          8.34989,
          8.3,
          1216547,
          "microstrategy",
          "microstrategy",
          "https://www.g2.com/products/microstrategy/reviews",
          "MicroStrategy",
          "MicroStrategy provides a high performance, scalable Business Intelligence platform delivering insight with interactive dashboards and superior analytics.",
          "Software",
          680992,
          1266
        ],
        [
          "3033823",
          "http://jumpcloud.com",
          "JumpCloud",
          "jumpcloud.com",
          "2023-07-22T00:00:00Z",
          1667,
          9.08578,
          9.1,
          1213205,
          "jumpcloud",
          "jumpcloud",
          "https://www.g2.com/products/jumpcloud/reviews",
          "JumpCloud Inc.",
          "The JumpCloud Directory Platform reimagines the directory as a complete platform for identity, access, and device management.",
          "Software",
          631811,
          1266
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          "2023-07-21T00:00:00Z",
          463,
          8.34989,
          8.3,
          1212961,
          "microstrategy",
          "microstrategy",
          "https://www.g2.com/products/microstrategy/reviews",
          "MicroStrategy",
          "MicroStrategy provides a high performance, scalable Business Intelligence platform delivering insight with interactive dashboards and superior analytics.",
          "Software",
          680992,
          1266
        ],
        [
          "3033823",
          "http://jumpcloud.com",
          "JumpCloud",
          "jumpcloud.com",
          "2023-07-21T00:00:00Z",
          1667,
          9.08578,
          9.1,
          1209619,
          "jumpcloud",
          "jumpcloud",
          "https://www.g2.com/products/jumpcloud/reviews",
          "JumpCloud Inc.",
          "The JumpCloud Directory Platform reimagines the directory as a complete platform for identity, access, and device management.",
          "Software",
          631811,
          1266
        ],
        [
          "17932068",
          "https://www.lacework.com",
          "Lacework",
          "lacework.com",
          "2023-07-21T00:00:00Z",
          219,
          8.78539,
          8.8,
          1209418,
          "lacework",
          "lacework",
          "https://www.g2.com/products/lacework/reviews",
          "Lacework",
          "Lacework automates security and compliance across AWS, Azure, GCP, and private clouds, providing a comprehensive view of risks across cloud workloads and containers. Lacework’s unified cloud security platform provides unmatched visibility, automates intrusion detection, delivers one-click investigation, and simplifies cloud compliance.",
          "Software",
          631280,
          1266
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          "2023-07-21T00:00:00Z",
          463,
          8.34989,
          8.3,
          1212961,
          "microstrategy",
          "microstrategy",
          "https://www.g2.com/products/microstrategy/reviews",
          "MicroStrategy",
          "MicroStrategy provides a high performance, scalable Business Intelligence platform delivering insight with interactive dashboards and superior analytics.",
          "Software",
          680992,
          1266
        ],
        [
          "3033823",
          "http://jumpcloud.com",
          "JumpCloud",
          "jumpcloud.com",
          "2023-07-20T00:00:00Z",
          1667,
          9.08578,
          9.1,
          1206033,
          "jumpcloud",
          "jumpcloud",
          "https://www.g2.com/products/jumpcloud/reviews",
          "JumpCloud Inc.",
          "The JumpCloud Directory Platform reimagines the directory as a complete platform for identity, access, and device management.",
          "Software",
          631811,
          1266
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          "2023-07-20T00:00:00Z",
          463,
          8.34989,
          8.3,
          1209375,
          "microstrategy",
          "microstrategy",
          "https://www.g2.com/products/microstrategy/reviews",
          "MicroStrategy",
          "MicroStrategy provides a high performance, scalable Business Intelligence platform delivering insight with interactive dashboards and superior analytics.",
          "Software",
          680992,
          1266
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          "2023-07-20T00:00:00Z",
          463,
          8.34989,
          8.3,
          1209375,
          "microstrategy",
          "microstrategy",
          "https://www.g2.com/products/microstrategy/reviews",
          "MicroStrategy",
          "MicroStrategy provides a high performance, scalable Business Intelligence platform delivering insight with interactive dashboards and superior analytics.",
          "Software",
          680992,
          1266
        ],
        [
          "17932068",
          "https://www.lacework.com",
          "Lacework",
          "lacework.com",
          "2023-07-20T00:00:00Z",
          219,
          8.78539,
          8.8,
          1205832,
          "lacework",
          "lacework",
          "https://www.g2.com/products/lacework/reviews",
          "Lacework",
          "Lacework automates security and compliance across AWS, Azure, GCP, and private clouds, providing a comprehensive view of risks across cloud workloads and containers. Lacework’s unified cloud security platform provides unmatched visibility, automates intrusion detection, delivers one-click investigation, and simplifies cloud compliance.",
          "Software",
          631280,
          1266
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          "2023-07-19T00:00:00Z",
          463,
          8.34989,
          8.3,
          1205789,
          "microstrategy",
          "microstrategy",
          "https://www.g2.com/products/microstrategy/reviews",
          "MicroStrategy",
          "MicroStrategy provides a high performance, scalable Business Intelligence platform delivering insight with interactive dashboards and superior analytics.",
          "Software",
          680992,
          1266
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          "2023-07-19T00:00:00Z",
          463,
          8.34989,
          8.3,
          1205789,
          "microstrategy",
          "microstrategy",
          "https://www.g2.com/products/microstrategy/reviews",
          "MicroStrategy",
          "MicroStrategy provides a high performance, scalable Business Intelligence platform delivering insight with interactive dashboards and superior analytics.",
          "Software",
          680992,
          1266
        ],
        [
          "3033823",
          "http://jumpcloud.com",
          "JumpCloud",
          "jumpcloud.com",
          "2023-07-19T00:00:00Z",
          1667,
          9.08578,
          9.1,
          1202447,
          "jumpcloud",
          "jumpcloud",
          "https://www.g2.com/products/jumpcloud/reviews",
          "JumpCloud Inc.",
          "The JumpCloud Directory Platform reimagines the directory as a complete platform for identity, access, and device management.",
          "Software",
          631811,
          1266
        ],
        [
          "17932068",
          "https://www.lacework.com",
          "Lacework",
          "lacework.com",
          "2023-07-19T00:00:00Z",
          219,
          8.78539,
          8.8,
          1202246,
          "lacework",
          "lacework",
          "https://www.g2.com/products/lacework/reviews",
          "Lacework",
          "Lacework automates security and compliance across AWS, Azure, GCP, and private clouds, providing a comprehensive view of risks across cloud workloads and containers. Lacework’s unified cloud security platform provides unmatched visibility, automates intrusion detection, delivers one-click investigation, and simplifies cloud compliance.",
          "Software",
          631280,
          1266
        ],
        [
          "3033823",
          "http://jumpcloud.com",
          "JumpCloud",
          "jumpcloud.com",
          "2023-07-18T00:00:00Z",
          1667,
          9.08578,
          9.1,
          1198861,
          "jumpcloud",
          "jumpcloud",
          "https://www.g2.com/products/jumpcloud/reviews",
          "JumpCloud Inc.",
          "The JumpCloud Directory Platform reimagines the directory as a complete platform for identity, access, and device management.",
          "Software",
          631811,
          1266
        ],
        [
          "17932068",
          "https://www.lacework.com",
          "Lacework",
          "lacework.com",
          "2023-07-18T00:00:00Z",
          219,
          8.78539,
          8.8,
          1198660,
          "lacework",
          "lacework",
          "https://www.g2.com/products/lacework/reviews",
          "Lacework",
          "Lacework automates security and compliance across AWS, Azure, GCP, and private clouds, providing a comprehensive view of risks across cloud workloads and containers. Lacework’s unified cloud security platform provides unmatched visibility, automates intrusion detection, delivers one-click investigation, and simplifies cloud compliance.",
          "Software",
          631280,
          1266
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          "2023-07-18T00:00:00Z",
          463,
          8.34989,
          8.3,
          1202203,
          "microstrategy",
          "microstrategy",
          "https://www.g2.com/products/microstrategy/reviews",
          "MicroStrategy",
          "MicroStrategy provides a high performance, scalable Business Intelligence platform delivering insight with interactive dashboards and superior analytics.",
          "Software",
          680992,
          1266
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          "2023-07-18T00:00:00Z",
          463,
          8.34989,
          8.3,
          1202203,
          "microstrategy",
          "microstrategy",
          "https://www.g2.com/products/microstrategy/reviews",
          "MicroStrategy",
          "MicroStrategy provides a high performance, scalable Business Intelligence platform delivering insight with interactive dashboards and superior analytics.",
          "Software",
          680992,
          1266
        ],
        [
          "17932068",
          "https://www.lacework.com",
          "Lacework",
          "lacework.com",
          "2023-07-17T00:00:00Z",
          219,
          8.78539,
          8.8,
          1195074,
          "lacework",
          "lacework",
          "https://www.g2.com/products/lacework/reviews",
          "Lacework",
          "Lacework automates security and compliance across AWS, Azure, GCP, and private clouds, providing a comprehensive view of risks across cloud workloads and containers. Lacework’s unified cloud security platform provides unmatched visibility, automates intrusion detection, delivers one-click investigation, and simplifies cloud compliance.",
          "Software",
          631280,
          1266
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          "2023-07-17T00:00:00Z",
          463,
          8.34989,
          8.3,
          1198617,
          "microstrategy",
          "microstrategy",
          "https://www.g2.com/products/microstrategy/reviews",
          "MicroStrategy",
          "MicroStrategy provides a high performance, scalable Business Intelligence platform delivering insight with interactive dashboards and superior analytics.",
          "Software",
          680992,
          1266
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          "2023-07-17T00:00:00Z",
          463,
          8.34989,
          8.3,
          1198617,
          "microstrategy",
          "microstrategy",
          "https://www.g2.com/products/microstrategy/reviews",
          "MicroStrategy",
          "MicroStrategy provides a high performance, scalable Business Intelligence platform delivering insight with interactive dashboards and superior analytics.",
          "Software",
          680992,
          1266
        ],
        [
          "3033823",
          "http://jumpcloud.com",
          "JumpCloud",
          "jumpcloud.com",
          "2023-07-17T00:00:00Z",
          1667,
          9.08578,
          9.1,
          1195275,
          "jumpcloud",
          "jumpcloud",
          "https://www.g2.com/products/jumpcloud/reviews",
          "JumpCloud Inc.",
          "The JumpCloud Directory Platform reimagines the directory as a complete platform for identity, access, and device management.",
          "Software",
          631811,
          1266
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          "2023-07-16T00:00:00Z",
          463,
          8.34989,
          8.3,
          1195031,
          "microstrategy",
          "microstrategy",
          "https://www.g2.com/products/microstrategy/reviews",
          "MicroStrategy",
          "MicroStrategy provides a high performance, scalable Business Intelligence platform delivering insight with interactive dashboards and superior analytics.",
          "Software",
          680992,
          1266
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          "2023-07-16T00:00:00Z",
          463,
          8.34989,
          8.3,
          1195031,
          "microstrategy",
          "microstrategy",
          "https://www.g2.com/products/microstrategy/reviews",
          "MicroStrategy",
          "MicroStrategy provides a high performance, scalable Business Intelligence platform delivering insight with interactive dashboards and superior analytics.",
          "Software",
          680992,
          1266
        ],
        [
          "3033823",
          "http://jumpcloud.com",
          "JumpCloud",
          "jumpcloud.com",
          "2023-07-16T00:00:00Z",
          1667,
          9.08578,
          9.1,
          1191689,
          "jumpcloud",
          "jumpcloud",
          "https://www.g2.com/products/jumpcloud/reviews",
          "JumpCloud Inc.",
          "The JumpCloud Directory Platform reimagines the directory as a complete platform for identity, access, and device management.",
          "Software",
          631811,
          1266
        ],
        [
          "17932068",
          "https://www.lacework.com",
          "Lacework",
          "lacework.com",
          "2023-07-16T00:00:00Z",
          219,
          8.78539,
          8.8,
          1191488,
          "lacework",
          "lacework",
          "https://www.g2.com/products/lacework/reviews",
          "Lacework",
          "Lacework automates security and compliance across AWS, Azure, GCP, and private clouds, providing a comprehensive view of risks across cloud workloads and containers. Lacework’s unified cloud security platform provides unmatched visibility, automates intrusion detection, delivers one-click investigation, and simplifies cloud compliance.",
          "Software",
          631280,
          1266
        ],
        [
          "17932068",
          "https://www.lacework.com",
          "Lacework",
          "lacework.com",
          "2023-07-15T00:00:00Z",
          219,
          8.78539,
          8.8,
          1187902,
          "lacework",
          "lacework",
          "https://www.g2.com/products/lacework/reviews",
          "Lacework",
          "Lacework automates security and compliance across AWS, Azure, GCP, and private clouds, providing a comprehensive view of risks across cloud workloads and containers. Lacework’s unified cloud security platform provides unmatched visibility, automates intrusion detection, delivers one-click investigation, and simplifies cloud compliance.",
          "Software",
          631280,
          1266
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          "2023-07-15T00:00:00Z",
          463,
          8.34989,
          8.3,
          1191445,
          "microstrategy",
          "microstrategy",
          "https://www.g2.com/products/microstrategy/reviews",
          "MicroStrategy",
          "MicroStrategy provides a high performance, scalable Business Intelligence platform delivering insight with interactive dashboards and superior analytics.",
          "Software",
          680992,
          1266
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          "2023-07-15T00:00:00Z",
          463,
          8.34989,
          8.3,
          1191445,
          "microstrategy",
          "microstrategy",
          "https://www.g2.com/products/microstrategy/reviews",
          "MicroStrategy",
          "MicroStrategy provides a high performance, scalable Business Intelligence platform delivering insight with interactive dashboards and superior analytics.",
          "Software",
          680992,
          1266
        ],
        [
          "3033823",
          "http://jumpcloud.com",
          "JumpCloud",
          "jumpcloud.com",
          "2023-07-15T00:00:00Z",
          1667,
          9.08578,
          9.1,
          1188103,
          "jumpcloud",
          "jumpcloud",
          "https://www.g2.com/products/jumpcloud/reviews",
          "JumpCloud Inc.",
          "The JumpCloud Directory Platform reimagines the directory as a complete platform for identity, access, and device management.",
          "Software",
          631811,
          1266
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          "2023-07-14T00:00:00Z",
          463,
          8.34989,
          8.3,
          1187859,
          "microstrategy",
          "microstrategy",
          "https://www.g2.com/products/microstrategy/reviews",
          "MicroStrategy",
          "MicroStrategy provides a high performance, scalable Business Intelligence platform delivering insight with interactive dashboards and superior analytics.",
          "Software",
          680992,
          1266
        ],
        [
          "3033823",
          "http://jumpcloud.com",
          "JumpCloud",
          "jumpcloud.com",
          "2023-07-14T00:00:00Z",
          1667,
          9.08578,
          9.1,
          1184517,
          "jumpcloud",
          "jumpcloud",
          "https://www.g2.com/products/jumpcloud/reviews",
          "JumpCloud Inc.",
          "The JumpCloud Directory Platform reimagines the directory as a complete platform for identity, access, and device management.",
          "Software",
          631811,
          1266
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          "2023-07-14T00:00:00Z",
          463,
          8.34989,
          8.3,
          1187859,
          "microstrategy",
          "microstrategy",
          "https://www.g2.com/products/microstrategy/reviews",
          "MicroStrategy",
          "MicroStrategy provides a high performance, scalable Business Intelligence platform delivering insight with interactive dashboards and superior analytics.",
          "Software",
          680992,
          1266
        ],
        [
          "17932068",
          "https://www.lacework.com",
          "Lacework",
          "lacework.com",
          "2023-07-14T00:00:00Z",
          219,
          8.78539,
          8.8,
          1184316,
          "lacework",
          "lacework",
          "https://www.g2.com/products/lacework/reviews",
          "Lacework",
          "Lacework automates security and compliance across AWS, Azure, GCP, and private clouds, providing a comprehensive view of risks across cloud workloads and containers. Lacework’s unified cloud security platform provides unmatched visibility, automates intrusion detection, delivers one-click investigation, and simplifies cloud compliance.",
          "Software",
          631280,
          1266
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          "2023-07-13T00:00:00Z",
          463,
          8.34989,
          8.3,
          1184273,
          "microstrategy",
          "microstrategy",
          "https://www.g2.com/products/microstrategy/reviews",
          "MicroStrategy",
          "MicroStrategy provides a high performance, scalable Business Intelligence platform delivering insight with interactive dashboards and superior analytics.",
          "Software",
          680992,
          1266
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          "2023-07-13T00:00:00Z",
          463,
          8.34989,
          8.3,
          1184273,
          "microstrategy",
          "microstrategy",
          "https://www.g2.com/products/microstrategy/reviews",
          "MicroStrategy",
          "MicroStrategy provides a high performance, scalable Business Intelligence platform delivering insight with interactive dashboards and superior analytics.",
          "Software",
          680992,
          1266
        ],
        [
          "17932068",
          "https://www.lacework.com",
          "Lacework",
          "lacework.com",
          "2023-07-13T00:00:00Z",
          219,
          8.78539,
          8.8,
          1180730,
          "lacework",
          "lacework",
          "https://www.g2.com/products/lacework/reviews",
          "Lacework",
          "Lacework automates security and compliance across AWS, Azure, GCP, and private clouds, providing a comprehensive view of risks across cloud workloads and containers. Lacework’s unified cloud security platform provides unmatched visibility, automates intrusion detection, delivers one-click investigation, and simplifies cloud compliance.",
          "Software",
          631280,
          1266
        ],
        [
          "3033823",
          "http://jumpcloud.com",
          "JumpCloud",
          "jumpcloud.com",
          "2023-07-13T00:00:00Z",
          1667,
          9.08578,
          9.1,
          1180931,
          "jumpcloud",
          "jumpcloud",
          "https://www.g2.com/products/jumpcloud/reviews",
          "JumpCloud Inc.",
          "The JumpCloud Directory Platform reimagines the directory as a complete platform for identity, access, and device management.",
          "Software",
          631811,
          1266
        ],
        [
          "3033823",
          "http://jumpcloud.com",
          "JumpCloud",
          "jumpcloud.com",
          "2023-07-12T00:00:00Z",
          1667,
          9.08578,
          9.1,
          1177345,
          "jumpcloud",
          "jumpcloud",
          "https://www.g2.com/products/jumpcloud/reviews",
          "JumpCloud Inc.",
          "The JumpCloud Directory Platform reimagines the directory as a complete platform for identity, access, and device management.",
          "Software",
          631811,
          1266
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          "2023-07-12T00:00:00Z",
          463,
          8.34989,
          8.3,
          1180687,
          "microstrategy",
          "microstrategy",
          "https://www.g2.com/products/microstrategy/reviews",
          "MicroStrategy",
          "MicroStrategy provides a high performance, scalable Business Intelligence platform delivering insight with interactive dashboards and superior analytics.",
          "Software",
          680992,
          1266
        ],
        [
          "17932068",
          "https://www.lacework.com",
          "Lacework",
          "lacework.com",
          "2023-07-12T00:00:00Z",
          219,
          8.78539,
          8.8,
          1177144,
          "lacework",
          "lacework",
          "https://www.g2.com/products/lacework/reviews",
          "Lacework",
          "Lacework automates security and compliance across AWS, Azure, GCP, and private clouds, providing a comprehensive view of risks across cloud workloads and containers. Lacework’s unified cloud security platform provides unmatched visibility, automates intrusion detection, delivers one-click investigation, and simplifies cloud compliance.",
          "Software",
          631280,
          1266
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          "2023-07-12T00:00:00Z",
          463,
          8.34989,
          8.3,
          1180687,
          "microstrategy",
          "microstrategy",
          "https://www.g2.com/products/microstrategy/reviews",
          "MicroStrategy",
          "MicroStrategy provides a high performance, scalable Business Intelligence platform delivering insight with interactive dashboards and superior analytics.",
          "Software",
          680992,
          1266
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          "2023-07-11T00:00:00Z",
          463,
          8.34989,
          8.3,
          1177101,
          "microstrategy",
          "microstrategy",
          "https://www.g2.com/products/microstrategy/reviews",
          "MicroStrategy",
          "MicroStrategy provides a high performance, scalable Business Intelligence platform delivering insight with interactive dashboards and superior analytics.",
          "Software",
          680992,
          1266
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          "2023-07-11T00:00:00Z",
          463,
          8.34989,
          8.3,
          1177101,
          "microstrategy",
          "microstrategy",
          "https://www.g2.com/products/microstrategy/reviews",
          "MicroStrategy",
          "MicroStrategy provides a high performance, scalable Business Intelligence platform delivering insight with interactive dashboards and superior analytics.",
          "Software",
          680992,
          1266
        ],
        [
          "3033823",
          "http://jumpcloud.com",
          "JumpCloud",
          "jumpcloud.com",
          "2023-07-11T00:00:00Z",
          1667,
          9.08578,
          9.1,
          1173759,
          "jumpcloud",
          "jumpcloud",
          "https://www.g2.com/products/jumpcloud/reviews",
          "JumpCloud Inc.",
          "The JumpCloud Directory Platform reimagines the directory as a complete platform for identity, access, and device management.",
          "Software",
          631811,
          1266
        ],
        [
          "17932068",
          "https://www.lacework.com",
          "Lacework",
          "lacework.com",
          "2023-07-11T00:00:00Z",
          219,
          8.78539,
          8.8,
          1173558,
          "lacework",
          "lacework",
          "https://www.g2.com/products/lacework/reviews",
          "Lacework",
          "Lacework automates security and compliance across AWS, Azure, GCP, and private clouds, providing a comprehensive view of risks across cloud workloads and containers. Lacework’s unified cloud security platform provides unmatched visibility, automates intrusion detection, delivers one-click investigation, and simplifies cloud compliance.",
          "Software",
          631280,
          1266
        ],
        [
          "3033823",
          "http://jumpcloud.com",
          "JumpCloud",
          "jumpcloud.com",
          "2023-07-10T00:00:00Z",
          1667,
          9.08578,
          9.1,
          1170173,
          "jumpcloud",
          "jumpcloud",
          "https://www.g2.com/products/jumpcloud/reviews",
          "JumpCloud Inc.",
          "The JumpCloud Directory Platform reimagines the directory as a complete platform for identity, access, and device management.",
          "Software",
          631811,
          1266
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          "2023-07-10T00:00:00Z",
          463,
          8.34989,
          8.3,
          1173515,
          "microstrategy",
          "microstrategy",
          "https://www.g2.com/products/microstrategy/reviews",
          "MicroStrategy",
          "MicroStrategy provides a high performance, scalable Business Intelligence platform delivering insight with interactive dashboards and superior analytics.",
          "Software",
          680992,
          1266
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          "2023-07-10T00:00:00Z",
          463,
          8.34989,
          8.3,
          1173515,
          "microstrategy",
          "microstrategy",
          "https://www.g2.com/products/microstrategy/reviews",
          "MicroStrategy",
          "MicroStrategy provides a high performance, scalable Business Intelligence platform delivering insight with interactive dashboards and superior analytics.",
          "Software",
          680992,
          1266
        ],
        [
          "17932068",
          "https://www.lacework.com",
          "Lacework",
          "lacework.com",
          "2023-07-10T00:00:00Z",
          219,
          8.78539,
          8.8,
          1169972,
          "lacework",
          "lacework",
          "https://www.g2.com/products/lacework/reviews",
          "Lacework",
          "Lacework automates security and compliance across AWS, Azure, GCP, and private clouds, providing a comprehensive view of risks across cloud workloads and containers. Lacework’s unified cloud security platform provides unmatched visibility, automates intrusion detection, delivers one-click investigation, and simplifies cloud compliance.",
          "Software",
          631280,
          1266
        ],
        [
          "3033823",
          "http://jumpcloud.com",
          "JumpCloud",
          "jumpcloud.com",
          "2023-07-09T00:00:00Z",
          1667,
          9.08578,
          9.1,
          1166587,
          "jumpcloud",
          "jumpcloud",
          "https://www.g2.com/products/jumpcloud/reviews",
          "JumpCloud Inc.",
          "The JumpCloud Directory Platform reimagines the directory as a complete platform for identity, access, and device management.",
          "Software",
          631811,
          1266
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          "2023-07-09T00:00:00Z",
          463,
          8.34989,
          8.3,
          1169929,
          "microstrategy",
          "microstrategy",
          "https://www.g2.com/products/microstrategy/reviews",
          "MicroStrategy",
          "MicroStrategy provides a high performance, scalable Business Intelligence platform delivering insight with interactive dashboards and superior analytics.",
          "Software",
          680992,
          1266
        ],
        [
          "17932068",
          "https://www.lacework.com",
          "Lacework",
          "lacework.com",
          "2023-07-09T00:00:00Z",
          219,
          8.78539,
          8.8,
          1166386,
          "lacework",
          "lacework",
          "https://www.g2.com/products/lacework/reviews",
          "Lacework",
          "Lacework automates security and compliance across AWS, Azure, GCP, and private clouds, providing a comprehensive view of risks across cloud workloads and containers. Lacework’s unified cloud security platform provides unmatched visibility, automates intrusion detection, delivers one-click investigation, and simplifies cloud compliance.",
          "Software",
          631280,
          1266
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          "2023-07-09T00:00:00Z",
          463,
          8.34989,
          8.3,
          1169929,
          "microstrategy",
          "microstrategy",
          "https://www.g2.com/products/microstrategy/reviews",
          "MicroStrategy",
          "MicroStrategy provides a high performance, scalable Business Intelligence platform delivering insight with interactive dashboards and superior analytics.",
          "Software",
          680992,
          1266
        ],
        [
          "3033823",
          "http://jumpcloud.com",
          "JumpCloud",
          "jumpcloud.com",
          "2023-07-08T00:00:00Z",
          1667,
          9.08578,
          9.1,
          1163001,
          "jumpcloud",
          "jumpcloud",
          "https://www.g2.com/products/jumpcloud/reviews",
          "JumpCloud Inc.",
          "The JumpCloud Directory Platform reimagines the directory as a complete platform for identity, access, and device management.",
          "Software",
          631811,
          1266
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          "2023-07-08T00:00:00Z",
          463,
          8.34989,
          8.3,
          1166343,
          "microstrategy",
          "microstrategy",
          "https://www.g2.com/products/microstrategy/reviews",
          "MicroStrategy",
          "MicroStrategy provides a high performance, scalable Business Intelligence platform delivering insight with interactive dashboards and superior analytics.",
          "Software",
          680992,
          1266
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          "2023-07-08T00:00:00Z",
          463,
          8.34989,
          8.3,
          1166343,
          "microstrategy",
          "microstrategy",
          "https://www.g2.com/products/microstrategy/reviews",
          "MicroStrategy",
          "MicroStrategy provides a high performance, scalable Business Intelligence platform delivering insight with interactive dashboards and superior analytics.",
          "Software",
          680992,
          1266
        ],
        [
          "17932068",
          "https://www.lacework.com",
          "Lacework",
          "lacework.com",
          "2023-07-08T00:00:00Z",
          219,
          8.78539,
          8.8,
          1162800,
          "lacework",
          "lacework",
          "https://www.g2.com/products/lacework/reviews",
          "Lacework",
          "Lacework automates security and compliance across AWS, Azure, GCP, and private clouds, providing a comprehensive view of risks across cloud workloads and containers. Lacework’s unified cloud security platform provides unmatched visibility, automates intrusion detection, delivers one-click investigation, and simplifies cloud compliance.",
          "Software",
          631280,
          1266
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          "2023-07-07T00:00:00Z",
          463,
          8.34989,
          8.3,
          1162757,
          "microstrategy",
          "microstrategy",
          "https://www.g2.com/products/microstrategy/reviews",
          "MicroStrategy",
          "MicroStrategy provides a high performance, scalable Business Intelligence platform delivering insight with interactive dashboards and superior analytics.",
          "Software",
          680992,
          1266
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          "2023-07-07T00:00:00Z",
          463,
          8.34989,
          8.3,
          1162757,
          "microstrategy",
          "microstrategy",
          "https://www.g2.com/products/microstrategy/reviews",
          "MicroStrategy",
          "MicroStrategy provides a high performance, scalable Business Intelligence platform delivering insight with interactive dashboards and superior analytics.",
          "Software",
          680992,
          1266
        ],
        [
          "17932068",
          "https://www.lacework.com",
          "Lacework",
          "lacework.com",
          "2023-07-07T00:00:00Z",
          219,
          8.78539,
          8.8,
          1159214,
          "lacework",
          "lacework",
          "https://www.g2.com/products/lacework/reviews",
          "Lacework",
          "Lacework automates security and compliance across AWS, Azure, GCP, and private clouds, providing a comprehensive view of risks across cloud workloads and containers. Lacework’s unified cloud security platform provides unmatched visibility, automates intrusion detection, delivers one-click investigation, and simplifies cloud compliance.",
          "Software",
          631280,
          1266
        ],
        [
          "3033823",
          "http://jumpcloud.com",
          "JumpCloud",
          "jumpcloud.com",
          "2023-07-07T00:00:00Z",
          1667,
          9.08578,
          9.1,
          1159415,
          "jumpcloud",
          "jumpcloud",
          "https://www.g2.com/products/jumpcloud/reviews",
          "JumpCloud Inc.",
          "The JumpCloud Directory Platform reimagines the directory as a complete platform for identity, access, and device management.",
          "Software",
          631811,
          1266
        ],
        [
          "3033823",
          "http://jumpcloud.com",
          "JumpCloud",
          "jumpcloud.com",
          "2023-07-06T00:00:00Z",
          1667,
          9.08578,
          9.1,
          1155829,
          "jumpcloud",
          "jumpcloud",
          "https://www.g2.com/products/jumpcloud/reviews",
          "JumpCloud Inc.",
          "The JumpCloud Directory Platform reimagines the directory as a complete platform for identity, access, and device management.",
          "Software",
          631811,
          1266
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          "2023-07-06T00:00:00Z",
          463,
          8.34989,
          8.3,
          1159171,
          "microstrategy",
          "microstrategy",
          "https://www.g2.com/products/microstrategy/reviews",
          "MicroStrategy",
          "MicroStrategy provides a high performance, scalable Business Intelligence platform delivering insight with interactive dashboards and superior analytics.",
          "Software",
          680992,
          1266
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          "2023-07-06T00:00:00Z",
          463,
          8.34989,
          8.3,
          1159171,
          "microstrategy",
          "microstrategy",
          "https://www.g2.com/products/microstrategy/reviews",
          "MicroStrategy",
          "MicroStrategy provides a high performance, scalable Business Intelligence platform delivering insight with interactive dashboards and superior analytics.",
          "Software",
          680992,
          1266
        ],
        [
          "17932068",
          "https://www.lacework.com",
          "Lacework",
          "lacework.com",
          "2023-07-06T00:00:00Z",
          219,
          8.78539,
          8.8,
          1155628,
          "lacework",
          "lacework",
          "https://www.g2.com/products/lacework/reviews",
          "Lacework",
          "Lacework automates security and compliance across AWS, Azure, GCP, and private clouds, providing a comprehensive view of risks across cloud workloads and containers. Lacework’s unified cloud security platform provides unmatched visibility, automates intrusion detection, delivers one-click investigation, and simplifies cloud compliance.",
          "Software",
          631280,
          1266
        ],
        [
          "3033823",
          "http://jumpcloud.com",
          "JumpCloud",
          "jumpcloud.com",
          "2023-07-05T00:00:00Z",
          1667,
          9.08578,
          9.1,
          1152243,
          "jumpcloud",
          "jumpcloud",
          "https://www.g2.com/products/jumpcloud/reviews",
          "JumpCloud Inc.",
          "The JumpCloud Directory Platform reimagines the directory as a complete platform for identity, access, and device management.",
          "Software",
          631811,
          1266
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          "2023-07-05T00:00:00Z",
          463,
          8.34989,
          8.3,
          1155585,
          "microstrategy",
          "microstrategy",
          "https://www.g2.com/products/microstrategy/reviews",
          "MicroStrategy",
          "MicroStrategy provides a high performance, scalable Business Intelligence platform delivering insight with interactive dashboards and superior analytics.",
          "Software",
          680992,
          1266
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          "2023-07-05T00:00:00Z",
          463,
          8.34989,
          8.3,
          1155585,
          "microstrategy",
          "microstrategy",
          "https://www.g2.com/products/microstrategy/reviews",
          "MicroStrategy",
          "MicroStrategy provides a high performance, scalable Business Intelligence platform delivering insight with interactive dashboards and superior analytics.",
          "Software",
          680992,
          1266
        ],
        [
          "17932068",
          "https://www.lacework.com",
          "Lacework",
          "lacework.com",
          "2023-07-05T00:00:00Z",
          219,
          8.78539,
          8.8,
          1152042,
          "lacework",
          "lacework",
          "https://www.g2.com/products/lacework/reviews",
          "Lacework",
          "Lacework automates security and compliance across AWS, Azure, GCP, and private clouds, providing a comprehensive view of risks across cloud workloads and containers. Lacework’s unified cloud security platform provides unmatched visibility, automates intrusion detection, delivers one-click investigation, and simplifies cloud compliance.",
          "Software",
          631280,
          1266
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          "2023-07-04T00:00:00Z",
          463,
          8.34989,
          8.3,
          1151999,
          "microstrategy",
          "microstrategy",
          "https://www.g2.com/products/microstrategy/reviews",
          "MicroStrategy",
          "MicroStrategy provides a high performance, scalable Business Intelligence platform delivering insight with interactive dashboards and superior analytics.",
          "Software",
          680992,
          1266
        ],
        [
          "3033823",
          "http://jumpcloud.com",
          "JumpCloud",
          "jumpcloud.com",
          "2023-07-04T00:00:00Z",
          1667,
          9.08578,
          9.1,
          1148657,
          "jumpcloud",
          "jumpcloud",
          "https://www.g2.com/products/jumpcloud/reviews",
          "JumpCloud Inc.",
          "The JumpCloud Directory Platform reimagines the directory as a complete platform for identity, access, and device management.",
          "Software",
          631811,
          1266
        ],
        [
          "17932068",
          "https://www.lacework.com",
          "Lacework",
          "lacework.com",
          "2023-07-04T00:00:00Z",
          219,
          8.78539,
          8.8,
          1148456,
          "lacework",
          "lacework",
          "https://www.g2.com/products/lacework/reviews",
          "Lacework",
          "Lacework automates security and compliance across AWS, Azure, GCP, and private clouds, providing a comprehensive view of risks across cloud workloads and containers. Lacework’s unified cloud security platform provides unmatched visibility, automates intrusion detection, delivers one-click investigation, and simplifies cloud compliance.",
          "Software",
          631280,
          1266
        ],
        [
          "3643",
          "http://www.microstrategy.com",
          "MicroStrategy",
          "microstrategy.com",
          "2023-07-04T00:00:00Z",
          463,
          8.34989,
          8.3,
          1151999,
          "microstrategy",
          "microstrategy",
          "https://www.g2.com/products/microstrategy/reviews",
          "MicroStrategy",
          "MicroStrategy provides a high performance, scalable Business Intelligence platform delivering insight with interactive dashboards and superior analytics.",
          "Software",
          680992,
          1266
        ]
      ],
      "is_trial_user": false
    }
    ```
    

### 8. Web Traffic

Use this request to get historical web-traffic of a company by domain

- **cURL**
    
    ```bash
    curl --request POST \
      --url 'https://api.crustdata.com/data_lab/webtraffic/' \
      --header 'Accept: */*' \
      --header 'Accept-Language: en-GB,en-US;q=0.9,en;q=0.8' \
      --header 'Authorization: Token $token' \
      --header 'Content-Type: application/json' \
      --data '{
        "filters": {
          "op": "or",
          "conditions": [
            {
              "column": "company_website",
              "type": "(.)",
              "value": "wefitanyfurniture.com"
            }
          ]
        },
        "offset": 0,
        "count": 100,
        "sorts": []
      }'
    ```
    
- **Result**
    
    ```bash
     {
    	"fields": [
    		{
    			"type": "foreign_key",
    			"api_name": "company_id",
    			"hidden": false,
    			"options": [],
    			"summary": "",
    			"local_metric": false,
    			"display_name": "",
    			"company_profile_name": "",
    			"preview_description": "",
    			"geocode": false
    		},
    		{
    			"type": "string",
    			"api_name": "company_website",
    			"hidden": false,
    			"options": [],
    			"summary": "",
    			"local_metric": false,
    			"display_name": "",
    			"company_profile_name": "",
    			"preview_description": "",
    			"geocode": false
    		},
    		{
    			"type": "string",
    			"api_name": "company_name",
    			"hidden": false,
    			"options": [],
    			"summary": "",
    			"local_metric": false,
    			"display_name": "",
    			"company_profile_name": "",
    			"preview_description": "",
    			"geocode": false
    		},
    		{
    			"type": "array",
    			"api_name": "similarweb_traffic_timeseries",
    			"hidden": false,
    			"options": [],
    			"summary": "",
    			"local_metric": false,
    			"display_name": "",
    			"company_profile_name": "",
    			"preview_description": "",
    			"geocode": false
    		}
    	],
    	"rows": [
    		[
    			1411045,
    			"wefitanyfurniture.com",
    			"WeFitAnyFurniture",
    			[
    				{
    					"date": "2024-07-01T00:00:00+00:00",
    					"monthly_visitors": 355,
    					"traffic_source_social_pct": null,
    					"traffic_source_search_pct": null,
    					"traffic_source_direct_pct": null,
    					"traffic_source_paid_referral_pct": null,
    					"traffic_source_referral_pct": null
    				},
    				{
    					"date": "2024-08-01T00:00:00+00:00",
    					"monthly_visitors": 1255,
    					"traffic_source_social_pct": null,
    					"traffic_source_search_pct": null,
    					"traffic_source_direct_pct": null,
    					"traffic_source_paid_referral_pct": null,
    					"traffic_source_referral_pct": null
    				},
    				{
    					"date": "2024-09-01T00:00:00+00:00",
    					"monthly_visitors": 3728,
    					"traffic_source_social_pct": 4.1587388254523585,
    					"traffic_source_search_pct": 48.335395016304005,
    					"traffic_source_direct_pct": 32.901089596227564,
    					"traffic_source_paid_referral_pct": 0.9439998798176015,
    					"traffic_source_referral_pct": 12.431220453595381
    				}
    			]
    		]
    	]
    }
    ```
    

**Key Points:**

- When querying a website, compute the domain (`$domain` ) and then pass it in the `conditions` object of the payload like
    
    ```bash
            [{
              "column": "company_website",
              "type": "(.)",
              "value": "$domain"
            }]
    ```
    
- If there is no data for the website, it will be auto-enriched in next 24 hours. Just query again.
- For parsing the response, please follow:
    - [https://www.notion.so/crustdata/Crustdata-Discovery-And-Enrichment-API-c66d5236e8ea40df8af114f6d447ab48?pvs=4#28de6e16940c4615b5872020a345766a](https://www.notion.so/Crustdata-Discovery-And-Enrichment-API-c66d5236e8ea40df8af114f6d447ab48?pvs=21)
    

### 9. Investor Portfolio

Retrieve portfolio details for a specified investor. Each investor, as returned in the [company enrichment endpoint](https://www.notion.so/Crustdata-Discovery-And-Enrichment-API-c66d5236e8ea40df8af114f6d447ab48?pvs=21), has a unique identifier (UUID), name, and type. This API allows you to fetch the full portfolio of companies associated with an investor, using either the investor's `uuid` or `name` as an identifier.

- **cURL**
    
    **Example 1: query by investor uuid** 
    
    Note: uuid for an investor can be retrieved from `/screener/company` response. It is available in `funding_and_investment.crunchbase_investors_info_list[*].uuid` field 
    
    ```bash
    curl 'https://api.crustdata.com/data_lab/investor_portfolio?investor_uuid=ce91bad7-b6d8-e56e-0f45-4763c6c5ca29' \
      --header 'Accept: application/json, text/plain, */*' \
      --header 'Accept-Language: en-US,en;q=0.9' \
      --header 'Authorization: Token $auth_token'
    ```
    
    **Example 2: query by investor name** 
    
    Note: uuid for an investor can be retrieved from `/screener/company` response. It is available in `funding_and_investment.crunchbase_investors_info_list[*].uuid` field 
    
    ```bash
    curl 'https://api.crustdata.com/data_lab/investor_portfolio?investor_name=Sequoia Capital' \
      --header 'Accept: application/json, text/plain, */*' \
      --header 'Accept-Language: en-US,en;q=0.9' \
      --header 'Authorization: Token $auth_token'
    ```
    
- **Result**
    
    Full sample: https://jsonhero.io/j/hSEHVFgv68pz