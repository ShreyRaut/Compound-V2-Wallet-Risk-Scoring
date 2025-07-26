Compound V2 Wallet Risk Scoring: Unpacking On-Chain Behavior
Hey there! I'm really excited to share this project where I built a system to give Compound V2 wallets a "risk score" from 0 to 1000. It's all about figuring out who's a reliable user and who might be a bit risky, just by looking at their past DeFi transactions.

The Challenge I Tackled
The core problem was to develop a robust system that could assign a risk score to each wallet based solely on its historical Compound V2 transaction data. Think of it like a credit score, but for crypto wallets! A higher score means responsible usage (lower risk), while a lower score might point to risky, bot-like, or even exploitative behavior.

My main tasks were:

Data Collection: How to get the transaction history for each wallet.

Feature Engineering: Turning raw transaction data into meaningful signals.

Risk Scoring: Developing a model to assign the 0-1000 score.

Documentation: Clearly explaining my choices and justifications.

My Approach: A Transparent, Rule-Based Scoring Engine
Given that I didn't have a pre-labeled list of "good" or "bad" wallets (which is typical for many real-world ML problems!), I opted for a rule-based risk scoring model. This isn't a traditional "trained" machine learning model in the sense of neural networks or complex ensembles. Instead, it's a carefully designed heuristic system.

Why this approach?

Interpretability is King: For something as sensitive as a "risk score," understanding why a score is what it is, is paramount. My model allows us to trace back every point added or deducted to a specific transaction behavior.

No Labeled Data Needed: I could build this model using my understanding of healthy vs. unhealthy DeFi interactions, without needing a pre-classified dataset.

Simplicity & Extensibility: It's a clean, one-step script, easy to run, and the rules can be tweaked or expanded as needed. It's a solid baseline for future, more complex models if labeled data becomes available.

1. Data Collection Method
In a real-world scenario, to get all that rich transaction data from Compound V2, I'd definitely turn to The Graph Protocol. It's like a super-efficient librarian for blockchain data; you ask it for specific events (like borrows, repays, liquidations for a wallet), and it gives you structured, indexed data back really fast. It's the go-to for this kind of on-chain analysis.

Conceptual Endpoint: https://api.thegraph.com/subgraphs/name/compound-finance/compound-v2

Method: I'd use GraphQL queries to fetch specific events for each wallet address, such as Mint (supply), Borrow, RepayBorrow, Redeem (withdraw), and LiquidateBorrow. Pagination would be crucial for wallets with extensive history.

For this project: Since I couldn't make live API calls within this specific environment, I created a simulated dataset within the Python script itself. This mock data is structured exactly how I'd expect to get it from The Graph, allowing me to fully demonstrate the feature engineering and scoring logic.

2. Feature Selection Rationale
To understand a wallet's risk, I focused on what really matters in a lending protocol like Compound: how well they manage their loans and collateral. My features are designed to capture that:

Financial Volumes (in USD): How much they've supplied (total_supplies_usd), borrowed (total_borrows_usd), and repaid (total_repays_usd). This gives us the scale of their activity.

Action Counts: Simple counts of supply_count, borrow_count, repay_count, redeem_count, and crucially, liquidation_events_count.

Repay-to-Borrow Ratio: This is key! Calculated as total_repays_usd / total_borrows_usd, it tells us if they're actually paying back what they borrow.

Activity Duration: Calculated as activity_duration_days from first_activity_timestamp and last_activity_timestamp – longer usually suggests more stability.

I made sure all financial calculations use Python's Decimal type for precision, just like you would in any serious financial application, avoiding floating-point errors.

3. Risk Scoring Method
I went with a rule-based scoring model that assigns a score between 0 and 1000. Higher scores mean lower risk. Why this approach? Because it's incredibly transparent. I wanted to be able to explain exactly why a wallet got its score.

Every wallet starts at a neutral 500 points.

Positive contributions (reducing risk) are added for responsible behaviors:

Supplying significant collateral.

Consistently repaying loans (especially achieving a high repay_to_borrow_ratio).

Being active for a long period.

Negative contributions (increasing risk) deduct points for problematic behaviors:

Liquidations: This hits the score hard because it's a direct sign of financial distress and failure to manage a position.

Not repaying borrows adequately (low repay_to_borrow_ratio).

Borrowing heavily without enough supplied collateral or proper repayment.

The final score is always clamped between 0 and 1000.

4. Justification of Risk Indicators Used
My chosen indicators directly reflect financial health and risk management in a decentralized lending environment:

liquidation_events_count (High Impact, Negative): This is the ultimate red flag. If a wallet gets liquidated, it means they failed to maintain their collateral. Multiple liquidations scream "high risk" and poor financial management.

repay_to_borrow_ratio (High Impact, Positive/Negative): This is fundamental to creditworthiness. A high ratio shows reliability and good debt servicing; a low one means unmanaged debt, which is inherently risky.

total_supplies_usd vs. total_borrows_usd (Moderate Impact, Positive/Negative): The balance between supplied collateral and borrowed debt indicates a wallet's leverage. If a wallet borrows a lot compared to what they've supplied, and they're not repaying well, it's a sign of potential over-leveraging and increased risk during market volatility.

activity_duration_days (Low Impact, Positive): Long-term, consistent users are generally more stable and less prone to short-term, high-risk maneuvers. This contributes to a sense of reliability.

How to Run My Code
It's a simple Python script (compound_risk_scorer.py) that reads wallet IDs from a CSV and outputs scores to another CSV.

Save the Code: Copy the Python code provided in the previous responses and save it as compound_risk_scorer.py.

Prepare Input CSV: Ensure your wallet IDs are in a CSV file named Wallet id - Sheet1.csv.

Place CSV: Put Wallet id - Sheet1.csv at the specific path defined in the script: S:\Project\Zeru\Problem 2\Wallet id - Sheet1.csv.

Important Note for Windows Users: The path S:\Project\Zeru\Problem 2\Wallet id - Sheet1.csv uses backslashes. In Python, it's best to use a "raw string" by prefixing the path with r (e.g., r"S:\Project\Zeru\Problem 2\Wallet id - Sheet1.csv") or convert backslashes to forward slashes (/). The provided code already uses the raw string format.

Install Dependencies: Make sure you have pandas installed. If not, open your terminal/command prompt and run:

pip install pandas

Run from Terminal: Open your terminal or command prompt, navigate to the directory where you saved compound_risk_scorer.py, and simply run:

python compound_risk_scorer.py

The script will print the calculated scores to your console and also save them neatly into a new CSV file named wallet_risk_scores.csv in the same directory where you run the script.

Thanks for checking it out!
