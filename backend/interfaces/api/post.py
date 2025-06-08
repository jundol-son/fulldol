from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from infrastructure.database import SessionLocal
from domain.models import Post
from schemas.post import PostCreate, PostOut, DeleteRequest
from typing import List

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/posts")
def create_post(post: PostCreate, db: Session = Depends(get_db)):
    new_post = Post(
        title=post.title,
        content=post.content,
        writer=post.writer
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"msg": "글이 저장되었습니다.", "id": new_post.id}

@router.get("/posts", response_model=List[PostOut])
def get_posts(db: Session = Depends(get_db)):
    return db.query(Post).order_by(Post.id.desc()).all()

@router.get("/posts/{post_id}", response_model=PostOut)
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="글을 찾을 수 없습니다.")
    return post


@router.put("/posts/{post_id}")
def update_post(post_id: int, updated: PostCreate, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="글을 찾을 수 없습니다.")
    if post.writer != updated.writer:
        raise HTTPException(status_code=403, detail="수정 권한이 없습니다.")


    post.title = updated.title
    post.content = updated.content
    post.writer = updated.writer

    db.commit()
    db.refresh(post)
    return {"msg": "수정 완료", "id": post.id}

@router.delete("/posts/{post_id}")
def delete_post(post_id: int, payload: DeleteRequest = Body(...), db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="글이 없습니다.")

    if post.writer != payload.writer:
        raise HTTPException(status_code=403, detail="삭제 권한이 없습니다.")

    db.delete(post)
    db.commit()
    return {"msg": "삭제 완료"}