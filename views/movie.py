from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Movie, db

movie_bp = Blueprint('movie_bp', __name__ )

@movie_bp.route("/movies", methods=['POST'])
def register_movie():
    data = request.get_json()
    title = data['title']
    director = data['director']
    release_year = data['release_year']
    user_id = data['user_id']


    check_movie = Movie.query.filter_by(title=title).first()

    if check_movie:
        return jsonify({'error': "movie already exists"})
    else:
        new_movie = Movie(title=title, director=director, release_year=release_year, user_id=user_id)
        db.session.add(new_movie)
        db.session.commit()

        return jsonify({'message': "movie registered successfully"}), 201

    # Update the movie account
@movie_bp.route("/movies/update", methods=['PATCH'])
@jwt_required()
def update_movie():
    current_movie_id = get_jwt_identity()

    movie = Movie.query.get(current_movie_id)

    if movie:
        data = request.get_json()

        title = data.get('title', movie.title)
        director = data.get('director', movie.director)
        release_year = data.get('release_year', movie.release_year)
        user_id = data.get('user_id', movie.user_id)

        check_movie = Movie.query.filter_by(movie=movie and id!=movie.id).first()

        if check_movie :
            return jsonify({'error': "moviename or email already exists"})
        else:
            movie.title = title
            movie.director = director
            movie.release_year = release_year
            movie.user_id = user_id

            db.session.commit()

            return jsonify({'message': "movie updated successful"})
    else:
        return jsonify({'error': "movie not found"}), 404

# Delete a movie
@movie_bp.route("/movies/delete", methods=['DELETE'])
@jwt_required()
def delete_movie():
    current_movie_id = get_jwt_identity()

    movie = Movie.query.get(current_movie_id)

    if movie:
        db.session.delete(movie)
        db.session.commit()

        return jsonify({'message': "movie deleted successfully"}), 200
    else:
        return jsonify({'error': "movie not found"}), 404