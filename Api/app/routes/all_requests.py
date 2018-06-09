"""Handle requests routes."""
from flask_restplus import Resource, Namespace, fields
from flask import request

# local imports
from app.DB import manage
from app.models.request import CreateRequest
from app.models.token import token_required

request_namespace = Namespace(
    'requests', description='Request Related Operation.')

request_model = request_namespace.model(
    'request_model', {
        'user_request':
        fields.String(
            required=True,
            description='Create a request',
            example='plumbering'),
        'category':
        fields.String(
            required=True,
            description="Category which request belongs",
            example="Maintenance/Repair"),
        'location':
        fields.String(
            required=True,
            description="Area",
            example="EASTMAERT St 45F Hurlin")
    })


@request_namespace.route('/requests')
@request_namespace.doc(
    responses={
        200: 'Requests found successfully',
        404: 'Requests not found',
    },
    security='apikey')
class AllReaquests(Resource):
    """Handle [endpoint] GET."""

    @token_required
    def get(self, current_user):
        user_req = manage.get_all_requests(current_user)
        if len(user_req) == 0:
            return {"Message": "No request found!"}, 404
        return user_req

    @token_required
    @request_namespace.doc(
        responses={
            201: 'Request successfully created',
            400: 'Invalid parameters provided'
        },
        security='apikey')
    @request_namespace.expect(request_model)
    def post(self, user_id):
        """Handle [Endpoint] POST."""
        data = request.get_json()
        try:
            user_request = data['user_request']
            category = data['category']
            location = data['location']
            create = CreateRequest(user_request, category, location, user_id)
            create.save_request()
            return {"Message": "Request Successfully created"}, 201
        except KeyError:
            return {'Message': "All input data required"}, 400


@request_namespace.route('/requests/<int:requestId>')
class UpdateRequest(Resource):
    """Handle [Endpoint] PUT."""

    @request_namespace.expect(request_model)
    @token_required
    @request_namespace.doc(
        responses={
            201: 'Request successfully updated!',
            400: 'Invalid parameters provided'
        },
        security='apikey')
    def put(self, current_user, requestId):
        edit_req = manage.get_request(requestId)
        if len(edit_req) == 0:
            return {"Message": "No request found!"}, 404
        data = request.get_json()
        try:
            edit_user_request = data['user_request']
            edit_category = data['category']
            edit_location = data['location']
            manage.update_request(edit_user_request, edit_category,
                                  edit_location, requestId)
            return {'Message': 'successfully updated'}, 201
        except KeyError:
            return {'Message': 'All input data required!'}, 400

    @token_required
    @request_namespace.doc(
        responses={
            200: 'Requests found successfully',
            404: 'Requests not found',
        },
        security='apikey')
    def get(self, current_user, requestId):
        req = manage.get_request(requestId)
        if len(req) == 0:
            return {'Message': 'No request found!'}
        return req

    @token_required
    @request_namespace.doc(
        responses={
            200: 'Request Deleted successfully',
            404: 'Request not found',
        },
        security='apikey')
    def delete(self, current_user, requestId):
        req = manage.get_request(requestId)
        manage.delete_request(requestId)
        if len(req) == 0:
            return {"Message": "Such request not found!!"}
        return {'Message': 'Deleted {} from your requests.'.format(req)}, 200
