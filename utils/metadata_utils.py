

def generate_next_scan_name(data_table):
    """
    Parse the scan name to get the experiment name and the scan number
    """
    # table_data is a list of dictionaries
    last_scan_name = data_table[-1]["scan_uri"]
    last_scan_name = last_scan_name.split("_")
    new_scan_count = int(last_scan_name[0])+1
    new_scan_uri = f"{new_scan_count}_"+"_".join(last_scan_name[1:])
    
    return new_scan_uri


def calculate_ratios(polymer_a, polymer_b, swell_ratio):
    
    # Calculate, r, a, b, c from the passed in numerical values
    print("input ratios:", polymer_a, polymer_b, swell_ratio)
    r = float(polymer_a)/float(polymer_b)

    swell_ratio = float(swell_ratio)
    c = (swell_ratio-1)/swell_ratio if swell_ratio > 1 else 0
    
    # Handle case where b = 0 (r is very large or undefined)
    #r = float(polymer_a)/float(polymer_b) if float(polymer_b) != 0 else float('inf')
    if r == float('inf') or r > 1e10:
        # If r is extremely large, set b = 0 and a = 1 - c
        b = 0
        a = 1 - c
    else:
        # Normal calculation
        b = 1 / (swell_ratio * (1 + r))
        a = r * b

    return a, b, c
