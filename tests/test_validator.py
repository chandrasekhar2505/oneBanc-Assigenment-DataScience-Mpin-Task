
from validator import evaluate_mpin, load_common_mpins
import os
import pytest # type: ignore

# Test Part A: Commonly Used MPIN (4-digit)
def test_commonly_used_4_digit():
    strength, reasons = evaluate_mpin("1234")
    assert strength == "WEAK"
    assert "COMMONLY_USED" in reasons

# Test Part B & C: Demographics (4-digit)
def test_demographic_dob_self_4_digit():
    strength, reasons = evaluate_mpin("0201", self_dob="1998-01-02")
    assert strength == "WEAK"
    assert "DEMOGRAPHIC_DOB_SELF" in reasons

def test_demographic_dob_spouse_4_digit():
    strength, reasons = evaluate_mpin("0302", spouse_dob="1995-02-03")
    assert strength == "WEAK"
    assert "DEMOGRAPHIC_DOB_SPOUSE" in reasons

def test_demographic_anniversary_4_digit():
    strength, reasons = evaluate_mpin("1205", anniversary="2010-05-12")
    assert strength == "WEAK"
    assert "DEMOGRAPHIC_ANNIVERSARY" in reasons

# Test Part D: 6-digit MPINs
def test_commonly_used_6_digit():
    strength, reasons = evaluate_mpin("123456")
    assert strength == "WEAK"
    assert "COMMONLY_USED" in reasons

def test_demographic_dob_self_6_digit():
    strength, reasons = evaluate_mpin("020198", self_dob="1998-01-02")
    assert strength == "WEAK"
    assert "DEMOGRAPHIC_DOB_SELF" in reasons
def test_demographic_dob_self_yyyy():
    strength, reasons = evaluate_mpin("1998", self_dob="1998-01-02")
    assert strength == "WEAK"
    assert "DEMOGRAPHIC_DOB_SELF" in reasons


# Test Strong MPINs
def test_strong_4_digit():
    strength, reasons = evaluate_mpin("9876")
    assert strength == "STRONG"
    assert not reasons

def test_strong_6_digit():
    strength, reasons = evaluate_mpin("987654")
    assert strength == "STRONG"
    assert not reasons

# Test Multiple Reasons for Weakness
def test_common_and_demographic():
    strength, reasons = evaluate_mpin("1122", self_dob="1922-11-01")
    assert strength == "WEAK"
    assert "COMMONLY_USED" in reasons
    assert "DEMOGRAPHIC_DOB_SELF" in reasons

# Additional Test Cases (to reach 20+)
def test_another_common_mpin():
    strength, reasons = evaluate_mpin("7777")
    assert strength == "WEAK"
    assert "COMMONLY_USED" in reasons

def test_dob_mmdd_format():
    strength, reasons = evaluate_mpin("1101", self_dob="1990-11-01")
    assert strength == "WEAK"
    assert "DEMOGRAPHIC_DOB_SELF" in reasons

def test_dob_yymm_format():
    strength, reasons = evaluate_mpin("9011", self_dob="1990-11-01")
    assert strength == "WEAK"
    assert "DEMOGRAPHIC_DOB_SELF" in reasons

def test_dob_ddyy_format():
    strength, reasons = evaluate_mpin("0190", self_dob="1990-11-01")
    assert strength == "WEAK"
    assert "DEMOGRAPHIC_DOB_SELF" in reasons

def test_anniversary_mmdd_format():
    strength, reasons = evaluate_mpin("0615", anniversary="2005-06-15")
    assert strength == "WEAK"
    assert "DEMOGRAPHIC_ANNIVERSARY" in reasons

def test_spouse_dob_mmdd_format():
    strength, reasons = evaluate_mpin("0720", spouse_dob="1988-07-20")
    assert strength == "WEAK"
    assert "DEMOGRAPHIC_DOB_SPOUSE" in reasons

def test_strong_mpin_with_demographics():
    strength, reasons = evaluate_mpin("5678", self_dob="1990-01-01")
    assert strength == "STRONG"
    assert not reasons

def test_empty_mpin():
    strength, reasons = evaluate_mpin("")
    assert strength == "INVALID"
    assert "INVALID_FORMAT" in reasons

def test_non_numeric_mpin():
    strength, reasons = evaluate_mpin("abcd")
    assert strength == "INVALID"
    assert "INVALID_FORMAT" in reasons

def test_no_demographics_provided():
    strength, reasons = evaluate_mpin("5432")
    assert strength == "STRONG"
    assert not reasons

def test_demographic_dob_self_yyyymmdd_invalid():
    strength, reasons = evaluate_mpin("19980102", self_dob="1998-01-02")
    assert strength == "INVALID"
    assert "INVALID_FORMAT" in reasons

def test_load_common_mpins_file_not_found():
    with pytest.raises(FileNotFoundError):
        load_common_mpins("non_existent_file.txt")