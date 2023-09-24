import datetime

from fastapi import HTTPException, Depends, APIRouter, status
from sqlalchemy import select, or_, and_, desc
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

import app.models as m
import app.schema as s
from app.logger import log
from config import config

from app.api.dependency import get_current_user
from app.database import get_db

# from app.hash_utils import hash_verify


user_router = APIRouter(prefix="/users", tags=["Users"])


@user_router.get("", status_code=status.HTTP_200_OK, response_model=s.User)
def get_current_user_profile(
    current_user: m.User = Depends(get_current_user),
):
    return current_user


@user_router.patch("", status_code=status.HTTP_200_OK, response_model=s.User)
def patch_user(
    data: s.UserUpdate,
    db: Session = Depends(get_db),
    current_user: m.User = Depends(get_current_user),
):
    if data.first_name:
        current_user.username = data.username
        log(
            log.INFO,
            "User [%s] username updated - [%s]",
            current_user.id,
            data.username,
        )

    if data.first_name:
        current_user.first_name = data.first_name
        log(
            log.INFO,
            "User [%s] first_name updated - [%s]",
            current_user.id,
            data.first_name,
        )

    if data.last_name:
        current_user.last_name = data.last_name
        log(
            log.INFO,
            "User [%s] last_name updated - [%s]",
            current_user.id,
            data.last_name,
        )

    if data.email:
        current_user.email = data.email
        log(log.INFO, "User [%s] email updated - [%s]", current_user.id, data.email)
    if data.picture:
        current_user.picture = data.picture
        log(log.INFO, "User [%s] picture updated", current_user.id)
    if data.phone:
        current_user.phone = data.phone
        current_user.country_code = data.country_code
        log(log.INFO, "User [%s] phone updated - [%s]", current_user.id, data.phone)

    if data.professions != current_user.professions:
        for profession in current_user.professions:
            profession_obj: m.UserProfession = db.scalar(
                select(m.UserProfession).where(
                    m.UserProfession.user_id == current_user.id,
                    m.UserProfession.profession_id == profession.id,
                )
            )
            db.delete(profession_obj)
        db.flush()
        for profession_id in data.professions:
            user_profession: m.UserProfession = db.scalar(
                select(m.UserProfession).where(
                    m.UserProfession.user_id == current_user.id,
                    m.UserProfession.profession_id == profession_id,
                )
            )
            if not user_profession:
                db.add(
                    m.UserProfession(
                        user_id=current_user.id, profession_id=profession_id
                    )
                )
                db.flush()

    if data.locations != current_user.locations:
        for location in current_user.locations:
            location_obj: m.UserLocation = db.scalar(
                select(m.UserLocation).where(
                    m.UserLocation.user_id == current_user.id,
                    m.UserLocation.location_id == location.id,
                )
            )
            db.delete(location_obj)
        db.flush()
        for location_id in data.locations:
            user_location: m.UserLocation = db.scalar(
                select(m.UserLocation).where(
                    m.UserLocation.user_id == current_user.id,
                    m.UserLocation.location_id == location_id,
                )
            )
            if not user_location:
                db.add(m.UserLocation(user_id=current_user.id, location_id=location_id))
                db.flush()
                log(
                    log.INFO,
                    "UserLocation [%s]-[%s] (user_id - location_id) created successfully",
                    current_user.id,
                    location_id,
                )

    try:
        db.commit()
    except SQLAlchemyError as e:
        log(log.INFO, "Error while updating user [%s] - %s", current_user.id, e)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Error updating user"
        )

    log(log.INFO, "User [%s] updated successfully", current_user.id)
    return current_user


@user_router.delete("", status_code=status.HTTP_200_OK, response_model=s.User)
def delete_user(
    device: s.LogoutIn,
    current_user: m.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    delete_user_view(device, current_user, db)
    return current_user


@user_router.post(
    "/check-password", status_code=status.HTTP_200_OK, response_model=s.PasswordStatus
)
def check_password(
    password: str,
    current_user: m.User = Depends(get_current_user),
):
    if not hash_verify(password, current_user.password):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Password does not match"
        )
    return s.PasswordStatus(status=s.PasswordStatus.PasswordStatusEnum.PASSWORD_MATCH)


