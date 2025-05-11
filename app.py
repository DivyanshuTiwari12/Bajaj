import requests


def generate_webhook():
    url = "https://bfhldevapigw.healthrx.co.in/hiring/generateWebhook/PYTHON"
    headers = {"Content-Type": "application/json"}
    payload = {
        "name": "Divyanshu Tiwari",
        "regNo": "0827AL221049",
        "email": "divyanshutiwari220089@acropolis.in"
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error generating webhook: {e}")
        return None


def get_sql_question(reg_no):
    last_digit = int(reg_no[-1])
    if last_digit % 2 == 0:
        question_url = "https://drive.google.com/file/d/1pO1ZemDqAZJv7tXRYsVben11Wp2HVb/view?usp=sharing"
    else:
        question_url = "https://drive.google.com/file/d/1q8F8g0EpyNzd5BWk-voe5CKbsxoskJWY/view?usp=sharing"
    return question_url


def solve_sql_problem(question_url):
    print(f"Solving SQL problem from: {question_url}")
    return """
    SELECT 
        p.AMOUNT AS SALARY,
        e.FIRST_NAME || ' ' || e.LAST_NAME AS NAME,
        (strftime('%Y', 'now') - strftime('%Y', e.DOB)) - 
        (CASE WHEN strftime('%m%d', 'now') < strftime('%m%d', e.DOB) 
              THEN 1 ELSE 0 END) AS AGE,
        d.DEPARTMENT_NAME
    FROM PAYMENTS p
    JOIN EMPLOYEE e ON p.EMP_ID = e.EMP_ID
    JOIN DEPARTMENT d ON e.DEPARTMENT = d.DEPARTMENT_ID
    WHERE strftime('%d', p.PAYMENT_TIME) != '01'
    ORDER BY p.AMOUNT DESC
    LIMIT 1
"""


def submit_solution(webhook_url, access_token, final_query):
    url = "https://bfhldevapigw.healthrx.co.in/hiring/testWebhook/PYTHON"
    headers = {
        "Authorization": access_token,
        "Content-Type": "application/json"
    }
    payload = {"finalQuery": final_query}
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        print("Solution submitted successfully!")
        return response.json()
    except requests.RequestException as e:
        print(f"Error submitting solution: {e}")
        return None


def main():
    webhook_response = generate_webhook()
    if not webhook_response:
        return
    
    webhook_url = webhook_response.get("webhook")
    access_token = webhook_response.get("accessToken")
    
    if not webhook_url or not access_token:
        print("Failed to retrieve webhook URL or access token")
        return
    
    reg_no = "0827AL221049"
    question_url = get_sql_question(reg_no)
    
    final_query = solve_sql_problem(question_url)
    
    submit_solution(webhook_url, access_token, final_query)

if __name__ == "__main__":
    main()