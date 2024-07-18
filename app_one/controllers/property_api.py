import ast
import json
from urllib.parse import parse_qs
from odoo import http
from odoo.http import request

# -*- coding: utf-8 -*-
from typing import Dict, List

import babel.dates
import base64
import copy
import itertools
import json
import pytz

from odoo import _, _lt, api, fields, models
from odoo.fields import Command
from odoo.models import BaseModel, NewId
from odoo.osv.expression import AND, TRUE_DOMAIN, normalize_domain
from odoo.tools import date_utils, unique
from odoo.tools.misc import OrderedSet, get_lang
from odoo.exceptions import UserError
from collections import defaultdict

class PropertyApi(http.Controller):


    @http.route("/api/tests", methods=["GET"], type="http", auth="none", csrf=False)
    def tests_endpoint(self):
        print("GET")

    @http.route("/v1/property", methods=["POST"], type="http", auth="none", csrf=False)
    def post_property(self):
        args = request.httprequest.data.decode()
        vals = json.loads(args)
        if not vals.get('name'):
            return request.make_json_response({
                "error": "Name is required!",
            }, status=400)
        try:
            res = request.env['property'].sudo().create(vals)
            if res:
                return request.make_json_response({
                    "message": "Property has been created successfully",
                    "id": res.id,
                    "name": res.name,
                }, status=200)
        except Exception as error:
            return request.make_json_response({
                "error": error,
            }, status=400)

    @http.route("/v1/property/json", methods=["POST"], type="json", auth="none", csrf=False)
    def post_property_json(self):
        args = request.httprequest.data.decode()
        vals = json.loads(args)
        res = request.env['property'].sudo().create(vals)
        if res:
            return [{
                "message": "Property has been created successfully",
            }]

    @http.route("/v1/property/<int:property_id>", methods=["PUT"], type="http", auth="none", csrf=False)
    def update_property(self, property_id):
        try:
            property_id = request.env['property'].sudo().search([('id','=',property_id)])
            if not property_id:
                return request.make_json_response({
                    "error": "ID does not exist!",
                }, status=400)
            args = request.httprequest.data.decode()
            vals = json.loads(args)
            property_id.write(vals)
            return request.make_json_response({
                "message": "Property has been update successfully",
                "id": property_id.id,
                "name": property_id.name,
            }, status=200)
        except Exception as error:
            return request.make_json_response({
                "error": error,
            }, status=400)

    @http.route("/v1/property/<int:property_id>", methods=["GET"], type="http", auth="none", csrf=False)
    def get_property(self, property_id):
        try:
            property_id = request.env['property'].sudo().search([('id','=',property_id)])
            if not property_id:
                return request.make_json_response({
                    "error": "ID does not exist!",
                }, status=400)
            return request.make_json_response({
                "id": property_id.id,
                "name": property_id.name,
                "ref": property_id.ref,
            }, status=200)
        except Exception as error:
            return request.make_json_response({
                "error": error,
            }, status=400)

    @http.route("/v1/property/<int:property_id>", methods=["DELETE"], type="http", auth="none", csrf=False)
    def delete_property(self, property_id):
        try:
            property_id = request.env['property'].sudo().search([('id','=',property_id)])
            if not property_id:
                return request.make_json_response({
                    "error": "ID does not exist!",
                }, status=400)
            property_id.unlink()
            return request.make_json_response({
                "message": "Property has been deleted successfully",
            }, status=200)
        except Exception as error:
            return request.make_json_response({
                "error": error,
            }, status=400)

    @http.route("/v1/properties", methods=["GET"], type="http", auth="none", csrf=False)
    def get_propert_list(self):
        try:
            params = parse_qs(request.httprequest.query_string.decode('utf-8'))
            property_domain = []
            if params.get('state'):
                property_domain += [('state','=',params.get('state')[0])]
            property_ids = request.env['property'].sudo().search(property_domain)
            if not property_ids:
                return request.make_json_response({
                    "error": "there are not records!",
                }, status=400)
            return request.make_json_response([{
                "id": property_id.id,
                "name": property_id.name,
                "ref": property_id.ref,
            } for property_id in property_ids], status=200)
        except Exception as error:
            return request.make_json_response({
                "error": error,
            }, status=400)

    @http.route(['/api3/<string:model>','/api3/<string:model>/<int:id>'], type='json', auth="none",methods=["PATCH"], csrf=False)
    def create_update_record(self, model, id=None):
        """ create or update a record of a model. """
        #_check_authenticated_user()
        if not request.env['ir.model'].sudo().search([('model', '=', model)]):
            raise Warning('There is no model named %s' % model)
        data = request.httprequest.data.decode('utf-8')
        data = ast.literal_eval(data)
        if not data:
            raise Exception("Invalid record data")
        # eval_request_params(data)
        fields = request.env[model].sudo().fields_get().keys()
        for key in data.keys():
            if key not in fields:
                raise Warning('There is no attribute named %s' % key)
        if id:
            record = request.env[model].sudo().search([('id', '=', id)])
            if not record:
                raise Exception('There is no record with id %s' % str(id))
            result = record.sudo().write(data)
            return result and 'Record with id %s successfully updated ' % str(id)