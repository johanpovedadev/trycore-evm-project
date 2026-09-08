

class TestEVMEndpoints:
    """Integration tests for EVM API endpoints."""

    def test_calculate_evm_success(self, client):
        """Test successful EVM calculation via API.

        Manual calc: CPI=450/400=1.125→1.13, EAC=1000/1.125=888.89
        """
        payload = {
            "bac": 1000,
            "planned_percentage": 50,
            "actual_percentage": 45,
            "actual_cost": 400,
        }

        response = client.post("/evm/calculate", json=payload)

        assert response.status_code == 200
        data = response.json()
        assert "indicators" in data
        indicators = data["indicators"]
        assert indicators["bac"] == "1000"
        assert indicators["pv"] == "500.00"
        assert indicators["ev"] == "450.00"
        assert indicators["ac"] == "400"
        assert indicators["cv"] == "50.00"
        assert indicators["sv"] == "-50.00"
        assert indicators["cpi"] == "1.13"
        assert indicators["spi"] == "0.90"
        assert indicators["eac"] == "888.89"
        assert indicators["vac"] == "111.11"

    def test_calculate_evm_ac_zero(self, client):
        """Test EVM calculation when AC=0 (CPI undefined)."""
        payload = {
            "bac": 1000,
            "planned_percentage": 50,
            "actual_percentage": 30,
            "actual_cost": 0,
        }

        response = client.post("/evm/calculate", json=payload)

        assert response.status_code == 200
        data = response.json()
        indicators = data["indicators"]
        assert indicators["cpi"] is None
        assert indicators["eac"] is None
        assert indicators["vac"] is None

    def test_calculate_evm_pv_zero(self, client):
        """Test EVM calculation when PV=0 (SPI undefined)."""
        payload = {
            "bac": 1000,
            "planned_percentage": 0,
            "actual_percentage": 10,
            "actual_cost": 100,
        }

        response = client.post("/evm/calculate", json=payload)

        assert response.status_code == 200
        data = response.json()
        indicators = data["indicators"]
        assert indicators["spi"] is None

    def test_calculate_evm_invalid_bac(self, client):
        """Test that BAC=0 returns validation error."""
        payload = {
            "bac": 0,
            "planned_percentage": 50,
            "actual_percentage": 45,
            "actual_cost": 400,
        }

        response = client.post("/evm/calculate", json=payload)

        assert response.status_code == 422

    def test_calculate_evm_negative_bac(self, client):
        """Test that negative BAC returns validation error."""
        payload = {
            "bac": -1000,
            "planned_percentage": 50,
            "actual_percentage": 45,
            "actual_cost": 400,
        }

        response = client.post("/evm/calculate", json=payload)

        assert response.status_code == 422

    def test_calculate_evm_invalid_percentage(self, client):
        """Test that out-of-range percentage returns validation error."""
        payload = {
            "bac": 1000,
            "planned_percentage": 150,
            "actual_percentage": 45,
            "actual_cost": 400,
        }

        response = client.post("/evm/calculate", json=payload)

        assert response.status_code == 422

    def test_calculate_evm_negative_ac(self, client):
        """Test that negative AC returns validation error."""
        payload = {
            "bac": 1000,
            "planned_percentage": 50,
            "actual_percentage": 45,
            "actual_cost": -100,
        }

        response = client.post("/evm/calculate", json=payload)

        assert response.status_code == 422

    def test_calculate_evm_at_100_percent(self, client):
        """Test EVM calculation at 100% completion."""
        payload = {
            "bac": 1000,
            "planned_percentage": 100,
            "actual_percentage": 100,
            "actual_cost": 950,
        }

        response = client.post("/evm/calculate", json=payload)

        assert response.status_code == 200
        data = response.json()
        indicators = data["indicators"]
        assert indicators["pv"] == "1000.00"
        assert indicators["ev"] == "1000.00"
        assert indicators["cpi"] == "1.05"
        assert indicators["spi"] == "1.00"

    def test_calculate_evm_over_budget(self, client):
        """Test EVM calculation showing over-budget scenario.

        Manual calc: EV=600, AC=700, CPI=600/700=0.857→0.86,
        EAC=1000/0.857=1166.67, VAC=1000-1166.67=-166.67
        """
        payload = {
            "bac": 1000,
            "planned_percentage": 50,
            "actual_percentage": 60,
            "actual_cost": 700,
        }

        response = client.post("/evm/calculate", json=payload)

        assert response.status_code == 200
        data = response.json()
        indicators = data["indicators"]
        assert indicators["cv"] == "-100.00"
        assert indicators["vac"] == "-166.67"

    def test_calculate_evm_decimal_inputs(self, client):
        """Test that decimal inputs are handled correctly."""
        payload = {
            "bac": 333.33,
            "planned_percentage": 33.33,
            "actual_percentage": 33.33,
            "actual_cost": 111.11,
        }

        response = client.post("/evm/calculate", json=payload)

        assert response.status_code == 200
        data = response.json()
        indicators = data["indicators"]
        assert "cpi" in indicators
        assert indicators["cpi"] is not None

    def test_calculate_evm_response_structure(self, client):
        """Test response structure contains all required fields."""
        payload = {
            "bac": 1000,
            "planned_percentage": 50,
            "actual_percentage": 45,
            "actual_cost": 400,
        }

        response = client.post("/evm/calculate", json=payload)

        assert response.status_code == 200
        data = response.json()
        assert "indicators" in data

        indicators = data["indicators"]
        required_fields = ["bac", "pv", "ev", "ac", "cv", "sv", "cpi", "spi", "eac", "vac"]
        for field in required_fields:
            assert field in indicators
