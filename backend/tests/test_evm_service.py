from decimal import Decimal

import pytest

from app.schemas.evm import EVMIndicators, EVMInput
from app.services.evm_service import EVMService


class TestEVMCalculations:
    """Test suite for EVM calculations."""

    def test_normal_calculation(self):
        """Test basic EVM calculation with normal values.

        Manual calc: CPI=450/400=1.125→1.13, EAC=1000/1.125=888.89
        """
        input_data = EVMInput(
            bac=Decimal("1000"),
            planned_percentage=Decimal("50"),
            actual_percentage=Decimal("45"),
            actual_cost=Decimal("400"),
        )

        indicators = EVMService.calculate_indicators(input_data)

        assert indicators.bac == Decimal("1000")
        assert indicators.pv == Decimal("500.00")
        assert indicators.ev == Decimal("450.00")
        assert indicators.ac == Decimal("400")
        assert indicators.cv == Decimal("50.00")
        assert indicators.sv == Decimal("-50.00")
        assert indicators.cpi == Decimal("1.13")
        assert indicators.spi == Decimal("0.90")
        assert indicators.eac == Decimal("888.89")
        assert indicators.vac == Decimal("111.11")

    def test_ac_zero_cpi_undefined(self):
        """When AC=0, CPI must be None."""
        input_data = EVMInput(
            bac=Decimal("1000"),
            planned_percentage=Decimal("50"),
            actual_percentage=Decimal("30"),
            actual_cost=Decimal("0"),
        )

        indicators = EVMService.calculate_indicators(input_data)

        assert indicators.cpi is None
        assert indicators.eac is None
        assert indicators.vac is None
        assert indicators.ac == Decimal("0")

    def test_pv_zero_spi_undefined(self):
        """When PV=0 (no planned work), SPI must be None."""
        input_data = EVMInput(
            bac=Decimal("1000"),
            planned_percentage=Decimal("0"),
            actual_percentage=Decimal("10"),
            actual_cost=Decimal("100"),
        )

        indicators = EVMService.calculate_indicators(input_data)

        assert indicators.spi is None
        assert indicators.pv == Decimal("0.00")

    def test_ev_zero_with_ac(self):
        """When EV=0 and AC>0, CPI should be 0 (valid, not undefined)."""
        input_data = EVMInput(
            bac=Decimal("1000"),
            planned_percentage=Decimal("50"),
            actual_percentage=Decimal("0"),
            actual_cost=Decimal("500"),
        )

        indicators = EVMService.calculate_indicators(input_data)

        assert indicators.ev == Decimal("0.00")
        assert indicators.cpi == Decimal("0.00")
        assert indicators.eac is None

    def test_ev_zero_with_pv(self):
        """When EV=0 and PV>0, SPI should be 0 (valid, not undefined)."""
        input_data = EVMInput(
            bac=Decimal("1000"),
            planned_percentage=Decimal("50"),
            actual_percentage=Decimal("0"),
            actual_cost=Decimal("100"),
        )

        indicators = EVMService.calculate_indicators(input_data)

        assert indicators.ev == Decimal("0.00")
        assert indicators.spi == Decimal("0.00")

    def test_progress_at_100_percent(self):
        """When progress is 100%, EV should equal BAC."""
        input_data = EVMInput(
            bac=Decimal("1000"),
            planned_percentage=Decimal("100"),
            actual_percentage=Decimal("100"),
            actual_cost=Decimal("950"),
        )

        indicators = EVMService.calculate_indicators(input_data)

        assert indicators.ev == Decimal("1000.00")
        assert indicators.pv == Decimal("1000.00")
        assert indicators.cpi == Decimal("1.05")
        assert indicators.spi == Decimal("1.00")

    def test_bac_validation(self):
        """BAC must be greater than 0."""
        with pytest.raises(ValueError):
            EVMInput(
                bac=Decimal("0"),
                planned_percentage=Decimal("50"),
                actual_percentage=Decimal("45"),
                actual_cost=Decimal("400"),
            )

        with pytest.raises(ValueError):
            EVMInput(
                bac=Decimal("-100"),
                planned_percentage=Decimal("50"),
                actual_percentage=Decimal("45"),
                actual_cost=Decimal("400"),
            )

    def test_percentage_validation(self):
        """Percentages must be between 0 and 100."""
        with pytest.raises(ValueError):
            EVMInput(
                bac=Decimal("1000"),
                planned_percentage=Decimal("-10"),
                actual_percentage=Decimal("45"),
                actual_cost=Decimal("400"),
            )

        with pytest.raises(ValueError):
            EVMInput(
                bac=Decimal("1000"),
                planned_percentage=Decimal("50"),
                actual_percentage=Decimal("150"),
                actual_cost=Decimal("400"),
            )

    def test_ac_cannot_be_negative(self):
        """AC must be >= 0."""
        with pytest.raises(ValueError):
            EVMInput(
                bac=Decimal("1000"),
                planned_percentage=Decimal("50"),
                actual_percentage=Decimal("45"),
                actual_cost=Decimal("-100"),
            )

    def test_negative_vac_valid(self):
        """Negative VAC is valid (indicates over budget).

        Manual calc: EV=600, AC=700, CPI=600/700=0.857→0.86,
        EAC=1000/0.857=1166.67, VAC=1000-1166.67=-166.67
        """
        input_data = EVMInput(
            bac=Decimal("1000"),
            planned_percentage=Decimal("50"),
            actual_percentage=Decimal("60"),
            actual_cost=Decimal("700"),
        )

        indicators = EVMService.calculate_indicators(input_data)

        assert indicators.vac == Decimal("-166.67")

    def test_consolidate_multiple_activities(self):
        """Test consolidation of multiple activities."""
        activity1 = EVMIndicators(
            bac=Decimal("1000"),
            pv=Decimal("500.00"),
            ev=Decimal("450.00"),
            ac=Decimal("400"),
            cv=Decimal("50.00"),
            sv=Decimal("-50.00"),
            cpi=Decimal("1.12"),
            spi=Decimal("0.90"),
            eac=Decimal("892.86"),
            vac=Decimal("107.14"),
        )

        activity2 = EVMIndicators(
            bac=Decimal("2000"),
            pv=Decimal("1000.00"),
            ev=Decimal("1000.00"),
            ac=Decimal("900"),
            cv=Decimal("100.00"),
            sv=Decimal("0.00"),
            cpi=Decimal("1.11"),
            spi=Decimal("1.00"),
            eac=Decimal("1800.00"),
            vac=Decimal("200.00"),
        )

        consolidated = EVMService.consolidate_indicators([activity1, activity2])

        assert consolidated.bac == Decimal("3000")
        assert consolidated.pv == Decimal("1500.00")
        assert consolidated.ev == Decimal("1450.00")
        assert consolidated.ac == Decimal("1300")
        assert consolidated.cv == Decimal("150.00")
        assert consolidated.sv == Decimal("-50.00")
        assert consolidated.cpi == Decimal("1.12")
        assert consolidated.spi == Decimal("0.97")

    def test_consolidate_no_averages(self):
        """Verify that consolidated indicators are NOT averages of individual CPI/SPI."""
        activity1 = EVMIndicators(
            bac=Decimal("1000"),
            pv=Decimal("500.00"),
            ev=Decimal("500.00"),
            ac=Decimal("1000"),
            cv=Decimal("-500.00"),
            sv=Decimal("0.00"),
            cpi=Decimal("0.50"),
            spi=Decimal("1.00"),
        )

        activity2 = EVMIndicators(
            bac=Decimal("1000"),
            pv=Decimal("500.00"),
            ev=Decimal("500.00"),
            ac=Decimal("500"),
            cv=Decimal("0.00"),
            sv=Decimal("0.00"),
            cpi=Decimal("1.00"),
            spi=Decimal("1.00"),
        )

        consolidated = EVMService.consolidate_indicators([activity1, activity2])

        average_cpi = (Decimal("0.50") + Decimal("1.00")) / Decimal("2")
        assert consolidated.cpi != average_cpi
        assert consolidated.cpi == Decimal("0.67")

    def test_consolidate_empty_list(self):
        """Consolidating an empty list should return zero indicators."""
        consolidated = EVMService.consolidate_indicators([])

        assert consolidated.bac == Decimal("0")
        assert consolidated.pv == Decimal("0")
        assert consolidated.ev == Decimal("0")
        assert consolidated.ac == Decimal("0")
        assert consolidated.cpi is None
        assert consolidated.spi is None
        assert consolidated.eac is None
        assert consolidated.vac is None

    def test_consolidate_single_activity(self):
        """Consolidating a single activity should return equivalent indicators."""
        activity = EVMIndicators(
            bac=Decimal("1000"),
            pv=Decimal("500.00"),
            ev=Decimal("450.00"),
            ac=Decimal("400"),
            cv=Decimal("50.00"),
            sv=Decimal("-50.00"),
            cpi=Decimal("1.13"),
            spi=Decimal("0.90"),
            eac=Decimal("888.89"),
            vac=Decimal("111.11"),
        )

        consolidated = EVMService.consolidate_indicators([activity])

        assert consolidated.bac == activity.bac
        assert consolidated.pv == activity.pv
        assert consolidated.ev == activity.ev
        assert consolidated.ac == activity.ac
        assert consolidated.cpi == activity.cpi
        assert consolidated.spi == activity.spi
        assert consolidated.eac == activity.eac
        assert consolidated.vac == activity.vac

    def test_decimal_precision(self):
        """Test that calculations maintain proper decimal precision."""
        input_data = EVMInput(
            bac=Decimal("333.33"),
            planned_percentage=Decimal("33.33"),
            actual_percentage=Decimal("33.33"),
            actual_cost=Decimal("111.11"),
        )

        indicators = EVMService.calculate_indicators(input_data)

        assert indicators.pv == Decimal("111.10")
        assert indicators.ev == Decimal("111.10")
        assert indicators.cpi == Decimal("1.00")

    def test_large_numbers(self):
        """Test with large monetary values."""
        input_data = EVMInput(
            bac=Decimal("1000000"),
            planned_percentage=Decimal("50"),
            actual_percentage=Decimal("45"),
            actual_cost=Decimal("450000"),
        )

        indicators = EVMService.calculate_indicators(input_data)

        assert indicators.pv == Decimal("500000.00")
        assert indicators.ev == Decimal("450000.00")
        assert indicators.cpi == Decimal("1.00")
        assert indicators.spi == Decimal("0.90")

    def test_float_conversion(self):
        """Test that float inputs are correctly converted to Decimal."""
        input_data = EVMInput(
            bac=1000.0,
            planned_percentage=50.0,
            actual_percentage=45.0,
            actual_cost=400.0,
        )

        indicators = EVMService.calculate_indicators(input_data)

        assert isinstance(indicators.bac, Decimal)
        assert isinstance(indicators.pv, Decimal)
        assert indicators.cpi == Decimal("1.13")