@user_router.post(
    "/forgot-password", status_code=status.HTTP_201_CREATED, response_model=s.User
)
def forgot_password(
    data: s.ForgotPassword,
    db: Session = Depends(get_db),
):
    user = db.scalar(
        select(m.User).where(
            and_(m.User.phone == data.phone, m.User.country_code == data.country_code)
        )
    )
    if not user or user.is_deleted:
        log(log.INFO, "User doesn't exist - %s %s", data.country_code, data.phone)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="User does not exist"
        )

    user.password = data.new_password
    try:
        db.commit()
    except SQLAlchemyError as e:
        log(log.INFO, "Error while updating user password - %s", e)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Error updating password"
        )

    log(log.INFO, "User [%s] password updated successfully", user.username)
    return user


@user_router.post(
    "/change-password",
    status_code=status.HTTP_201_CREATED,
    response_model=s.PasswordStatus,
)
def change_password(
    data: s.ChangePassword,
    db: Session = Depends(get_db),
    current_user: m.User = Depends(get_current_user),
):
    if not hash_verify(data.current_password, current_user.password):
        log(
            log.INFO, "Current password is not correct for user %s" % current_user.email
        )
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Bad current password"
        )

    current_user.password = data.new_password
    try:
        db.commit()
    except SQLAlchemyError as e:
        log(log.INFO, "Error while updating user password - %s", e)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Error updating password"
        )

    log(log.INFO, "User [%s] password updated successfully", current_user.username)
    return s.PasswordStatus(status=s.PasswordStatus.PasswordStatusEnum.PASSWORD_UPDATED)


@user_router.get(
    "/applications", status_code=status.HTTP_200_OK, response_model=s.ApplicationList
)
def get_user_applications(
    type: str | None = None,
    db: Session = Depends(get_db),
    current_user: m.User = Depends(get_current_user),
):
    query = select(m.Application)
    if not type:
        query = query.filter(
            or_(
                m.Application.worker_id == current_user.id,
                m.Application.owner_id == current_user.id,
            )
        )
    elif type == "owner":
        query = query.where(
            and_(
                m.Application.owner_id == current_user.id,
                m.Application.status == s.BaseApplication.ApplicationStatus.PENDING,
            )
        )
    elif type == "worker":
        query = query.where(m.Application.worker_id == current_user.id).filter(
            m.Application.created_at
            > datetime.datetime.utcnow() - datetime.timedelta(weeks=1)
        )
    else:
        log(log.INFO, "Wrong filter %s", type)
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Wrong filter")

    log(log.INFO, "[%s] type applications for User [%s]", type, current_user.username)
    applications = db.scalars(query.order_by(desc(m.Application.created_at))).all()
    applications_schema_list = [
        s.ApplicationOut.from_orm(application) for application in applications
    ]

    return s.ApplicationList(applications=applications_schema_list)


@user_router.get("/jobs", status_code=status.HTTP_200_OK, response_model=s.ListJob)
def get_user_jobs(
    manage_tab: s.Job.TabFilter | None = None,
    db: Session = Depends(get_db),
    current_user: m.User = Depends(get_current_user),
):
    query = select(m.Job).where(
        or_(m.Job.worker_id == current_user.id, m.Job.owner_id == current_user.id)
    )
    log(log.INFO, "Manage tab query parameter: (%s)", str(manage_tab))

    if manage_tab:
        query = manage_tab_controller(db, current_user, query, manage_tab)

    jobs: list[m.Job] = db.scalars(query.order_by(desc(m.Job.created_at))).all()
    log(
        log.INFO,
        "User [%s] with id (%s) got [%s] jobs total",
        current_user.username,
        current_user.id,
        len(jobs),
    )
    return s.ListJob(jobs=jobs)


