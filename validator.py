import datetime

def load_common_mpins(filename="common_mpins.txt"):
    """Loads a set of common MPINs from a file."""
    with open(filename, "r") as f:
        return {line.strip() for line in f}

def extract_combinations(date_str):
    """Extracts various date combinations from a date string."""
    if not date_str:
        return set()
    date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d")
    dd = f"{date_obj.day:02}"
    mm = f"{date_obj.month:02}"
    yy = str(date_obj.year)[2:]
    yyyy = str(date_obj.year)
    
    return {
        dd + mm, mm + dd, yy + mm, mm + yy, dd + yy, yy + dd,
        dd + mm + yy, yy + mm + dd, dd + mm + yyyy, yyyy + mm + dd,
        yyyy
    }

def evaluate_mpin(mpin, self_dob=None, spouse_dob=None, anniversary=None, common_mpins_filename="common_mpins.txt"):
    """
    Evaluates the strength of an MPIN based on common patterns and demographic data.
    """
    reasons = []
    
    # Basic validation for MPIN format
    if not (mpin.isdigit() and len(mpin) in [4, 6]):
        return "INVALID", ["INVALID_FORMAT"]

    common_mpins = load_common_mpins(common_mpins_filename)

    if mpin in common_mpins:
        reasons.append("COMMONLY_USED")

    if self_dob:
        if mpin in extract_combinations(self_dob):
            reasons.append("DEMOGRAPHIC_DOB_SELF")
    if spouse_dob:
        if mpin in extract_combinations(spouse_dob):
            reasons.append("DEMOGRAPHIC_DOB_SPOUSE")
    if anniversary:
        if mpin in extract_combinations(anniversary):
            reasons.append("DEMOGRAPHIC_ANNIVERSARY")

    strength = "WEAK" if reasons else "STRONG"
    return strength, reasons