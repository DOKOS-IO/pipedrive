## Pipedrive

### Alpha version: Please open issues for any bug found or any enhancement proposals. Thanks!

#### Installation

This application requires [Frappe](https://github.com/frappe/frappe) and [ERPNext](https://github.com/frappe/erpnext) v10 (not tested on higher versions).

1. `bench get-app pipedrive https://github.com/DOKOS-IO/pipedrive/`
2. `bench install-app pipedrive`
3. `bench restart && bench migrate`

In ERPNext, add your API token, the link to your pipedrive accountand save.

The application is scheduled to run hourly by default.
Verify that your scheduler is enabled (`bench enable-scheduler`).

#### Features

##### Pipedrive Organizations to ERPNext Leads

*Basic Mapping*  

|Source|Flow|Target|
|---|---|---|
|Name| --> |Lead Name|
|Name| --> |Company Name|

##### Pipedrive Persons to ERPNext Contacts

*Basic Mapping*  

|Source|Flow|Target|
|---|---|---|
|First Name| --> |First Name|
|Last Name| --> |Last Name|
|Email| --> |Email ID|
|Phone| --> |Phone|
|Mobile| --> |Mobile No|

*Data modifications*  

ERPNext only proposes individual fields for email, phone and mobile n°, whereas Pipedrive allows the addition of multiple emails and phone numbers.
Therefore, this application adds the phone number with the label 'mobile' as mobile n°, one of the phone numbers with the labels "work, home or other" as the phone number and the email address with the label "work" as email ID.

The organization linked to the person in Pipedrive is also linked in ERPNext as a Lead.


#### License
GPLv3
