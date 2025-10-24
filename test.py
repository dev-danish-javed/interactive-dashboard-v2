from services.prompts import process_result_query

message="I'm message"
sql_result="I'm sql result"
sql_command="I'm sql command"

process_result_prompt = process_result_query
process_result_prompt = process_result_prompt.replace("<user_query>", message).replace("<sql_query>", sql_command).replace("<db_result>", sql_result)
print(process_result_prompt)