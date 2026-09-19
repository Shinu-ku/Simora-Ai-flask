import os
import time
import requests

BASE_URL = "http://localhost:8000/api/v1"
client = requests.Session()

def print_step(step):
    print(f"\n{'='*50}\n[STEP] {step}\n{'='*50}")

try:
    print_step("REGISTER")
    email = f"demo_{int(time.time())}@example.com"
    res = client.post(f"{BASE_URL}/auth/register", json={
        "email": email,
        "password": "password123",
        "full_name": "Demo User"
    })
    res.raise_for_status()
    print("Registered successfully:", res.json()['email'])

    print_step("LOGIN")
    res = client.post(f"{BASE_URL}/auth/login", data={
        "username": email,
        "password": "password123"
    })
    res.raise_for_status()
    token = res.json()['access_token']
    client.headers.update({"Authorization": f"Bearer {token}"})
    print("Logged in successfully.")

    print_step("CREATE BUSINESS")
    res = client.post(f"{BASE_URL}/business/", json={
        "name": "Rajesh Electronics",
        "industry": "Retail",
        "currency": "USD"
    })
    res.raise_for_status()
    print("Business created:", res.json()['name'])

    print_step("LOAD DEMO DATA")
    # Endpoint loads demo products and 1000 sales
    res = client.post(f"{BASE_URL}/products/demo/seed")
    res.raise_for_status()
    print(res.json()['message'])
    
    products = client.get(f"{BASE_URL}/products/").json()
    headphones = next((p for p in products if 'headphone' in p['name'].lower()), products[0])
    print(f"Target product: {headphones['name']} ({headphones['id']})")

    print_step("BUILD DIGITAL TWIN")
    res = client.post(f"{BASE_URL}/digital-twin/generate")
    res.raise_for_status()
    twin = res.json()
    print(f"Twin Version: {twin['model_version']}, Confidence: {twin['confidence']}")

    print_step("NATURAL LANGUAGE SIMULATION")
    res = client.post(f"{BASE_URL}/simulate/natural-language", json={
        "query": "What if I give 10% discount on headphones this weekend?"
    })
    res.raise_for_status()
    sim_result = res.json()
    print(f"AI Parsed: {sim_result['ai_parsed']}")
    print(f"Explanation: {sim_result['explanation']}")
    
    baseline = sim_result['baseline']
    cf = sim_result['counterfactual']
    print(f"Baseline -> Revenue: ${baseline['projected_revenue']}, Profit: ${baseline['projected_profit']}, Units: {baseline['projected_units']}")
    print(f"Counterfactual -> Revenue: ${cf['projected_revenue']}, Profit: ${cf['projected_profit']}, Units: {cf['projected_units']}")

    print_step("MERCHANT APPROVAL")
    # Send decision
    res = client.post(f"{BASE_URL}/decisions/", json={
        "product_id": headphones['id'],
        "action_type": "discount",
        "value": 0.10,
        "duration_days": 2,
        "predicted_units": cf['projected_units'],
        "predicted_revenue": cf['projected_revenue'],
        "predicted_profit": cf['projected_profit']
    })
    res.raise_for_status()
    decision = res.json()
    print("Decision created. Status:", decision['status'])

    # Approve
    res = client.post(f"{BASE_URL}/decisions/{decision['id']}/approve")
    res.raise_for_status()
    print("Decision approved. Status:", res.json()['status'])

    print_step("DEMO EXECUTION")
    res = client.post(f"{BASE_URL}/decisions/{decision['id']}/execute")
    res.raise_for_status()
    print("Decision executed via DemoExecutor. Status:", res.json()['status'])

    print_step("ACTUAL OUTCOME & PREDICTED VS ACTUAL")
    # Simulate that we sold 20% fewer units than predicted
    actual_units = int(cf['projected_units'] * 0.8) 
    actual_revenue = actual_units * (headphones['price'] * 0.90)
    actual_profit = actual_revenue - (actual_units * headphones['cost'])
    
    print(f"Predicted Units: {cf['projected_units']} | Actual Units: {actual_units}")
    
    res = client.post(f"{BASE_URL}/decisions/{decision['id']}/outcome", json={
        "actual_units": actual_units,
        "actual_revenue": actual_revenue,
        "actual_profit": actual_profit
    })
    res.raise_for_status()
    print("Outcome recorded successfully.")

    print_step("COGNEE MEMORY & CALIBRATION (LEARNING LOOP)")
    memories = client.get(f"{BASE_URL}/memory/").json()
    print("Latest Observation Memory:", memories[0]['content'] if memories else "None")
    
    calibrations = client.get(f"{BASE_URL}/memory/calibrations").json()
    discount_cal = next(c for c in calibrations if c['action_type'] == 'discount')
    print(f"Calibration Factor learned for 'discount': {discount_cal['calibration_factor']} (Avg Error: {discount_cal['average_error']})")

    print_step("NEW SIMULATION (LEARNED INFORMATION)")
    # Re-run same simulation
    res = client.post(f"{BASE_URL}/simulate/natural-language", json={
        "query": "What if I give 10% discount on headphones this weekend?"
    })
    res.raise_for_status()
    new_sim = res.json()
    new_cf = new_sim['counterfactual']
    
    print(f"First Prediction Units: {cf['projected_units']}")
    print(f"Calibrated Second Prediction Units: {new_cf['projected_units']}")
    
    if new_cf['projected_units'] < cf['projected_units']:
        print("\n✅ SUCCESS: The system successfully learned from the negative outcome and adjusted its future prediction!")
    else:
        print("\n❌ FAILURE: The system did not apply the calibration factor.")
        exit(1)
        
    print_step("E2E JOURNEY COMPLETE")

except Exception as e:
    print(f"\n❌ ERROR during E2E flow: {e}")
    if hasattr(e, 'response') and e.response:
        print(e.response.text)
