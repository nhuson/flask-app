from flask import jsonify, request
from src import app, redis_client
from src.middlewares.authenicate import authenicate_required
from src.services.Address import AddressService

addressService = AddressService()

@app.route('/countries')
def getCountry():
    try:
        countries = addressService.getCountries()
        return jsonify({"data": countries})
    except Exception as error:
        return jsonify({ "success": False, "message": str(error) }), 500

@app.route('/address')
def getAddress():
    try:
        country = request.args.get('country')
        province = request.args.get('province')
        district = request.args.get('district')
        
        data = []
        if country:
            data = addressService.getProvinceByCountryId(country)
        if province:
                data = addressService.getDistrictByProvinceId(province)
        if district:
            data = addressService.getTownByDistrictId(district)

        return jsonify({ "data": data, "success": True })   
    except Exception as error:
       return jsonify({ "success": False, "message": str(error) }), 500
        
@app.route('/get-customer-group', methods=["POST"])
@authenicate_required()
def getCustomerGroupByAddress():
    try:
        params = {
            "province": request.json.get('province', None),
            "district": request.json.get('district', None),
            "town": request.json.get('town', None),
            "cluster_by": request.json.get('cluster_by', None),
            "address": request.json.get('address', None),
            "organizationIds": request.json.get('organizationIds', None)
        }
        
        result = addressService.getCustomerGroupByAddress(params)
        
        return jsonify({ "success": True, "data": result })
    except Exception as error:
        return jsonify({ "success": False, "message": str(error) }), 500

@app.route('/valid-address', methods=["GET"])
@authenicate_required()
def validAddress():
    try:
        params = {
            "province": request.args.get('province', None),
            "district": request.args.get('district', None),
            "town": request.args.get('town')
        }

        addressService.validAddress(params)
        
        return jsonify({ "success": True })

    except Exception as error:
        return jsonify({ "success": False, "message": str(error) }), 500

@app.route('/generate-customer-group', methods=["POST"])
@authenicate_required()
def generateCustomerGroup():
    try:
        if request.json.get('cluster_by') is None:
            raise Exception("Cluster By is required!")

        if request.json.get('address') is None:
            raise Exception("Address is required!")

        params = {
            "address": request.json.get('address'),
            "cluster_by": request.json.get('cluster_by')
        }

        result = addressService.generateCustomerGroup(params)
        
        return jsonify({ "success": True, "data": result })

    except Exception as error:
        return jsonify({ "success": False, "message": str(error) }), 500

@app.route('/customer-group-to-address', methods=["GET"])
@authenicate_required()
def customerGroupToAddress():
    try:
        if request.args.get('customer_group') is None:
            raise Exception("Customer group is required!")
        
        result = addressService.customerGroupToAddress(request.args.get('customer_group'))
        return jsonify({"success": True, "data": result})
    except Exception as error:
        return jsonify({ "success": False, "message": str(error) }), 500

@app.route('/get-address-name', methods=["GET"])
def getDistrictsByProvinceName():
    try:
        params = {
            "province": request.args.get('province', None),
            "district": request.args.get('district', None)
        }
        result = addressService.getAddressByName(params)
        return jsonify({"success": True, "data": result})
    except Exception as error:
        return jsonify({ "success": False, "message": str(error) }), 500

@app.route('/get-address', methods=["POST"])
def getAddressDetail():
    try:
        if request.json.get('address') is None:
            raise Exception("Address is required.")

        params = {
            "address": request.json.get('address'),
        }
        
        result = addressService.getAddressDetail(params)
        
        return jsonify({ "success": True, "data": result })
    except Exception as error:
        return jsonify({ "success": False, "message": str(error) }), 500