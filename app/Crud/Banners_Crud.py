from sqlalchemy.orm import Session
from app.models.banners import Banner
from app.schemas.Banner_schema import BannerCreate, BannerUpdate


def get_all_banners(db: Session):
    return db.query(Banner).all()


def get_banner_by_id(db: Session, banner_id: int):
    return db.query(Banner).filter(Banner.id == banner_id).first()


def create_banner(db: Session, banner: BannerCreate):
    db_banner = Banner(
        badge=banner.badge,
        title1=banner.title1,
        highlight=banner.highlight,
        title2=banner.title2,
        desc1=banner.desc1,
        desc2=banner.desc2,
        image=banner.image,
        alt=banner.alt,
    )
    db.add(db_banner)
    return db_banner  


def update_banner(db: Session, banner_id: int, banner: BannerUpdate):
    db_banner = get_banner_by_id(db, banner_id)
    if not db_banner:
        return None

    for key, value in banner.model_dump(exclude_unset=True).items():
        setattr(db_banner, key, value)

    return db_banner  


def delete_banner(db: Session, banner: Banner):
    db.delete(banner)
