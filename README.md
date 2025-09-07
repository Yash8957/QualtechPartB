Intelligent Background Verification in Video Calls (Part B : Hard)
Background
With the rapid adoption of digital KYC, remote onboarding, video-based insurance claims, and
online verification, organizations increasingly interact with customers over video calls. While
these calls allow verification of identity documents and live interaction with the customer, they
miss a powerful source of information — the customer’s environment in the background.
For example:
● A customer claims to be at their home, but the video background clearly shows a shop
or warehouse.
● An applicant declares they run a retail shop with large inventory, but the background
shows only an empty room.
● A user states they are in an office, but the background objects (bed, wardrobe, TV)
suggest otherwise.

Such mismatches can indicate fraud, misrepresentation, or non-compliance. Automating
background verification in real time can significantly reduce fraud risk and strengthen trust in
remote processes.
Your Challenge
Design and develop an AI-powered solution that can analyze a customer’s background during
a live or recorded video call and provide actionable insights to the verifying agent.
The solution should be able to:
1. Analyze the video background in real time.
○ Extract video frames and process them efficiently.
2.
3. Classify the environment type.
○ Detect whether the customer is in a home, office, shop, warehouse, or outdoor
setting.

4.

5. Identify key background objects.
○ Furniture: sofa, bed, table, chair, cupboard.
○ Appliances: TV, fridge, AC, washing machine.
○ Shop/Business assets: shelves, counters, products, boxes, inventory.
○ Office items: desk, computer, whiteboard, meeting table.
○ Vehicles: car, scooter, bike.
6.
7. Compare against declared data.
○ Example: If a customer declared “Shop with stock of
200 bottles”, the system should confirm whether shop shelves and
product stock are visible.
○ Highlight mismatches in type (declared “office” but detected “home”)

or asset count.

8.
9. Provide a confidence score.
○ Each classification (environment and objects) should include a
confidence percentage to assist the human agent.

10.
11. Flag potential fraud cases.
○ Output a structured summary highlighting discrepancies.
○ Suggest “Pass / Review Needed” for decision support.

Expected Output Example
Environment Detected: Shop (Confidence: 0.89)
Declared Environment: Home
Detected Objects:
● Shelves: 5

● Bottled Products: ~150
● Refrigerator: 1
● Counter Table: 1

Mismatch Highlighted:
● Declared “Home” → Detected “Shop”
● Declared “Fridge: 2” → Detected “Fridge: 1”

Risk Flag: Potential Misrepresentation (Review Required)
