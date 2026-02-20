import os
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
import httpx
from dotenv import load_dotenv

load_dotenv()

AWS_REGION = os.getenv("AWS_REGION", "us-west-2")
COGNITO_USER_POOL_ID = os.getenv("COGNITO_USER_POOL_ID")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

security = HTTPBearer()


class CognitoJWTVerifier:
    def __init__(self):
        self.jwks = None
        self.jwks_url = (
            f"https://cognito-idp.{AWS_REGION}.amazonaws.com"
            f"/{COGNITO_USER_POOL_ID}/.well-known/jwks.json"
        )
        self.issuer = (
            f"https://cognito-idp.{AWS_REGION}.amazonaws.com/{COGNITO_USER_POOL_ID}"
        )

    async def get_jwks(self) -> dict:
        if self.jwks is None:
            async with httpx.AsyncClient() as client:
                response = await client.get(self.jwks_url)
                response.raise_for_status()
                self.jwks = response.json()
        return self.jwks

    async def verify_token(self, token: str) -> dict:
        try:
            header = jwt.get_unverified_header(token)
            kid = header.get("kid")

            jwks = await self.get_jwks()
            key = next(
                (k for k in jwks.get("keys", []) if k.get("kid") == kid), None
            )
            if key is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Public key not found",
                )

            claims = jwt.decode(
                token,
                key,
                algorithms=["RS256"],
                issuer=self.issuer,
            )
            return claims
        except JWTError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=str(e),
            )


cognito_verifier = CognitoJWTVerifier()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),) -> dict:
        return await cognito_verifier.verify_token(credentials.credentials)


@app.get("/")
async def health_check():
    return {"status": "ok"}


@app.get("/auth/me")
async def get_me(user: dict = Depends(get_current_user)):
    return {"user": user}
