
INSERT_FILENOTE_HERE = None
prompt = f"""


You are a claims data analyst. Extract standardized attribute values from the filenote text below. Only return one of the following options for each attribute:

Yes

No

Not Applicable (if it’s irrelevant in this context)

Not Available (if not mentioned or unclear)

Filenote Text:
"{INSERT_FILENOTE_HERE}"

Attributes to extract:
Previous medical history mentioned?

Delay in medical procedure?

Was the worker using safety gear?

Same worker involved in prior incidents?

Delay in reporting the incident?

Was the employer cooperative?

Any prior audits or warnings ignored?

Was specific equipment involved?

Was the equipment in poor condition?

Worksite layout contributed to the incident?

Output format:
Return as a JSON object with attribute keys and one of the above four values.

{{
  "previous_medical_history": "No",
  "delay_in_medical_procedure": "Yes",
  "use_of_safety_gear": "No",
  "repeat_worker_involved": "Not Available",
  "delay_in_reporting": "Yes",
  "employer_cooperation": "No",
  "ignored_prior_audits": "Yes",
  "equipment_involved": "Yes",
  "equipment_condition": "Yes",
  "worksite_layout_contributed": "Yes"
}}

"""