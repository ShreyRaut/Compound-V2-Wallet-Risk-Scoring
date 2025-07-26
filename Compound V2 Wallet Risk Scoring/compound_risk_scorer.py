import pandas as pd
import io
import json
from collections import defaultdict
from datetime import datetime
from decimal import Decimal, getcontext
import random # Import random for more varied simulations

# Set high precision for financial calculations to avoid floating-point inaccuracies
getcontext().prec = 30

def get_simulated_compound_transactions(wallet_addresses):
    """
    Simulates fetching Compound V2 transaction data for a list of wallet addresses.
    This version introduces more varied simulated behaviors for a more diverse score distribution.
    """
    print("Simulating Compound V2 transaction data for wallets with varied behaviors...")
    mock_transactions = []

    # Define specific sample behaviors with placeholder wallet IDs.
    # These will be mapped to the first few actual wallet_addresses.
    specific_sample_behaviors = [
        # Behavior 1: Good behavior (supply, borrow, repay, long-term) - Should get a high score
        [{"wallet_placeholder": "wallet_0", "type": "Mint", "timestamp": 1600000000, "amountUSD": "1000.0"},
         {"wallet_placeholder": "wallet_0", "type": "Borrow", "timestamp": 1600010000, "amountUSD": "500.0"},
         {"wallet_placeholder": "wallet_0", "type": "RepayBorrow", "timestamp": 1600020000, "amountUSD": "500.0"},
         {"wallet_placeholder": "wallet_0", "type": "Mint", "timestamp": 1601000000, "amountUSD": "500.0"},
         {"wallet_placeholder": "wallet_0", "type": "Redeem", "timestamp": 1602000000, "amountUSD": "200.0"},
         {"wallet_placeholder": "wallet_0", "type": "Mint", "timestamp": 1640000000, "amountUSD": "2000.0"}], # More recent activity for duration bonus

        # Behavior 2: Risky behavior (multiple liquidations, partial repay) - Should get a very low score
        [{"wallet_placeholder": "wallet_1", "type": "Mint", "timestamp": 1600000000, "amountUSD": "200.0"},
         {"wallet_placeholder": "wallet_1", "type": "Borrow", "timestamp": 1600050000, "amountUSD": "150.0"},
         {"wallet_placeholder": "wallet_1", "type": "LiquidateBorrow", "timestamp": 1600100000, "amountUSD": "75.0", "borrower_placeholder": "wallet_1"},
         {"wallet_placeholder": "wallet_1", "type": "Borrow", "timestamp": 1600150000, "amountUSD": "50.0"},
         {"wallet_placeholder": "wallet_1", "type": "LiquidateBorrow", "timestamp": 1600200000, "amountUSD": "25.0", "borrower_placeholder": "wallet_1"}],

        # Behavior 3: Supply only (very low risk) - Should get a high score
        [{"wallet_placeholder": "wallet_2", "type": "Mint", "timestamp": 1610000000, "amountUSD": "5000.0"},
         {"wallet_placeholder": "wallet_2", "type": "Mint", "timestamp": 1610050000, "amountUSD": "1000.0"},
         {"wallet_placeholder": "wallet_2", "type": "Redeem", "timestamp": 1610100000, "amountUSD": "500.0"}],

        # Behavior 4: Borrowed, no repay (high risk) - Should get a low score
        [{"wallet_placeholder": "wallet_3", "type": "Mint", "timestamp": 1620000000, "amountUSD": "100.0"},
         {"wallet_placeholder": "wallet_3", "type": "Borrow", "timestamp": 1620010000, "amountUSD": "80.0"},
         {"wallet_placeholder": "wallet_3", "type": "Borrow", "timestamp": 1620020000, "amountUSD": "50.0"}],

        # Behavior 5: Mixed behavior, some repayment - Should get a moderate score
        [{"wallet_placeholder": "wallet_4", "type": "Mint", "timestamp": 1630000000, "amountUSD": "300.0"},
         {"wallet_placeholder": "wallet_4", "type": "Borrow", "timestamp": 1630010000, "amountUSD": "100.0"},
         {"wallet_placeholder": "wallet_4", "type": "RepayBorrow", "timestamp": 1630020000, "amountUSD": "50.0"},
         {"wallet_placeholder": "wallet_4", "type": "Redeem", "timestamp": 1630030000, "amountUSD": "100.0"}]
    ]

    # Define various default behavior templates for the remaining wallets
    # This will ensure more varied scores
    default_behavior_templates = [
        # Template A: Standard good user
        [{"type": "Mint", "amountUSD": "500.0"}, {"type": "Borrow", "amountUSD": "200.0"}, {"type": "RepayBorrow", "amountUSD": "200.0"}],
        # Template B: Larger supplier, no borrows
        [{"type": "Mint", "amountUSD": "1500.0"}, {"type": "Mint", "amountUSD": "500.0"}, {"type": "Redeem", "amountUSD": "100.0"}],
        # Template C: Small borrower, full repay, short activity
        [{"type": "Mint", "amountUSD": "100.0"}, {"type": "Borrow", "amountUSD": "50.0"}, {"type": "RepayBorrow", "amountUSD": "50.0"}],
        # Template D: Medium supplier, partial borrow, partial repay
        [{"type": "Mint", "amountUSD": "800.0"}, {"type": "Borrow", "amountUSD": "400.0"}, {"type": "RepayBorrow", "amountUSD": "200.0"}],
        # Template E: Small supplier, small borrow, no repay
        [{"type": "Mint", "amountUSD": "50.0"}, {"type": "Borrow", "amountUSD": "30.0"}],
        # Template F: Very active, but small amounts
        [{"type": "Mint", "amountUSD": "50.0"}, {"type": "Borrow", "amountUSD": "20.0"}, {"type": "RepayBorrow", "amountUSD": "20.0"},
         {"type": "Mint", "amountUSD": "30.0"}, {"type": "Borrow", "amountUSD": "10.0"}, {"type": "RepayBorrow", "amountUSD": "10.0"}],
    ]


    # Assign specific behaviors to the first few wallets from the input list
    assigned_wallets = set()
    for i, behavior_list in enumerate(specific_sample_behaviors):
        if i < len(wallet_addresses):
            actual_wallet_id = wallet_addresses[i]
            assigned_wallets.add(actual_wallet_id)
            for event in behavior_list:
                event_copy = event.copy()
                event_copy['wallet'] = actual_wallet_id
                if 'borrower_placeholder' in event_copy:
                    event_copy['borrower'] = actual_wallet_id
                    del event_copy['borrower_placeholder']
                del event_copy['wallet_placeholder']
                mock_transactions.append(event_copy)

    # Assign varied default behaviors to the remaining wallets
    base_timestamp_for_new = 1645000000
    for i, wallet_id in enumerate(wallet_addresses):
        if wallet_id not in assigned_wallets:
            # Randomly pick a behavior template
            chosen_template = random.choice(default_behavior_templates)
            current_ts = base_timestamp_for_new + (i * 5000) + random.randint(0, 1000) # Add randomness to timestamp

            for j, event_template in enumerate(chosen_template):
                event_copy = event_template.copy()
                event_copy['wallet'] = wallet_id
                event_copy['timestamp'] = current_ts + (j * random.randint(100, 500)) # Vary timestamps within a template

                # Introduce small random variations to amounts
                if 'amountUSD' in event_copy:
                    original_amount = Decimal(event_copy['amountUSD'])
                    variation = original_amount * Decimal(str(random.uniform(0.9, 1.1))) # +/- 10% variation
                    event_copy['amountUSD'] = str(variation.quantize(Decimal('0.01'))) # Keep 2 decimal places

                if 'borrower_placeholder' in event_copy:
                    event_copy['borrower'] = wallet_id
                    del event_copy['borrower_placeholder']
                mock_transactions.append(event_copy)
    return mock_transactions