@user_router.get("/rates", status_code=status.HTTP_200_OK, response_model=s.RateList)
def get_user_rates(
    db: Session = Depends(get_db),
    current_user: m.User = Depends(get_current_user),
):
    rates: s.RateList = db.scalars(
        select(m.Rate).where(m.Rate.owner_id == current_user.id)
    ).all()
    log(
        log.INFO,
        "User [%s] with id (%s) have [%s] rates total",
        current_user.username,
        current_user.id,
        len(rates),
    )
    return s.RateList(rates=rates)


@user_router.get("/postings", status_code=status.HTTP_200_OK, response_model=s.ListJob)
def get_user_postings(
    db: Session = Depends(get_db),
    current_user: m.User = Depends(get_current_user),
):
    """Get list of jobs where current user is a owner"""
    query = select(m.Job).where(m.Job.owner_id == current_user.id)

    jobs: list[m.Job] = db.scalars(query.order_by(m.Job.created_at)).all()
    log(
        log.INFO,
        "User [%s] with id (%s) have [%s] jobs owning",
        current_user.username,
        current_user.id,
        len(jobs),
    )
    return s.ListJob(jobs=jobs)


@user_router.get("/{user_uuid}", response_model=s.User)
def get_user_profile(
    user_uuid: str,
    db: Session = Depends(get_db),
):
    user: m.User = db.scalars(select(m.User).where(m.User.uuid == user_uuid)).first()
    if not user or user.is_deleted:
        log(
            log.ERROR,
            "User %s not found",
            user_uuid,
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    log(log.INFO, "User [%s] info", user.username)
    return user


@user_router.patch(
    "/notification-settings",
    status_code=status.HTTP_200_OK,
    response_model=s.User,
)
def patch_user_notification_settings(
    notification_settings: s.UserNotificationSettingsIn,
    db: Session = Depends(get_db),
    current_user: m.User = Depends(get_current_user),
):
    if notification_settings.notification_job_status is not None:
        current_user.notification_job_status = (
            notification_settings.notification_job_status
        )

    if notification_settings.notification_profession is not None and len(
        notification_settings.notification_profession
    ):
        for profession in current_user.notification_profession:
            profession_obj: m.UserNotificationsProfessions = db.scalar(
                select(m.UserNotificationsProfessions).where(
                    m.UserNotificationsProfessions.user_id == current_user.id,
                    m.UserNotificationsProfessions.profession_id == profession.id,
                )
            )
            db.delete(profession_obj)
        for profession_id in notification_settings.notification_profession:
            db.add(
                m.UserNotificationsProfessions(
                    user_id=current_user.id, profession_id=profession_id
                )
            )

    if notification_settings.notification_profession_flag is not None:
        current_user.notification_profession_flag = (
            notification_settings.notification_profession_flag
        )

    if notification_settings.notification_locations is not None and len(
        notification_settings.notification_locations
    ):
        for location in current_user.notification_locations:
            location_obj: m.UserNotificationLocation = db.scalar(
                select(m.UserNotificationLocation).where(
                    m.UserNotificationLocation.user_id == current_user.id,
                    m.UserNotificationLocation.location_id == location.id,
                )
            )
            db.delete(location_obj)
        for location_id in notification_settings.notification_locations:
            db.add(
                m.UserNotificationLocation(
                    user_id=current_user.id, location_id=location_id
                )
            )

    if notification_settings.notification_locations_flag is not None:
        current_user.notification_locations_flag = (
            notification_settings.notification_locations_flag
        )

    try:
        db.commit()
    except SQLAlchemyError as e:
        log(
            log.INFO,
            "Error while updating notifications settings user [%s] - %s",
            current_user.id,
            e,
        )
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Error updating notifications settings",
        )

    log(log.INFO, "User [%s] notifications updated successfully", current_user.id)
    return current_user


@user_router.post(
    "/payplus-token",
    status_code=status.HTTP_200_OK,
    response_model=s.User,
    openapi_extra={
        "responses": {
            status.HTTP_409_CONFLICT: {},
        }
    },
)
def post_user_payplus_token(
    card_data: s.CardIn,
    db: Session = Depends(get_db),
    settings: Settings = Depends(get_settings),
    current_user: m.User = Depends(get_current_user),
):
    create_payplus_token(card_data, current_user, settings, db)
    return current_user
