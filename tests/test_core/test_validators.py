"""Input validator tests."""

import pytest

from beaversec.core.validators import InputValidator
from beaversec.core.exceptions import ValidationError


class TestInputValidator:
    """Test cases for InputValidator class."""

    def test_validate_ip_valid(self):
        """Test validating valid IP addresses."""
        assert InputValidator.validate_ip("8.8.8.8") is True
        assert InputValidator.validate_ip("2001:4860:4860::8888") is True
        assert InputValidator.validate_ip("192.168.1.1") is True

    def test_validate_ip_invalid(self):
        """Test validating invalid IP addresses."""
        with pytest.raises(ValidationError):
            InputValidator.validate_ip("999.999.999.999")

        with pytest.raises(ValidationError):
            InputValidator.validate_ip("invalid")

    def test_validate_domain_valid(self):
        """Test validating valid domain names."""
        assert InputValidator.validate_domain("example.com") is True
        assert InputValidator.validate_domain("sub.example.com") is True
        assert InputValidator.validate_domain("test123.example.com") is True

    def test_validate_domain_invalid(self):
        """Test validating invalid domain names."""
        with pytest.raises(ValidationError):
            InputValidator.validate_domain("")

        with pytest.raises(ValidationError):
            InputValidator.validate_domain("invalid..domain")

        with pytest.raises(ValidationError):
            InputValidator.validate_domain(".leading")

        # Domain too long
        long_domain = "a" * 300 + ".com"
        with pytest.raises(ValidationError):
            InputValidator.validate_domain(long_domain)

    def test_validate_port_valid(self):
        """Test validating valid ports."""
        assert InputValidator.validate_port(80) is True
        assert InputValidator.validate_port(443) is True
        assert InputValidator.validate_port(65535) is True

    def test_validate_port_invalid(self):
        """Test validating invalid ports."""
        with pytest.raises(ValidationError):
            InputValidator.validate_port(-1)

        with pytest.raises(ValidationError):
            InputValidator.validate_port(0)

        with pytest.raises(ValidationError):
            InputValidator.validate_port(99999)

    def test_validate_ports_valid(self):
        """Test validating valid port specifications."""
        result = InputValidator.validate_ports("80")
        assert result == [80]

        result = InputValidator.validate_ports("22,443,8080")
        assert result == [22, 443, 8080]

        result = InputValidator.validate_ports(["80", "443"])
        assert result == [80, 443]

    def test_validate_ports_invalid(self):
        """Test validating invalid port specifications."""
        with pytest.raises(ValidationError):
            InputValidator.validate_ports("99999")

        with pytest.raises(ValidationError):
            InputValidator.validate_ports("abc")

        with pytest.raises(ValidationError):
            InputValidator.validate_ports(["80", "invalid"])

        # Too many ports
        many_ports = [str(i) for i in range(1, 200)]
        with pytest.raises(ValidationError):
            InputValidator.validate_ports(many_ports)

    def test_validate_format_valid(self):
        """Test validating valid output formats."""
        assert InputValidator.validate_output_format("json") is True
        assert InputValidator.validate_output_format("html") is True
        assert InputValidator.validate_output_format("csv") is True

    def test_validate_format_invalid(self):
        """Test validating invalid output formats."""
        with pytest.raises(ValidationError):
            InputValidator.validate_output_format("invalid")

        with pytest.raises(ValidationError):
            InputValidator.validate_output_format("pdf")

    def test_validate_params_required(self):
        """Test validating required parameters."""
        params = {"target": "8.8.8.8", "port": "80"}
        required = ["target"]

        result = InputValidator.validate_params(params, required)
        assert "target" in result
        assert result["target"] == "8.8.8.8"

        # Missing required parameter
        with pytest.raises(ValidationError):
            InputValidator.validate_params({"port": "80"}, ["target"])

        # Empty required list
        result = InputValidator.validate_params(params, [])
        assert result == params

    def test_validate_param_value(self):
        """Test validating individual parameter values."""
        assert InputValidator.validate_parameter_value("target", "8.8.8.8") is True

        with pytest.raises(ValidationError):
            InputValidator.validate_parameter_value("target", None)

        with pytest.raises(ValidationError):
            InputValidator.validate_parameter_value("target", "invalid")

        assert InputValidator.validate_parameter_value("port", 80) is True

        with pytest.raises(ValidationError):
            InputValidator.validate_parameter_value("port", -1)