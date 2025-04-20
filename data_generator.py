import pandas as pd
import numpy as np
import random
from datetime import timedelta, datetime

# Set random seed for reproducibility
random.seed(42)
np.random.seed(42)

# Define categories
cause_of_loss_themes = [
    'Manual Handling', 'Machine Entanglement', 'Slip and Fall',
    'Repetitive Strain', 'Electrical Incident'
]

hazard_signal_themes = {
    'Manual Handling': ['Heavy Lifting', 'Poor Posture', 'Awkward Movements'],
    'Machine Entanglement': ['No Guarding', 'Loose Clothing', 'Unsafe Maintenance'],
    'Slip and Fall': ['Wet Surface', 'Uneven Floor', 'Obstructed Path'],
    'Repetitive Strain': ['Long Hours', 'Monotony', 'Poor Ergonomics'],
    'Electrical Incident': ['Exposed Wires', 'Faulty Equipment', 'Inadequate PPE']
}

granular_signals = {
    'Heavy Lifting': ['Lift >20kg', 'Lift >30kg'],
    'Poor Posture': ['Bent Neck', 'Slouched Back'],
    'Awkward Movements': ['Twist + Lift', 'Overreach'],
    'No Guarding': ['Missing Shield', 'Bypassed Sensor'],
    'Loose Clothing': ['Hoodie Strings', 'Untucked Shirt'],
    'Unsafe Maintenance': ['Hot Fix', 'Power-On Service'],
    'Wet Surface': ['Spilled Oil', 'Condensation'],
    'Uneven Floor': ['Cracks', 'Sunken Tile'],
    'Obstructed Path': ['Tool Left Behind', 'Loose Cable'],
    'Long Hours': ['12+ hour shifts', 'No Breaks'],
    'Monotony': ['Same Task >4hrs', 'Repetitive Motion'],
    'Poor Ergonomics': ['Non-adjustable Chair', 'Wrong Table Height'],
    'Exposed Wires': ['Frayed Ends', 'Unshielded'],
    'Faulty Equipment': ['Short Circuit', 'Unstable Voltage'],
    'Inadequate PPE': ['No Gloves', 'Wrong Footwear']
}

def data_gen(num_samples=1000):
    # Generate data
    records = []

    # Define date range
    start_date = datetime(2020, 1, 1)
    end_date = datetime(2023, 12, 31)

    for i in range(num_samples):
        claim_id = f"CLM{i + 1:04d}"

        cause_theme = random.choice(cause_of_loss_themes)
        hazard_theme = random.choice(hazard_signal_themes[cause_theme])
        hazard_granular = random.choice(granular_signals[hazard_theme])

        # Simulate paid amount based on risk profile
        base_amount = {
            'Manual Handling': 50000,
            'Machine Entanglement': 90000,
            'Slip and Fall': 40000,
            'Repetitive Strain': 30000,
            'Electrical Incident': 80000
        }[cause_theme]

        total_paid = round(np.random.normal(loc=base_amount, scale=base_amount * 0.5))
        total_paid = max(0, total_paid)  # No negative paid values

        # Simulate random LossDate within the range
        loss_date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))

        records.append({
            'ClaimKey': claim_id,
            'CauseOfLossTheme': cause_theme,
            'HazardSignalTheme': hazard_theme,
            'HazardSignalGranular': hazard_granular,
            'TotalPaidAmount': total_paid,
            'LossDate': loss_date

        })

    return pd.DataFrame(records)
