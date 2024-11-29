# backend/routes/prompt.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Prompt, User
from utils.prompt_optimizer import optimize_prompt_text

prompt_bp = Blueprint('prompt', __name__)

@prompt_bp.route('/', methods=['GET'])
@jwt_required()
def get_prompts():
    user_id = get_jwt_identity()
    prompts = Prompt.query.filter_by(user_id=user_id).all()
    prompts_data = [
        {
            "id": prompt.id,
            "original_text": prompt.original_text,
            "optimized_text": prompt.optimized_text,
            "created_at": prompt.created_at
        } for prompt in prompts
    ]
    return jsonify(prompts_data), 200

@prompt_bp.route('/', methods=['POST'])
@jwt_required()
def create_prompt():
    user_id = get_jwt_identity()
    data = request.get_json()
    original_text = data.get('original_text')

    if not original_text:
        return jsonify({"msg": "Original prompt text is required"}), 400

    optimized_text = optimize_prompt_text(original_text)

    new_prompt = Prompt(
        original_text=original_text,
        optimized_text=optimized_text,
        user_id=user_id
    )
    db.session.add(new_prompt)
    db.session.commit()

    return jsonify({
        "id": new_prompt.id,
        "original_text": new_prompt.original_text,
        "optimized_text": new_prompt.optimized_text,
        "created_at": new_prompt.created_at
    }), 201

@prompt_bp.route('/<int:prompt_id>', methods=['PUT'])
@jwt_required()
def update_prompt(prompt_id):
    user_id = get_jwt_identity()
    prompt = Prompt.query.filter_by(id=prompt_id, user_id=user_id).first()

    if not prompt:
        return jsonify({"msg": "Prompt not found"}), 404

    data = request.get_json()
    original_text = data.get('original_text')

    if original_text:
        prompt.original_text = original_text
        prompt.optimized_text = optimize_prompt_text(original_text)

    db.session.commit()

    return jsonify({
        "id": prompt.id,
        "original_text": prompt.original_text,
        "optimized_text": prompt.optimized_text,
        "created_at": prompt.created_at
    }), 200

@prompt_bp.route('/<int:prompt_id>', methods=['DELETE'])
@jwt_required()
def delete_prompt(prompt_id):
    user_id = get_jwt_identity()
    prompt = Prompt.query.filter_by(id=prompt_id, user_id=user_id).first()

    if not prompt:
        return jsonify({"msg": "Prompt not found"}), 404

    db.session.delete(prompt)
    db.session.commit()

    return jsonify({"msg": "Prompt deleted successfully"}), 200
