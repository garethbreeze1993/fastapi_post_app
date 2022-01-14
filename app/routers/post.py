from typing import List, Optional

from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import exc, func

from app import models, oauth2
from app.database import engine, get_db
from app.schemas import PostCreate, Post, PostOut

router = APIRouter(prefix='/posts', tags=['Posts'])


@router.get("/", response_model=List[PostOut])
def get_posts(db: Session = Depends(get_db), current_user: 'models.User' = Depends(oauth2.get_current_user),
              limit: int = 10, skip: int = 0, search: Optional[str] = ''):
    # Below is left outer join from posts table to votes
    posts = db.query(models.Post,
                     func.count(models.Votes.post_id).label('votes')) \
        .join(models.Votes, models.Votes.post_id == models.Post.id, isouter=True) \
        .group_by(models.Post.id) \
        .filter(models.Post.title.contains(search)) \
        .limit(limit) \
        .offset(skip) \
        .all()
    return posts


@router.get("/{id_}", response_model=PostOut)
def get_post(id_: int, db: Session = Depends(get_db), current_user: 'models.User' = Depends(oauth2.get_current_user)):
    post = db.query(models.Post,
                    func.count(models.Votes.post_id).label('votes')) \
        .join(models.Votes, models.Votes.post_id == models.Post.id, isouter=True) \
        .group_by(models.Post.id) \
        .filter(models.Post.id == id_)\
        .first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post not found id={id_}')
    return post


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Post)
def create_posts(post: PostCreate, db: Session = Depends(get_db),
                 current_user: 'models.User' = Depends(oauth2.get_current_user)):
    # Unpack dictionary and put in kwargs to new model
    new_post = models.Post(**post.dict())
    new_post.owner_id = current_user.id
    db.add(new_post)
    try:
        db.commit()
    except exc.SQLAlchemyError as e:
        # Handle error better
        return {'error', e}
    db.refresh(new_post)
    return new_post


@router.delete("/{id_}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id_: int, db: Session = Depends(get_db),
                current_user: 'models.User' = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).get(id_)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post not found id={id_}')
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not authorised to perform requested action')
    db.delete(post)
    try:
        db.commit()
    except exc.SQLAlchemyError as e:
        # Handle error better
        return {'error', e}
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id_}", response_model=Post)
def update_post(id_: int, updated_post: PostCreate, db: Session = Depends(get_db),
                current_user: 'models.User' = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).get(id_)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post not found id={id_}')
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not authorised to perform requested action')
    for field in ['title', 'content', 'published']:
        setattr(post, field, getattr(updated_post, field))
    db.add(post)
    try:
        db.commit()
    except exc.SQLAlchemyError as e:
        # Handle error better
        return {'error', e}
    db.refresh(post)
    return post
