from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import exc, and_

from app import models, oauth2
from app.database import engine, get_db
from app.schemas import Vote


router = APIRouter(prefix='/vote', tags=['Vote'])


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote_req: Vote, db: Session = Depends(get_db), current_user: 'models.User' = Depends(oauth2.get_current_user)):

    post = db.query(models.Post).get(vote_req.post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post not found id={vote_req.post_id}')

    vote_obj = db.query(models.Votes) \
        .filter(and_(models.Votes.post_id == vote_req.post_id,
                     models.Votes.user_id == current_user.id)) \
        .first()

    if vote_req.vote_dir == 1:

        if vote_obj is not None:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f'User {current_user.id} has already liked this post {vote_req.post_id}')
        vote_obj = models.Votes(post_id=vote_req.post_id, user_id=current_user.id)
        db.add(vote_obj)
        message = 'Successfuly added vote'

    else:  # vote_dir is 0

        if vote_obj is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Unable to find post')

        db.delete(vote_obj)
        message = 'Successfuly deleted vote'

    try:
        db.commit()
    except exc.SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)

    return {'message': message}
