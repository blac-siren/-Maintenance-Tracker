"""Module for admin routes only."""
from flask_restplus import Resource, Namespace, fields
from flask import request

# local imports
from app.DB import manage
from app.models.token import token_required

ns = Namespace('admin', description='admin Related Operation.')

status_model = ns.model(
    'status_model', {
        'status':
        fields.String(
            required=True,
            description='Status of the request.',
            example='Pending')
    })


@ns.doc(
    responses={
        200: 'Requests found successfully',
        404: 'Requests not found',
    },
    security='apikey')
@ns.route('/')
class AllReaquests(Resource):
    """Handle [endpoint] GET."""

    @token_required
    def get(self, current_user):
        """Get all request."""
        # confirm if current user is admin.
        confirm = manage.confirm_admin(current_user)
        if len(confirm) == 0:
            return {
                'Status': 'error',
                'Message': 'Access Denied!, Must be an admin.'
            }, 403

        all_req = manage.all_requests_admin()
        if len(all_req) == 0:
            return {"Message": "No request found!"}, 404
        return {
            "total request": len(all_req),
            "requests": all_req,
            "status": "success"
        }, 200


@ns.doc(
    responses={
        201: 'Successfully updated',
        404: 'Requests not found',
        403: 'Access Denied!'
    },
    security='apikey')
@ns.route('/<int:requestId>/approve')
class ApproveRequest(Resource):
    """Handle PUT routes. Only accessible to admin user."""

    @ns.expect(status_model)
    @token_required
    def put(self, current_user, requestId):
        """Approve a pending request."""
        confirm = manage.confirm_admin(current_user)
        if len(confirm) == 0:
            return {
                'Status': 'error',
                'Message': 'Access Denied!, Must be an admin.'
            }, 403

        # check if request exist.
        req = manage.get_request(requestId)
        if len(req) == 0:
            return {'Message': 'Request was not found!'}, 404

        data = request.get_json()
        status = data['status']

        if status != 'approve':
            return {"message": 'Url for approve request only.'}, 403
        else:
            manage.update_status(status, requestId)
            return {
                "Message": "Status successfully updated",
                'UserID': current_user
            }, 201


@ns.doc(
    responses={
        201: 'Successfully updated',
        404: 'Requests not found',
        403: 'Access Denied!'
    },
    security='apikey')
@ns.route('/<int:requestId>/disapprove')
class DisaproveRequest(Resource):
    """Admin disapprove request."""

    @ns.expect(status_model)
    @token_required
    def put(self, current_user, requestId):
        """Disapprove a pending request."""

        confirm = manage.confirm_admin(current_user)
        if len(confirm) == 0:
            return {
                'Status': 'error',
                'Message': 'Access Denied!, Must be an admin.'
            }, 403

        # check if request exist.
        req = manage.get_request(requestId)
        if len(req) == 0:
            return {'Message': 'Request was not found!'}, 404

        data = request.get_json()
        status = data['status']

        if status != 'disapprove':
            return {"message": 'Url for disapprove request only.'}, 403
        else:
            manage.update_status(status, requestId)
            return {
                "Message": "Status successfully updated",
                'UserID': current_user
            }, 201


@ns.doc(
    responses={
        201: 'Successfully updated',
        404: 'Requests not found',
        403: 'Access Denied!'
    },
    security='apikey')
@ns.route('/<int:requestId>/resolve')
class ResolveRequest(Resource):
    """Handle route for resolve request."""

    @ns.expect(status_model)
    @token_required
    def put(self, current_user, requestId):
        """Resolve a approve request."""

        confirm = manage.confirm_admin(current_user)
        if len(confirm) == 0:
            return {
                'Status': 'error',
                'Message': 'Access Denied!, Must be an admin.'
            }, 403
        # check if request exist.
        req = manage.get_request(requestId)
        if len(req) == 0:
            return {'Message': 'Request was not found!'}, 404

        data = request.get_json()
        status = data['status']

        if status != 'resolve':
            return {"message": 'Url for resolve request only.'}, 403
        else:
            manage.update_status(status, requestId)
            return {
                "Message": "Status successfully updated",
                'UserID': current_user
            }, 201