import time
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.auth import SendCodeRequest, VerifyCodeRequest, VerificationProof
from app.services.otp_service import otp_service
from app.services.email_service import email_service
from app.services.user_service import user_service
from app.services.signer_service import VerificationSigner
from app.services.rate_limit import rate_limit_dependency

router = APIRouter()

@router.post("/send-code", status_code=status.HTTP_200_OK, dependencies=[Depends(rate_limit_dependency)])
async def send_code(request: SendCodeRequest):
    """
    Generates an OTP, stores it in Redis, and sends it via email.
    """
    otp = otp_service.generate_otp()
    await otp_service.store_otp(request.project_id, request.email, otp)
    await email_service.send_otp_email(request.email, otp, request.project_id)
    return {"message": "Verification code sent successfully"}

@router.post("/verify-code", response_model=VerificationProof)
async def verify_code(request: VerifyCodeRequest, db: AsyncSession = Depends(get_db)):
    """
    Verifies the OTP and returns a signed identity proof.
    """
    is_valid = await otp_service.verify_otp(request.project_id, request.email, request.code)
    
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired verification code"
        )
    
    # Identify/Create User
    user = await user_service.get_or_create_user(db, request.email)
    await user_service.update_last_verified(db, user)
    
    # Prepare Signed Proof
    issued_at = int(time.time())
    payload = {
        "auth_user_id": str(user.id),
        "email": user.email,
        "project_id": request.project_id,
        "verified": True,
        "issued_at": issued_at
    }
    
    signature = VerificationSigner.sign_payload(payload)
    
    return VerificationProof(
        auth_user_id=user.id,
        email=user.email,
        project_id=request.project_id,
        verified=True,
        issued_at=issued_at,
        signature=signature
    )

