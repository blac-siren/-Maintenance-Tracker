"""Handle requests routes."""
from flask_restplus import Resource, Namespace, fields
from flask import request

# local imports
from app import manage
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
class AllReaquests(Resource):
    @request_namespace.doc(
        responses={
            200: 'Requests found successfully',
            404: 'Requests not found',
            422: 'Invalid parameters provided'
        },
        security='apikey')
    @token_required
    def get(self, current_user):
        user_req = manage.all_request_of_user(current_user)
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
            create = CreateRequest(
                user_request, category, location, created_by=user_id)
            create.save_request()
            import pdb
            pdb.set_trace()
            return {"Message": "Request Successfully created"}, 201

        except KeyError:
            return {'Message': "All input data required"}, 400
