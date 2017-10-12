# Rule Engine

Woocation rule engine is a generic application to store business rules, and to be able to search for rules according to the data passed to it.
It is capable of searching as a partial match if exact match is not available.

### Rule
A rule consists of following:

* Condition

     ```
     {
      "condition": {
            "source": {
                "operator": "equal_to",
                "dataType": "String",
                "value": "India",
                "caseSensitive": false,
                "weight": 10
            }
      }
      ```
    
* Action

    ```
    "action": {
        "milk": "true"
      }
    ```
    
### Field

Field has following possible attributes:


| Attribute|Mandatory| DataType|
|-----------|---------|--------|
operator|YES|N.A
dataType|YES|N.A
value|YES|N.A
caseSensitive|NO|String
weight|NO|N.A

Example field:

    "source": {
                "operator": "equal_to",
                "dataType": "String",
                "value": "India",
                "caseSensitive": false,
                "weight": 10
            }


### Data types and Operators

* String 

| DataType|Operator|
|------------------------------|---------|
String|equal_to|
String|contains|
String|regex|
String|pre|
String|post|

Note:   

* Number

| DataType|Operator|
|------------------------------|---------|
Number|equal_to|
Number|less_than|
Number|greater_than|
Number|less_than_or_equal_to|
Number|greater_than_or_equal_to|

* Date

| DataType|Operator|
|------------------------------|---------|
Date|equal_to|
Date|less_than|
Date|greater_than|
Date|less_than_or_equal_to|
Date|greater_than_or_equal_to|


### Endpoints

| Endpoint                     | Method  | Commment                    |
|------------------------------|---------|-----------------------------|
|/                             | GET     | Ping                        |   
| /rule/type/{ruleType}        | PUT     | Add a rule type             |
| /rule/type/{ruleType}        | GET| Get a rule type             |
| /rule/type/{ruleType}        |DELETE| DELETE a rule type             |
| /rule/type/{ruleType}/rule/{ruleName}| PUT     | Add a rule                  |
| /rule/type/{ruleType}/rule/{ruleName}| GET     | GET a rule                  |
| /rule/type/{ruleType}/rule/{ruleName}| DELETE| DELETE a rule                  |
| /rule/type/{ruleType}/rule/search   | POST    | Find a rule                 |
| /rule/status/update          | POST    | Enable/Disbale a rule       |


### API doc

#### 1. Ping

Request: `GET`

    /

Response:

    {
        message: "Hey, I'm running"
    }
   
#### 2. Add a rule Type

Request: `PUT`

    /rule/type/{{ruleType}}
    
Response:

    {
      "message": "58ccfbb20e3da61df79ce834"
    }

#### 3 GET a rule type

Request: `GET`

    /rule/type/{{ruleType}}

#### 4. DELETE a rule type  

Request: `DELETE`

    /rule/type/{{ruleType}}
    
#### 5. Add Rule

Request: `PUT`

    /rule/type/{{ruleType}}/rule/{{ruleName}}
    
Body:

    {
      "condition": {
        "source": {
            "operator": "equal_to",
            "dataType": "String",
            "value": "India",
            "caseSensitive": false,
            "weight": 10
        },
        "age": {
            "operator": "equal_to",
            "dataType": "Number",
            "value": 20
        },
        "title": {
            "operator": "regex",
            "dataType": "String",
            "value": "h..\\swas.."
        }
      },
      "action": {
        "milk": "true"
      }
    }

Response:

    {
      "message": "58ccfbb20e3da61df79ce834"
    }
    
#### 6. GET a rule

Request: `GET`

    /rule/type/{{ruleType}}/rule/{{ruleName}}

#### 7. DELETE a rule

Request: `DELETE`

    /rule/type/{{ruleType}}/rule/{{ruleName}}

#### 8. Find rules

Request: `POST`

    /rule/type/{ruleType}/rule/search?factors=true

Note: factors=true will make all factors appear in response, else only actions will be returned.
Body:

    {
        "source": "indIA",
        "age": 10
    }
    
Response:

    [
      {
        "action": {
          "milk": "true"
        },
        "_meta": {
          "_ruleName": "afghanistan_rule",
          "_ruleType": "firstruletype",
          "_partial": false,
          "_enabled": true
        },
        "_condition": {
          "title": {
            "caseSensitive": true,
            "operator": "regex",
            "dataType": "String",
            "weight": 1,
            "value": "h..\\swas.."
          },
          "source": {
            "caseSensitive": false,
            "operator": "equal_to",
            "dataType": "String",
            "weight": 10,
            "value": "Afghanistan"
          },
          "age": {
            "caseSensitive": true,
            "operator": "greater_than",
            "dataType": "Number",
            "weight": 1,
            "value": 20
          }
        }
      }
    ]
    
#### 9. Enable/Disable a rule
  
Request: `POST`

    /rule/status/update    
    
Body: 

    {
        "ruleType": "abcd",
        "ruleName": "myrule",
        "enable": true
    }
    
Response:

    {
      "message": "{'n': 1, 'nModified': 0, 'updatedExisting': True, 'ok': 1.0}"
    }
  
 