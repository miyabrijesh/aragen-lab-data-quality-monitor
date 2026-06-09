import pandas as pd
import numpy as np
import pytest
def apply_quality_rules(df):
    df = df.copy()
    # Rule 1: measured_value not null
    df["rule_1"] = df["measured_value"].notna().astype(int)

    # Rule 2: unit not null
    df["rule_2"] = df["unit"].notna().astype(int)

    # Rule 3: status not null
    df["rule_3"] = df["status"].notna().astype(int)

    # Rule 4: no duplicate sample_id
    df["rule_4"] = (~df["sample_id"].duplicated(keep=False)).astype(int)

    # Rule 5: measured_value >= 0
    df["rule_5"] = (df["measured_value"].fillna(-1) >= 0).astype(int)

    # Rule 6: measured_value <= 120
    df["rule_6"] = (df["measured_value"].fillna(999) <= 120).astype(int)

    # Rule 7: status in valid list
    valid_statuses = ["Pass", "Fail", "Pending"]
    df["rule_7"] = df["status"].isin(valid_statuses).astype(int)

    # Rule 8: Pass status must have measured_value
    df["rule_8"] = np.where(
        (df["status"] == "Pass") & (df["measured_value"].isna()), 0, 1
    )

    # Rule 9: Fail status must have measured_value
    df["rule_9"] = np.where(
        (df["status"] == "Fail") & (df["measured_value"].isna()), 0, 1
    )

    # Rule 10: unit in approved list
    approved_units = ["mg/mL", "g/L", "µg/mL", "ng/mL", "%"]
    df["rule_10"] = df["unit"].isin(approved_units).astype(int)

    # Rule 11: recorded_at within 24hrs of experiment_date
    df["experiment_date"] = pd.to_datetime(df["experiment_date"])
    df["recorded_at"] = pd.to_datetime(df["recorded_at"])
    diff_hours = (df["recorded_at"] - df["experiment_date"]).dt.total_seconds() / 3600
    df["rule_11"] = (diff_hours.abs() <= 24).astype(int)

    # Rule 12: placeholder — referential integrity (always pass in unit tests)
    df["rule_12"] = 1

    rule_cols = [f"rule_{i}" for i in range(1, 13)]
    df["quality_score"] = (df[rule_cols].sum(axis=1) / len(rule_cols)) * 100
    df["quality_score"] = df["quality_score"].round(2)

    df["severity"] = np.select(
        [df["quality_score"] < 50,
         (df["quality_score"] >= 50) & (df["quality_score"] < 80),
         df["quality_score"] >= 80],
        ["Critical", "Major", "Minor"],
        default="Minor"
    )

    return df

#helper
def make_record(**overrides):
    base = {
        "sample_id": "LAB-00001",
        "experiment_date": "2026-01-01",
        "recorded_at": "2026-01-01 06:00:00",
        "measured_value": 50.0,
        "unit": "mg/mL",
        "status": "Pass",
    }
    base.update(overrides)
    return pd.DataFrame([base])


#tests
def test_perfect_record_scores_100():
    df = apply_quality_rules(make_record())
    assert df["quality_score"].iloc[0] == 100.0

def test_null_measured_value_fails_rule_1():
    df = apply_quality_rules(make_record(measured_value=None))
    assert df["rule_1"].iloc[0] == 0

def test_null_unit_fails_rule_2():
    df = apply_quality_rules(make_record(unit=None))
    assert df["rule_2"].iloc[0] == 0

def test_null_status_fails_rule_3():
    df = apply_quality_rules(make_record(status=None))
    assert df["rule_3"].iloc[0] == 0

def test_negative_value_fails_rule_5():
    df = apply_quality_rules(make_record(measured_value=-5.0))
    assert df["rule_5"].iloc[0] == 0

def test_out_of_range_value_fails_rule_6():
    df = apply_quality_rules(make_record(measured_value=999.0))
    assert df["rule_6"].iloc[0] == 0

def test_invalid_status_fails_rule_7():
    df = apply_quality_rules(make_record(status="Unknown"))
    assert df["rule_7"].iloc[0] == 0

def test_pass_status_with_null_value_fails_rule_8():
    df = apply_quality_rules(make_record(status="Pass", measured_value=None))
    assert df["rule_8"].iloc[0] == 0

def test_invalid_unit_fails_rule_10():
    df = apply_quality_rules(make_record(unit="xyz"))
    assert df["rule_10"].iloc[0] == 0

def test_stale_timestamp_fails_rule_11():
    df = apply_quality_rules(make_record(
        experiment_date="2026-01-01",
        recorded_at="2026-01-05 00:00:00"  # 4 days later
    ))
    assert df["rule_11"].iloc[0] == 0

def test_duplicate_sample_id_fails_rule_4():
    df = pd.concat([
        make_record(sample_id="LAB-00001"),
        make_record(sample_id="LAB-00001")
    ]).reset_index(drop=True)
    df = apply_quality_rules(df)
    assert df["rule_4"].iloc[0] == 0

def test_severity_critical_below_50():
    df = apply_quality_rules(make_record(
        measured_value=None, unit=None, status=None
    ))
    assert df["severity"].iloc[0] == "Critical"

def test_severity_minor_at_100():
    df = apply_quality_rules(make_record())
    assert df["severity"].iloc[0] == "Minor"