def calculate_risk_scores(wallet_addresses, transaction_events):
    """
    Calculates a risk score (0-1000) for each wallet based on its Compound V2 transaction history.
    Higher score means lower risk.
    """
    wallet_summaries = defaultdict(lambda: {
        'total_supplies_usd': Decimal('0.0'),
        'total_borrows_usd': Decimal('0.0'),
        'total_repays_usd': Decimal('0.0'),
        'liquidation_events_count': 0,
        'supply_count': 0,
        'borrow_count': 0,
        'repay_count': 0,
        'redeem_count': 0,
        'first_activity_timestamp': float('inf'),
        'last_activity_timestamp': float('-inf'),
    })

    print("Aggregating wallet features...")
    for event in transaction_events:
        wallet = event.get('wallet')
        event_type = event.get('type')
        timestamp = event.get('timestamp')
        amount_usd_str = event.get('amountUSD')

        if not all([wallet, event_type, timestamp is not None, amount_usd_str]):
            continue

        try:
            usd_value = Decimal(amount_usd_str)
        except Exception:
            continue

        # Update activity timestamps for the wallet
        wallet_summaries[wallet]['first_activity_timestamp'] = min(wallet_summaries[wallet]['first_activity_timestamp'], timestamp)
        wallet_summaries[wallet]['last_activity_timestamp'] = max(wallet_summaries[wallet]['last_activity_timestamp'], timestamp)

        # Categorize and sum up financial metrics and counts
        if event_type == 'Mint':
            wallet_summaries[wallet]['supply_count'] += 1
            wallet_summaries[wallet]['total_supplies_usd'] += usd_value
        elif event_type == 'Borrow':
            wallet_summaries[wallet]['borrow_count'] += 1
            wallet_summaries[wallet]['total_borrows_usd'] += usd_value
        elif event_type == 'RepayBorrow':
            wallet_summaries[wallet]['repay_count'] += 1
            wallet_summaries[wallet]['total_repays_usd'] += usd_value
        elif event_type == 'Redeem':
            wallet_summaries[wallet]['redeem_count'] += 1
        elif event_type == 'LiquidateBorrow':
            # Crucially, only count if this wallet was the one liquidated
            if event.get('borrower') == wallet:
                wallet_summaries[wallet]['liquidation_events_count'] += 1

    print("Applying risk scoring logic...")
    scored_wallets = []
    for wallet_id in wallet_addresses:
        # Get features for the current wallet, or default empty features if no transactions found
        features = wallet_summaries.get(wallet_id, defaultdict(int))

        # Calculate key ratios and durations from aggregated features
        repay_to_borrow_ratio = Decimal('0.0')
        if features['total_borrows_usd'] > Decimal('0.0'):
            repay_to_borrow_ratio = features['total_repays_usd'] / features['total_borrows_usd']
        elif features['borrow_count'] == 0:
            repay_to_borrow_ratio = Decimal('1.0') # Perfect ratio if no debt was ever taken

        activity_duration_days = 0
        if features['last_activity_timestamp'] > 0 and features['first_activity_timestamp'] < float('inf'):
            activity_duration_days = (features['last_activity_timestamp'] - features['first_activity_timestamp']) / (60 * 60 * 24)

        # --- Risk Score Calculation (0-1000, higher is lower risk) ---
        score = 500 # Starting neutral score

        # Positive contributions (reduce risk)
        # Reward substantial collateral supplied to the protocol
        score += min(int(features['total_supplies_usd'] / Decimal('500')), 150) # Max 150 points for supplies

        # Reward strong repayment discipline based on the repay-to-borrow ratio
        if repay_to_borrow_ratio >= Decimal('1.0'): # Full repayment or overpayment
            score += 200
        elif repay_to_borrow_ratio > Decimal('0.8'): # Very good repayment
            score += 100
        elif repay_to_borrow_ratio > Decimal('0.5'): # Decent repayment
            score += 50

        # Reward long-term, sustained engagement
        if activity_duration_days > 365: # Over a year of activity
            score += 30
        elif activity_duration_days > 180: # Over six months of activity
            score += 15

        # Negative contributions (increase risk)
        # Heavily penalize liquidations - this is a direct failure to manage risk
        score -= features['liquidation_events_count'] * 250

        # Penalize significant unrepaid debt
        if features['total_borrows_usd'] > Decimal('0.0') and repay_to_borrow_ratio < Decimal('0.5'):
            score -= 150 # Major deduction for poor repayment

        # Penalize high leverage without sufficient repayment or frequent borrowing without repaying
        if (features['total_supplies_usd'] > Decimal('0.0') and
            features['total_borrows_usd'] > features['total_supplies_usd'] * Decimal('0.8')): # Borrowed more than 80% of supplied
            if repay_to_borrow_ratio < Decimal('0.7') or features['borrow_count'] > features['repay_count'] * 2: # And repayment is weak or borrows are much more frequent than repays
                score -= 100 # Deduction for potentially risky leverage

        # Ensure the score stays within the valid range [0, 1000]
        final_score = max(0, min(1000, int(score)))
        scored_wallets.append({'wallet_id': wallet_id, 'score': final_score})

    return pd.DataFrame(scored_wallets)

