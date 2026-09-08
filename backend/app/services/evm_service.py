from decimal import ROUND_HALF_UP, Decimal
from typing import Optional

from app.schemas.evm import EVMIndicators, EVMInput


class EVMService:
    """Service for EVM (Earned Value Management) calculations."""

    DECIMAL_PLACES = 2

    @staticmethod
    def calculate_indicators(evm_input: EVMInput) -> EVMIndicators:
        """Calculate EVM indicators from input data.

        Handles all edge cases:
        - AC = 0 → CPI = null
        - PV = 0 → SPI = null
        - EV = 0 → valid (0/AC or 0/PV)
        - CPI = 0 → EAC = null, VAC = null

        Precision: All intermediate calculations use full Decimal precision.
        Rounding to 2 places occurs only in final serialization.
        """
        bac = evm_input.bac
        planned_percentage = evm_input.planned_percentage / Decimal(100)
        actual_percentage = evm_input.actual_percentage / Decimal(100)
        ac = evm_input.actual_cost

        pv = planned_percentage * bac
        ev = actual_percentage * bac

        cv = ev - ac
        sv = ev - pv

        cpi = EVMService._calculate_cpi(ev, ac)
        spi = EVMService._calculate_spi(ev, pv)
        eac = EVMService._calculate_eac(bac, cpi)
        vac = EVMService._calculate_vac(bac, eac)

        return EVMIndicators(
            bac=bac,
            pv=EVMService._round_value(pv),
            ev=EVMService._round_value(ev),
            ac=ac,
            cv=EVMService._round_value(cv),
            sv=EVMService._round_value(sv),
            cpi=EVMService._round_value(cpi),
            spi=EVMService._round_value(spi),
            eac=EVMService._round_value(eac),
            vac=EVMService._round_value(vac),
        )

    @staticmethod
    def _round_value(value: Optional[Decimal]) -> Optional[Decimal]:
        """Round Decimal to DECIMAL_PLACES. Used only in final output."""
        if value is None:
            return None
        return value.quantize(
            Decimal(10) ** -EVMService.DECIMAL_PLACES, rounding=ROUND_HALF_UP
        )

    @staticmethod
    def _calculate_cpi(ev: Decimal, ac: Decimal) -> Optional[Decimal]:
        """Calculate Cost Performance Index. Returns None if AC = 0.

        No rounding: result preserves full precision for EAC calculation.
        """
        if ac == 0:
            return None
        return ev / ac

    @staticmethod
    def _calculate_spi(ev: Decimal, pv: Decimal) -> Optional[Decimal]:
        """Calculate Schedule Performance Index. Returns None if PV = 0.

        No rounding: result preserves full precision.
        """
        if pv == 0:
            return None
        return ev / pv

    @staticmethod
    def _calculate_eac(bac: Decimal, cpi: Optional[Decimal]) -> Optional[Decimal]:
        """Calculate Estimate At Completion. Returns None if CPI is None or 0.

        No rounding: uses unrounded CPI for precision.
        """
        if cpi is None or cpi == 0:
            return None
        return bac / cpi

    @staticmethod
    def _calculate_vac(bac: Decimal, eac: Optional[Decimal]) -> Optional[Decimal]:
        """Calculate Variance At Completion. Returns None if EAC is None.

        No rounding: uses unrounded EAC for precision.
        """
        if eac is None:
            return None
        return bac - eac

    @staticmethod
    def consolidate_indicators(indicators_list: list[EVMIndicators]) -> EVMIndicators:
        """Consolidate indicators from multiple activities.

        Calculates totals first, then computes consolidated indicators.
        NEVER averages CPI/SPI from individual activities.
        Uses full precision in intermediate calculations.
        """
        if not indicators_list:
            return EVMIndicators(
                bac=Decimal(0),
                pv=Decimal(0),
                ev=Decimal(0),
                ac=Decimal(0),
                cv=Decimal(0),
                sv=Decimal(0),
                cpi=None,
                spi=None,
                eac=None,
                vac=None,
            )

        bac_total = sum(ind.bac for ind in indicators_list)
        pv_total = sum(ind.pv for ind in indicators_list)
        ev_total = sum(ind.ev for ind in indicators_list)
        ac_total = sum(ind.ac for ind in indicators_list)

        cv_total = ev_total - ac_total
        sv_total = ev_total - pv_total

        cpi_total = EVMService._calculate_cpi(ev_total, ac_total)
        spi_total = EVMService._calculate_spi(ev_total, pv_total)
        eac_total = EVMService._calculate_eac(bac_total, cpi_total)
        vac_total = EVMService._calculate_vac(bac_total, eac_total)

        return EVMIndicators(
            bac=bac_total,
            pv=EVMService._round_value(pv_total),
            ev=EVMService._round_value(ev_total),
            ac=ac_total,
            cv=EVMService._round_value(cv_total),
            sv=EVMService._round_value(sv_total),
            cpi=EVMService._round_value(cpi_total),
            spi=EVMService._round_value(spi_total),
            eac=EVMService._round_value(eac_total),
            vac=EVMService._round_value(vac_total),
        )
