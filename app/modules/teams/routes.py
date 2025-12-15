from flask import Blueprint,request,jsonify
from flask_jwt_extended import jwt_required,get_jwt_identity
from .services import TeamService
from pydantic import ValidationError
from .schemas import (AddMemberSchema,TeamCreateSchema,TeamMemberReadSchema,RemoveMemberParamsSchema,UpdateMemberRoleSchema)
from app.modules.teams.models import HackathonTeam,HackathonTeamMember
team_bp = Blueprint("teams", __name__)

@team_bp.route('/',methods=['GET'])
def check_team():
    return jsonify("This is home team route")

@team_bp.route('/create',methods=['POST'])
@jwt_required()
def create_team():  
    try:
        payload = TeamCreateSchema(**request.get_json())
    except ValidationError as e:
        return {"errors": e.errors()}, 400

    user_id = int(get_jwt_identity())

    team = TeamService.create_team(payload.name, user_id)

    return jsonify({
        "id": team.id,
        "name": team.name,
        "created_by": team.created_by,
        "created_at": team.created_at.isoformat()
    }), 201


@team_bp.route('/<team_id>/members',methods=['POST'])
@jwt_required() 
def add_member(team_id):
    try:
        payload = AddMemberSchema(**request.get_json())
    except ValidationError as e:
        return {"errors": e.errors()}, 400

    requester_id = int(get_jwt_identity())

    member = TeamService.add_member(
        team_id=team_id,
        requester_id=requester_id,
        member_id=payload.member_id,
        role=payload.role.value
    )

    return jsonify({
        "id": member.id,
        "hackathon_team_id": member.hackathon_team_id,
        "member_id": member.member_id,
        "role": member.role.value,
        "joined_at": member.joined_at.isoformat()
    }), 201

@team_bp.route('/<team_id>/members/<member_id>',methods=['DELETE'])
@jwt_required()
def remove_member(team_id,member_id):
    try:
        params = RemoveMemberParamsSchema(
            team_id=team_id,
            member_id=member_id
        )
    except ValidationError as e:
        return {"errors": e.errors()}, 400

    requester_id = int(get_jwt_identity())

    try:
        TeamService.remove_member(
            team_id=params.team_id,
            member_id=params.member_id,
            requester_id=requester_id
        )
    except Exception:
        return {"error": "Internal server error"}, 500

    return jsonify({
        "message": "Member removed successfully"
    }), 200

@team_bp.route('/<string:team_id>/members/<int:member_id>/role',methods=['PUT'])
@jwt_required()
def update_member_role(team_id,member_id):
    try:
           
        data = UpdateMemberRoleSchema(**request.get_json()) 
    except ValidationError as e:
        return {"errors": e.errors()}, 400

    requester_id = int(get_jwt_identity())
    try:
        member = TeamService.update_member_role(
            team_id=team_id,
            member_id=member_id,
            new_role=data.role.value,
            requester_id=requester_id
        )
    except Exception:
        return {"error": "Internal server error"}, 500

    return jsonify({
        "id": member.id,
        "hackathon_team_id": member.hackathon_team_id,
        "member_id": member.member_id,
        "role": member.role.value,
        "joined_at": member.joined_at.isoformat()
    }), 200


@team_bp.route('/<string:team_id>', methods=['GET'])
@jwt_required()
def get_team(team_id):
    team = HackathonTeam.query.get(team_id)
    if not team:
        return {"error": "Team not found"}, 404

    return jsonify(
        TeamService._serialize_team(team)
    ), 200

@team_bp.route("/my-teams", methods=["GET"])
@jwt_required()
def get_my_teams():
    user_id = int(get_jwt_identity())

    teams = TeamService.get_my_teams(user_id)

    return jsonify({
        "results": teams,
        "total": len(teams)
    }), 200