if __name__ == "__main__":
    # Define the exact path to your CSV file
    # Using a raw string (r"...") is recommended for Windows paths to avoid issues with backslashes
    csv_file_path = r"S:\Project\Zeru\Problem 2\Wallet id - Sheet1.csv"

    initial_wallet_ids = []
    try:
        # Read the wallet IDs from the specified CSV file
        wallet_df = pd.read_csv(csv_file_path)
        initial_wallet_ids = wallet_df['wallet_id'].tolist()
        print(f"Loaded {len(initial_wallet_ids)} wallet IDs from '{csv_file_path}'.")
    except FileNotFoundError:
        print(f"Error: The file was not found at '{csv_file_path}'. Please check the path and filename.")
    except Exception as e:
        print(f"An error occurred while reading the CSV file: {e}")

    if initial_wallet_ids:
        # Simulate fetching transaction data for these wallets
        simulated_transactions = get_simulated_compound_transactions(initial_wallet_ids)

        # Calculate and generate the risk scores
        risk_scores_df = calculate_risk_scores(initial_wallet_ids, simulated_transactions)

        # Save the results to a CSV file in the current working directory
        output_csv_filename = "wallet_risk_scores.csv"
        risk_scores_df.to_csv(output_csv_filename, index=False)
        print(f"\nSuccessfully generated and saved risk scores to '{output_csv_filename}'")

        # Display a preview of the results
        print("\nFirst 10 risk scores:")
        print(risk_scores_df.head(10).to_string(index=False))
    else:
        print("No wallet IDs were loaded. Cannot proceed with scoring.")

