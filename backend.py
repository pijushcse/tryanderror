import json
import openai
from flask import Flask, request, jsonify

openai.api_key = "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"

def extract_ids(string):
    try:
        data = json.loads(string)
        ids = [item["id"] for item in data]
        return ids
    except (json.JSONDecodeError, KeyError):
        return []

def find_matching_data(ids, json_data):
    try:
        data = json.loads(json_data)
        matching_data = [item for item in data["data"] if item["id"] in ids]
        return matching_data
    except (json.JSONDecodeError, KeyError):
        return []


app = Flask(__name__)

@app.route('/api', methods=['POST'])
def process_request():
    # Extract request data
    request_data = request.json
    prompt = request_data.get('prompt')
    base_prompt= """
        I am a vehicle search engine. I will search vehicle based on following json input data. The model should iterate through the input json data, look for value of the json property and if it find any match then return that particular vehicle id in json format. If it does not find any match for a request, it should return an empty json data. For example, if I search for all blue color vehicle, it should iterate through the json input data, look for exterior_color property and return if it find a value blue. Similarly, if I search for vehicle with certain mileage, it should iterate through the json data, check mileage property and compare if the requested mileage is falling into that range or not, if it find a match return the vehicle id otherwise return empty json. ###
        Input data: ###
        {"data":[{"id":"-7932487686042285633","vin":"2C3CDXGJ5PH552841","make":"Dodge","model":"Charger","trim":"Scat Pack","body_style":"Sedan","exterior_color":"Orange","engine":"8 Cyl","transmission":"Automatic","drive_type":"RWD","fuel":"Gasoline","vehicle_condition":"New","mpg_combined":18,"year":2023,"mileage":2,"price":58222,"mpg_city":15,"mpg_highway":24,"dealer":{"name":"Greensboro Chrysler Dodge Jeep Ram","country":"United States","state":"NC","city":"Greensboro","zip":"27407","street":"3710 W Wendover Avenue","distance":4}},{"id":"-4477316342679034490","vin":"1FT8W2BN3PEC96392","make":"Ford","model":"F-250","trim":"XLT","body_style":"Pickup","exterior_color":"Black","engine":"8 Cyl","transmission":"Automatic","drive_type":"4WD","fuel":"Gasoline","vehicle_condition":"New","year":2023,"mileage":15,"price":67230,"dealer":{"name":"Parkway Ford Lincoln","country":"United States","state":"NC","city":"Lexington","zip":"27295","street":"98 New Highway 64 West","distance":29}},{"id":"-3079516331302376356","vin":"1FTFW1ED8PFB42193","make":"Ford","model":"F-150","trim":"King Ranch","body_style":"Pickup","exterior_color":"Red","engine":"6 Cyl","transmission":"Automatic","drive_type":"4WD","fuel":"Hybrid","vehicle_condition":"New","mpg_combined":23,"year":2023,"mileage":7,"price":84520,"mpg_city":23,"mpg_highway":23,"dealer":{"name":"Parkway Ford","country":"United States","state":"NC","city":"Winston-Salem","zip":"27127","street":"2104 Peterscreek Parkway","distance":21}},{"id":"8983559685067755594","vin":"4S4BTGLDXP3214571","make":"Subaru","model":"Outback","trim":"Onyx Edition","body_style":"Wagon","exterior_color":"Silver","engine":"4 Cyl","transmission":"Automatic","drive_type":"AWD","fuel":"Gasoline","vehicle_condition":"New","mpg_combined":25,"year":2023,"mileage":8,"price":40156,"mpg_city":22,"mpg_highway":29,"dealer":{"name":"Capital Subaru Hyundai of Greensboro","country":"United States","state":"NC","city":"Greensboro","zip":"27405","street":"801 E Bessemer Avenue","distance":6}},{"id":"-21614355526434654","vin":"1HGCY1F27PA028923","make":"Honda","model":"Accord","trim":"LX","body_style":"Sedan","exterior_color":"White","engine":"4 Cyl","transmission":"Automatic","drive_type":"FWD","fuel":"Gasoline","vehicle_condition":"New","mpg_combined":32,"year":2023,"mileage":2,"price":29271,"mpg_city":29,"mpg_highway":37,"dealer":{"name":"Greensboro Honda","country":"United States","state":"NC","city":"Greensboro","zip":"27407","street":"3633 W Wendover Avenue","distance":4}},{"id":"2215576295202101220","vin":"2C3CDZFJ9PH544447","make":"Dodge","model":"Challenger","trim":"R/T","body_style":"Coupe","exterior_color":"White","engine":"8 Cyl","transmission":"Automatic","drive_type":"RWD","fuel":"Gasoline","vehicle_condition":"New","mpg_combined":18,"year":2023,"mileage":5,"price":54115,"mpg_city":15,"mpg_highway":24,"dealer":{"name":"Hillsborough Chrysler Dodge Jeep Ram","country":"United States","state":"NC","city":"Hillsborough","zip":"27278","street":"259 S Churton Street","distance":44}},{"id":"8223781617808049737","vin":"2C3CDXBG5PH600799","make":"Dodge","model":"Charger","trim":"SXT","body_style":"Sedan","exterior_color":"Gray","engine":"6 Cyl","transmission":"Automatic","drive_type":"RWD","fuel":"Gasoline","vehicle_condition":"New","mpg_combined":23,"year":2023,"mileage":5,"price":39680,"mpg_city":19,"mpg_highway":30,"dealer":{"name":"Hillsborough Chrysler Dodge Jeep Ram","country":"United States","state":"NC","city":"Hillsborough","zip":"27278","street":"259 S Churton Street","distance":44}},{"id":"-6701557851749527305","vin":"1C6SRFKT9PN606670","make":"Ram","model":"1500","trim":"Longhorn","body_style":"Pickup","exterior_color":"Red","engine":"8 Cyl","transmission":"Automatic","drive_type":"4WD","fuel":"Gasoline","vehicle_condition":"New","mpg_combined":17,"year":2023,"mileage":18,"price":71410,"mpg_city":15,"mpg_highway":21,"dealer":{"name":"Greensboro Chrysler Dodge Jeep Ram","country":"United States","state":"NC","city":"Greensboro","zip":"27407","street":"3710 W Wendover Avenue","distance":4}},{"id":"8354242540373941781","vin":"2FMPK4J91PBA33798","make":"Ford","model":"Edge","trim":"SEL","body_style":"SUV","exterior_color":"Blue","engine":"4 Cyl","transmission":"Automatic","drive_type":"AWD","fuel":"Gasoline","vehicle_condition":"New","year":2023,"mileage":15,"price":38138,"dealer":{"name":"Parkway Ford Lincoln","country":"United States","state":"NC","city":"Lexington","zip":"27295","street":"98 New Highway 64 West","distance":29}},{"id":"-1475846225309116216","vin":"7FARS4H26PE021210","make":"Honda","model":"CR-V","trim":"LX","body_style":"SUV","exterior_color":"Blue","engine":"4 Cyl","transmission":"Automatic","drive_type":"AWD","fuel":"Gasoline","vehicle_condition":"New","mpg_combined":29,"year":2023,"mileage":10,"price":31205,"mpg_city":27,"mpg_highway":32,"dealer":{"name":"Greensboro Honda","country":"United States","state":"NC","city":"Greensboro","zip":"27407","street":"3633 W Wendover Avenue","distance":4}}]}
        Response format: ###
        [{"id": <String>}] ###

        Q: show me all orange car ###
        [{"id":"-7932487686042285633"}]

        Q: show me all car price between 67225 and 67235 ###
        [{"id":"-4477316342679034490"}]

        Q: show me all red car with mileage between 15 and 19 ###
        [{"id":"-6701557851749527305"}] 
        """;
    new_prompt = base_prompt + "\nQ: " + prompt + ' ###'

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=new_prompt,
        temperature=0.7,
        max_tokens=100,
        top_p=0.7,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )    
    print ("Response from OpenAI=",response);
    # Extract relevant information from OpenAI response
    vechile_response = response['choices'][0]['text']
    vechile_ids = extract_ids (vechile_response)
    print ("Vehicle ids=", vechile_ids)
    json_data = """
        {"data":[{"id":"-7932487686042285633","vin":"2C3CDXGJ5PH552841","make":"Dodge","model":"Charger","trim":"Scat Pack","body_style":"Sedan","exterior_color":"Orange","engine":"8 Cyl","transmission":"Automatic","drive_type":"RWD","fuel":"Gasoline","vehicle_condition":"New","mpg_combined":18,"year":2023,"mileage":2,"price":58222,"mpg_city":15,"mpg_highway":24,"dealer":{"name":"Greensboro Chrysler Dodge Jeep Ram","country":"United States","state":"NC","city":"Greensboro","zip":"27407","street":"3710 W Wendover Avenue","distance":4}},{"id":"-4477316342679034490","vin":"1FT8W2BN3PEC96392","make":"Ford","model":"F-250","trim":"XLT","body_style":"Pickup","exterior_color":"Purple","engine":"8 Cyl","transmission":"Automatic","drive_type":"4WD","fuel":"Gasoline","vehicle_condition":"New","year":2023,"mileage":15,"price":67230,"dealer":{"name":"Parkway Ford Lincoln","country":"United States","state":"NC","city":"Lexington","zip":"27295","street":"98 New Highway 64 West","distance":29}},{"id":"-3079516331302376356","vin":"1FTFW1ED8PFB42193","make":"Ford","model":"F-150","trim":"King Ranch","body_style":"Pickup","exterior_color":"Red","engine":"6 Cyl","transmission":"Automatic","drive_type":"4WD","fuel":"Hybrid","vehicle_condition":"New","mpg_combined":23,"year":2023,"mileage":7,"price":84520,"mpg_city":23,"mpg_highway":23,"dealer":{"name":"Parkway Ford","country":"United States","state":"NC","city":"Winston-Salem","zip":"27127","street":"2104 Peterscreek Parkway","distance":21}},{"id":"8983559685067755594","vin":"4S4BTGLDXP3214571","make":"Subaru","model":"Outback","trim":"Onyx Edition","body_style":"Wagon","exterior_color":"Silver","engine":"4 Cyl","transmission":"Automatic","drive_type":"AWD","fuel":"Gasoline","vehicle_condition":"New","mpg_combined":25,"year":2023,"mileage":8,"price":40156,"mpg_city":22,"mpg_highway":29,"dealer":{"name":"Capital Subaru Hyundai of Greensboro","country":"United States","state":"NC","city":"Greensboro","zip":"27405","street":"801 E Bessemer Avenue","distance":6}},{"id":"-21614355526434654","vin":"1HGCY1F27PA028923","make":"Honda","model":"Accord","trim":"LX","body_style":"Sedan","exterior_color":"White","engine":"4 Cyl","transmission":"Automatic","drive_type":"FWD","fuel":"Gasoline","vehicle_condition":"New","mpg_combined":32,"year":2023,"mileage":2,"price":29271,"mpg_city":29,"mpg_highway":37,"dealer":{"name":"Greensboro Honda","country":"United States","state":"NC","city":"Greensboro","zip":"27407","street":"3633 W Wendover Avenue","distance":4}},{"id":"2215576295202101220","vin":"2C3CDZFJ9PH544447","make":"Dodge","model":"Challenger","trim":"R/T","body_style":"Coupe","exterior_color":"White","engine":"8 Cyl","transmission":"Automatic","drive_type":"RWD","fuel":"Gasoline","vehicle_condition":"New","mpg_combined":18,"year":2023,"mileage":5,"price":54115,"mpg_city":15,"mpg_highway":24,"dealer":{"name":"Hillsborough Chrysler Dodge Jeep Ram","country":"United States","state":"NC","city":"Hillsborough","zip":"27278","street":"259 S Churton Street","distance":44}},{"id":"8223781617808049737","vin":"2C3CDXBG5PH600799","make":"Dodge","model":"Charger","trim":"SXT","body_style":"Sedan","exterior_color":"Gray","engine":"6 Cyl","transmission":"Automatic","drive_type":"RWD","fuel":"Gasoline","vehicle_condition":"New","mpg_combined":23,"year":2023,"mileage":5,"price":39680,"mpg_city":19,"mpg_highway":30,"dealer":{"name":"Hillsborough Chrysler Dodge Jeep Ram","country":"United States","state":"NC","city":"Hillsborough","zip":"27278","street":"259 S Churton Street","distance":44}},{"id":"-6701557851749527305","vin":"1C6SRFKT9PN606670","make":"Ram","model":"1500","trim":"Longhorn","body_style":"Pickup","exterior_color":"Red","engine":"8 Cyl","transmission":"Automatic","drive_type":"4WD","fuel":"Gasoline","vehicle_condition":"New","mpg_combined":17,"year":2023,"mileage":18,"price":71410,"mpg_city":15,"mpg_highway":21,"dealer":{"name":"Greensboro Chrysler Dodge Jeep Ram","country":"United States","state":"NC","city":"Greensboro","zip":"27407","street":"3710 W Wendover Avenue","distance":4}},{"id":"8354242540373941781","vin":"2FMPK4J91PBA33798","make":"Ford","model":"Edge","trim":"SEL","body_style":"SUV","exterior_color":"Blue","engine":"4 Cyl","transmission":"Automatic","drive_type":"AWD","fuel":"Gasoline","vehicle_condition":"New","year":2023,"mileage":15,"price":38138,"dealer":{"name":"Parkway Ford Lincoln","country":"United States","state":"NC","city":"Lexington","zip":"27295","street":"98 New Highway 64 West","distance":29}},{"id":"-1475846225309116216","vin":"7FARS4H26PE021210","make":"Honda","model":"CR-V","trim":"LX","body_style":"SUV","exterior_color":"Blue","engine":"4 Cyl","transmission":"Automatic","drive_type":"AWD","fuel":"Gasoline","vehicle_condition":"New","mpg_combined":29,"year":2023,"mileage":10,"price":31205,"mpg_city":27,"mpg_highway":32,"dealer":{"name":"Greensboro Honda","country":"United States","state":"NC","city":"Greensboro","zip":"27407","street":"3633 W Wendover Avenue","distance":4}}]}
        """
    vechiles = find_matching_data(vechile_ids, json_data)
    # # Prepare and return the response
    # response = {
    #     'vin': parsed_data.get('vin'),
    #     'make': parsed_data.get('make'),
    #     'model': parsed_data.get('model'),
    #     'trim': parsed_data.get('trim'),
    #     'body_style': parsed_data.get('body_style'),
    #     'dealer': {
    #         'name': parsed_data.get('dealer', {}).get('name')
    #     }
    # }

    return jsonify(vechiles), 200

def extract_ids(string):
    try:
        data = json.loads(string)
        ids = [item["id"] for item in data]
        return ids
    except (json.JSONDecodeError, KeyError):
        return []

if __name__ == '__main__':
    app.run()
