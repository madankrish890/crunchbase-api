import requests
from flask import Flask, jsonify, render_template

app = Flask(__name__)

# Define the Crunchbase API endpoint
url = "https://crunchbase-crunchbase-v1.p.rapidapi.com/searches/organizations"

payload = {
    "field_ids": ["identifier", "location_identifiers", "short_description", "rank_org"],
    "limit": 50,
    "order": [
        {
            "field_id": "rank_org",
            "sort": "asc"
        }
    ],
    "query": [
        {
            "field_id": "location_identifiers",
            "operator_id": "includes",
            "type": "predicate",
            "values": ["6106f5dc-823e-5da8-40d7-51612c0b2c4e"]
        },
        {
            "field_id": "facet_ids",
            "operator_id": "includes",
            "type": "predicate",
            "values": ["company"]
        }
    ]
}

headers = {
    "content-type": "application/json",
    "X-RapidAPI-Key": "1b2826a25dmsh9d86c195a8439afp1a1b81jsn1ff37b2ff8f0",
    "X-RapidAPI-Host": "crunchbase-crunchbase-v1.p.rapidapi.com"
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/organizations', methods=['GET'])
def get_organizations():
    response = requests.post(url, json=payload, headers=headers)
    data = response.json()
    organizations = []
    for entity in data['entities']:
        org_data = {
            'uuid': entity['uuid'],
            'name': entity['properties']['identifier']['value'],
            'image': entity['properties']['identifier']['image_id'],
            'description': entity['properties']['short_description'],
            'rank': entity['properties']['rank_org'],
            'locations': [location['value'] for location in entity['properties']['location_identifiers']]
        }
        organizations.append(org_data)
    return jsonify(organizations)

@app.route('/organizations/rank/<int:rank>', methods=['GET'])
def get_organizations_by_rank(rank):
    response = requests.post(url, json=payload, headers=headers)
    data = response.json()
    organizations = []
    for entity in data['entities']:
        if entity['properties']['rank_org'] == rank:
            org_data = {
                'uuid': entity['uuid'],
                'name': entity['properties']['identifier']['value'],
                'image': entity['properties']['identifier']['image_id'],
                'description': entity['properties']['short_description'],
                'rank': entity['properties']['rank_org'],
                'locations': [location['value'] for location in entity['properties']['location_identifiers']]
            }
            organizations.append(org_data)
    if organizations:
        return render_template('rank.html', organizations=organizations)
    else:
        return jsonify({'error': 'No organizations found for the given rank'}), 404

@app.route('/organizations/locations/<location>', methods=['GET'])
def get_organizations_by_location(location):
    response = requests.post(url, json=payload, headers=headers)
    data = response.json()
    organizations = []
    for entity in data['entities']:
        locations = [loc['value'] for loc in entity['properties']['location_identifiers']]
        if location in locations:
            org_data = {
                'uuid': entity['uuid'],
                'name': entity['properties']['identifier']['value'],
                'image': entity['properties']['identifier']['image_id'],
                'description': entity['properties']['short_description'],
                'rank': entity['properties']['rank_org'],
                'locations': locations
            }
            organizations.append(org_data)
    if organizations:
        return render_template('location.html', organizations=organizations)
    else:
        return jsonify({'error': 'No organizations found for the given location'}), 404


@app.route('/organizations/uuid/<uuid>', methods=['GET'])
def get_organization_by_uuid(uuid):
    response = requests.post(url, json=payload, headers=headers)
    data = response.json()
    for entity in data['entities']:
        if entity['uuid'] == uuid:
            org_data = {
                'uuid': entity['uuid'],
                'name': entity['properties']['identifier']['value'],
                'image': entity['properties']['identifier']['image_id'],
                'description': entity['properties']['short_description'],
                'rank': entity['properties']['rank_org'],
                'locations': [location['value'] for location in entity['properties']['location_identifiers']]
            }
            return render_template('uuid.html', organization=org_data)
    return jsonify({'error': 'Organization not found'}), 404

@app.route('/organizations/name/<name>', methods=['GET'])
def get_organizations_by_name(name):
    response = requests.post(url, json=payload, headers=headers)
    data = response.json()
    organizations = []
    for entity in data['entities']:
        if entity['properties']['identifier']['value'].lower() == name.lower():
            org_data = {
                'uuid': entity['uuid'],
                'name': entity['properties']['identifier']['value'],
                'image': entity['properties']['identifier']['image_id'],
                'description': entity['properties']['short_description'],
                'rank': entity['properties']['rank_org'],
                'locations': [location['value'] for location in entity['properties']['location_identifiers']]
            }
            organizations.append(org_data)
    if organizations:
        return render_template('name.html', organizations=organizations)
    else:
        return jsonify({'error': 'No organizations found for the given name'}), 404

@app.route('/organizations/description/<description>', methods=['GET'])
def get_organizations_by_description(description):
    response = requests.post(url, json=payload, headers=headers)
    data = response.json()
    organizations = []
    for entity in data['entities']:
        if description.lower() in entity['properties']['short_description'].lower():
            org_data = {
                'uuid': entity['uuid'],
                'name': entity['properties']['identifier']['value'],
                'image': entity['properties']['identifier']['image_id'],
                'description': entity['properties']['short_description'],
                'rank': entity['properties']['rank_org'],
                'locations': [location['value'] for location in entity['properties']['location_identifiers']]
            }
            organizations.append(org_data)
    if organizations:
        return render_template('description.html', organizations=organizations)
    else:
        return jsonify({'error': 'No organizations found for the given description'}), 404


if __name__ == '__main__':
    app.run()
