from fastapi import APIRouter, HTTPException

from app.schemas.evm import EVMActivityResponse, EVMInput
from app.services.evm_service import EVMService

router = APIRouter(prefix="/evm", tags=["evm"])


@router.post("/calculate", response_model=EVMActivityResponse)
async def calculate_evm(evm_input: EVMInput) -> EVMActivityResponse:
    """Calculate EVM indicators for given input data.

    Calculates:
    - PV (Planned Value)
    - EV (Earned Value)
    - CV (Cost Variance)
    - SV (Schedule Variance)
    - CPI (Cost Performance Index)
    - SPI (Schedule Performance Index)
    - EAC (Estimate At Completion)
    - VAC (Variance At Completion)

    Edge cases handled:
    - AC=0 → CPI=null
    - PV=0 → SPI=null
    - CPI=0 → EAC=null, VAC=null
    """
    try:
        indicators = EVMService.calculate_indicators(evm_input)
        return EVMActivityResponse(indicators=indicators)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Calculation error")
