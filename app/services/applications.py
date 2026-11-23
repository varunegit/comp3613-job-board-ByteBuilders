"""Application create / read / status transitions via lifecycle tracker."""

from __future__ import annotations

from typing import Any

from sqlmodel import Session, select

from app.database import engine
from app.models.application import Application
from app.models.listing import Listing
from app.services.board_auth import get_user
from app.services.application_states import InvalidTransitionError
from app.services.lifecycle import apply_action


def apply(
    graduate_id: int,
    listing_id: int,
    cover_letter: str,
    resume_text: str | None = None,
) -> dict[str, Any]:
    user = get_user(graduate_id)
    if not user or user["role"] != "graduate":
        return {"ok": False, "error": "graduates only"}
    # DEFECT: no programme eligibility check

    with Session(engine) as session:
        listing = session.get(Listing, listing_id)
        if listing is None:
            return {"ok": False, "error": "listing not found"}

        # DEFECT: allows apply on pending / expired; external still creates a row
        resume = resume_text or user.get("resume_text") or ""
        application = Application(
            listing_id=listing_id,
            graduate_id=graduate_id,
            cover_letter=cover_letter,
            resume_text=resume,
            status="submitted",
        )
        session.add(application)
        session.commit()
        session.refresh(application)
        return {
            "ok": True,
            "application_id": application.id,
            "status": "submitted",
        }


def my_applications(graduate_id: int) -> list[dict[str, Any]]:
    with Session(engine) as session:
        rows = session.exec(
            select(Application)
            .where(Application.graduate_id == graduate_id)
            .order_by(Application.id)
        ).all()
        return [row.model_dump() for row in rows]


def listing_applicants(viewer_id: int, listing_id: int) -> dict[str, Any]:
    viewer = get_user(viewer_id)
    if not viewer:
        return {"ok": False, "error": "unknown user"}
    with Session(engine) as session:
        listing = session.get(Listing, listing_id)
        if listing is None:
            return {"ok": False, "error": "listing not found"}
        if viewer["role"] not in {"employer", "admin"}:
            return {"ok": False, "error": "forbidden"}
        if viewer["role"] == "employer" and listing.employer_id != viewer_id:
            return {"ok": False, "error": "forbidden"}
        rows = session.exec(
            select(Application)
            .where(Application.listing_id == listing_id)
            .order_by(Application.id)
        ).all()
        return {"ok": True, "applicants": [r.model_dump() for r in rows]}


def export_applicants(admin_id: int, listing_id: int) -> dict[str, Any]:
    admin = get_user(admin_id)
    if not admin or admin["role"] != "admin":
        return {"ok": False, "error": "admin only"}
    result = listing_applicants(admin_id, listing_id)
    if not result.get("ok"):
        return result
    return {"ok": True, "format": "json", "package": result["applicants"]}


class ApplicationNotFound(Exception):
    pass


class TransitionForbidden(Exception):
    pass


def transition_application(
    actor_id: int, application_id: int, action: str
) -> dict[str, Any]:
    """Change an application's status through the State Pattern."""
    with Session(engine) as session:
        row = session.get(Application, application_id)
        if row is None:
            raise ApplicationNotFound("application not found")

        actor = get_user(actor_id)
        if not actor or actor["role"] != "employer":
            raise TransitionForbidden("only the listing's employer may change status")

        listing = session.get(Listing, row.listing_id)
        if listing is None or listing.employer_id != actor_id:
            raise TransitionForbidden("only the listing's employer may change status")

        apply_action(row, action)
        session.add(row)
        session.commit()
        session.refresh(row)
        return {"ok": True, "application": row.model_dump()}
